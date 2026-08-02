"""Visualization logic for bank marketing data analysis.

Pure functions that generate matplotlib figures. Separated from
Streamlit UI so they can be unit-tested independently.
"""

import matplotlib.pyplot as plt
import pandas as pd

# ── Colour palette ──
PRIMARY = "#1f77b4"
ACCENT = "#ff7f0e"
SUCCESS = "#2ca02c"
DANGER = "#d62728"


def _ensure_matplotlib_font() -> None:
    """Set a broadly available sans-serif font to avoid CJK glyph warnings."""
    plt.rcParams["font.family"] = "sans-serif"


def fig_age_distribution(df: pd.DataFrame) -> plt.Figure:
    """Histogram of customer age distribution."""
    _ensure_matplotlib_font()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["age"].dropna(), bins=30, color=PRIMARY, edgecolor="white", alpha=0.85)
    ax.set_xlabel("Age")
    ax.set_ylabel("Count")
    ax.set_title("Age Distribution")
    fig.tight_layout()
    return fig


def fig_job_subscribe_rate(df: pd.DataFrame) -> plt.Figure:
    """Bar chart: subscribe rate by job category."""
    _ensure_matplotlib_font()
    job_rate = (
        df.groupby("job")["subscribe"]
        .apply(lambda x: (x == "yes").mean() * 100)
        .sort_values(ascending=False)
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(job_rate.index, job_rate.values, color=ACCENT, edgecolor="white")
    ax.set_xlabel("Job")
    ax.set_ylabel("Subscribe Rate (%)")
    ax.set_title("Subscribe Rate by Job")
    ax.tick_params(axis="x", rotation=45)
    for bar, val in zip(bars, job_rate.values, strict=False):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{val:.1f}%",
            ha="center",
            fontsize=8,
        )
    fig.tight_layout()
    return fig


def fig_marital_pie(df: pd.DataFrame) -> plt.Figure:
    """Pie chart of marital status distribution."""
    _ensure_matplotlib_font()
    counts = df["marital"].value_counts()
    colors = [PRIMARY, ACCENT, SUCCESS, DANGER][: len(counts)]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", colors=colors, startangle=90)
    ax.set_title("Marital Status Distribution")
    return fig


def fig_education_distribution(df: pd.DataFrame) -> plt.Figure:
    """Bar chart of education level distribution."""
    _ensure_matplotlib_font()
    edu_counts = df["education"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(edu_counts.index, edu_counts.values, color=PRIMARY, edgecolor="white")
    ax.set_xlabel("Education")
    ax.set_ylabel("Count")
    ax.set_title("Education Level Distribution")
    ax.tick_params(axis="x", rotation=30)
    for bar, val in zip(bars, edu_counts.values, strict=False):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 50,
            str(val),
            ha="center",
            fontsize=9,
        )
    fig.tight_layout()
    return fig


def fig_contact_distribution(df: pd.DataFrame) -> plt.Figure:
    """Pie chart of contact type distribution."""
    _ensure_matplotlib_font()
    counts = df["contact"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=[PRIMARY, ACCENT],
        startangle=90,
    )
    ax.set_title("Contact Type Distribution")
    return fig


def fig_month_subscribe_rate(df: pd.DataFrame) -> plt.Figure:
    """Bar chart: subscribe rate by month."""
    _ensure_matplotlib_font()
    month_order = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ]
    month_rate = df.groupby("month")["subscribe"].apply(lambda x: (x == "yes").mean() * 100)
    available = [m for m in month_order if m in month_rate.index]
    ordered = month_rate[available]
    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(ordered.index, ordered.values, color=SUCCESS, edgecolor="white")
    ax.set_xlabel("Month")
    ax.set_ylabel("Subscribe Rate (%)")
    ax.set_title("Subscribe Rate by Month")
    for bar, val in zip(bars, ordered.values, strict=False):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{val:.1f}%",
            ha="center",
            fontsize=8,
        )
    fig.tight_layout()
    return fig


def fig_day_of_week_subscribe_rate(df: pd.DataFrame) -> plt.Figure:
    """Bar chart: subscribe rate by day of week."""
    _ensure_matplotlib_font()
    day_order = ["mon", "tue", "wed", "thu", "fri"]
    day_rate = df.groupby("day_of_week")["subscribe"].apply(lambda x: (x == "yes").mean() * 100)
    available = [d for d in day_order if d in day_rate.index]
    ordered = day_rate[available]
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(ordered.index, ordered.values, color=ACCENT, edgecolor="white")
    ax.set_xlabel("Day of Week")
    ax.set_ylabel("Subscribe Rate (%)")
    ax.set_title("Subscribe Rate by Day of Week")
    for bar, val in zip(bars, ordered.values, strict=False):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{val:.1f}%",
            ha="center",
            fontsize=9,
        )
    fig.tight_layout()
    return fig


def fig_economic_indicators(df: pd.DataFrame) -> plt.Figure:
    """Histogram grid for 5 economic indicators."""
    _ensure_matplotlib_font()
    indicators = [
        "emp_var_rate",
        "cons_price_index",
        "cons_conf_index",
        "lending_rate3m",
        "nr_employed",
    ]
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()
    for i, col in enumerate(indicators):
        axes[i].hist(df[col].dropna(), bins=40, color=PRIMARY, edgecolor="white", alpha=0.85)
        axes[i].set_title(col.replace("_", " ").title())
        axes[i].set_xlabel("")
        axes[i].set_ylabel("Count")
    # Hide unused 6th subplot
    axes[5].set_visible(False)
    fig.suptitle("Economic Indicators Distribution", fontsize=14)
    fig.tight_layout()
    return fig


def fig_subscribe_pie(df: pd.DataFrame) -> plt.Figure:
    """Pie chart of overall subscribe rate."""
    _ensure_matplotlib_font()
    counts = df["subscribe"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        counts.values,
        labels=["No", "Yes"],
        autopct="%1.1f%%",
        colors=[DANGER, SUCCESS],
        startangle=90,
        explode=(0, 0.05),
    )
    ax.set_title("Overall Subscribe Rate")
    return fig


def fig_categorical_subscribe_rate(df: pd.DataFrame, col: str, top_n: int = 10) -> plt.Figure:
    """Generic bar chart: subscribe rate for any categorical column."""
    _ensure_matplotlib_font()
    rate = (
        df.groupby(col)["subscribe"]
        .apply(lambda x: (x == "yes").mean() * 100)
        .sort_values(ascending=False)
        .head(top_n)
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(rate.index, rate.values, color=PRIMARY, edgecolor="white")
    ax.set_xlabel(col.replace("_", " ").title())
    ax.set_ylabel("Subscribe Rate (%)")
    ax.set_title(f"Subscribe Rate by {col.replace('_', ' ').title()}")
    ax.tick_params(axis="x", rotation=45)
    for bar, val in zip(bars, rate.values, strict=False):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{val:.1f}%",
            ha="center",
            fontsize=8,
        )
    fig.tight_layout()
    return fig
