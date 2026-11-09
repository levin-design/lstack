# lstack

[pstack](https://github.com/cursor/plugins/tree/main/pstack) 的简体中文翻译与 GitHub Copilot 移植版。

pstack 是 Lauren Tan（poteto）的严谨工程工作流：把任务匹配到剧本，交给全新的子代理执行，应用工程原则，并在宣布完成前对真实产物进行验证。本仓库不是官方仓库，只做本地化与编辑器适配。

## 仓库结构

```text
.
├── pstack/                       # 上游插件源码（Cursor 插件形态）
│   ├── skills/                   # 58 个内置技能
│   ├── docs/                     # 指南与 Claude Code 适配文档（已译）
│   ├── automations/benny/        # Slack issue 自动化包（已译）
│   └── agents/                   # poteto-agent、comment-sicko
└── .github/                      # VS Code Copilot 形态
    ├── skills/pstack/            # 项目技能：唯一入口 /pstack
    │   ├── SKILL.md
    │   └── references/
    │       ├── skills/           # 58 个内置技能（references/skills/<name>/<name>.md）
    │       └── agents/
    └── agents/                   # Copilot 自定义代理
        ├── poteto-agent.agent.md
        └── comment-sicko.agent.md
```

## 在 VS Code Copilot 中使用

把 `.github/` 放进目标仓库根目录，然后在 Copilot Chat 中运行：

```text
/pstack <任务、问题或 setup>
```

- `/pstack` 是唯一注册的斜杠命令。内置技能里的 `/how`、`/tdd` 等是简写，由入口技能按需读取 `references/` 下的文件执行，不会出现在斜杠菜单里。
- 首次使用可运行 `/pstack setup` 生成模型配置；该文件是可选的，缺省时子代理继承父会话模型。
- 两个自定义代理（`poteto-agent`、`comment-sicko`）随 `.github/agents/` 提供。

## 在 Cursor 中使用上游插件

原版安装方式：

```bash
/add-plugin pstack
```

Claude Code 的安装与字段映射见 [`pstack/docs/harness/claude-code.md`](./pstack/docs/harness/claude-code.md)。

## 翻译说明

- `pstack/docs/**` 与 `pstack/automations/**` 已完整译为简体中文；`.github/skills/pstack/**` 同步翻译。
- 技能名、剧本名、原则名、命令、代码块、路径与配置字段保持英文，以免破坏契约与调用方式。
- 代码围栏、链接目标与 `[benny:*]` 等标记保持原样；`docs` 小节标题已译并同步改写跨页锚点。

## 上游与许可

基于 pstack v0.15.36，MIT 许可证。

- 上游：<https://github.com/cursor/plugins/tree/main/pstack>
- 作者：Lauren Tan
- 许可证：见 [`pstack/LICENSE`](./pstack/LICENSE)（Copyright (c) 2026 Lauren Tan）

本仓库的翻译与 Copilot 适配同样以 MIT 许可证发布；上游版权归原作者所有。
