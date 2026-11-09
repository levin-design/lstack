### Trace forensics

**从产物做诊断由你负责。**

区别于 **Runtime forensics**，后者对活进程做埋点。这里捕获已经存在。产物是固定的数据集，读它，不要重跑。工具保持通用：cpuprofile 和 `.json.gz` 用 DevTools 或 trace 解析器，spindump 用文本编辑器，heapsnapshot 用你的堆分析工具。

1. 识别格式并用正确的工具加载。在子代理中解析大产物（**principle-guard-the-context-window** 技能），把归约后的发现留在主线程。按 Subagents 一节为每项工作选择子代理的推理级别以及快速或标准速度。
2. 把原始产物转换为可查询的形式。把 trace 或堆快照导入 sqlite，每个样本、帧或节点一行。在阅读之前先达到可查询的形态。
3. 收窄到原因。查询占时间最多的帧，并沿调用树走到热路径。对泄漏，从泄漏对象沿持有链跟到 GC 根。对 spindump，找出卡在 CPU 上或被阻塞的线程及其等待原因。
4. 归因到源码。用产物自身的符号把热帧映射到文件、符号和行。没有源码映射的帧还不构成诊断。解析符号，或明确说明产物未携带它们。
5. 如果有成对的捕获，diff 前后产物以确认。否则把发现标记为产物所支持的最强假设，而不是已确认的原因。
6. 交回带引用的诊断，除非被要求否则不修复。原因明确后路由到 Bug fix 或 Perf issue。throughput checkpoint 保持一行：`throughput checkpoint: n/a, read-only forensics`。

**回复：** 产物与格式、归约后的发现、源码位置、产物路径，以及是否有成对捕获予以确认。
