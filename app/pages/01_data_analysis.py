"""Data Analysis page — explore bank marketing data through interactive charts."""

import streamlit as st

from app.models import visualizer
from app.models.data_loader import get_basic_stats, get_column_info, load_train_data

st.set_page_config(page_title="数据分析", page_icon="📊", layout="wide")

st.title("📊 数据分析")


# ── Load data (cached) ──
@st.cache_data
def _load_data():
    return load_train_data()


df = _load_data()
stats = get_basic_stats(df)
col_info = get_column_info()

# ── Overview ──
st.header("数据概览")
c1, c2, c3, c4 = st.columns(4)
c1.metric("总记录数", f"{stats['row_count']:,}")
c2.metric("特征数", stats["col_count"])
c3.metric("认购率", f"{stats['subscribe_rate']}%")
c4.metric("认购人数", f"{stats['subscribe_yes']:,}")

st.markdown("---")

# ── Sidebar dimension selector ──
st.sidebar.header("分析维度")
analysis_type = st.sidebar.radio(
    "选择视图",
    ["客户画像", "营销效果", "经济指标", "自定义分析"],
)

st.header(analysis_type)

if analysis_type == "客户画像":
    tab1, tab2, tab3, tab4 = st.tabs(["年龄", "职业", "婚姻", "教育"])
    with tab1:
        st.pyplot(visualizer.fig_age_distribution(df))
    with tab2:
        st.pyplot(visualizer.fig_job_subscribe_rate(df))
    with tab3:
        st.pyplot(visualizer.fig_marital_pie(df))
    with tab4:
        st.pyplot(visualizer.fig_education_distribution(df))

elif analysis_type == "营销效果":
    tab1, tab2, tab3 = st.tabs(["联系方式", "月份趋势", "星期趋势"])
    with tab1:
        st.pyplot(visualizer.fig_contact_distribution(df))
    with tab2:
        st.pyplot(visualizer.fig_month_subscribe_rate(df))
    with tab3:
        st.pyplot(visualizer.fig_day_of_week_subscribe_rate(df))
    st.markdown("---")
    st.subheader("总体认购率")
    st.pyplot(visualizer.fig_subscribe_pie(df))

elif analysis_type == "经济指标":
    st.pyplot(visualizer.fig_economic_indicators(df))

elif analysis_type == "自定义分析":
    cat_col = st.selectbox(
        "选择分类特征",
        col_info["categorical"],
        index=col_info["categorical"].index("job"),
    )
    top_n = st.slider("显示 Top N", 5, 20, 10)
    st.pyplot(visualizer.fig_categorical_subscribe_rate(df, cat_col, top_n))

st.sidebar.caption(f"数据: train.csv · {stats['row_count']:,} 条记录")
