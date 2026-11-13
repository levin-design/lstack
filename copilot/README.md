# lstack（Copilot 版）

poteto 的严谨工程工作流：把任务匹配到剧本，交给全新的子代理执行，应用工程原则，并在宣布完成前对真实产物进行验证。

本目录是 pstack 的 Copilot 适配包。每个技能都是 Copilot 原生的 `SKILL.md`；工具调用、模型策略、会话路径与安装说明都按 GitHub Copilot（VS Code）重写，不依赖上游宿主产品的专有机制。

## 安装

把内容复制到项目根目录：

```bash
cp -R skills/. <project>/.github/skills/
cp agents/*.agent.md <project>/.github/agents/
```

装好后：

- `/lstack <任务>` 进入 poteto 模式，这是完整工作流的入口。
- 每个内置技能也已独立注册，可以直接用 `/技能名` 调用。
- 角色模型与推理预算写在 `<project>/.github/skills/lstack/references/lstack-models.md`；包内提供全 `inherit-parent` 的默认配置，可运行 `/setup-lstack` 覆盖。
- 需要按名派生子代理时，`poteto-agent` 与 `comment-sicko` 已在 `.github/agents/`。
- `agents/` 还提供一组不绑定具体项目的数字员工，见 [agents/README.md](agents/README.md)。

完整用法、并行机制、模型配置与常见问题见 [docs/实用指南.md](docs/实用指南.md)。

## 结构

```
skills/lstack/SKILL.md                        入口技能与技能地图
skills/lstack/references/lstack-models.md     角色模型配置（可选）
skills/<name>/SKILL.md                        58 个内置技能，各自独立注册
skills/<name>/references/...                  技能自带的参考资料
skills/<name>/playbooks/...                   剧本
skills/<name>/scripts/...                     可执行脚本与测试
agents/poteto-agent.agent.md                  委派执行子任务的子代理
agents/comment-sicko.agent.md                删注释评审子代理
agents/tech-lead.agent.md                     数字员工队长（总编排）
agents/architect.agent.md                     数字员工：架构师
agents/engineer.agent.md                      数字员工：工程师
agents/ci-engineer.agent.md                   数字员工：CI/CD 工程师
agents/reviewer.agent.md                      数字员工：审查员
agents/verifier.agent.md                      数字员工：验证员
agents/writer.agent.md                        数字员工：技术写作者
agents/README.md                              数字员工名册
docs/实用指南.md                              使用指南
```

## 与上游的关系

- 上游：Lauren Tan 的 pstack v0.15.36（MIT 许可证，见 `LICENSE`），https://github.com/cursor/plugins/tree/main/pstack
- 本包把产品名改为 lstack，并把上游对 Cursor 的依赖替换为 Copilot 的等价物：`runSubagent`、`vscode_askQuestions`、自定义代理、`VSCODE_TARGET_SESSION_LOG` 会话日志、GitHub Copilot 评审线程识别。
- 上游的 `skills/<name>/SKILL.md` 在本包中展开为 `skills/<name>/SKILL.md`，因此每个技能都能被 Copilot 发现并单独调用；技能之间的链接全部改指同级 `SKILL.md`。
- 上游的 `docs/` 与 `automations/` 没有包含在内，它们属于 Cursor 发行形态；本包的 `docs/` 只有这份实用指南。

## 已知限制

- `runSubagent` 同步且无状态：没有后台运行、恢复或中途干预。
- 没有 `/loop`、自定义模式、定时自动化或云 VM；重复执行靠用户重新发送 `/lstack`。
- `arena cross-judge pool` 需要至少一个已确认的真实模型标签，`inherit-parent` 不参与跨模型评判。
