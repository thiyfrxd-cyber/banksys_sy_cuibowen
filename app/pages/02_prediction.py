"""Online Prediction page — point-and-click form for subscribe prediction."""

import streamlit as st

from app.models.predictor import get_feature_schema, predict

st.set_page_config(page_title="在线预测", page_icon="🤖", layout="wide")

st.title("🤖 在线预测系统")


# ── Load feature schema ──
@st.cache_data
def _load_schema():
    return get_feature_schema()


schema = _load_schema()

st.markdown("请填写客户特征信息，点击预测按钮获取认购意愿结果。")

# ── Form ──
with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)

    features = {}
    cat_cols = list(schema.keys())[:10]  # First 10 = categorical
    num_cols = list(schema.keys())[10:]  # Remaining 10 = numerical

    # Categorical features (first 10 in column 1-2)
    for i, col in enumerate(cat_cols):
        target_col = col1 if i < 5 else col2
        info = schema[col]
        features[col] = target_col.selectbox(
            col.replace("_", " ").title(),
            options=info["options"],
            index=0,
        )

    # Numerical features (10 in column 2-3)
    for i, col in enumerate(num_cols):
        target_col = col2 if i < 5 else col3
        info = schema[col]
        features[col] = target_col.number_input(
            col.replace("_", " ").title(),
            value=float(info["default"]),
            format="%.2f",
        )

    submitted = st.form_submit_button("🔮 预测", type="primary", use_container_width=True)

# ── Result ──
if submitted:
    try:
        result = predict(features)

        st.markdown("---")
        st.header("预测结果")

        res_col1, res_col2, res_col3 = st.columns(3)

        with res_col1:
            label = "✅ 会认购" if result["subscribe"] else "❌ 不会认购"
            st.metric("预测标签", label)

        with res_col2:
            pct = result["probability"] * 100
            st.metric("认购概率", f"{pct:.1f}%")

        with res_col3:
            conf_map = {"high": "🟢 高", "medium": "🟡 中", "low": "🔴 低"}
            st.metric("置信度", conf_map[result["confidence"]])

        # Probability bar
        st.progress(result["probability"])

        # Suggestion text
        if result["subscribe"]:
            st.success("建议：该客户有较高的认购意愿，可优先跟进营销。")
        else:
            st.info("建议：该客户认购意愿较低，可考虑观望或培养后再跟进。")

    except FileNotFoundError:
        st.error("⚠️ 模型尚未训练，请联系管理员。")
        st.info("管理员请运行：`python -m app.ml.train --overwrite`")

# ── Sidebar ──
st.sidebar.markdown("### 使用说明")
st.sidebar.markdown("""
1. 在表单中选择/输入客户特征
2. 点击"预测"按钮
3. 查看预测结果和概率
""")
st.sidebar.caption("模型: RandomForest · AUC 0.89")
