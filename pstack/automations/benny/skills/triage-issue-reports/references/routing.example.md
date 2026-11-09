# Routing map 示例

把这个文件复制到 `.cursor/automations/benny/` 之外，例如 `.cursor/benny/routing.md`，并替换每一个占位符。让 `routing.map_path` 指向该副本。包刷新绝不能覆盖它。

triage skill 把它当作数据。一条路由需要来自报告或原因追踪的证据。仅靠关键词匹配是不够的。

```yaml
routes:
  - name: "billing-example"
    match:
      product_areas:
        - "billing-area-placeholder"
      code_paths:
        - "billing-code-path-placeholder"
      error_signatures:
        - "billing-error-placeholder"
    destination:
      slack_channel: "billing-channel-placeholder"
      tracker_team: "billing-team-placeholder"
    owners:
      - "billing-owner-placeholder"
    allow_feature_owner_ping: false

  - name: "desktop-example"
    match:
      product_areas:
        - "desktop-area-placeholder"
      code_paths:
        - "desktop-code-path-placeholder"
      error_signatures:
        - "desktop-error-placeholder"
    destination:
      slack_channel: "desktop-channel-placeholder"
      tracker_team: "desktop-team-placeholder"
    owners:
      - "desktop-owner-placeholder"
    allow_feature_owner_ping: false

fallback:
  destination: ""
  owners: []
  allow_feature_owner_ping: false

ping_policy:
  default: "off"
  allow:
    - "configured-feature-owner"
    - "confirmed-regression-author"
  deny:
    - "broad-on-call-group"
    - "unverified-owner"
```

## 规则

- 保持 `fallback.destination` 为空，除非有一个团队接受所有未匹配的报告。
- 使用稳定的产品领域、代码路径和错误签名。
- 不要在公开副本中包含私有数据。
- 不要把原始用户 ID 或 channel ID 粘贴进将要发布的示例中。
- 在目标团队同意之前，保持 feature-owner ping 关闭。
- 改派只是告诉报告者该去哪里。automation 绝不跨频道转发。
