# 数字员工

通用角色团队，不绑定任何具体项目。项目差异通过任务书和项目根目录的 `AGENT.md`、`README.md`、设计文档传入。

| 文件 | 岗位 | 工具边界 | 何时使用 |
|---|---|---|---|
| `tech-lead.agent.md` | 技术负责人（队长） | 全部 + `agent` | 跨角色任务的总编排 |
| `architect.agent.md` | 架构师 | 只读 | 接口、模块边界、契约与权衡 |
| `frontend-engineer.agent.md` | 前端工程师 | 读写 + 执行 | UI、组件、无障碍与浏览器行为 |
| `backend-engineer.agent.md` | 后端工程师 | 读写 + 执行 | API、服务、数据与服务端安全 |
| `engineer.agent.md` | 通用工程师 | 读写 + 执行 | 跨层或小型实现；无明确归属时兜底 |
| `ci-engineer.agent.md` | 工程与运维工程师（CI/CD） | 读写 + 执行 | 流水线、缓存、产物与发布自动化 |
| `reviewer.agent.md` | 审查员 | 只读 | 合并前找会出错的地方 |
| `verifier.agent.md` | 验证员 | 只读 + 执行 | 独立运行构建/测试/验收 |
| `writer.agent.md` | 技术写作者 | 读写文档 | README、设计文档、PR 描述 |

## 使用方式

1. 安装到项目的 `.github/agents/`。
2. 在 agent 选择器里选 `tech-lead`，用一段话说明目标、范围和完成标准。
3. 需要单独用某个岗位时，把对应文件的 `user-invocable` 改成 `true`。

## 与其他 agent 的关系

- `poteto-agent` 和 `comment-sicko` 是 lstack 自带的专用角色，分别服务于 `/lstack` 流程和删注释评审。
- 数字员工是通用岗位，可以被任何流程调用，也可以组合成自己的团队。

## 定制原则

- 项目专属信息不要写进 agent 文件，写进项目文档或任务书。
- 需要固定项目角色时，复制其中一个文件，改 `name`、`description`、岗位边界和引用文档。
- 角色之间只通过任务书和落盘产物协作，不依赖共享上下文。
