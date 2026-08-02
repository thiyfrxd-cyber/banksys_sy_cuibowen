"""Tests for app.models.visualizer — figure generation functions."""

import matplotlib
import pandas as pd
import pytest

matplotlib.use("Agg")  # Non-interactive backend for testing

from app.models import visualizer
from app.models.data_loader import load_train_data


@pytest.fixture(scope="module")
def train_df():
    return load_train_data()


class TestAgeDistribution:
    def test_returns_figure(self, train_df):
        fig = visualizer.fig_age_distribution(train_df)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_has_single_axes(self, train_df):
        fig = visualizer.fig_age_distribution(train_df)
        assert len(fig.axes) == 1

    def test_title_set(self, train_df):
        fig = visualizer.fig_age_distribution(train_df)
        assert fig.axes[0].get_title() != ""


class TestJobSubscribeRate:
    def test_returns_figure(self, train_df):
        fig = visualizer.fig_job_subscribe_rate(train_df)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_bars_match_job_categories(self, train_df):
        fig = visualizer.fig_job_subscribe_rate(train_df)
        bars = fig.axes[0].containers[0]
        assert len(bars) == train_df["job"].nunique()


class TestMaritalPie:
    def test_returns_figure(self, train_df):
        fig = visualizer.fig_marital_pie(train_df)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_pie_has_wedges(self, train_df):
        fig = visualizer.fig_marital_pie(train_df)
        assert len(fig.axes[0].patches) >= 2


class TestEducationDistribution:
    def test_returns_figure(self, train_df):
        fig = visualizer.fig_education_distribution(train_df)
        assert isinstance(fig, matplotlib.figure.Figure)


class TestContactDistribution:
    def test_returns_figure(self, train_df):
        fig = visualizer.fig_contact_distribution(train_df)
        assert isinstance(fig, matplotlib.figure.Figure)


class TestMonthSubscribeRate:
    def test_returns_figure(self, train_df):
        fig = visualizer.fig_month_subscribe_rate(train_df)
        assert isinstance(fig, matplotlib.figure.Figure)


class TestDayOfWeekSubscribeRate:
    def test_returns_figure(self, train_df):
        fig = visualizer.fig_day_of_week_subscribe_rate(train_df)
        assert isinstance(fig, matplotlib.figure.Figure)


class TestEconomicIndicators:
    def test_returns_figure(self, train_df):
        fig = visualizer.fig_economic_indicators(train_df)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_has_multiple_subplots(self, train_df):
        fig = visualizer.fig_economic_indicators(train_df)
        # 6 subplots created, 1 hidden = 5 visible
        visible = [ax for ax in fig.axes if ax.get_visible()]
        assert len(visible) == 5


class TestSubscribePie:
    def test_returns_figure(self, train_df):
        fig = visualizer.fig_subscribe_pie(train_df)
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_has_two_wedges(self, train_df):
        fig = visualizer.fig_subscribe_pie(train_df)
        _ = [t.get_text() for t in fig.axes[0].texts if t.get_text()]
        assert len(fig.axes[0].patches) == 2


class TestCategoricalSubscribeRate:
    def test_returns_figure(self, train_df):
        fig = visualizer.fig_categorical_subscribe_rate(train_df, "job")
        assert isinstance(fig, matplotlib.figure.Figure)

    def test_respects_top_n(self, train_df):
        fig = visualizer.fig_categorical_subscribe_rate(train_df, "education", top_n=3)
        bars = fig.axes[0].containers[0]
        assert len(bars) <= 3


class TestFontSettings:
    def test_font_family_is_set(self):
        visualizer._ensure_matplotlib_font()
        family = matplotlib.rcParams["font.family"]
        assert "sans-serif" in family


class TestSmokeWithSmallData:
    """Verify functions handle a small artificial dataset without crashing."""

    @pytest.fixture
    def small_df(self):
        return pd.DataFrame(
            {
                "age": [30, 40, 50],
                "job": ["admin.", "blue-collar", "technician"],
                "marital": ["single", "married", "divorced"],
                "education": ["high.school", "university.degree", "basic.9y"],
                "contact": ["cellular", "telephone", "cellular"],
                "month": ["may", "jun", "jul"],
                "day_of_week": ["mon", "tue", "wed"],
                "subscribe": ["yes", "no", "yes"],
                "emp_var_rate": [1.4, -1.8, 0.5],
                "cons_price_index": [90.0, 95.0, 92.0],
                "cons_conf_index": [-35.0, -40.0, -38.0],
                "lending_rate3m": [0.69, 4.05, 3.0],
                "nr_employed": [5000.0, 5100.0, 5050.0],
            }
        )

    def test_all_functions_no_crash(self, small_df):
        """Each visualization function should not crash."""
        visualizer.fig_age_distribution(small_df)
        visualizer.fig_job_subscribe_rate(small_df)
        visualizer.fig_marital_pie(small_df)
        visualizer.fig_education_distribution(small_df)
        visualizer.fig_contact_distribution(small_df)
        visualizer.fig_month_subscribe_rate(small_df)
        visualizer.fig_day_of_week_subscribe_rate(small_df)
        visualizer.fig_economic_indicators(small_df)
        visualizer.fig_subscribe_pie(small_df)
