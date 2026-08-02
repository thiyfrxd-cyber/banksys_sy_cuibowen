# PROGRESS · banksys_sy_cuibowen 〔本项目活记忆 · 状态机〕

> **作用**：这是项目的"存档点"。任意 AI、任意重启会话，读它即可知道当前做到哪、下一步做什么、踩过什么坑。
> **更新时机**：每完成一个有意义步骤、每次会话结束前。
> **格式要求**：时间倒序，最新在上；短、准、可接力。

---

## 当前状态 (最后更新: 2026-08-02 · by AI)

- **阶段**: `第⑤步 — PR #1 已创建，CI 运行中，等待 CI 全绿后人工 Review`
- **仓库**: https://github.com/thiyfrxd-cyber/banksys_sy_cuibowen（PUBLIC，Secrets 已配置）
- **开发策略**: 按六步交付流程逐模块推进，先 US-1 建仓通 CI/CD，再依次实现 US-2~US-8
- **上一步完成**: 
  - ①~② 建仓 + 配置 Secrets + 开 feature 分支 ✅
  - ③ 本地模块化开发（15 个文件，6 个模块）✅
  - ④ 本地 CI 自检（ruff format ✅ / ruff check ✅ / pytest 10/10 passed ✅）
  - ⑤ PR #1 已创建 ✅
- **下一步**: 等待 CI 全绿 → 人工 Review → 人工 Merge → CD 自动部署 → 验证端口 8888
- **阻塞项**: CI 运行中

---

## 待办清单 (TODO，按优先级)

### 第一批：初始化项目工程化与 CI/CD（US-1）
- [x] ① 建仓 `banksys_sy_cuibowen`（PUBLIC 开源仓库）+ 配 GitHub Secrets（SSH_PRIVATE_KEY / SSH_HOST / SSH_USER）
- [x] ② 开 feature 分支 `feature/1-init-project`
- [x] ③ 本地模块化开发（15 个文件）：
  - [x] 包初始化（app/__init__.py, app/utils/, app/pages/, app/models/, app/ml/）
  - [x] requirements.txt + requirements-dev.txt
  - [x] pyproject.toml（ruff + pytest + coverage 配置）
  - [x] .gitignore（含 app/ml/model/）
  - [x] app/main.py（Streamlit 首页导航）
  - [x] Dockerfile（python:3.11-slim，构建时训练模型，Python HEALTHCHECK）
  - [x] .github/workflows/ci.yml（ruff + pytest + docker build）
  - [x] .github/workflows/cd.yml（SSH 部署 + 端口 8888 + 健康检查）
  - [x] tests/test_health.py（10 个测试）+ conftest.py
- [x] ④ 本地 CI 自检全绿（ruff format ✅ / ruff check ✅ / pytest 10/10 passed）
- [x] ⑤ PR #1 已创建
- [ ] ⑥ CI 全绿 → 人工 Review → 人工 Merge → CD 部署 → 验证端口 8888

### 第二批：数据加载与预处理模块（US-2）
- [ ] 实现 `app/models/data_loader.py`
- [ ] 编写 `tests/test_data_loader.py`（≥80% 覆盖）
- [ ] 提 PR + CI + Review + 合并 + CD

### 第三批：数据分析交互页面（US-3）⭐ 核心功能
- [ ] 实现 `app/models/visualizer.py`（可视化逻辑与 UI 分离）
- [ ] 实现 `app/pages/01_data_analysis.py`
- [ ] 编写 `tests/test_visualizer.py`
- [ ] 提 PR + CI + Review + 合并 + CD

### 第四批：模型训练脚本（US-4）
- [ ] 实现 `app/ml/train.py`（Pipeline + 固定种子 + CLI 参数）
- [ ] 编写 `tests/test_train.py`
- [ ] 提 PR + CI + Review + 合并 + CD

### 第五批：预测服务核心逻辑（US-5）
- [ ] 实现 `app/models/predictor.py`
- [ ] 编写 `tests/test_predictor.py`（≥80% 覆盖）
- [ ] 提 PR + CI + Review + 合并 + CD

### 第六批：在线预测页面（US-6）⭐ 核心功能
- [ ] 实现 `app/pages/02_prediction.py`（点选式表单 + 结果展示）
- [ ] 与 predictor 模块集成验证
- [ ] 提 PR + CI + Review + 合并 + CD

### 第七批：健康检查 + 质量门禁完善（US-7 & US-8）
- [ ] 确认 `/_stcore/health` 可用
- [ ] 确认核心逻辑覆盖率 ≥80%
- [ ] 端到端验证：数据分析页面 + 预测页面 + 健康检查

---

## 关键决策记录 (ADR)

| 日期 | 决策 | 理由 |
|---|---|---|
| 2026-08-02 | 选择 Streamlit 作为 Web 框架 | 课程要求；快速构建数据应用；内置多页导航与健康检查 |
| 2026-08-02 | 模型训练离线，预测在线 | 训练是重操作不适合实时请求；预测是轻操作需快速响应 |
| 2026-08-02 | 数据集进 Git，模型产物不进 Git | 教学用公开数据方便复现；模型二进制大文件不应进版本控制 |
| 2026-08-02 | Docker 构建时训练模型（非运行时） | 镜像自包含，无需运行时再训练；避免容器启动慢 |
| 2026-08-02 | 端口选择 8888 | 课程指定端口；Streamlit 容器内 8501，Docker 映射到主机 8888 |
| 2026-08-02 | 仓库名与容器名均为 `banksys_sy_cuibowen` | 与数据源项目命名一致，便于识别 |

---

## 已知坑 (GOTCHAS)

> 暂无。开发过程中遇到的实际故障将记录于此，包含现象、根因、解决方案、验证结果。

---

## 里程碑 (DONE)

- [x] 2026-08-02：填写项目规范文档（00-project-context / 01-requirements / PROGRESS）

> 反臃肿：里程碑超过 15 条时，把更早内容合并成一行摘要，保持本文件可快速阅读。
