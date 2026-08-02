"""banksys_sy_cuibowen — 银行营销数据分析与认购预测系统.

Streamlit 主入口。提供首页概览与多页导航。
"""

import streamlit as st

st.set_page_config(
    page_title="银行营销分析系统",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏦 银行营销数据分析与认购预测系统")

st.markdown("---")

# ── 概览卡片 ──
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="📊 数据规模", value="41,188 条", help="训练集样本数")
with col2:
    st.metric(label="🎯 特征维度", value="21 个", help="客户特征字段")
with col3:
    st.metric(label="📈 认购率", value="11.7%", help="历史认购比例")

st.markdown("---")

# ── 功能介绍 ──
st.subheader("🔍 系统功能")
tab1, tab2 = st.tabs(["📊 数据分析", "🤖 在线预测"])

with tab1:
    st.markdown("""
    ### 数据分析交互页面
    通过可视化图表探索银行营销数据，快速理解客户特征分布与营销效果。

    **主要功能：**
    - 数据概览：总记录数、认购率、特征统计
    - 客户画像：年龄分布、职业分布、婚姻状况、教育水平
    - 营销分析：联系方式效果、月份/星期趋势
    - 经济指标：就业变化率、消费者价格指数、消费者信心指数等分布
    - 交互筛选：动态切换分析维度，图表实时更新

    👉 请通过左侧导航栏进入 **"数据分析"** 页面。
    """)

with tab2:
    st.markdown("""
    ### 在线预测系统
    基于历史数据训练的机器学习模型，通过点选式表单输入客户特征，实时预测认购意愿。

    **主要功能：**
    - 点选式表单：16 个特征通过下拉框/滑块/数值输入完成
    - 实时预测：点击按钮后立即返回预测结果
    - 结果展示：认购标签、概率进度条、置信度、建议文案
    - 重置功能：一键清空表单重新输入

    👉 请通过左侧导航栏进入 **"在线预测"** 页面。
    """)

st.markdown("---")
st.caption(
    "技术栈: Python 3.11 · Streamlit · scikit-learn · pandas · Docker  |  "
    "仓库: github.com/thiyfrxd-cyber/banksys_sy_cuibowen"
)
