from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy.typing as npt

if not hasattr(npt, "NDArray"):
    class NDArray:
        def __class_getitem__(cls, item):
            return cls

    npt.NDArray = NDArray

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
import nibabel as nib
import numpy as np
from scipy import ndimage


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "qualitative_paired_cases"
OUT_DIR = DATA_DIR / "output"
OUT_DIR.mkdir(exist_ok=True)

FIG_BASE = OUT_DIR / "Figure_paired_filtering_anatomy"

CASE_ORDER = [
    "case_regular_fold1_sub-verse153",
    "case_D175_worse_fold2_sub-verse030",
    "case_D175_slightly_better_fold2_sub-verse116",
    "case_ID_difference_fold0_sub-verse022",
]

ROLE_LABELS = {
    "case_regular": "Matched case",
    "case_D175_worse": "Filtered worse",
    "case_D175_slightly_better": "Tiny Dice gain",
    "case_ID_difference": "ID-rate change",
}

METHOD_LABELS = {
    "gt": "Ground truth",
    "d129": "Student-8+PL70",
    "d175": "Filtered Student-8+PL",
}

D129_COLOR = "#2A6FBB"
D175_COLOR = "#D87828"
GAIN_COLOR = "#1B9E77"
LOSS_COLOR = "#D95F02"
PERSIST_COLOR = "#6A51A3"

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 7,
        "axes.linewidth": 0.55,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
    }
)


def load_volume(path: Path) -> tuple[nib.Nifti1Image, np.ndarray]:
    image = nib.as_closest_canonical(nib.load(str(path)))
    return image, np.asanyarray(image.dataobj)


def label_cmap() -> ListedColormap:
    tab20 = mpl.cm.get_cmap("tab20")
    set3 = mpl.cm.get_cmap("Set3")
    order = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    colors = [(0, 0, 0, 0)]
    colors.extend(tab20(i) for i in order)
    colors.extend(set3(i) for i in range(6))
    return ListedColormap(colors)


def rgba_labels(labels: np.ndarray, cmap: ListedColormap, alpha: float = 0.55) -> np.ndarray:
    clipped = np.clip(labels.astype(int), 0, cmap.N - 1)
    rgba = cmap(clipped)
    rgba[..., 3] = np.where(clipped > 0, alpha, 0.0)
    return rgba


def sagittal_view(volume: np.ndarray, x_index: int) -> np.ndarray:
    return np.flipud(volume[x_index, :, :].T)


def sagittal_projection(labels: np.ndarray) -> np.ndarray:
    projection = labels.max(axis=0)
    return np.flipud(projection.T)


def normalize_nonzero(values: np.ndarray) -> np.ndarray:
    vmax = float(values.max())
    return values / vmax if vmax > 0 else values


def choose_sagittal_index(gt: np.ndarray, d129: np.ndarray, d175: np.ndarray) -> int:
    region = (gt > 0) | (d129 > 0) | (d175 > 0)
    area = region.sum(axis=(1, 2)).astype(float)
    label_disagreement = ((d129 != d175) & region).sum(axis=(1, 2)).astype(float)
    d175_loss = ((d129 == gt) & (d175 != gt) & region).sum(axis=(1, 2)).astype(float)
    score = 0.50 * normalize_nonzero(area) + 0.30 * normalize_nonzero(label_disagreement) + 0.20 * normalize_nonzero(d175_loss)
    candidates = np.flatnonzero(area > 0)
    if len(candidates) == 0:
        return int(gt.shape[0] // 2)
    return int(candidates[np.argmax(score[candidates])])


def crop_box(mask: np.ndarray, margin: int = 10, min_height: int = 48, min_width: int = 48) -> tuple[int, int, int, int]:
    rows, cols = np.where(mask)
    if len(rows) == 0:
        return 0, mask.shape[0], 0, mask.shape[1]
    r0 = max(0, int(rows.min()) - margin)
    r1 = min(mask.shape[0], int(rows.max()) + margin + 1)
    c0 = max(0, int(cols.min()) - margin)
    c1 = min(mask.shape[1], int(cols.max()) + margin + 1)

    if r1 - r0 < min_height:
        extra = min_height - (r1 - r0)
        r0 -= extra // 2
        r1 += extra - extra // 2
    if c1 - c0 < min_width:
        extra = min_width - (c1 - c0)
        c0 -= extra // 2
        c1 += extra - extra // 2

    r0 = max(0, r0)
    c0 = max(0, c0)
    r1 = min(mask.shape[0], r1)
    c1 = min(mask.shape[1], c1)
    return r0, r1, c0, c1


def contour_binary(ax: plt.Axes, binary: np.ndarray, color: str, linewidth: float = 0.85, alpha: float = 0.95) -> None:
    if int(binary.sum()) == 0:
        return
    ax.contour(binary.astype(float), levels=[0.5], colors=[color], linewidths=linewidth, alpha=alpha)


def ct_window(ct_slice: np.ndarray) -> np.ndarray:
    arr = np.clip(ct_slice.astype(float), -500, 1200)
    return (arr + 500) / 1700


def read_metrics(case_dir: Path) -> dict[str, str]:
    with (case_dir / "metrics.csv").open(newline="", encoding="utf-8") as f:
        return next(csv.DictReader(f))


def load_cases_summary() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    summary = DATA_DIR / "selected_cases_summary.csv"
    with summary.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["case_id"]] = row
    return out


def method_metric_text(metrics: dict[str, str]) -> str:
    d129 = float(metrics["dice_D129"])
    d175 = float(metrics["dice_D175"])
    ddice = float(metrics["diff_dice_D175_minus_D129"])
    id129 = float(metrics["id_rate_D129"])
    id175 = float(metrics["id_rate_D175"])
    did = float(metrics["diff_id_rate_D175_minus_D129"])
    return f"Dice {d129:.3f}->{d175:.3f} ({ddice:+.3f})\nID {id129:.2f}->{id175:.2f} ({did:+.2f})"


def draw_label_panel(ax: plt.Axes, labels: np.ndarray, title: str, cmap: ListedColormap) -> None:
    ax.imshow(np.zeros_like(labels), cmap="gray", vmin=0, vmax=1)
    ax.imshow(rgba_labels(labels, cmap, alpha=0.85))
    if title:
        ax.set_title(title, pad=2)
    ax.set_axis_off()


def draw_ct_overlay(ax: plt.Axes, ct_slice: np.ndarray, labels: np.ndarray, title: str, cmap: ListedColormap) -> None:
    ax.imshow(ct_window(ct_slice), cmap="gray", vmin=0, vmax=1)
    ax.imshow(rgba_labels(labels, cmap, alpha=0.48))
    contour_binary(ax, labels > 0, "white", linewidth=0.45, alpha=0.75)
    if title:
        ax.set_title(title, pad=2)
    ax.set_axis_off()


def draw_error_panel(
    ax: plt.Axes,
    ct_slice: np.ndarray,
    gt: np.ndarray,
    d129: np.ndarray,
    d175: np.ndarray,
    title: str,
) -> dict[str, int]:
    region = (gt > 0) | (d129 > 0) | (d175 > 0)
    corrected = (d129 != gt) & (d175 == gt) & region
    lost = (d129 == gt) & (d175 != gt) & region
    persistent = (d129 != gt) & (d175 != gt) & region & ~corrected & ~lost

    ax.imshow(ct_window(ct_slice), cmap="gray", vmin=0, vmax=1)
    overlay = np.zeros((*gt.shape, 4), dtype=float)
    overlay[persistent] = mpl.colors.to_rgba(PERSIST_COLOR, 0.33)
    overlay[corrected] = mpl.colors.to_rgba(GAIN_COLOR, 0.72)
    overlay[lost] = mpl.colors.to_rgba(LOSS_COLOR, 0.72)
    ax.imshow(overlay)
    if title:
        ax.set_title(title, pad=2)
    ax.set_axis_off()
    return {
        "corrected_voxels_in_slice": int(corrected.sum()),
        "lost_voxels_in_slice": int(lost.sum()),
        "persistent_error_voxels_in_slice": int(persistent.sum()),
    }


def add_panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(
        0.02,
        0.98,
        label,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8,
        fontweight="bold",
        color="black",
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.82, "pad": 0.8},
    )


def main() -> None:
    cmap = label_cmap()
    case_summary = load_cases_summary()

    fig = plt.figure(figsize=(7.45, 8.25))
    gs = fig.add_gridspec(
        nrows=4,
        ncols=5,
        width_ratios=[0.95, 1.0, 1.0, 1.0, 1.05],
        wspace=0.035,
        hspace=0.23,
    )

    headers = [
        "Whole-spine label projection",
        "GT on CT",
        "Student-8+PL70",
        "Filtered Student-8+PL",
        "D175 vs D129 error",
    ]

    qa = {
        "core_conclusion": "Paired qualitative cases show that fixed confidence filtering does not produce a consistent anatomical correction relative to the unfiltered teacher-transfer baseline.",
        "figure_archetype": "image plate + quant",
        "backend": "python/matplotlib",
        "source_data_dir": str(DATA_DIR),
        "cases": [],
    }

    for row, case_name in enumerate(CASE_ORDER):
        case_dir = DATA_DIR / case_name
        metrics = read_metrics(case_dir)
        case_id = metrics["case_id"]
        role = metrics["role"]
        fold = metrics["fold"]

        ct_img, ct = load_volume(case_dir / "ct.nii.gz")
        _, gt = load_volume(case_dir / "gt.nii.gz")
        _, d129 = load_volume(case_dir / "pred_D129.nii.gz")
        _, d175 = load_volume(case_dir / "pred_D175.nii.gz")
        gt = gt.astype(np.int16)
        d129 = d129.astype(np.int16)
        d175 = d175.astype(np.int16)

        if not (ct.shape == gt.shape == d129.shape == d175.shape):
            raise ValueError(f"Shape mismatch in {case_name}")

        x_index = choose_sagittal_index(gt, d129, d175)
        views = {
            "ct": sagittal_view(ct, x_index),
            "gt": sagittal_view(gt, x_index),
            "d129": sagittal_view(d129, x_index),
            "d175": sagittal_view(d175, x_index),
        }
        union_slice = (views["gt"] > 0) | (views["d129"] > 0) | (views["d175"] > 0)
        crop = crop_box(union_slice, margin=13)
        r0, r1, c0, c1 = crop
        cropped = {key: value[r0:r1, c0:c1] for key, value in views.items()}

        proj_gt = sagittal_projection(gt)
        proj_d129 = sagittal_projection(d129)
        proj_d175 = sagittal_projection(d175)
        proj_union = (proj_gt > 0) | (proj_d129 > 0) | (proj_d175 > 0)
        pcrop = crop_box(proj_union, margin=8)
        pr0, pr1, pc0, pc1 = pcrop
        p_gt = proj_gt[pr0:pr1, pc0:pc1]
        p_d129 = proj_d129[pr0:pr1, pc0:pc1]
        p_d175 = proj_d175[pr0:pr1, pc0:pc1]

        axes = [fig.add_subplot(gs[row, col]) for col in range(5)]
        for col, ax in enumerate(axes):
            if row == 0:
                ax.set_title(headers[col], fontsize=7.2, pad=6)

        axes[0].imshow(np.zeros_like(p_gt), cmap="gray", vmin=0, vmax=1)
        axes[0].imshow(rgba_labels(p_gt, cmap, alpha=0.82))
        contour_binary(axes[0], p_d129 > 0, D129_COLOR, linewidth=0.70)
        contour_binary(axes[0], p_d175 > 0, D175_COLOR, linewidth=0.70)
        axes[0].set_axis_off()

        draw_ct_overlay(axes[1], cropped["ct"], cropped["gt"], "", cmap)
        draw_ct_overlay(axes[2], cropped["ct"], cropped["d129"], "", cmap)
        draw_ct_overlay(axes[3], cropped["ct"], cropped["d175"], "", cmap)
        slice_errors = draw_error_panel(axes[4], cropped["ct"], cropped["gt"], cropped["d129"], cropped["d175"], "")

        row_title = f"{ROLE_LABELS.get(role, role)} | {case_id}, fold {fold}"
        axes[0].text(
            0.0,
            -0.11,
            row_title,
            transform=axes[0].transAxes,
            ha="left",
            va="top",
            fontsize=7,
            fontweight="bold",
        )
        axes[4].text(
            1.0,
            -0.11,
            method_metric_text(metrics),
            transform=axes[4].transAxes,
            ha="right",
            va="top",
            fontsize=6.5,
            linespacing=1.15,
        )
        if row == 0:
            add_panel_label(axes[0], "a")
            add_panel_label(axes[1], "b")
            add_panel_label(axes[2], "c")
            add_panel_label(axes[3], "d")
            add_panel_label(axes[4], "e")

        qa["cases"].append(
            {
                "case_dir": case_name,
                "role": role,
                "case_id": case_id,
                "fold": int(fold),
                "shape": list(ct.shape),
                "spacing_mm": [float(x) for x in ct_img.header.get_zooms()[:3]],
                "sagittal_x_index": int(x_index),
                "slice_crop_rc": [int(x) for x in crop],
                "projection_crop_rc": [int(x) for x in pcrop],
                "metrics": {
                    "dice_D129": float(metrics["dice_D129"]),
                    "dice_D175": float(metrics["dice_D175"]),
                    "diff_dice_D175_minus_D129": float(metrics["diff_dice_D175_minus_D129"]),
                    "id_rate_D129": float(metrics["id_rate_D129"]),
                    "id_rate_D175": float(metrics["id_rate_D175"]),
                    "diff_id_rate_D175_minus_D129": float(metrics["diff_id_rate_D175_minus_D129"]),
                },
                "slice_error_counts": slice_errors,
                "selected_summary": case_summary.get(case_id, {}),
            }
        )

    legend_handles = [
        Line2D([0], [0], color=D129_COLOR, lw=1.4, label="D129 contour"),
        Line2D([0], [0], color=D175_COLOR, lw=1.4, label="D175 contour"),
        Line2D([0], [0], marker="s", color="none", markerfacecolor=GAIN_COLOR, markersize=6, label="D175 correction"),
        Line2D([0], [0], marker="s", color="none", markerfacecolor=LOSS_COLOR, markersize=6, label="D175 loss"),
        Line2D([0], [0], marker="s", color="none", markerfacecolor=PERSIST_COLOR, markersize=6, label="persistent error"),
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        ncol=5,
        bbox_to_anchor=(0.5, 0.012),
        frameon=False,
        fontsize=6.8,
        handlelength=1.4,
        columnspacing=1.2,
    )
    fig.suptitle(
        "Paired anatomical examples of train-only confidence filtering",
        x=0.5,
        y=0.992,
        fontsize=9,
        fontweight="bold",
    )
    fig.text(
        0.5,
        0.965,
        "Rows show identical evaluation cases for the unfiltered Student-8+PL70 baseline and the filtered Student-8+PL model.",
        ha="center",
        va="top",
        fontsize=6.8,
    )

    fig.subplots_adjust(left=0.035, right=0.99, top=0.93, bottom=0.065)
    for suffix in [".png", ".pdf", ".svg"]:
        fig.savefig(FIG_BASE.with_suffix(suffix), dpi=600, bbox_inches="tight")
    fig.savefig(FIG_BASE.with_suffix(".tiff"), dpi=600, bbox_inches="tight", pil_kwargs={"compression": "tiff_lzw"})
    plt.close(fig)

    qa["outputs"] = {
        "png": str(FIG_BASE.with_suffix(".png")),
        "pdf": str(FIG_BASE.with_suffix(".pdf")),
        "svg": str(FIG_BASE.with_suffix(".svg")),
        "tiff": str(FIG_BASE.with_suffix(".tiff")),
    }
    (FIG_BASE.with_name(FIG_BASE.name + "_QA.json")).write_text(json.dumps(qa, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
