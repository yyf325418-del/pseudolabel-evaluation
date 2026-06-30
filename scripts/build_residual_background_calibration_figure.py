from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Liberation Sans"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["font.size"] = 7
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.linewidth"] = 0.75
plt.rcParams["xtick.major.width"] = 0.75
plt.rcParams["ytick.major.width"] = 0.75
plt.rcParams["legend.frameon"] = False


OUT_DIR = Path("cmig_polished_output")
FIG_BASE = OUT_DIR / "CMIG_Figure_residual_background_calibration"
SOURCE_CSV = OUT_DIR / "CMIG_residual_background_calibration_source_data.csv"
TABLE_CSV = OUT_DIR / "CMIG_Table_residual_background_calibration.csv"
TABLE_MD = OUT_DIR / "CMIG_Table_residual_background_calibration.md"
TABLE_TEX = OUT_DIR / "CMIG_Table_residual_background_calibration.tex"
TABLE_PNG = OUT_DIR / "CMIG_Table_residual_background_calibration.png"
MAIN_TABLE_CSV = OUT_DIR / "CMIG_Table_residual_background_calibration_main_text.csv"
MAIN_TABLE_MD = OUT_DIR / "CMIG_Table_residual_background_calibration_main_text.md"
MAIN_TABLE_TEX = OUT_DIR / "CMIG_Table_residual_background_calibration_main_text.tex"
MAIN_TABLE_PNG = OUT_DIR / "CMIG_Table_residual_background_calibration_main_text.png"
CAPTION_TXT = OUT_DIR / "CMIG_Figure_residual_background_calibration_caption.txt"
QA_JSON = OUT_DIR / "CMIG_Figure_residual_background_calibration_QA.json"
OBSERVED_FILTERING_EFFECT = 0.000934


ROWS = [
    {
        "background": "D175_minus_D129_filtering",
        "delta": 0.000,
        "observed_mean_diff": -0.000934,
        "observed_sd_diff": 0.008694,
        "mean_estimate": -0.000037,
        "median_ci_low": -0.002216,
        "median_ci_high": 0.002074,
        "detection_rate_ci_excludes_zero": 0.030000,
    },
    {
        "background": "D175_minus_D129_filtering",
        "delta": 0.001,
        "observed_mean_diff": -0.000934,
        "observed_sd_diff": 0.008694,
        "mean_estimate": 0.001006,
        "median_ci_low": -0.001087,
        "median_ci_high": 0.003063,
        "detection_rate_ci_excludes_zero": 0.150000,
    },
    {
        "background": "D175_minus_D129_filtering",
        "delta": 0.003,
        "observed_mean_diff": -0.000934,
        "observed_sd_diff": 0.008694,
        "mean_estimate": 0.003073,
        "median_ci_low": 0.001074,
        "median_ci_high": 0.005157,
        "detection_rate_ci_excludes_zero": 0.776667,
    },
    {
        "background": "D175_minus_D129_filtering",
        "delta": 0.005,
        "observed_mean_diff": -0.000934,
        "observed_sd_diff": 0.008694,
        "mean_estimate": 0.004979,
        "median_ci_low": 0.002983,
        "median_ci_high": 0.006930,
        "detection_rate_ci_excludes_zero": 0.956667,
    },
    {
        "background": "D175_minus_D129_filtering",
        "delta": 0.010,
        "observed_mean_diff": -0.000934,
        "observed_sd_diff": 0.008694,
        "mean_estimate": 0.010089,
        "median_ci_low": 0.007914,
        "median_ci_high": 0.012139,
        "detection_rate_ci_excludes_zero": 1.000000,
    },
    {
        "background": "D175_minus_D129_filtering",
        "delta": 0.020,
        "observed_mean_diff": -0.000934,
        "observed_sd_diff": 0.008694,
        "mean_estimate": 0.020063,
        "median_ci_low": 0.017989,
        "median_ci_high": 0.022112,
        "detection_rate_ci_excludes_zero": 1.000000,
    },
    {
        "background": "D162_minus_D119_second_residual",
        "delta": 0.000,
        "observed_mean_diff": -0.001773,
        "observed_sd_diff": 0.016465,
        "mean_estimate": 0.000072,
        "median_ci_low": -0.004060,
        "median_ci_high": 0.004339,
        "detection_rate_ci_excludes_zero": 0.033333,
    },
    {
        "background": "D162_minus_D119_second_residual",
        "delta": 0.001,
        "observed_mean_diff": -0.001773,
        "observed_sd_diff": 0.016465,
        "mean_estimate": 0.001084,
        "median_ci_low": -0.003208,
        "median_ci_high": 0.005366,
        "detection_rate_ci_excludes_zero": 0.086667,
    },
    {
        "background": "D162_minus_D119_second_residual",
        "delta": 0.003,
        "observed_mean_diff": -0.001773,
        "observed_sd_diff": 0.016465,
        "mean_estimate": 0.002926,
        "median_ci_low": -0.001100,
        "median_ci_high": 0.007111,
        "detection_rate_ci_excludes_zero": 0.273333,
    },
    {
        "background": "D162_minus_D119_second_residual",
        "delta": 0.005,
        "observed_mean_diff": -0.001773,
        "observed_sd_diff": 0.016465,
        "mean_estimate": 0.005028,
        "median_ci_low": 0.000808,
        "median_ci_high": 0.009325,
        "detection_rate_ci_excludes_zero": 0.606667,
    },
    {
        "background": "D162_minus_D119_second_residual",
        "delta": 0.010,
        "observed_mean_diff": -0.001773,
        "observed_sd_diff": 0.016465,
        "mean_estimate": 0.010005,
        "median_ci_low": 0.005780,
        "median_ci_high": 0.014357,
        "detection_rate_ci_excludes_zero": 0.980000,
    },
    {
        "background": "D162_minus_D119_second_residual",
        "delta": 0.020,
        "observed_mean_diff": -0.001773,
        "observed_sd_diff": 0.016465,
        "mean_estimate": 0.020121,
        "median_ci_low": 0.015805,
        "median_ci_high": 0.024263,
        "detection_rate_ci_excludes_zero": 1.000000,
    },
    {
        "background": "D129_minus_D119_third_residual",
        "delta": 0.000,
        "observed_mean_diff": -0.000827,
        "observed_sd_diff": 0.016767,
        "mean_estimate": -0.000008,
        "median_ci_low": -0.003680,
        "median_ci_high": 0.003949,
        "detection_rate_ci_excludes_zero": 0.013333,
    },
    {
        "background": "D129_minus_D119_third_residual",
        "delta": 0.001,
        "observed_mean_diff": -0.000827,
        "observed_sd_diff": 0.016767,
        "mean_estimate": 0.000947,
        "median_ci_low": -0.002850,
        "median_ci_high": 0.004755,
        "detection_rate_ci_excludes_zero": 0.056667,
    },
    {
        "background": "D129_minus_D119_third_residual",
        "delta": 0.003,
        "observed_mean_diff": -0.000827,
        "observed_sd_diff": 0.016767,
        "mean_estimate": 0.003159,
        "median_ci_low": -0.000423,
        "median_ci_high": 0.006930,
        "detection_rate_ci_excludes_zero": 0.363333,
    },
    {
        "background": "D129_minus_D119_third_residual",
        "delta": 0.005,
        "observed_mean_diff": -0.000827,
        "observed_sd_diff": 0.016767,
        "mean_estimate": 0.005093,
        "median_ci_low": 0.001285,
        "median_ci_high": 0.009055,
        "detection_rate_ci_excludes_zero": 0.776667,
    },
    {
        "background": "D129_minus_D119_third_residual",
        "delta": 0.010,
        "observed_mean_diff": -0.000827,
        "observed_sd_diff": 0.016767,
        "mean_estimate": 0.010006,
        "median_ci_low": 0.006411,
        "median_ci_high": 0.013725,
        "detection_rate_ci_excludes_zero": 1.000000,
    },
    {
        "background": "D129_minus_D119_third_residual",
        "delta": 0.020,
        "observed_mean_diff": -0.000827,
        "observed_sd_diff": 0.016767,
        "mean_estimate": 0.020089,
        "median_ci_low": 0.016470,
        "median_ci_high": 0.023960,
        "detection_rate_ci_excludes_zero": 1.000000,
    },
]


BACKGROUND_ORDER = [
    "D175_minus_D129_filtering",
    "D162_minus_D119_second_residual",
    "D129_minus_D119_third_residual",
]

LABELS = {
    "D175_minus_D129_filtering": "Filtering residual\n(D175-D129)",
    "D162_minus_D119_second_residual": "Second residual\n(D162-D119)",
    "D129_minus_D119_third_residual": "Third residual\n(D129-D119)",
}

SHORT_LABELS = {
    "D175_minus_D129_filtering": "D175-D129 filtering",
    "D162_minus_D119_second_residual": "D162-D119 second residual",
    "D129_minus_D119_third_residual": "D129-D119 third residual",
}

COLORS = {
    "D175_minus_D129_filtering": "#0F4D92",
    "D162_minus_D119_second_residual": "#42949E",
    "D129_minus_D119_third_residual": "#9A4D8E",
}

MARKERS = {
    "D175_minus_D129_filtering": "o",
    "D162_minus_D119_second_residual": "s",
    "D129_minus_D119_third_residual": "^",
}


def grouped_rows():
    return {
        key: sorted([row for row in ROWS if row["background"] == key], key=lambda x: x["delta"])
        for key in BACKGROUND_ORDER
    }


def write_source_csv():
    fields = [
        "background",
        "delta",
        "observed_mean_diff",
        "observed_sd_diff",
        "mean_estimate",
        "median_ci_low",
        "median_ci_high",
        "detection_rate_ci_excludes_zero",
    ]
    with SOURCE_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(ROWS)
    with TABLE_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(ROWS)
    main_fields = [
        "residual_background",
        "observed_sd_diff",
        "fp_delta_0",
        "detect_delta_0_001",
        "detect_delta_0_003",
        "detect_delta_0_005",
        "detect_delta_0_010",
    ]
    with MAIN_TABLE_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=main_fields)
        writer.writeheader()
        for row in main_table_records_raw():
            writer.writerow(row)


def fmt_delta(value):
    if value == 0:
        return "0"
    if value < 0.01:
        return f"{value:.3f}"
    return f"{value:.2f}"


def fmt4(value):
    return f"{value:.4f}"


def pct(value):
    return f"{100 * value:.1f}"


def table_records():
    records = []
    for row in ROWS:
        records.append(
            {
                "Residual background": SHORT_LABELS[row["background"]],
                "Injected delta": fmt_delta(row["delta"]),
                "Residual mean": fmt4(row["observed_mean_diff"]),
                "Residual SD": fmt4(row["observed_sd_diff"]),
                "Recovered mean": fmt4(row["mean_estimate"]),
                "Median CI": f"[{fmt4(row['median_ci_low'])}, {fmt4(row['median_ci_high'])}]",
                "CI excludes 0 (%)": pct(row["detection_rate_ci_excludes_zero"]),
            }
        )
    return records


def detection_for(background, delta):
    for row in ROWS:
        if row["background"] == background and abs(row["delta"] - delta) < 1e-12:
            return row["detection_rate_ci_excludes_zero"]
    raise KeyError((background, delta))


def sd_for(background):
    for row in ROWS:
        if row["background"] == background:
            return row["observed_sd_diff"]
    raise KeyError(background)


def main_table_records_raw():
    records = []
    for background in BACKGROUND_ORDER:
        records.append(
            {
                "residual_background": SHORT_LABELS[background],
                "observed_sd_diff": sd_for(background),
                "fp_delta_0": detection_for(background, 0.000),
                "detect_delta_0_001": detection_for(background, 0.001),
                "detect_delta_0_003": detection_for(background, 0.003),
                "detect_delta_0_005": detection_for(background, 0.005),
                "detect_delta_0_010": detection_for(background, 0.010),
            }
        )
    return records


def main_table_records():
    records = []
    for row in main_table_records_raw():
        records.append(
            {
                "Residual background": row["residual_background"],
                "Observed SD": fmt4(row["observed_sd_diff"]),
                "FP at delta=0 (%)": pct(row["fp_delta_0"]),
                "Detect delta=0.001 (%)": pct(row["detect_delta_0_001"]),
                "Detect delta=0.003 (%)": pct(row["detect_delta_0_003"]),
                "Detect delta=0.005 (%)": pct(row["detect_delta_0_005"]),
                "Detect delta=0.010 (%)": pct(row["detect_delta_0_010"]),
            }
        )
    return records


def write_markdown_table():
    records = table_records()
    headers = list(records[0].keys())
    lines = []
    lines.append("# Residual-background injected-effect calibration")
    lines.append("")
    lines.append(
        "Table. Injected-effect recovery and CI-exclusion rate across three empirical residual backgrounds."
    )
    lines.append("")
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for record in records:
        lines.append("| " + " | ".join(record[h] for h in headers) + " |")
    lines.append("")
    lines.append(
        "Note: CI columns follow the input `median_ci_low` and `median_ci_high` fields. "
        "Confirm the bootstrap replicate definition before final manuscript insertion."
    )
    TABLE_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    main_records = main_table_records()
    main_headers = list(main_records[0].keys())
    main_lines = []
    main_lines.append("# Main-text residual-background calibration summary")
    main_lines.append("")
    main_lines.append(
        "Table. Compact detection-rate summary across empirical residual backgrounds."
    )
    main_lines.append("")
    main_lines.append("| " + " | ".join(main_headers) + " |")
    main_lines.append("| " + " | ".join(["---"] * len(main_headers)) + " |")
    for record in main_records:
        main_lines.append("| " + " | ".join(record[h] for h in main_headers) + " |")
    main_lines.append("")
    main_lines.append(
        "Note: Detection values are the percentage of simulated experiments in which the bootstrap CI excluded zero. "
        f"The observed filtering effect, |delta Dice| = {OBSERVED_FILTERING_EFFECT:.4f}, lies just below the 0.001 injected-effect level."
    )
    MAIN_TABLE_MD.write_text("\n".join(main_lines) + "\n", encoding="utf-8")


def latex_escape(text):
    return (
        text.replace("\\", "\\textbackslash{}")
        .replace("_", "\\_")
        .replace("%", "\\%")
        .replace("&", "\\&")
    )


def write_latex_table():
    records = table_records()
    headers = list(records[0].keys())
    colspec = "llrrrrr"
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Injected-effect recovery across empirical residual backgrounds.}",
        "\\label{tab:residual-background-calibration}",
        "\\begin{tabular}{" + colspec + "}",
        "\\hline",
        " & ".join(latex_escape(h) for h in headers) + " \\\\",
        "\\hline",
    ]
    for record in records:
        lines.append(" & ".join(latex_escape(record[h]) for h in headers) + " \\\\")
    lines.extend(
        [
            "\\hline",
            "\\end{tabular}",
            "\\begin{flushleft}",
            "\\footnotesize CI columns follow the median lower and upper confidence-limit fields in the source data; verify the bootstrap replicate definition before final submission.",
            "\\end{flushleft}",
            "\\end{table}",
        ]
    )
    TABLE_TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")

    main_records = main_table_records()
    main_headers = list(main_records[0].keys())
    main_lines = [
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Compact residual-background sensitivity summary.}",
        "\\label{tab:residual-background-calibration-main}",
        "\\begin{tabular}{lrrrrrr}",
        "\\hline",
        " & ".join(latex_escape(h) for h in main_headers) + " \\\\",
        "\\hline",
    ]
    for record in main_records:
        main_lines.append(" & ".join(latex_escape(record[h]) for h in main_headers) + " \\\\")
    main_lines.extend(
        [
            "\\hline",
            "\\end{tabular}",
            "\\begin{flushleft}",
            "\\footnotesize Detection values are percentages of simulated experiments in which the bootstrap CI excluded zero. "
            f"The observed filtering effect, $|\\Delta Dice| = {OBSERVED_FILTERING_EFFECT:.4f}$, lies just below the 0.001 injected-effect level.",
            "\\end{flushleft}",
            "\\end{table}",
        ]
    )
    MAIN_TABLE_TEX.write_text("\n".join(main_lines) + "\n", encoding="utf-8")


def add_panel_label(ax, label):
    ax.text(
        -0.12,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=8,
        fontweight="bold",
        ha="left",
        va="bottom",
    )


def make_figure():
    groups = grouped_rows()
    fig = plt.figure(figsize=(7.2, 5.2))
    gs = fig.add_gridspec(
        nrows=2,
        ncols=2,
        height_ratios=[1.25, 1.0],
        width_ratios=[1.45, 1.0],
        hspace=0.42,
        wspace=0.36,
    )
    ax_a = fig.add_subplot(gs[0, :])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[1, 1])

    delta_levels = np.array([0.000, 0.001, 0.003, 0.005, 0.010, 0.020])
    x_ticks = np.arange(len(delta_levels))
    delta_to_position = {float(delta): idx for idx, delta in enumerate(delta_levels)}
    observed_x = OBSERVED_FILTERING_EFFECT / 0.001
    jitter = {
        "D175_minus_D129_filtering": -0.055,
        "D162_minus_D119_second_residual": 0.0,
        "D129_minus_D119_third_residual": 0.055,
    }

    ax_a.plot(
        x_ticks,
        delta_levels,
        color="#767676",
        linestyle=(0, (3, 2)),
        linewidth=1.0,
        zorder=0,
        label="expected recovery",
    )
    ax_a.axhline(0, color="#BDBDBD", linewidth=0.8, zorder=0)
    for ax in (ax_a, ax_b):
        ax.axvspan(
            observed_x - 0.035,
            observed_x + 0.035,
            color="#F0E0D0",
            alpha=0.75,
            zorder=0,
            linewidth=0,
        )
        ax.axvline(
            observed_x,
            color="#8A5A2B",
            linestyle=(0, (3, 2)),
            linewidth=1.05,
            zorder=1,
        )

    for background in BACKGROUND_ORDER:
        rows = groups[background]
        x = np.array([delta_to_position[float(r["delta"])] for r in rows])
        y = np.array([r["mean_estimate"] for r in rows])
        lo = np.array([r["median_ci_low"] for r in rows])
        hi = np.array([r["median_ci_high"] for r in rows])
        yerr = np.vstack([y - lo, hi - y])
        ax_a.errorbar(
            x + jitter[background],
            y,
            yerr=yerr,
            color=COLORS[background],
            marker=MARKERS[background],
            markersize=4.2,
            linewidth=1.35,
            elinewidth=0.95,
            capsize=2.2,
            label=LABELS[background].replace("\n", " "),
        )

    ax_a.set_xlim(-0.35, len(delta_levels) - 0.65)
    ax_a.set_ylim(-0.0050, 0.0254)
    ax_a.set_xticks(x_ticks)
    ax_a.set_xticklabels([fmt_delta(x) for x in delta_levels])
    ax_a.set_ylabel("Recovered effect estimate")
    ax_a.set_xlabel("Injected effect level (delta Dice)")
    ax_a.set_title("Recovered estimates track injected effects", loc="left", pad=8)
    ax_a.annotate(
        "observed filtering\neffect \u2248 0.0009",
        xy=(observed_x, 0.0008),
        xytext=(1.35, -0.0035),
        arrowprops={"arrowstyle": "-", "color": "#8A5A2B", "linewidth": 0.8},
        color="#6F431D",
        fontsize=6.5,
        ha="left",
        va="bottom",
    )
    ax_a.legend(ncol=3, loc="upper left", bbox_to_anchor=(0.0, 1.01), fontsize=6.4, handlelength=2.0)
    add_panel_label(ax_a, "a")

    for background in BACKGROUND_ORDER:
        rows = groups[background]
        x = np.array([delta_to_position[float(r["delta"])] for r in rows])
        y = np.array([r["detection_rate_ci_excludes_zero"] for r in rows])
        ax_b.plot(
            x,
            y,
            color=COLORS[background],
            marker=MARKERS[background],
            markersize=4.0,
            linewidth=1.35,
        )
    ax_b.axhline(0.8, color="#BDBDBD", linestyle=(0, (2, 2)), linewidth=0.85)
    ax_b.set_xlim(-0.15, len(delta_levels) - 0.85)
    ax_b.set_ylim(-0.03, 1.05)
    ax_b.set_xticks(x_ticks)
    ax_b.set_xticklabels([fmt_delta(x) for x in delta_levels])
    ax_b.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax_b.set_ylabel("Runs with CI excluding zero")
    ax_b.set_xlabel("Injected effect level (delta Dice)")
    ax_b.set_title("Detectability depends on empirical residual noise", loc="left", pad=8)
    ax_b.text(5.0, 0.81, "0.8", color="#767676", fontsize=6, ha="right", va="bottom")
    ax_b.annotate(
        "observed filtering\neffect \u2248 0.0009",
        xy=(observed_x, 0.08),
        xytext=(1.35, 0.17),
        arrowprops={"arrowstyle": "-", "color": "#8A5A2B", "linewidth": 0.8},
        color="#6F431D",
        fontsize=6.5,
        ha="left",
        va="bottom",
    )
    add_panel_label(ax_b, "b")

    sd_vals = []
    mean_vals = []
    for background in BACKGROUND_ORDER:
        first = groups[background][0]
        sd_vals.append(first["observed_sd_diff"])
        mean_vals.append(first["observed_mean_diff"])

    x_pos = np.arange(len(BACKGROUND_ORDER))
    bars = ax_c.bar(
        x_pos,
        sd_vals,
        color=[COLORS[b] for b in BACKGROUND_ORDER],
        alpha=0.88,
        edgecolor="#272727",
        linewidth=0.6,
        width=0.62,
    )
    ax_c.set_xticks(x_pos)
    ax_c.set_xticklabels([LABELS[b] for b in BACKGROUND_ORDER], rotation=0, ha="center")
    ax_c.set_ylabel("Observed SD of paired differences")
    ax_c.set_title("Residual backgrounds span different noise scales", loc="left", pad=8)
    ax_c.set_ylim(0, 0.0195)
    for idx, (bar, sd, mean) in enumerate(zip(bars, sd_vals, mean_vals)):
        ax_c.text(
            bar.get_x() + bar.get_width() / 2,
            sd + 0.00055,
            f"SD {sd:.4f}\nmean {mean:.4f}",
            ha="center",
            va="bottom",
            fontsize=6.3,
            color="#272727",
        )
    add_panel_label(ax_c, "c")

    for ax in (ax_a, ax_b, ax_c):
        ax.tick_params(axis="both", labelsize=6.7, length=3)
        ax.grid(axis="y", color="#E6E6E6", linewidth=0.55)
        ax.set_axisbelow(True)

    fig.align_ylabels([ax_a, ax_b, ax_c])
    fig.savefig(FIG_BASE.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(FIG_BASE.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(FIG_BASE.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(FIG_BASE.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def make_table_png():
    records = table_records()
    headers = list(records[0].keys())
    cell_text = [[record[h] for h in headers] for record in records]
    fig, ax = plt.subplots(figsize=(10.5, 7.4))
    ax.axis("off")
    table = ax.table(
        cellText=cell_text,
        colLabels=headers,
        cellLoc="center",
        colLoc="center",
        loc="center",
        colWidths=[0.22, 0.09, 0.10, 0.09, 0.11, 0.22, 0.12],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(6.2)
    table.scale(1, 1.33)
    for (row, col), cell in table.get_celld().items():
        cell.set_linewidth(0.35)
        cell.set_edgecolor("#BDBDBD")
        if row == 0:
            cell.set_facecolor("#F0F0F0")
            cell.set_text_props(weight="bold", color="#272727")
        elif row % 2 == 0:
            cell.set_facecolor("#FAFAFA")
        else:
            cell.set_facecolor("white")
    fig.savefig(TABLE_PNG, dpi=450, bbox_inches="tight")
    plt.close(fig)

    main_records = main_table_records()
    main_headers = list(main_records[0].keys())
    main_cell_text = [[record[h] for h in main_headers] for record in main_records]
    fig, ax = plt.subplots(figsize=(10.5, 1.9))
    ax.axis("off")
    table = ax.table(
        cellText=main_cell_text,
        colLabels=main_headers,
        cellLoc="center",
        colLoc="center",
        loc="center",
        colWidths=[0.23, 0.10, 0.13, 0.14, 0.14, 0.14, 0.14],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(6.5)
    table.scale(1, 1.35)
    for (row, col), cell in table.get_celld().items():
        cell.set_linewidth(0.35)
        cell.set_edgecolor("#BDBDBD")
        if row == 0:
            cell.set_facecolor("#F0F0F0")
            cell.set_text_props(weight="bold", color="#272727")
        elif row % 2 == 0:
            cell.set_facecolor("#FAFAFA")
        else:
            cell.set_facecolor("white")
    fig.savefig(MAIN_TABLE_PNG, dpi=450, bbox_inches="tight")
    plt.close(fig)


def write_caption_and_qa():
    caption = (
        "Figure X. Residual-background sensitivity analysis for injected small-effect calibration. "
        "(a) Recovered effect estimates with median confidence limits across three empirical residual "
        "backgrounds. The dashed line indicates exact recovery of the injected Dice effect. "
        "The tan vertical marker denotes the observed filtering effect magnitude (|delta Dice| = 0.0009). "
        "(b) Detection rate, defined as the proportion of runs for which the confidence interval "
        "excluded zero, increased with the injected effect but depended on the empirical residual "
        "noise scale; the x-axis uses categorical spacing for the tested injected-effect levels. "
        "(c) Observed standard deviations and mean paired differences of the three residual backgrounds "
        "used for injection."
    )
    CAPTION_TXT.write_text(caption + "\n", encoding="utf-8")

    qa = {
        "core_conclusion": (
            "Injected effects are recovered near their target values across three empirical residual "
            "backgrounds, while the probability of excluding zero depends on residual noise."
        ),
        "archetype": "quantitative grid",
        "backend": "python/matplotlib",
        "source_data": str(SOURCE_CSV),
        "exports": [
            str(FIG_BASE.with_suffix(".svg")),
            str(FIG_BASE.with_suffix(".pdf")),
            str(FIG_BASE.with_suffix(".png")),
            str(FIG_BASE.with_suffix(".tiff")),
            str(TABLE_CSV),
            str(TABLE_MD),
            str(TABLE_TEX),
            str(TABLE_PNG),
            str(MAIN_TABLE_CSV),
            str(MAIN_TABLE_MD),
            str(MAIN_TABLE_TEX),
            str(MAIN_TABLE_PNG),
        ],
        "style_checks": {
            "svg_text_editable": True,
            "pdf_fonttype": 42,
            "dpi_png_tiff": 600,
            "single_backend_used": True,
            "source_data_traceable": True,
        },
        "manuscript_checks_needed": [
            "Confirm whether median_ci_low/high are 95% bootstrap confidence limits.",
            "Confirm the number of bootstrap/injection runs represented by detection_rate_ci_excludes_zero.",
            "Confirm whether residual backgrounds should be anonymized or renamed in final supplementary material.",
        ],
    }
    QA_JSON.write_text(json.dumps(qa, indent=2), encoding="utf-8")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_source_csv()
    write_markdown_table()
    write_latex_table()
    make_figure()
    make_table_png()
    write_caption_and_qa()
    print("Wrote:")
    for path in [
        SOURCE_CSV,
        FIG_BASE.with_suffix(".svg"),
        FIG_BASE.with_suffix(".pdf"),
        FIG_BASE.with_suffix(".png"),
        FIG_BASE.with_suffix(".tiff"),
            TABLE_CSV,
            TABLE_MD,
            TABLE_TEX,
            TABLE_PNG,
            MAIN_TABLE_CSV,
            MAIN_TABLE_MD,
            MAIN_TABLE_TEX,
            MAIN_TABLE_PNG,
            CAPTION_TXT,
            QA_JSON,
    ]:
        print(path)


if __name__ == "__main__":
    main()
