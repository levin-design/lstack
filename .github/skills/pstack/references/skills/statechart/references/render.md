# 渲染图表

用 npm 包 `pele@1.9.0` 渲染你展示的每个 `.mmd` 文件，并把 SVG 交给用户。在仓库之外安装一次 Pele。把每个 SVG 写在对应 `.mmd` 文件旁边，使用相同的名称。API 位于 https://pele.run/api。把 `{ limit: 1_000_000, outputLimit: 8_000_000, maxEdges: 10_000 }` 作为 `render` 的选项传入。Pele 的默认值小于一个有 500 个状态的图表可能达到的规模。当 Pele 抛出 `PeleError` 时，向用户展示 Mermaid 文本和该错误。

## 颜色

Pele 忽略 Mermaid 的 `theme` 和 `themeVariables`。在 `.pele` 上设置它的 `--pele-*` CSS 变量。https://pele.run/theming 列出了这些变量。命令给每个状态其所属组的颜色类，例如 `class sN teal`。它用 `class sN breaks` 或 `class sN mayBreak` 标记每个坏状态，用 `class sN bugPath` 标记通往 bug 的最短路径上的每个状态，并用 `class sN repeats` 标记 PROPERTY 反例永远重复的每个状态。Pele 把这些类放在状态的节点上。用 CSS 给这些类着色。

`.mmd` 文件为 `breaks` 和 `mayBreak` 各有一行 `classDef`，以便任何 Mermaid 查看器都能显示 bug 标记。它没有为组颜色、`bugPath` 或 `repeats` 提供 `classDef`。Pele 把每个 `classDef` 颜色写成节点上的 `style` 属性，而 `style` 属性优先于普通 CSS 规则。因此下面针对标记的规则使用 `!important`。没有它，暗色主题会保留浅色的标记颜色。bug 标记设置填充和文字，`bugPath` 和 `repeats` 设置边框。把标记规则放在组颜色之后，使标记显示在组颜色之上。

这些颜色是建议值。它们是旧技能的颜色。把它们放在每个 SVG 开头的 `<style>` 元素中。这样每个 SVG 会遵循查看器的浅色或暗色设置。

```css
.pele {
  --pele-bg: #ffffff;
  --pele-fg: #1c1c1c;
  --pele-muted: #656565;
  --pele-line: #808080;
  --pele-surface: #fcfcfc;
  --pele-surface-alt: #f1f1f1;
  --pele-border: #c9c9c9;
}
.pele .blue rect { fill: #c3e0ff; }
.pele .orange rect { fill: #f0d3bf; }
.pele .purple rect { fill: #e3d5ff; }
.pele .yellow rect { fill: #f0dcbf; }
.pele .teal rect { fill: #bfe3df; }
.pele .tan rect { fill: #e5d9ce; }
.pele .pink rect { fill: #ffcbe6; }
.pele .breaks rect {
  fill: #ffecee !important;
  stroke: #e72e3b !important;
  stroke-width: 2.5px !important;
}
.pele .breaks text {
  fill: #cd2834 !important;
}
.pele .mayBreak rect {
  fill: #fff3e6 !important;
  stroke: #e8730c !important;
  stroke-width: 2.5px !important;
}
.pele .mayBreak text {
  fill: #b85a06 !important;
}
.pele .bugPath rect {
  stroke: #1680f3 !important;
  stroke-width: 2.5px !important;
}
.pele .repeats rect {
  stroke: #9b35d6 !important;
  stroke-width: 2.5px !important;
  stroke-dasharray: 6 3;
}
@media (prefers-color-scheme: dark) {
  .pele {
    --pele-bg: #1f1f1f;
    --pele-fg: #f5f5f5;
    --pele-muted: #acacac;
    --pele-line: #939393;
    --pele-surface: #121212;
    --pele-surface-alt: #2c2c2c;
    --pele-border: #4e4e4e;
  }
  .pele .blue rect { fill: #1b3857; }
  .pele .orange rect { fill: #573117; }
  .pele .purple rect { fill: #3c2e57; }
  .pele .yellow rect { fill: #573d17; }
  .pele .teal rect { fill: #174641; }
  .pele .tan rect { fill: #3d3127; }
  .pele .pink rect { fill: #57233e; }
  .pele .breaks rect {
    fill: #2e2021 !important;
    stroke: #cf2b35 !important;
  }
  .pele .breaks text {
    fill: #ff6463 !important;
  }
  .pele .mayBreak rect {
    fill: #2e2619 !important;
    stroke: #d0700f !important;
  }
  .pele .mayBreak text {
    fill: #ffa257 !important;
  }
  .pele .bugPath rect {
    stroke: #116dd2 !important;
  }
  .pele .repeats rect {
    stroke: #9a3fcf !important;
  }
}
```
