---
name: setup-benny
description: 配置 Benny 并准备其 triage 和 repro 自动化。在安装 Benny 或更改其 Slack、tracker、仓库、routing、control、model 或预算设置时使用。
disable-model-invocation: true
---

# 设置 Benny

Benny 作为 pstack 内的休眠自动化包发布。插件清单只暴露 pstack 的常规 skill 根目录；本文件和两个操作文件都不是 slash skill。

人类通过让 Cursor 指向包内的 `FOR_AGENTS.md` 来进入 setup。引导流程把整个包复制进目标仓库，然后直接在 `.cursor/automations/benny/skills/setup-benny/SKILL.md` 读取本文件。

Benny 需要外部配置和两个线上 Cursor automation。

在用户明确要求之前，不要创建或更新任何 automation。绝不要把密钥值放入插件文件、prompt 或已提交的配置中。

## 1. 复制包并启用共享 pstack 技能

在询问 Benny 配置之前、在调用内置 `/automate` skill 之前完成此步骤。

询问哪个仓库将运行这些 automation。源包是包含 `FOR_AGENTS.md` 的目录。目标是 `<target-repository>/.cursor/automations/benny/`。

把整个源包合并到目标：

1. 目标不存在时创建它。
2. 把每个源文件复制到相同的相对路径。
3. 保留目标端独有的文件。安装或刷新期间绝不删除无关文件。
4. 把用户自有的配置、feature map 和 routing map 放在目标目录之外。绝不覆盖它们。
5. 当源管理的文件已存在且内容不同时，检查 diff 并在不丢弃本地修改的前提下合并。如果归属不明确，停下来并询问，然后再替换。
6. 验证目标包含 `FOR_AGENTS.md`、本 setup 文件、两个操作文件、它们的 references 以及 templates。

如果本文件已经从目标位置被读取，视为复制已完成，并在继续之前运行同样的验证。

把 pstack 添加到目标仓库的 `.cursor/settings.json`。如果文件或 `.cursor` 目录不存在，则创建它。

把这条记录合并到现有 JSON 或 JSONC：

```json
{
	"plugins": {
		"pstack": { "enabled": true }
	}
}
```

保留所有无关的顶层设置和每一个其他插件条目。如果 `plugins.pstack` 已存在，只更改其 `enabled` 值。当文件使用 JSONC 时，保留注释和有效的 JSONC 语法。编辑后验证文件。

重新加载目标项目，或以它为根启动一个全新 agent。验证以下共享 pstack 技能能从项目作用域解析：

- `how`
- `why`
- `tdd`
- `unslop`
- `principle-separate-before-serializing-shared-state`
- `principle-minimize-reader-load`
- `principle-guard-the-context-window`
- `principle-sequence-verifiable-units`
- `principle-fix-root-causes`
- `principle-prove-it-works`

不要计入从当前会话或用户作用域插件加载的技能。该检查必须表明目标仓库中的全新 agent 通过项目设置获得了 pstack。

如果项目作用域的插件安装不可用，或任何共享依赖无法解析，停止并解释失败原因。

Benny 的文件直接从 `.cursor/automations/benny/` 读取。不要把该目录加入插件清单，也不要指望其 `SKILL.md` 文件出现在 slash-skill 列表中。

告诉用户，在启用任一自动化之前，必须提交 `.cursor/settings.json`、`.cursor/automations/benny/` 以及任何被引用的不含密钥的配置。除非用户要求，不要提交它们。

一旦此检查通过，线上 automation prompt 可以通过稳定的仓库相对路径读取已提交的操作文件。它们不得嵌入插件缓存路径或复制文件内容。

## 2. 改编配置

打开这些复制过来的示例：

- `../../templates/configuration.example.yaml`
- `../reproduce-and-fix-issues/references/feature-map.example.md`

在 `.cursor/automations/benny/` 之外创建用户自有的副本。这些是配置文件，不是包文件。示例位置：

- 项目配置，例如 `.cursor/benny/configuration.yaml`
- 项目 feature map，例如 `.cursor/benny/feature-map.md`
- 项目 routing map，例如 `.cursor/benny/routing.md`
- 用户配置，例如 `~/.config/benny/configuration.yaml`
- 用户 feature map，例如 `~/.config/benny/feature-map.md`

为自动化可能复现的每一个面向用户的功能填写一个 feature-map 小节。保持用户视角。不要在地图中固化实现细节或当前代码路径。

不要编辑复制过来的示例。包刷新可能在冲突审查后更新源管理的文件，但绝不能触碰用户自有的副本。

当全新的 automation 检出需要读取时，优先使用目标仓库中已提交的、不含密钥的文件。否则把所需值转述进线上 prompt。只有在内置 `/automate` skill 确认文件已提交到 automation 运行的仓库之后，才引用仓库文件。

对已提交的包和配置文件使用稳定的仓库相对路径。绝不要从线上 automation 引用插件源目录或插件缓存路径。

## 3. 填写必需的选项

询问或确认：

- Source Slack channel ID
- 可选的 operations 或状态 channel ID
- 仓库 URL 和默认分支
- Triage 身份或 Slack user ID
- Issue tracker 类型、team、project、labels 和 intake 状态
- Tracker adapter skill 或 MCP 操作
- 可选的 routing map 路径
- 必需的 control skill 名称
- 必需的面向用户 feature-map 路径
- 状态 emoji 字符串
- Pull request URL 格式
- 轮询和工作量预算
- triage、repro、代码工作和媒体审阅使用的 model slug

只使用用户 Cursor model picker 或受支持模型列表中显示为可用的 model slug。不要猜测 slug，也不要沿用私有默认值。

source channel、triage 身份、仓库、tracker adapter、control skill 和 feature map 必须明确。如果任何必需值仍含糊不清，setup 失败。

在保存最终 automation 名称、描述和 prompt shim 之前，让它们经过 pstack 的 `unslop` skill。

## 4. 检查集成能力

triage 自动化需要：

- 对配置的 source Slack channel 及其 thread 的读取权限
- 在该频道中的 thread 回复权限
- 当报告包含媒体时的附件元数据和文件下载权限
- 通过配置的 issue-tracker adapter 进行搜索、读取、创建和更新权限

repro 自动化需要：

- 对 source thread 的读取权限
- source channel 中的 thread 回复权限
- 可选的、在配置的 operations channel 中发帖和编辑的权限
- 仓库读取和历史访问权限
- 能打开草稿 pull request 的 pull request 操作
- 配置的 control-adapter skill

读取和发帖优先使用配置的 Cursor Slack actions。可选的 `BENNY_SLACK_BOT_TOKEN` 可以填补狭窄缺口，例如编辑一条 operations 状态消息或下载附件。把值保存在 secret manager 或环境变量中，而不是 YAML 中。

不要使用未文档化的集成端点。

## 5. 准备 routing map

如果用户需要改派或 owner ping：

1. 把 `../triage-issue-reports/references/routing.example.md` 复制到 `.cursor/automations/benny/` 之外。
2. 用公开值或组织内值替换每一个占位符。
3. 默认保持 owner ping 关闭。
4. 只允许对配置的 feature owner 或已确认的可能回归作者发 ping。

如果没有配置 routing map，triage 可以分类报告，但不得猜测目的地或 owner。

## 6. 验证 control adapter

读取 `../reproduce-and-fix-issues/references/control-adapter.md` 以及用户已完成的 feature map。

确认指定的 skill 能够：

- 启动目标应用
- 通过真实 UI 导航到每个已映射的功能
- 通过声明的 adapter 动作演练已映射的状态
- 检查状态而不强制产生结果
- 采集截图
- 启动和停止录制
- 清理其进程和临时数据

如果任何能力缺失，让 repro 自动化保持禁用。它必须 fail closed，而不是声称一个它并未执行的复现。

## 7. 准备线上自动化

询问这是首次创建，还是配置现有自动化。

从复制后的包中读取 `../../FOR_AGENTS.md`，作为任一流程的主要用户意图来源。用它理解两个触发、工具、指令、结果和共享规则。

### 首次创建

一次创建一个自动化。

对于每个自动化：

1. 读取匹配的复制 prompt 模板，作为次要的内部源材料。
2. 把 `FOR_AGENTS.md`、最终的 Benny 配置和模板意图转化为一条完整的自然语言请求。
3. 告诉线上 prompt 读取并遵循 `.cursor/automations/benny/` 下确切的已提交操作文件。
4. 使用稳定的仓库相对路径，而不是插件源或缓存路径。不要把操作文件内容复制进线上 prompt。
5. 读取并遵循内置的 `automate` skill。
6. 让 `automate` 发现 Slack channel、仓库和已连接的集成。
7. 让 `automate` 确认复制包和任何被引用的配置文件已提交到 automation 将要运行的同一仓库。
8. 让 `automate` 展示草稿表、获取批准、询问就绪状态，并打开 Automations 编辑器。
9. 在开始下一个自动化之前，完成本次的编辑器交接。

把以下完整的 triage 意图交给 `automate`（从配置填写）：

- 名称 `benny-triage`。
- 每次运行都读取并遵循 `.cursor/automations/benny/skills/triage-issue-reports/SKILL.md`。
- 在配置的 source Slack channel 中对每条新的顶层报告触发。
- 读取触发的 thread，并只在其内部回复。
- 使用配置的 issue-tracker 集成。
- 分类、检查证据、追踪原因、去重，并且只为明确的新 bug 创建工单。
- 用配置的 `[benny:bug]`、`[benny:performance]` 或 `[benny:other]` 标记和可选的 tracker URL 结束一条仅限 thread 的结论。
- 绝不发布 source-channel 根消息。

在 triage 编辑器交接完成后，把以下完整的 repro 和 fix 意图交给 `automate`：

- 名称 `benny-reproduce`。
- 每次运行都读取并遵循 `.cursor/automations/benny/skills/reproduce-and-fix-issues/SKILL.md`。
- 在配置的 source Slack channel 中对同一批新顶层报告触发。
- 使用配置的仓库和默认分支。
- 读取 source thread，并只在其内部回复。
- 包含 pull request 创建以及配置的 tracker、control-adapter 和 feature-map 要求。除非 `automate` 确认同一仓库中存在符合条件的已提交文件，否则转述映射的用户路径和状态。
- 行动前等待可信的 triage 标记。
- 通过已映射的真实 UI 两次复现完全相同的症状，并采集证据。
- 验证现有修复，而不在其之上另写实现。
- 只有在确认复现后才尝试可选的有边界修复，然后在证明和检查通过时打开草稿 pull request。
- 绝不发布 source-channel 根消息。

不要重复 `automate` 的 Slack、仓库、集成、完整性、认证、草稿审阅、批准、就绪或编辑器交接工作。

### 现有自动化

内置的 `automate` skill 仅用于创建。不要用它搜索、检查或更新现有自动化。

完成配置、routing、control-adapter 和 feature-map 的验证。然后给用户这份简明的编辑器检查清单。

对于现有的 triage 自动化，更新：

- 名称和描述
- 直接要求读取 `.cursor/automations/benny/skills/triage-issue-reports/SKILL.md` 的指令
- 新顶层 Slack 报告触发和 source channel
- Slack thread 读取与回复能力
- Issue-tracker 集成
- 转述的 triage 指令、仅限 thread 规则和 Benny 结论标记

对于现有的 repro 自动化，更新：

- 名称和描述
- 直接要求读取 `.cursor/automations/benny/skills/reproduce-and-fix-issues/SKILL.md` 的指令
- 匹配的 Slack 触发和 source channel
- 仓库和默认分支
- Slack thread 读取与回复能力
- Pull request 操作
- Tracker、control-adapter 和 feature-map 要求
- 转述的标记等待、证据、验证和有边界修复指令

请用户直接在各自的 Automations 编辑器中更新每个现有自动化。不要创建替代项或重复项。

### 创建边界

绝不要调用直接的自动化后端服务或后端自动化工具。绝不使用携带草稿字段的浏览器 URL。绝不构建或打开 Cursor 协议深链接。对于新自动化，唯一的完成路径是内置 `automate` skill 的、经过审阅的 Automations 编辑器交接。

在编辑器保存后线程安全测试通过之前，不要启用任一自动化。

## 8. 测试线程安全

使用一个测试频道或一条无害的测试报告。

在测试之前，确认目标仓库的 `.cursor/settings.json`、`.cursor/automations/benny/` 以及每个被引用的不含密钥的配置文件都已提交到 automation 检出所使用的分支。确认两个线上 prompt 都指向其确切的已提交操作文件。如果任何检查失败，停止。告诉用户该自动化尚不能启用。

验证：

1. Triage 存储根 `thread_ts`，并恰好发布一条结论作为回复。
2. 结论包含一个配置的标记。
3. Repro 只接受来自配置的 triage 身份的标记。
4. Repro 保持相同的不可变 source 坐标。
5. 不出现 source-channel 根消息。
6. 被委派的 worker 无法使用任何 Slack 写操作。
7. 坐标缺失、parent 被删除或 preflight 失败时不产生任何帖子，也不创建 tracker issue。

只有在全部七项检查通过之后，才启用正常流量。
