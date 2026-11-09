# benny

benny 为 slack issue report 提供两个 cursor automation。一个负责分类每份报告，另一个复现已确认的 bug，并可能准备一个小型草稿修复。

本目录中的文件是休眠状态的安装与自动化源文件。它们不会作为 slash skill 出现。

## 设置

1. 让 cursor 指向 [`FOR_AGENTS.md`](./FOR_AGENTS.md)，并说明目标仓库。
2. 让 setup 把整个目录合并到目标的 `.cursor/automations/benny/`。它必须保留目标端独有的文件，并审查冲突，而不是覆盖本地修改。
3. 让 setup 在目标仓库的 `.cursor/settings.json` 中为共享依赖启用 pstack：

```json
{
	"plugins": {
		"pstack": { "enabled": true }
	}
}
```

4. 把用户自有的配置放在复制包之外，例如放在 `.cursor/benny/`。改编 [`configuration.example.yaml`](./templates/configuration.example.yaml) 和 [`feature-map.example.md`](./skills/reproduce-and-fix-issues/references/feature-map.example.md)。
5. 在启用任一自动化之前，提交 `.cursor/settings.json`、`.cursor/automations/benny/` 以及任何不含密钥的配置。
6. 审阅每个新自动化草稿，或在编辑器中更新现有自动化。然后发送一条无害的测试报告，并确认每条 source-channel 帖子都留在原始 thread 中。
