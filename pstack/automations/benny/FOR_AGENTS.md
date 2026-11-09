# benny 自动化意图

## 我想自动化什么

我想要两个在同一条 slack issue channel 中协同工作的 cursor automation。

### automation 1：分类 issue report

- 触发：当有人在我配置的 source slack channel 中发布新的顶层报告时，我希望这个 automation 从该报告开始，并保持其原始 thread 坐标。
- 行为：我希望它读取 thread 和附件，把报告分类为 bug 或性能问题、功能请求、问题或反馈，或改派，并在改派之前追踪可能的归属层级。
- tracker：我希望它在配置的 tracker 中搜索重复项，更新有把握的重复项，并且只为明确的全新 bug 创建工单。
- 工具：我希望拥有 slack thread 读取与回复权限、配置的 tracker 集成，以及可选的 routing map。
- 结果：我希望在 source thread 中恰好回复一条，包含简短结论和 `[benny:bug]`、`[benny:performance]` 或 `[benny:other]`。bug 或 performance 标记可以附带 tracker url。
- 边界：我绝不允许这个 automation 在 source channel 中发布根消息。

### automation 2：复现并修复已确认的 bug

- 触发：我希望这个 automation 从同一个新顶层报告开始，或从 setup 期间选择的另一个受支持的触发开始，然后在原始 thread 中等待可信的 triage 标记。
- 门禁：当有人明确负责该修复时，我希望它停止。如果现有 pull request 或已合并 commit 可能修复该报告，我希望进行验证，而不是提交竞争性的改动。
- 行为：我希望它使用我配置的 control adapter 和 feature map，通过真实 ui 两次复现完全相同的症状，并采集截图、视频和只读状态交叉核对。
- 修复：我希望它验证现有 pull request，而不是在其之上另写实现。在确认复现之后，它可以尝试一次有边界的根因修复，在测试成本低时使用 tdd，对 blast radius 做冒烟检查，并且只有在前后对比证明通过时才创建草稿 pull request。
- 工具：我希望拥有 slack thread 读取与回复权限、仓库与历史访问权限、创建草稿 pull request 的能力、配置的 tracker，以及我的 control adapter。
- 结果：我希望在 source thread 或可选的 operations thread 中得到证据和经过验证的结果，外加一个可选的草稿 pull request。更新应当简洁。
- 边界：我绝不允许这个 automation 在 source channel 中发布根消息。

### 共享规则

- 我希望 source channel 和根 thread 坐标在整个运行期间保持不变。
- 我把工具机器人和调试机器人视为证据来源，而非委派对象或修复负责人。
- 我允许子代理协助，但它们不能向 slack 发帖，也不能接收 slack 凭据。
- 我希望整个包提交到目标仓库的 `.cursor/automations/benny/`。其中的 `SKILL.md` 文件是直接的自动化指令，不是注册的插件 skill。
- 我希望只通过目标仓库已提交的 `.cursor/settings.json` 启用 pstack，且仅用于共享依赖，例如 `how`、`why`、`tdd`、`unslop` 以及所需的原则技能。
- 我希望每个线上自动化 prompt 直接读取其已提交的操作文件。我不希望使用插件缓存路径、复制的摘录或 slash-skill 发现机制。
- 我把用户自有的配置、feature map、routing map 和密钥放在 `.cursor/automations/benny/` 之外，这样包刷新不会覆盖它们。
- 当 channel 坐标、tracker 访问、control adapter 或 feature map 缺失或不确定时，我希望两个自动化都 fail closed。
- 我只希望草稿 pull request。不要合并或部署。

### 我的配置

- source slack channel：`<channel>`
- 可选的 operations channel：`<channel or none>`
- 仓库与默认分支：`<repo>`、`<branch>`
- tracker：`<type, team, project, labels, intake status>`
- routing map：`<path or none>`
- triage 身份：`<slack identity>`
- control skill：`<configured skill or adapter>`
- feature map：`<committed same-repo path outside the copied pack, or behavior to paraphrase>`
- models：`<triage, reproduce, code, media review>`
- 状态 emoji 字符串：`<seen, reproducing, reproduced, blocked, fixing, failed, pull request opened>`
- 预算：`<polling, verdict wait, follow-up, repro, rejection, fix>`
- 可选的 bot token 能力：`<none, file download, or editable operations status>`

从 [`configuration.example.yaml`](./templates/configuration.example.yaml) 和 [`feature-map.example.md`](./skills/reproduce-and-fix-issues/references/feature-map.example.md) 开始。把它们复制到本包之外并填写，例如放在 `.cursor/benny/` 下。密钥值保存在 secret manager 或环境变量中。

## 给 agent

人类通过让 cursor 指向本文件来进入 setup。不要寻找或调用已发现的 benny slash skill。

1. 询问哪个仓库将运行这些 automation。
2. 把包含本 `FOR_AGENTS.md` 的目录视为源包。
3. 把整个源包合并到 `<target-repository>/.cursor/automations/benny/`。
4. 保留每个目标端独有的文件。绝不要删除无关文件，也不要覆盖用户自有的配置、feature map 或 routing map。
5. 当源管理的路径下已存在不同的目标文件时，审查 diff 并在不丢弃本地修改的前提下合并。如果归属不明确，停下来并询问，然后再替换。
6. 确认目标仓库中存在复制后的 `FOR_AGENTS.md` 和 `skills/setup-benny/SKILL.md`。
7. 直接从目标仓库读取并遵循 `.cursor/automations/benny/skills/setup-benny/SKILL.md`。

我希望你把这条记录合并到目标仓库的 `.cursor/settings.json`：

```json
{
	"plugins": {
		"pstack": { "enabled": true }
	}
}
```

保留所有无关的设置和插件。当现有文件使用 jsonc 时，保留注释和有效的 jsonc 语法。

我希望由一个以目标仓库为根的全新 agent 进行验证。确认 pstack 的 `how`、`why`、`tdd`、`unslop` 以及 benny 使用的原则技能都能在项目作用域中解析。不要计入从当前会话或用户级安装加载的技能。

如果项目作用域的插件不可用，或任何共享依赖无法解析，停下来并解释失败原因。不要把 `.cursor/automations/benny/skills/` 加入插件清单，也不要指望其文件出现在 slash-skill 列表中。

告诉我，在启用任一自动化之前，必须提交 `.cursor/settings.json`、`.cursor/automations/benny/` 以及任何被引用的不含密钥的配置。在我明确要求之前，不要创建或更新任何 automation。

首次创建时，对 triage 使用一次内置的 `/automate`，对 repro and fix 再使用一次。在开始第二个自动化之前，先完成第一个自动化的草稿审阅、批准、就绪检查和 Automations 编辑器交接。

把这份意图和最终配置转述到每个草稿中。triage prompt 必须读取并遵循 `.cursor/automations/benny/skills/triage-issue-reports/SKILL.md`。repro prompt 必须读取并遵循 `.cursor/automations/benny/skills/reproduce-and-fix-issues/SKILL.md`。只有在 `/automate` 确认这些路径已提交到 automation 将要运行的仓库之后，才使用这些仓库相对路径。

对于现有自动化，不要用 `/automate` 检查或更新它们。先验证配置，然后使用复制后的 setup 文件中的简明字段清单，以便我能在各自的编辑器中直接编辑每个自动化。不要创建重复项。
