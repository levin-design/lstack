---
name: unslop
description: 从任何写作中剔除 AI 痕迹。
disable-model-invocation: true
---

# Unslop

编辑文本，删除 AI 模式。扫描下列模式，然后重写。保留原意，并匹配预期语气。

## 要检测并修复的模式

规则编号是稳定的 id，其他技能会引用它们。删除某条规则会留下空缺。

### 内容

3. **表面的 -ing 短语。** "highlighting..."、"ensuring..."、"reflecting..."、"showcasing..."、"fostering..."。删除，或用真实来源展开。
5. **含糊的归属。** "Experts believe"、"Industry reports suggest"、"Some critics argue"。点名来源，或删除。

### 语言

7. **AI 词汇。** Additionally、crucial、delve、enduring、enhance、fostering、garner、interplay、intricate、landscape（抽象用法）、pivotal、showcase、tapestry（抽象用法）、testament、underscore、vibrant。换成朴素词。
8. **"is" 的花哨说法。** "serves as"、"stands as"、"boasts"、"features"。就说 "is" 或 "has"。
9. **"Not just X, but Y"。** 改为直接陈述要点。
10. **三法则。** 不要强行把想法凑成三组。用自然的数目。
11. **同义词轮换。** 同一段里出现 protagonist、main character、central figure、hero。选一个，重复用它。
12. **虚假区间。** "from X to Y"，而 X 与 Y 并不在同一个有意义的刻度上。直接列出主题。

### 风格

13. **em dash 滥用。** 完全避免 em dash。只用句号或逗号（不用括号，不用 en dash，也不用连字符冒充破折号）。如果某个想法需要分隔，就结束句子，或用逗号。
14. **冒号滥用。** 列表或示例前用冒号没问题，但不要把它当句中连接器。"If you're coming from traditional automation: instead of registering event handlers, you describe conditions" 这个冒号什么都没加。重写，让要点独立成立，不靠对比框架。"Describing when the scheduler should fire works best as plain English." 意思相同，不靠拐杖标点。
15. **粗体滥用。** 不要给每个专有名词或缩写加粗。
16. **行内标题式列表。** 特征是粗体标签加冒号，然后复述该行："**Performance:** Performance improved..."。把这些改写成散文。以句号结尾、点明条目、后面接真正新细节的粗体引导语（"**Schema in TypeScript.** Tables live in one file."）是可以的，不算特征。
17. **标题用 title case。** 改用句首大写（sentence case）。
18. **装饰性 emoji。** 从标题和项目符号中删除。
19. **弯引号。** 用直引号。

### 交流痕迹

20. **聊天机器人式短语。** "I hope this helps!"、"Let me know if..."、"Of course!"、"Certainly!"、"Found the smoking gun!"。删除。
22. **谄媚语气。** "Great question! You're absolutely right!" 直接回应。

### 填充

23. **填充短语。** "In order to" 改为 "To"。"Due to the fact that" 改为 "Because"。删除 "It is important to note that"。
24. **过度模糊限定。** "could potentially possibly be argued that it might" 改为 "may"。
25. **泛泛的结论。** "The future looks bright." 改为陈述具体计划或事实。

### 行话

26. **抽象隐喻名词。** Substrate（base）、wedge、wedge in（add）、vector（way, method）、locus、vantage、nexus、作名词用的 primitive、作隐喻的 harness、"API surface" 中的 surface、bedrock、作隐喻的 scaffolding、modality、paradigm、gold-plating（超出任务所需）、作隐喻的 ratchet（写出机制的真实名称，或写成只会收紧的限制）、用于移动代码的 evacuate（move out）、endgame（last phase）、north star、flywheel。这些词读起来像术语，但通常有更朴素的具象词。选那个具象词。

### 朴素表达

27. **说它做什么，不说它给人什么感觉。** "the database stays close at hand"、"SQL you can read"、"types that follow your schema" 命名的是一种感觉。修法是命名机制或给出数字："`.toSQL()` returns the exact string sent to the database"、"a column rename fails the build"。问这句话要读者做什么或知道什么，然后那样写。如果无法重述为具体的指令、事实或数字，就删掉。再检查一点：如果这句话原封不动放进另一个项目的文档也说得通，那它没有说明本项目的任何事。删掉。
28. **拆开或缩短密集句子。** 如果读者必须回头重读才能解析一句话，就一分为二，或删掉从句。一句话一个想法。
29. **主动语态。** 优先使用。抓住 "is/are/was/were + 过去分词"，并点明施动者："queries are validated" 改为 "the compiler validates queries"，"the file is parsed by the loader" 改为 "the loader parses the file"。仅当施动者未知或确实无关紧要时，才用被动。
30. **删掉副词，或换更强的动词。** "runs quickly" 改为 "is fast" 或给出数字，"significantly improves" 改为测得的增量。副词在支撑一个孱弱的动词，说明动词选错了。
31. **优先用朴素词。** "utilize" 和 "leverage" 改为 "use"，"facilitate" 改为 "help"，"numerous" 改为 "many"，"in the event that" 改为 "if"。更花哨的同义词很少更清楚。
32. **做作的行文。** 在有字面说法时用隐喻或装饰：格言（"wire it or delete it"）、为效果而用的修辞性片段、给代码拟人（"the plan holds it"）、比喻性动词（"rides along"、"stands on"）、套路化框架短语。"A dial worth turning" 改为 "a parameter worth varying"。说清你的意思。规则 26 覆盖隐喻名词。
33. **过度压缩。** 省略冠词、没有动词的片段、符号化表达，以及需要读者解码而不是阅读的缩写。"Parser rejects bad date → exit 2, no write" 改为 "The parser rejects a bad date, exits with code 2, and writes nothing." 写完整的句子，带上冠词和动词，并把箭头和缩写写全。
