"""
visualizations.py
Generates all figures for the Beaumont ISD STAAR Analytics project.
Outputs PNG files to the /outputs/ directory.

Author : [Your Name]
Course : COSC5302 – Python Programming & Data Analytics
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from analysis import load_data, bisd_trend, district_comparison, subject_breakdown, gap_vs_state

# ── Setup ─────────────────────────────────────────────────────────────────────
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

PALETTE = {
    "primary":   "#1B4F8A",   # deep blue – BISD brand-adjacent
    "accent":    "#E87722",   # orange
    "light":     "#AEC6E8",
    "gray":      "#6B7280",
    "red":       "#C0392B",
    "green":     "#27AE60",
}
BISD_COLOR = PALETTE["primary"]
BISD = "Beaumont ISD"

sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({"figure.dpi": 150, "savefig.bbox": "tight",
                     "font.family": "DejaVu Sans"})


# ── Figure 1 – BISD trend line vs state average ───────────────────────────────

def fig_trend_vs_state(df: pd.DataFrame) -> None:
    gap = gap_vs_state(df)
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(gap["year"], gap["pct_met_grade_level"], marker="o", linewidth=2.5,
            color=BISD_COLOR, label="Beaumont ISD", zorder=3)
    ax.plot(gap["year"], gap["state_avg_met"], marker="s", linewidth=2.5,
            linestyle="--", color=PALETTE["accent"], label="Texas State Average", zorder=3)

    ax.fill_between(gap["year"], gap["pct_met_grade_level"], gap["state_avg_met"],
                    alpha=0.12, color=PALETTE["red"], label="Achievement Gap")

    # annotate gap in 2024
    last = gap[gap["year"] == 2024].iloc[0]
    ax.annotate(f"Gap: {last['gap']:.0f}pp",
                xy=(2024, (last["pct_met_grade_level"] + last["state_avg_met"]) / 2),
                xytext=(2022.8, 58), fontsize=10, color=PALETTE["red"],
                arrowprops=dict(arrowstyle="->", color=PALETTE["red"]),)

    ax.axvspan(2019.5, 2020.5, color="gray", alpha=0.1)
    ax.text(2020, 18, "COVID\n(No Test)", ha="center", fontsize=9, color=PALETTE["gray"])

    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel("% Met Grade Level", fontsize=11)
    ax.set_title("Beaumont ISD vs. Texas State Average\nSTAAR % Meeting Grade Level (2019–2024)", fontsize=13, fontweight="bold")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100))
    ax.set_ylim(0, 95)
    ax.legend(loc="lower right")
    plt.tight_layout()
    out = OUTPUT_DIR / "fig1_trend_vs_state.png"
    plt.savefig(out)
    plt.close()
    print(f"Saved {out}")


# ── Figure 2 – Regional district comparison bar chart ─────────────────────────

def fig_district_comparison(df: pd.DataFrame) -> None:
    comp = district_comparison(df, 2024)
    colors = [BISD_COLOR if d == BISD else PALETTE["light"] for d in comp["district"]]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(comp["district"], comp["avg_pct_met"], color=colors, edgecolor="white", height=0.6)

    for bar, val in zip(bars, comp["avg_pct_met"]):
        ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height() / 2,
                f"{val:.0f}%", va="center", fontsize=10)

    ax.axvline(comp[comp["district"] == BISD]["avg_pct_met"].values[0],
               color=BISD_COLOR, linestyle=":", linewidth=1.5, label="BISD baseline")

    ax.set_xlabel("Avg. % Meeting Grade Level", fontsize=11)
    ax.set_title("2024 STAAR Performance: Beaumont ISD vs. Jefferson County Region\n(All Subjects Combined)", fontsize=12, fontweight="bold")
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=100))
    ax.set_xlim(0, 85)
    plt.tight_layout()
    out = OUTPUT_DIR / "fig2_district_comparison.png"
    plt.savefig(out)
    plt.close()
    print(f"Saved {out}")


# ── Figure 3 – Subject-level heatmap for BISD ────────────────────────────────

def fig_subject_heatmap(df: pd.DataFrame) -> None:
    sub = subject_breakdown(df, BISD)
    pivot = sub.pivot(index="subject", columns="year", values="pct_met_grade_level")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="RdYlGn",
                vmin=20, vmax=75, linewidths=0.5, ax=ax,
                cbar_kws={"label": "% Met Grade Level"})
    ax.set_title("Beaumont ISD – STAAR Performance by Subject & Year\n(% Meeting Grade Level)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("")
    plt.tight_layout()
    out = OUTPUT_DIR / "fig3_subject_heatmap.png"
    plt.savefig(out)
    plt.close()
    print(f"Saved {out}")


# ── Figure 4 – Achievement gap over time (bar) ───────────────────────────────

def fig_achievement_gap(df: pd.DataFrame) -> None:
    gap = gap_vs_state(df)
    fig, ax = plt.subplots(figsize=(8, 4))
    bar_colors = [PALETTE["red"] if g > 17 else PALETTE["accent"] for g in gap["gap"]]
    bars = ax.bar(gap["year"], gap["gap"], color=bar_colors, edgecolor="white", width=0.6)
    for bar, val in zip(bars, gap["gap"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                f"{val:.1f}pp", ha="center", fontsize=10, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Percentage Point Gap")
    ax.set_title("Beaumont ISD Achievement Gap vs. Texas State Average\n(Percentage Points Below State)", fontsize=12, fontweight="bold")
    ax.set_ylim(0, 28)
    plt.tight_layout()
    out = OUTPUT_DIR / "fig4_achievement_gap.png"
    plt.savefig(out)
    plt.close()
    print(f"Saved {out}")


# ── Figure 5 – Math vs ELA trend comparison ──────────────────────────────────

def fig_math_vs_ela(df: pd.DataFrame) -> None:
    bisd_df = df[df["district"] == BISD]
    math_trend = bisd_df[bisd_df["subject"] == "Math"].groupby("year")["pct_met_grade_level"].mean().reset_index()
    ela_trend  = bisd_df[bisd_df["subject"] == "Reading/ELA"].groupby("year")["pct_met_grade_level"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(math_trend["year"], math_trend["pct_met_grade_level"], marker="o",
            linewidth=2.5, color=BISD_COLOR, label="Math")
    ax.plot(ela_trend["year"], ela_trend["pct_met_grade_level"], marker="^",
            linewidth=2.5, color=PALETTE["accent"], linestyle="--", label="Reading / ELA")

    ax.set_xlabel("Year")
    ax.set_ylabel("% Met Grade Level")
    ax.set_title("Beaumont ISD: Math vs. Reading/ELA Performance Trends (2019–2024)", fontsize=12, fontweight="bold")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=100))
    ax.set_ylim(0, 80)
    ax.legend()
    plt.tight_layout()
    out = OUTPUT_DIR / "fig5_math_vs_ela.png"
    plt.savefig(out)
    plt.close()
    print(f"Saved {out}")


# ── Run all ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    df = load_data()
    fig_trend_vs_state(df)
    fig_district_comparison(df)
    fig_subject_heatmap(df)
    fig_achievement_gap(df)
    fig_math_vs_ela(df)
    print("\nAll figures saved to /outputs/")
