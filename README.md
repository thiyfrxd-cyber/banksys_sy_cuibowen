# banksys_sy_cuibowen

基于银行营销数据的可视化分析与认购预测 Web 应用。

## 功能

- **数据分析交互页面**：可视化探索客户特征分布、营销效果分析
- **在线预测系统**：点选式表单输入客户特征，实时预测认购意愿

## 技术栈

Python 3.11 · Streamlit · scikit-learn · pandas · pytest · ruff · Docker

## 快速启动

```bash
# 安装依赖
pip install -r requirements.txt -r requirements-dev.txt

# 训练模型
python -m app.ml.train

# 启动应用
streamlit run app/main.py --server.port 8501
```

## 端口

- 容器内: 8501 (Streamlit 默认)
- 主机映射: 8888
