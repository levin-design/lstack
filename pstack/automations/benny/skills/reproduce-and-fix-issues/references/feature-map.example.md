# Feature map 示例

映射 Benny 可能复现的每一个面向用户的功能。在驱动应用之前读取相关小节。让这份地图保持在用户视角。在运行时发现内部实现和当前代码路径，而不是在此固化它们。

把这个文件复制到 `.cursor/automations/benny/` 之外，例如 `.cursor/benny/feature-map.md`，并把 `control.feature_map_path` 指向该副本。包刷新绝不能覆盖它。

## 每个功能的模板

### `<feature name>`

`<一句面向用户的用途说明>`

#### How a user gets there

- 点击路径：`<screen> -> <menu, tab, or panel> -> <control>`
- 键盘快捷键：`<shortcut or none>`

#### How the control adapter drives it

- `<adapter action>` 配合 `<inputs>` 应当 `<visible result>`。
- 重置：`<how the adapter returns to a fresh state>`。

#### Stable selectors

- `<role and accessible name>`
- `<ARIA relationship>`
- `<data-component or purpose-named data attribute>`

绝不要使用生成的 CSS 或 StyleX 类名、动态哈希、子节点索引或脆弱的 DOM 位置。

#### States to exercise

- Default、hover、focus-visible、active、disabled
- Loading、empty、error
- Selected、open、expanded
- `<relevant feature-specific variants>`

标注不适用的小节。

#### Preconditions and setup

- 认证：`<account state>`
- 数据：`<fixture>`
- 权限：`<role>`
- Flag：`<flag or none>`
- 服务：`<required availability>`

#### Evidence and cross-check

- 截图：`<app identity, feature, and discriminating state>`
- 视频：`<entry path, interaction, and final state>`
- 交叉核对：`<read-only state or value that confirms the UI>`

#### Gotchas

- `<known dead end or wrong surface>`
- `<safe environment translation>`

## 虚构示例

这些功能属于一个虚构的任务应用。它们是示例，并非 Benny 必需的功能。

### 登录

让用户进入任务应用。

#### How a user gets there

- 打开应用并选择 `Sign in`。无快捷键。

#### How the control adapter drives it

- `open_app`、`click Sign in`、`fill credentials` 和 `click Continue` 应打开条目列表。
- 通过退出登录并清除一次性会话来重置。

#### Stable selectors

- 按钮 `Sign in`、文本框 `Email` 和 `Password`、`data-component="sign-in-form"`

#### States to exercise

- Default、focus-visible、submitting、disabled、loading、error

#### Preconditions and setup

- 一次性账号和可用的认证服务

#### Evidence and cross-check

- 录制从落地页到条目列表。检查只读会话状态。

#### Gotchas

- 营销页面是错误的界面。认证服务缺失属于阻塞。

### 条目列表与详情

让用户浏览条目并打开其中一个。

#### How a user gets there

- 打开 `Items` 标签页，然后选择一行。

#### How the control adapter drives it

- `select_tab Items` 和 `click <fixture item>` 应打开其详情。
- 通过关闭详情并清除选择来重置。

#### Stable selectors

- 名为 `Items` 的标签页和列表、以 fixture 命名的行、`data-component="item-detail"`

#### States to exercise

- Loading、empty、error、selected、open、expanded

#### Preconditions and setup

- 具名 fixture 条目、读取权限、可用的条目服务

#### Evidence and cross-check

- 展示选择状态和匹配的详情标题。检查选中条目的 ID。

#### Gotchas

- 搜索结果可能看起来相似，但走的是不同路径。

### 条目编辑器

让用户创建或编辑条目。

#### How a user gets there

- 从详情中选择 `Edit`，或从列表中选择 `New item`。

#### How the control adapter drives it

- `click Edit`、`fill <field>` 和 `click Save` 应更新详情。
- 通过恢复 fixture 来重置。

#### Stable selectors

- 按钮 `Edit`、`New item`、`Save`，表单 `Item editor`，与 label 关联的字段

#### States to exercise

- Default、focus-visible、dirty、validating、disabled、saving、error、success

#### Preconditions and setup

- 可编辑的 fixture、写入权限、可用的保存服务

#### Evidence and cross-check

- 展示字段变更到更新后的详情。只读检查存储的条目值。

#### Gotchas

- 不要注入表单状态。只读的详情字段不是编辑器。

### 设置

让用户更改个人偏好。

#### How a user gets there

- 打开个人资料菜单，然后选择 `Settings`。

#### How the control adapter drives it

- `open_menu Profile`、`click Settings` 和 `toggle <preference>` 应更新控件。
- 通过恢复初始偏好来重置。

#### Stable selectors

- 按钮 `Profile`、菜单项 `Settings`、区域 `Settings`、按用途命名的偏好属性

#### States to exercise

- Closed、open、selected、focus-visible、disabled、loading、error

#### Preconditions and setup

- 已登录的测试账号、已知的偏好、可用的偏好服务

#### Evidence and cross-check

- 展示菜单路径和最终控件状态。只读检查偏好值。

#### Gotchas

- 操作系统设置是另一个界面。

## 完整性检查清单

- 每个可复现的面向用户功能都有一个小节。
- 每个小节都写明用户路径、adapter 动作和重置方式。
- 选择器使用 role、名称、ARIA、稳定的组件标记或按用途命名的属性。
- 没有选择器使用生成的类名或 DOM 位置。
- 覆盖了相关的交互、加载、空白、错误、选中和展开状态。
- 认证、fixture、权限、flag 和服务均已明确。
- 截图、视频和底层交叉核对要求均已明确。
- 列出了错误的界面、死路和安全的环境转译。
- 实现细节仍然留给运行时发现。
