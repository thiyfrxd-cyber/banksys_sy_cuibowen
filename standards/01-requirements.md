# 01 · 需求 / 活 PRD 〔本项目活记忆 · AI 维护〕

> **作用**：这是本项目唯一的需求文档。所有新功能、缺陷、技术债都追加到这里，不要另起多个 PRD 文件。
> **更新时机**：每次有新需求、需求变更、验收标准变化时更新。

---

## 1. 需求来源

| 类型 | 来源 | 进入方式 |
|---|---|---|
| 功能需求 Feature | 课程作业要求 | 写成用户故事 |
| 缺陷 Bug | 测试 / 线上日志 / 用户反馈 | 写复现步骤和期望结果 |
| 技术债 Tech Debt | 开发 / Review / CI/CD 故障 | 写影响和修复目标 |

---

## 2. Issue 生命周期

| 阶段 | 状态 | 动作 |
|---|---|---|
| 提出 | Open | 写清场景、目标、验收标准 |
| 排期 | Backlog / Todo | 决定优先级和负责人 |
| 开发 | In Progress | 从 main 开 feature 分支 |
| 评审 | In Review | 提 PR，等待 CI 和 Review |
| 合并 | Done | PR 合并 main，自动关闭 Issue |
| 验收 | Verified | 按验收标准确认 |

**追踪规则**：分支名带 Issue 号，PR 描述写 `closes #<编号>`。

---

## 3. 用户故事模板

```text
### US-<编号> <一句话标题> · 状态: Backlog
作为 <角色>，
我想要 <能力>，
以便 <价值>。

验收标准：
- AC1: Given <前提>，When <动作>，Then <可验证结果>。
- AC2: <补充标准>

技术备注：
- <可选：约束、边界、风险>
```

---

## 4. 需求清单

### US-1 初始化项目工程化与 CI/CD · 状态: Backlog

作为 **项目开发者**，
我想要 项目具备基础工程结构、测试、CI 与 CD，
以便 后续每次开发都能自动检查并自动部署。

验收标准：
- AC1: 从 `main` 开 feature 分支完成初始化，不直接 push main。
- AC2: PR 触发 CI，至少包含格式检查（ruff）、静态检查（ruff）、单元测试（pytest）、构建检查（docker build）。
- AC3: CI 全绿后合并 main。
- AC4: 合并 main 自动触发 CD，部署后健康检查通过（端口 8888）。
- AC5: 完成后更新 `standards/PROGRESS.md`。

技术备注：
- 首个 US 必须完整演示六步交付流程。
- 建仓后必须提示配置 GitHub Secrets（SSH_PRIVATE_KEY / SSH_HOST / SSH_USER）。

---

### US-2 数据加载与预处理模块 · 状态: Backlog

作为 **开发者**，
我想要 一个可复用的数据加载模块，
以便 支持数据分析页面和模型训练的数据需求。

验收标准：
- AC1: Given 数据文件存在，When 调用 `load_train_data()` 和 `load_test_data()`，Then 返回 pandas DataFrame。
- AC2: Given 原始数据，When 加载数据，Then 列包含 22 列（id / age / job / marital / education / default / housing / loan / contact / month / day_of_week / duration / campaign / pdays / previous / poutcome / emp_var_rate / cons_price_index / cons_conf_index / lending_rate3m / nr_employed / subscribe）。
- AC3: Given 数据加载，When 访问数据，Then 能正确处理缺失值（标记为 unknown / nonexistent 等）。
- AC4: Given 数据加载模块，When 编写单元测试，Then 覆盖正常加载、文件不存在、空文件场景。
- AC5: Given 数据目录，When 部署，Then `data/` 目录在镜像内正确可用。

技术备注：
- 数据文件是 UTF-8 编码的 CSV。
- `train.csv` 含 subscribe 标签用于训练，`test.csv` 无标签用于预测。

---

### US-3 数据分析交互页面 · 状态: Backlog

作为 **业务分析师**，
我想要 通过可视化界面探索银行营销数据，
以便 快速理解客户特征分布和营销效果。

验收标准：
- AC1: Given 访问"数据分析"页面，When 页面加载，Then 显示数据概览（总记录数、认购率、特征数量）。
- AC2: Given 数据分析页面，When 选择分析维度，Then 展示对应图表：
  - 年龄分布（直方图/饼图）
  - 职业分布与认购率（柱状图）
  - 婚姻状况分布（饼图）
  - 教育水平分布（柱状图）
  - 联系方式分布
  - 认购率按月份/星期分析
  - 经济指标（emp_var_rate / cons_price_index / cons_conf_index / lending_rate3m / nr_employed）分布
- AC3: Given 数据分析页面，When 进行交互操作（筛选、维度切换），Then 图表实时更新。
- AC4: Given 页面存在，When 在 Docker 容器中访问，Then 页面正常渲染，Streamlit 组件可用。
- AC5: Given 页面功能，When 编写测试，Then 核心可视化逻辑（visualizer.py）有单元测试覆盖，覆盖率 ≥80%。

技术备注：
- 使用 Streamlit 的 `st.metric` / `st.pyplot` / `st.plotly_chart` / `st.selectbox` 等组件。
- 可视化逻辑与 UI 分离：`app/models/visualizer.py` 负责生成 matplotlib/plotly 图表对象，页面只负责渲染。

---

### US-4 模型训练脚本与流程 · 状态: Backlog

作为 **开发者**，
我想要 一个离线训练脚本，
以便 从历史数据中学习认购预测模型，供在线预测服务使用。

验收标准：
- AC1: Given 训练数据（`data/train.csv`），When 执行 `python -m app.ml.train`，Then 在 `app/ml/model/` 目录输出模型文件（`model.pkl`）和编码器。
- AC2: Given 训练过程，When 训练完成，Then 打印关键指标到日志：AUC（≥0.75）、准确率、精确率、召回率、F1、分类报告。
- AC3: Given 模型文件已存在，When 再次执行训练，Then 支持 `--overwrite` 覆盖或默认跳过（命令行参数）。
- AC4: Given 训练脚本，When 在 CI / Docker 构建环境运行，Then 训练可复现（固定 `random_state`）。
- AC5: Given 模型产物，When 提交代码，Then `app/ml/model/` 在 `.gitignore` 中，不进 Git。

技术备注：
- 使用 scikit-learn Pipeline（ColumnTransformer + OneHotEncoder + 分类器）。
- 分类器可选 RandomForestClassifier / LogisticRegression / XGBoost。
- 固定 `random_state=42` 保证可复现。
- 训练脚本同时保存编码器（或 Pipeline 自带），确保预测时特征处理一致。

---

### US-5 预测服务核心逻辑 · 状态: Backlog

作为 **系统**，
我想要 一个预测服务模块，
以便 根据用户输入的特征返回认购预测结果。

验收标准：
- AC1: Given 模型文件存在，When 调用 `predict(features_dict)`，Then 返回预测结果字典，包含 `subscribe`（bool）、`probability`（float）、`confidence`（str: high / medium / low）。
- AC2: Given 特征输入，When 输入合法特征值，Then 正确编码并调用模型，返回有效预测。
- AC3: Given 特征输入，When 输入缺失或非法值，Then 返回友好错误提示或使用合理默认值处理。
- AC4: Given 预测模块，When 编写测试，Then 覆盖：正常预测、模型文件缺失、缺失特征、非法数值、未知类别、响应时间。
- AC5: Given 预测服务，When 响应请求，Then 单次预测响应时间 <1s（预热后）。

技术备注：
- 特征编码必须与训练时一致（使用保存的 Pipeline 或 encoder）。
- 返回格式示例：`{"subscribe": true, "probability": 0.82, "confidence": "high"}`。
- 使用 `lru_cache` 缓存模型加载，避免每次预测重新加载。

---

### US-6 在线预测页面 · 状态: Backlog

作为 **营销人员**，
我想要 通过点选式表单输入客户特征，
以便 快速预测该客户是否会认购定期存款，辅助营销决策。

验收标准：
- AC1: Given 访问"在线预测"页面，When 页面加载，Then 显示点选式表单，包含所有必要特征的选择器：
  - 年龄（数值输入/滑块）
  - 职业（下拉选择，选项从训练数据动态取值）
  - 婚姻状况（下拉选择）
  - 教育水平（下拉选择）
  - 信贷违约（是/否）
  - 住房贷款（是/否）
  - 个人贷款（是/否）
  - 联系方式（下拉选择）
  - 月份（下拉选择）
  - 星期几（下拉选择）
  - 通话时长（数值输入）
  - 营销活动次数（数值输入）
  - 上次联系间隔天数（数值输入）
  - 之前联系次数（数值输入）
  - 上次营销结果（下拉选择）
  - 经济指标（5 个数值输入，提供默认值/参考范围）
- AC2: Given 表单填写完成，When 点击"预测"按钮，Then 页面显示预测结果：是否认购（是/否标签）、概率（进度条/仪表盘）、置信度、建议文案。
- AC3: Given 预测结果，When 显示结果，Then 概率用可视化进度条展示，颜色随概率变化（低概率红色 → 高概率绿色）。
- AC4: Given 表单，When 用户操作，Then 支持"重置"按钮清空表单、"重新预测"更新结果。
- AC5: Given 模型文件缺失，When 页面加载，Then 显示友好提示"模型尚未训练，请联系管理员"，而非报错崩溃。
- AC6: Given 预测页面，When 在 Docker 容器中访问，Then 预测功能正常工作。

技术备注：
- 使用 Streamlit 的 `st.selectbox` / `st.slider` / `st.number_input` / `st.button` 组件。
- 类别型字段的选项从训练数据列的唯一值动态生成，不硬编码。
- 结果展示：`st.metric` + `st.progress` + 条件着色。

---

### US-7 健康检查与监控 · 状态: Backlog

作为 **运维/CD 流水线**，
我想要 一个健康检查端点，
以便 验证服务是否正常运行。

验收标准：
- AC1: Given 服务运行，When 访问 `/_stcore/health`，Then 返回 200 状态码。
- AC2: Given 模型加载，When 服务启动，Then 模型文件成功加载，预测功能可用。
- AC3: Given CD 部署脚本，When CD 执行，Then 健康检查失败时 CD 流水线报错退出。

技术备注：
- Streamlit 默认提供 `/_stcore/health` 端点。
- Docker HEALTHCHECK 使用 Python（urllib）访问健康端点，避免额外安装 curl（避免国内服务器 apt 超时）。

---

### US-8 测试覆盖与质量门禁 · 状态: Backlog

作为 **CI 流水线**，
我想要 完整的测试覆盖，
以便 保证代码质量，防止回归。

验收标准：
- AC1: Given 核心业务逻辑（data_loader / visualizer / predictor / train），When 运行 `pytest --cov`，Then 覆盖率 ≥80%。
- AC2: Given CI 触发（PR 提交），When CI 执行，Then 依次跑通：格式检查（ruff format）、静态检查（ruff check）、单元测试（pytest --cov）、Docker 构建（docker build）。
- AC3: Given 任意检查失败，When CI 红灯，Then PR 不能合并。
- AC4: Given 本地开发，When 提交前，Then 开发者（AI）本地执行自检并全绿才推送。

---

## 5. 非功能需求

- **安全**：密钥只进 GitHub Secrets，不进 Git；不硬编码任何凭证。
- **可维护**：一需求一小 PR（<400 行），避免大爆炸式提交。
- **可测试**：核心逻辑必须有单元测试；UI 页面逻辑与渲染分离。
- **可部署**：Dockerfile 构建时完成模型训练，镜像自包含；部署后健康检查验证。
- **性能**：单次预测响应 <1s；页面首屏加载 <3s。
- **端口**：服务端口固定 8888（Docker 主机端口），容器内 Streamlit 默认 8501。
- **仓库命名**：GitHub 仓库名与 Docker 容器名均为 `banksys_sy_lixiaohua`。
