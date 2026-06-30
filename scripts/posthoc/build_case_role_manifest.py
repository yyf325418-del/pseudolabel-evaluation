import csv
import json
import os
from pathlib import Path

ROOT = Path(os.environ.get("VERSE_PROJECT_ROOT", ".")).resolve()
PREP_ROOTS = [ROOT / "nnunet_preprocessed"]
for value in os.environ.get(
    "NNUNET_PREPROCESSED_ROOTS", ""
).split(os.pathsep):
    if value:
        PREP_ROOTS.append(
            Path(value).expanduser().resolve()
        )
RAW = ROOT / "nnunet_data"
PRED = ROOT / "nnunet_predictions"
OUT = Path(
    os.environ.get(
        "CMIG_MANIFEST_OUTPUT",
        str(ROOT / "repository_outputs/manifests"),
    )
).resolve()
OUT.mkdir(parents=True, exist_ok=True)

DATASETS = {
    "D119": "Dataset119_VerSe19",
    "D128": "Dataset128_VerSe19Labeled08_seed42",
    "D129": "Dataset129_VerSe19Pseudo70_seed42",
    "D130": "Dataset130_VerSe19Labeled16_seed42",
    "D132": "Dataset132_VerSe19Labeled04_seed42",
    "D134": "Dataset134_VerSe19Pseudo63Conf080_seed42",
    "D161": "Dataset161_VerSe19Labeled16Pseudo70_seed42",
    "D162": "Dataset162_VerSe19Labeled04Pseudo70_seed42",
    "D175": "Dataset175_VerSe19Pseudo70TrainConfFilterPaired129_seed42",
}

EXPECTED_FILTERED = {
    "sub-verse005",
    "sub-verse031",
    "sub-verse036",
    "sub-verse065",
    "sub-verse139",
    "sub-verse146",
    "sub-verse405_split-verse259",
}

EXPECTED_PSEUDO_MISSING = {
    "sub-verse006",
    "sub-verse074",
}


def normalize_case(filename):
    for suffix in (
        "_seg-vert_msk.nii.gz",
        "_0000.nii.gz",
        ".nii.gz",
    ):
        if filename.endswith(suffix):
            return filename[:-len(suffix)]
    return filename


def load_splits(dataset_name):
    searched = []

    for prep_root in PREP_ROOTS:
        path = prep_root / dataset_name / "splits_final.json"
        searched.append(str(path))

        if path.exists():
            print(f"[split] {dataset_name}: {path}")
            data = json.loads(path.read_text())

            if not data:
                raise RuntimeError(
                    f"{dataset_name}: split file contains no folds: {path}"
                )

            print(
                f"[split-count] {dataset_name}: "
                f"{len(data)} fold(s)"
            )
            return data

    raise FileNotFoundError(
        "Missing split file for "
        + dataset_name
        + "\nSearched:\n  "
        + "\n  ".join(searched)
    )


def pool_from_splits(splits):
    cases = set()
    for fold in splits:
        cases.update(fold["train"])
        cases.update(fold["val"])
    return cases


splits = {
    key: load_splits(dataset_name)
    for key, dataset_name in DATASETS.items()
}

pools = {
    key: pool_from_splits(dataset_splits)
    for key, dataset_splits in splits.items()
}

gt4 = pools["D132"]
gt8 = pools["D128"]
gt16 = pools["D130"]

gt_reference = {
    "D119": pools["D119"],
    "D128": gt8,
    "D129": gt8,
    "D130": gt16,
    "D132": gt4,
    "D134": gt8,
    "D161": gt16,
    "D162": gt4,
    "D175": gt8,
}

# ---------------------------------------------------------------------
# 1. Complete case/fold role manifest
# ---------------------------------------------------------------------

manifest_rows = []
d175_checks = []

for key, dataset_name in DATASETS.items():
    for fold_index, fold_split in enumerate(splits[key]):
        train = set(fold_split["train"])
        val = set(fold_split["val"])

        if train & val:
            raise RuntimeError(
                f"{key} fold{fold_index}: train/val overlap detected"
            )

        if key == "D175":
            base_train = set(splits["D129"][fold_index]["train"])
            base_val = set(splits["D129"][fold_index]["val"])
            base_pool = base_train | base_val

            val_identical = val == base_val
            train_is_subset = train <= base_train
            removed = sorted(base_train - train)

            d175_checks.append({
                "fold": fold_index,
                "D129_train_n": len(base_train),
                "D175_train_n": len(train),
                "D129_val_n": len(base_val),
                "D175_val_n": len(val),
                "validation_identical": val_identical,
                "D175_train_subset_of_D129": train_is_subset,
                "removed_from_train_n": len(removed),
                "removed_from_train": removed,
            })

            if not val_identical:
                raise RuntimeError(
                    f"D175 fold{fold_index}: validation differs from D129"
                )
            if not train_is_subset:
                raise RuntimeError(
                    f"D175 fold{fold_index}: unexpected cases added to train"
                )

            for case_id in sorted(base_pool):
                if case_id in val:
                    role = "validation"
                elif case_id in train:
                    role = "train"
                elif case_id in base_train:
                    role = "excluded_from_train_by_filter"
                else:
                    raise RuntimeError(
                        f"D175 fold{fold_index}: unclassified case {case_id}"
                    )

                manifest_rows.append({
                    "dataset_key": key,
                    "dataset_name": dataset_name,
                    "fold": fold_index,
                    "case_id": case_id,
                    "fold_role": role,
                    "label_source": (
                        "ground_truth"
                        if case_id in gt_reference[key]
                        else "teacher_pseudo_label"
                    ),
                    "paired_reference": "D129",
                })
        else:
            for case_id in sorted(train | val):
                manifest_rows.append({
                    "dataset_key": key,
                    "dataset_name": dataset_name,
                    "fold": fold_index,
                    "case_id": case_id,
                    "fold_role": (
                        "train" if case_id in train else "validation"
                    ),
                    "label_source": (
                        "ground_truth"
                        if case_id in gt_reference[key]
                        else "teacher_pseudo_label"
                    ),
                    "paired_reference": "",
                })

manifest_path = OUT / "case_fold_role_manifest.csv"

with manifest_path.open("w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "dataset_key",
            "dataset_name",
            "fold",
            "case_id",
            "fold_role",
            "label_source",
            "paired_reference",
        ],
    )
    writer.writeheader()
    writer.writerows(manifest_rows)

# ---------------------------------------------------------------------
# 2. Dataset pool summary
# ---------------------------------------------------------------------

summary_rows = []

for key, dataset_name in DATASETS.items():
    summary_rows.append({
        "dataset_key": key,
        "dataset_name": dataset_name,
        "pool_cases": len(pools[key]),
        "folds": len(splits[key]),
        "ground_truth_cases": len(pools[key] & gt_reference[key]),
        "pseudo_label_cases": len(pools[key] - gt_reference[key]),
    })

summary_path = OUT / "dataset_pool_summary.csv"

with summary_path.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=summary_rows[0].keys())
    writer.writeheader()
    writer.writerows(summary_rows)

# ---------------------------------------------------------------------
# 3. Historical D129/D134 pool difference
# ---------------------------------------------------------------------

difference_rows = []

for case_id in sorted(pools["D129"] | pools["D134"]):
    in_d129 = case_id in pools["D129"]
    in_d134 = case_id in pools["D134"]

    if in_d129 and in_d134:
        status = "retained"
    elif in_d129 and not in_d134:
        status = "removed_by_historical_filter"
    else:
        status = "unexpected_D134_only"

    difference_rows.append({
        "case_id": case_id,
        "in_D129": in_d129,
        "in_D134": in_d134,
        "status": status,
        "label_source": (
            "ground_truth" if case_id in gt8
            else "teacher_pseudo_label"
        ),
    })

difference_path = OUT / "d129_d134_pool_difference.csv"

with difference_path.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=difference_rows[0].keys())
    writer.writeheader()
    writer.writerows(difference_rows)

# ---------------------------------------------------------------------
# 4. Fixed 40-case VerSe external test manifest
# ---------------------------------------------------------------------

images_ts = RAW / DATASETS["D129"] / "imagesTs"

if not images_ts.exists():
    raise FileNotFoundError(f"Missing imagesTs: {images_ts}")

external40 = {
    normalize_case(path.name)
    for path in images_ts.glob("*_0000.nii.gz")
}

external_path = OUT / "fixed_verse_external40_manifest.csv"

with external_path.open("w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["case_id", "role", "source_directory"],
    )
    writer.writeheader()

    for case_id in sorted(external40):
        writer.writerow({
            "case_id": case_id,
            "role": "fixed_external_test",
            "source_directory": str(images_ts),
        })

# ---------------------------------------------------------------------
# 5. Pseudo-generation 72 -> 70 manifest
# ---------------------------------------------------------------------

# The original 72-case candidate pool is reconstructed from the frozen
# 80-case D119 source pool minus the 8 labeled D128 cases. The current
# imagesUnlabeledTr folder contains only the 70 retained/available files,
# so it must not be treated as the original 72-case candidate list.

pseudo_candidates = pools["D119"] - gt8

unlabeled_dir = RAW / DATASETS["D128"] / "imagesUnlabeledTr"
pseudo_dir = PRED / "dataset128_seed42_unlabeled_teacher01234"

if not unlabeled_dir.exists():
    raise FileNotFoundError(f"Missing staged input directory: {unlabeled_dir}")

if not pseudo_dir.exists():
    raise FileNotFoundError(f"Missing pseudo output directory: {pseudo_dir}")

staged_input_files = {
    normalize_case(path.name)
    for path in unlabeled_dir.glob("*_0000.nii.gz")
}

pseudo_outputs = {
    normalize_case(path.name)
    for path in pseudo_dir.glob("*.nii.gz")
}

pseudo_rows = []

for case_id in sorted(
    pseudo_candidates | staged_input_files | pseudo_outputs
):
    in_candidate_pool = case_id in pseudo_candidates
    input_present = case_id in staged_input_files
    output_present = case_id in pseudo_outputs

    if in_candidate_pool and input_present and output_present:
        status = "pseudo_generated"
    elif in_candidate_pool and not input_present and not output_present:
        status = "candidate_missing_from_staged_input_and_output"
    elif in_candidate_pool and input_present and not output_present:
        status = "prediction_output_missing"
    elif in_candidate_pool and not input_present and output_present:
        status = "output_present_without_current_input_file"
    else:
        status = "unexpected_case"

    pseudo_rows.append({
        "case_id": case_id,
        "in_original_candidate72": in_candidate_pool,
        "staged_input_file_present": input_present,
        "pseudo_output_present": output_present,
        "status": status,
    })

pseudo_path = OUT / "pseudo_generation_72_to_70_manifest.csv"

with pseudo_path.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=pseudo_rows[0].keys())
    writer.writeheader()
    writer.writerows(pseudo_rows)

# ---------------------------------------------------------------------
# 6. Integrity checks
# ---------------------------------------------------------------------

d129_minus_d134 = pools["D129"] - pools["D134"]
d134_only = pools["D134"] - pools["D129"]

candidate_without_staged_input = (
    pseudo_candidates - staged_input_files
)
candidate_without_output = pseudo_candidates - pseudo_outputs
staged_inputs_without_output = (
    staged_input_files - pseudo_outputs
)
outputs_outside_candidate = pseudo_outputs - pseudo_candidates

checks = {
    "D119_pool": len(pools["D119"]),
    "D128_ground_truth_pool": len(pools["D128"]),
    "D128_pseudo_candidate_pool": len(pseudo_candidates),
    "staged_imagesUnlabeledTr_files": len(staged_input_files),
    "pseudo_outputs": len(pseudo_outputs),
    "D129_pool": len(pools["D129"]),
    "D134_pool": len(pools["D134"]),
    "D161_pool": len(pools["D161"]),
    "D162_pool": len(pools["D162"]),
    "D175_union_pool": len(pools["D175"]),
    "fixed_external_test": len(external40),
    "D129_minus_D134": sorted(d129_minus_d134),
    "D134_only": sorted(d134_only),
    "candidate72_without_staged_input": sorted(
        candidate_without_staged_input
    ),
    "candidate72_without_pseudo_output": sorted(
        candidate_without_output
    ),
    "staged_inputs_without_output": sorted(
        staged_inputs_without_output
    ),
    "outputs_outside_candidate72": sorted(
        outputs_outside_candidate
    ),
    "pseudo70_intersection_external40": sorted(
        pseudo_outputs & external40
    ),
    "D119_intersection_external40": sorted(
        pools["D119"] & external40
    ),
    "D175_fold_checks": d175_checks,
}

assert len(pools["D119"]) == 80, checks
assert len(pools["D128"]) == 8, checks
assert len(pseudo_candidates) == 72, checks
assert len(staged_input_files) == 70, checks
assert len(pseudo_outputs) == 70, checks
assert len(pools["D129"]) == 78, checks
assert len(pools["D134"]) == 71, checks
assert len(external40) == 40, checks

assert d129_minus_d134 == EXPECTED_FILTERED, checks
assert d134_only == set(), checks

assert candidate_without_staged_input == EXPECTED_PSEUDO_MISSING, checks
assert candidate_without_output == EXPECTED_PSEUDO_MISSING, checks
assert staged_inputs_without_output == set(), checks
assert outputs_outside_candidate == set(), checks

assert pseudo_outputs & external40 == set(), checks
assert pools["D119"] & external40 == set(), checks

checks_path = OUT / "manifest_integrity_checks.json"
checks_path.write_text(
    json.dumps(checks, indent=2, ensure_ascii=False)
)

print("=== MANIFEST INTEGRITY CHECKS PASSED ===")
print(json.dumps(checks, indent=2, ensure_ascii=False))

print("\nGenerated files:")
for path in [
    manifest_path,
    summary_path,
    difference_path,
    external_path,
    pseudo_path,
    checks_path,
]:
    print(path)
