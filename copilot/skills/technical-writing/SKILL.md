---
name: technical-writing
description: "分层技术写作标准：Diátaxis 结构、Google 开发者文风句子、STE 指令规则、Global English 语法。用于 /technical-writing，或在写作/评审文档、RFC、readme、PR 描述或提交信息时使用。"
disable-model-invocation: true
---

# 技术写作

让疲惫的工程师第一遍就能读懂。四层规则全部适用。

有三条规则高于这些层次：

- **砍掉每个不起作用的词。** 如果一个句子去掉某个词仍然成立，这个词就该去掉。"In order to" 就是 "to"。"It is important to note that" 什么都不是。
- **用简短、日常的词。** 用 "Use"，不用 "utilize"。用 "Help"，不用 "facilitate"。用 "Do"，不用 "perform"。长词必须用精确性来换取它的长度。
- **当某条规则让句子变糟时，换个方式修句子，或者别动它。** 一个遵守所有规则、但读起来像机器写的句子，是失败的。

代码库就是词表。写真实的符号、文件、标志或命令名，不要写同义词或对它的描述。

不要生造行话。用开发者会脱口而出的词："move"、"delete"、"a budget that only decreases"，而不是 "evacuate"、"ratchet" 或 "endgame"。首次出现时说明了含义的模式名可以用。若想新增一个违规词及其替代说法，在你的回复里把它作为 `unslop` 抽象隐喻规则的新增条目提出，并附上 diff。不要编辑那个技能。

## 变化节奏

一篇文档可以遵守每一层规则，读起来仍然像机器写的：每句都被削短，哪里都没有观点，没有任何具体内容。

- 有意混合句长。短句落定一个要点。长句承载带有条件或后果的事实。
- 一句一个想法，不等于每句一样长。把承载两个想法的句子拆开。保留承载一个想法的长句。
- 在文体允许的地方给出观点。讲解要权衡取舍，所以说出你的判断，而不是罗列优缺点。参考文档保持冷静。
- 要具体，不要干瘪。不是 "schema changes can cause issues"，而是 "a column rename fails the build"。

## 先选模式（Diátaxis）

一篇文档，一个模式。两个问题就能确定它：内容是在指导行动（doing）还是理解（thinking），是服务于学习还是工作？

- 行动 + 学习：**教程**。
- 行动 + 工作：**操作指南**。
- 理解 + 工作：**参考**。
- 理解 + 学习：**讲解**。

指南针可以用在整篇文档上，也可以用在单个句子上。

**教程：边做边学。** 学习者的成功是你的责任，不是他们的。开头说明学习者将要构建什么，而不是他们将“学到”什么。每一步都要产生可见结果，要早、要频繁。告诉他们应该看到什么：预期输出、提示符变化、日志行。讲解压缩到一个从句加一个链接。保持具体。用“我们”来写，用命令式："First, do x. Now, do y."

**操作指南：通向目标的步骤。** 解决一个人遇到的问题，而不是机器能执行的操作。假定读者已胜任，跳过教学。只讲行动：不要离题，不要背景，不为完整而完整。那些改为链接。允许分叉和判断："If you want x, do y." 用任务给指南命名："How to calibrate the radar array"，而不是 "Radar array calibration"。

**参考：供查阅的事实。** 只做描述。没有指令，没有说服，没有观点。冷静、完整、确定。陈述事实、选项、限制和错误，不加任何模糊限定。镜像所描述事物的结构，让代码与文档可以互相对照浏览。把材料放在读者预期的地方。尽可能从代码生成。

**讲解：理解与原因。** 一个界限明确的话题，可以脱离产品单独阅读。每个标题都应能容忍前面加一个隐含的“关于……”。锚定在一个真实的“为什么”问题上。给出背景：设计决策、历史、约束、备选方案。只有这里允许观点，别处不允许。

不要混用模式：教程里不要放参考表格，参考里不要放教程式手把手，操作指南里不要辩论。拆开，然后链接。

## 面向读者写句子（Google 开发者文风）

- 把读者称为 "you"，用现在时。"Will" 只用于确实以后才发生的事。
- 说清谁做什么："the compiler checks"，而不是 "is checked"。仅当施动者未知或无关紧要时才用被动。
- 把指令写成命令："Click Submit." 平实陈述事实。绝不用 "should be done"。
- 把条件放在指令前："To delete the document, click Delete."
- 先写常见情况。例外放在后面。
- 听起来像一位懂行的朋友。不要流行术语，不要比喻，指令里不要加 "please"，流程中绝不用 "simply"、"easy" 或 "quickly"。如果真简单，读者就不会在这里了。
- 不要预告（"we will soon support..."），也不要让连续句子以同一短语开头。
- 用能说明去向的文字做链接：页面标题或简短描述。绝不用 "click here"。宁可页面上多一句上下文，也不要跳出去的链接。
- 标题要承载要点，而不只是主题（"Pick the mode first"，而不是 "Modes"）。用句首大写。任务型标题是光秃秃的动词短语（"Create an instance"）。概念型标题是名词短语。每页一个 h1，不跳级。
- 序列用编号列表，其余用项目符号。用完整句子引出列表。保持条目并列。
- 代码用等宽字体。UI 元素用粗体。用牛津逗号。删掉 "etc."，并在开头说明列表并不完整。

## 让陈述一次只承载一件事（STE 规则）

- 一句话一条指令。其他地方也是一句话一个想法。
- 指令超过约 20 词就拆分，其他句子超过约 25 词也拆分。
- 把警告或条件放在它所保护的步骤之前："If hot oil touches your skin, injuries can occur."
- 保留 "the" 和 "a"："Remove backup file" 有两种读法。"Remove the backup file" 只有一种。
- 让每个词只有一个含义、一项职责，并保持一致。如果 "check" 表示检查，就不要同时用它表示克制。
- 每个动作固定用一个词："start" 就在这里用 "start"，别在别处换成 "initiate"。
- 把流程写成直接命令，绝不要写成叙述，也绝不用被动："Install the component"，而不是 "the component must be installed"。
- 尽可能避免 "-ing" 形式的词。

## 不让句子有两种读法（Global English）

- 把 "only"、"not" 这类词放在它们所修饰的词旁边："only fails on growth" 与 "fails only on growth" 意思不同。
- 拆开长名词串："the proto import budget check script" 改为 "the script that checks the proto-import budget"。
- 让每个 "it"、"they"、"this" 都明确指向一个对象。拿不准时就重复名词。绝不用 "this" 或 "which" 指向整个从句。
- 不要省略动词："Phase 1 moves the converters and Phase 2 the runtime" 让 Phase 2 没有动词。给它补上。
- 保留标示结构的小词，例如 "Ensure that the switch is off" 中的 "that"。绝不为字数牺牲清晰。
- 当系列中省略冠词会导致误读时，重复冠词："the client and the host"，而不是 "the client and host"，因为它们是两样东西。
- 当句子可以有两种分组方式时，说明 "and" 或 "or" 连接的是哪几部分。"Both...and"、"either...or"、"if...then" 是免费消歧器。
- 用句号，不用分号。用新句子替代 em dash。
- 让括号内的文字成为完整的语法单位，或独立成句。绝不用 "(s)" 构成复数。
- 不要用斜杠：写 "a, b, or both"，而不是 "a/b" 或 "and/or"。
- 每样东西处处只用一个名称。一篇文档对同一事物说 "the gate"、"the ratchet" 和 "the budget check"，就是在教三样东西。没变的东西不要来回改叫法。
- 避开习语、口语、拉丁缩写和隐喻。

## 语气与仓库约定

- 对本技能涉及的每篇文档都应用 **unslop** 技能。那个技能负责 slop 模式目录：AI 词汇、填充、模糊限定、格式特征。
- PR 描述和提交信息也是写作。除 Diátaxis 以外的每一层都适用。PR 正文是一份评审者能在一分钟内读完的简报。不要粘贴 swarm 日志、SHA 列表或指标表格。链接它们。
- 产品 UI 文案不是文档。那些用你产品的文案指南。
- 代码片段用 tab 缩进。写真实路径。让每个计数或目录树声明在落地它的那个提交上成立，并附上可重新生成它的命令。

## 示例

修改前：

> 对 proto import ratchet budget 脚本参数的配置通过 budget.json 执行。请注意务必记住，带 --write 运行会把已提交的预算更新为当前计数，因此只应在下调预算时这样做。若超出，CI 会失败。

修改后：

> `budget.mjs` 从 `budget.json` 读取已提交的预算，并统计导入 protos 的文件数。若计数超出预算，CI 会失败。仅在需要下调预算时运行 `budget.mjs --write`。
