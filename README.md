# lstack

[pstack](https://github.com/cursor/plugins/tree/main/pstack) 的简体中文翻译与多编辑器适配版，当前提供 GitHub Copilot 与 Claude Code 两个适配包。

pstack 是 Lauren Tan（poteto）的严谨工程工作流：把任务匹配到剧本，交给全新的子代理执行，应用工程原则，并在宣布完成前对真实产物进行验证。本仓库不是官方仓库，只做本地化与编辑器适配。

## 仓库结构

```text
.
├── pstack/                       # 上游 pstack v0.15.36（Cursor 插件形态）
│   ├── skills/                   # 58 个内置技能（英文）
│   ├── docs/                     # 指南、harness 文档（已译）
│   ├── automations/benny/        # Slack issue 自动化包（已译）
│   └── agents/                   # poteto-agent、comment-sicko
├── copilot/                      # GitHub Copilot（VS Code）适配包（中文）
│   ├── skills/                   # lstack 入口 + 58 个内置技能（setup-lstack 替代 setup-pstack）
│   ├── agents/                   # 2 个专用角色 + 7 个通用数字员工
│   └── docs/实用指南.md
└── claude_code/                  # Claude Code 适配包（英文）
    ├── skills/                   # 58 个上游技能（仅重写 setup-pstack）
    ├── agents/                   # 2 个专用角色 + 7 个通用数字员工
    └── docs/                     # 适配映射、实用指南、模型规则示例
```

## 在 GitHub Copilot 中使用

把 `copilot/` 的内容复制到目标仓库：

```bash
cp -R copilot/skills/. <project>/.github/skills/
cp copilot/agents/*.agent.md <project>/.github/agents/
```

然后在 Copilot Chat 中运行：

```text
/lstack <任务、问题或 setup>
```

- `/lstack` 是入口命令；内置技能也各自注册，可以直接用 `/技能名` 调用。
- 首次使用可运行 `/setup-lstack` 生成模型配置；缺省时子代理继承父会话模型。
- 2 个专用角色（`poteto-agent`、`comment-sicko`）与 7 个通用数字员工（`tech-lead` 等）随包提供，见 [`copilot/agents/README.md`](./copilot/agents/README.md)。
- 完整用法、并行机制与常见问题见 [`copilot/docs/实用指南.md`](./copilot/docs/实用指南.md)。

## 在 Claude Code 中使用

把 `claude_code/` 的内容复制到目标仓库或用户目录：

```bash
cp -R claude_code/skills/. <project>/.claude/skills/
find claude_code/agents -maxdepth 1 -name '*.md' ! -name README.md \
  -exec cp {} <project>/.claude/agents/ \;
```

会话开始时读一次 [`claude_code/docs/claude-code-adapter.md`](./claude_code/docs/claude-code-adapter.md)，按表映射 Cursor 字段。要点：

- 技能以 `/pstack:<skill>`（插件安装）或 `/<skill>`（直接安装）调用；无法解析时直接读 `.claude/skills/<skill>/SKILL.md`。
- 模型配置写入 `~/.claude/rules/pstack-models.md`，示例见 [`claude_code/docs/pstack-models.example.md`](./claude_code/docs/pstack-models.example.md)。
- 包结构与安装细节见 [`claude_code/README.md`](./claude_code/README.md)；Copilot 包的对应说明见 [`copilot/README.md`](./copilot/README.md)。
- 上游 Cursor 到 Claude Code 的字段映射（中文版）另见 [`pstack/docs/harness/claude-code.md`](./pstack/docs/harness/claude-code.md)。

## 在 Cursor 中使用上游插件

原版安装方式：

```bash
/add-plugin pstack
```

## 翻译与适配说明

- `pstack/docs/**` 与 `pstack/automations/**` 已完整译为简体中文。
- `copilot/skills/**` 与 `copilot/agents/**` 为中文适配；`claude_code/` 保持英文，与上游技能一致。
- 技能名、剧本名、原则名、命令、代码块、路径与配置字段保持英文，以免破坏契约与调用方式。
- 代码围栏、链接目标与 `[benny:*]` 等标记保持原样；`docs` 小节标题已译并同步改写跨页锚点。
- 各适配包对上游技能的有意改动，均在对应包的 README 中列出。

## 上游与许可

基于 pstack v0.15.36，MIT 许可证。

- 上游：<https://github.com/cursor/plugins/tree/main/pstack>
- 作者：Lauren Tan
- 许可证：见 [`pstack/LICENSE`](./pstack/LICENSE)（Copyright (c) 2026 Lauren Tan）

本仓库的翻译与适配同样以 MIT 许可证发布；上游版权归原作者所有。
