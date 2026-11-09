# 值得照抄的提示词

换成真实路径、技能和完成检查。口语化措辞即可。

## 理解

- `/pstack read <thread>. restate the underlying issue in your own words, in plain english.`
- `/in-your-own-words <long or messy ask>`
- `/sharpen <the prompt you're about to send>`
- `/pstack investigate why <symptom>. give me what we know, what data you used, and your best hypotheses. don't change any code yet.`
- `use /how to understand <subsystem>. then use /why to find out why it broke recently.`
- `/recall my work on <topic> from last week, then read <issue>.`
- `/teach me why you implemented it this way and not <other way>. what did you trade off?`
- `/pstack take over this branch. read the decision log, find what's done, and continue. don't redo finished work.`

## 构建

- Bug：`/pstack <symptom>. repro first, then fix and verify.`
- 应用中的 bug：`/pstack repro this with /verify-<app>. if it repros on main, fix it and show me a video as proof.`
- 有廉价测试的 bug：`/pstack repro <bug> first. if there's a cheap test path, /tdd it. then fix and rerun.`
- 功能：`/pstack add <behavior>. <current output> stays byte-identical. verify both.`
- 重构：`/pstack move <code> into one module, zero behavior change. record the current output first and prove it's unchanged after.`
- 性能：`/pstack <operation> takes <time> on <fixture>. trace it, fix the measured cause, show me before and after.`

## 设计与计划

- `/pstack prototype a few options for <feature>. take screenshots or videos for me to compare.`
- `/pstack we need <feature>. /architect it first, and answer open questions with prototypes. let me review before proceeding.`
- `/pstack write a tutorial for how i would use <new package> first. then /teach me why it beats the current one.`
- `ask /arena for a second opinion on this thread and our approach.`
- `/pstack turn this design into a plan. small verifiable PRs, each with its own verification steps.`
- `/pstack plan the migration of <library> to <target>. small verifiable PRs. the result must match the original exactly, bugs included.`

## 审查与发布

- `/interrogate the whole branch, but skeptically. don't change anything yet. no nitpicks unless it's a real bug or regression.` 也要读 Dropped 列表。
- `/create-formal-verification-skill prove <property> holds in <module>, even when <steps> interleave or retry.` 在该代码合并或重构之后：`/maintain-formal-verification-skill`。
- `/swarm check every package under <dir> against its check script. one worker per package. one report.`
- `/pstack open the pr. small ordered commits, evidence in the description.`
- `/pstack babysit this pr. get it green.` 只看状态时：`/pstack check on pr <number>. anything outstanding?`
- `/pstack land the stack.`

## 离开与回来

- `/pstack im going to bed. <goal> in a fresh worktree off <base>. done means <checks>. keep a decision log. don't ask me before committing. run until done. if you're truly stuck after a few hours, stop and write up why.`
- `/show-me-your-work catch me up on what you did last night.` 先读它的 Attention 小节。
- `/ketchup` 让你了解本次对话自上次消息以来的进展，并列出所有等待你处理的调用。
- `/pstack full autopilot on this queue. each item is independent.`
- `/pstack autopilot these changes, but don't merge. i'll land them.`
- `/reflect capture what we learned so the next run doesn't repeat it.` 只批准那些会改变未来决策的修改。
- `/bro` 用大白话复述上一条回复。
