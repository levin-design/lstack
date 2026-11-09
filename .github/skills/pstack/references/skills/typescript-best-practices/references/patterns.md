# TypeScript 模式

`SKILL.md` 中每条规则的代码示例。其背后的原则与语言无关。参见 **type-system-discipline** 和 **boundary-discipline** 原则技能。

## 品牌类型

为原始类型打上品牌，使其不会被混用。在边界处校验一次。下游代码信任该类型。

```ts
type AgentId = string & { readonly __brand: "AgentId" };

function isAgentId(input: string): input is AgentId {
  return isUUID(input);
}

function parseAgentId(input: string): AgentId {
  if (!isAgentId(input)) throw new Error(`Invalid agent id: ${input}`);
  return input;
}

function focusAgent(id: AgentId): void {
  /* input is trusted */
}
```

沿用 `readonly __brand: 'X'` 的形状。不要自创一套新约定。

## 可辨识联合

用字面量判别字段为各变体建模。所有变体共用同一字段名，且各变体的值互不相同，因此不可能的组合无法被表示。

```ts
// Don't. Boolean + optionals lets contradictory states exist.
type DiffState = { loading: boolean; diff?: GitDiff; error?: string };

// Do. Only valid states exist.
type DiffState =
  | { kind: "loading" }
  | { kind: "ready"; diff: GitDiff }
  | { kind: "error"; error: string };
```

选定一个判别字段名（`kind`、`type`、`tag`）并坚持使用。

## 构造式建模

用全部合法的部件构造类型，而不是靠运行时检查去限制一个宽松类型。

非空，用可变参数元组表示：

```ts
type NonEmpty<T> = [T, ...T[]];

// Don't: T[] plus a length check every caller must repeat
function pickWinner(entries: string[]): string {
  if (entries.length === 0) throw new Error("no entries");
  return entries[Math.floor(Math.random() * entries.length)];
}

// Do: an empty value of the type can't exist
function pickWinner(entries: NonEmpty<string>): string {
  return entries[Math.floor(Math.random() * entries.length)];
}
```

当传入的是普通 `T[]` 时，用守卫收窄一次。此后这一事实会随类型一起传递：

```ts
const isNonEmpty = <T>(arr: T[]): arr is NonEmpty<T> => arr.length > 0;
```

偶数长度，用成对元组表示：

```ts
type Pairs<T> = [T, T][];
```

时间区间，用起点加时长表示：

```ts
// Don't: a comment holds the invariant
type TimeRange = { start: Date; end: Date }; // start <= end

// Do: a negative range can't be written; derive end when needed
type TimeRange = { start: Date; durationMs: number };
```

让 `durationMs` 保持普通 number。仅当原始数字可能被传进期望时长的位置时才打品牌（参见品牌类型一节），不要条件反射式地打。选择能让坏状态无法构造的表示法，然后在其上暴露你需要的读取方式（`pairs.flat()`、`rangeEnd()` 辅助函数）。

## 最简全函数类型

不要什么都强化。只要对其的所有操作都是全函数，就保留 `T[]`：

```ts
const sum = (xs: number[]) => xs.reduce((a, b) => a + b, 0); // [] is 0, fine
```

当宽松类型在某个使用点迫使你撒谎时才强化。征兆是 `!`、`arr[0] as T`，以及“不应发生”的 throw：

```ts
// Don't: partiality smuggled past the compiler
function newestSession(sessions: Session[]): Session {
  return sessions.at(0)!;
}

// Do: strengthen the input; the assertion disappears
function newestSession(sessions: NonEmpty<Session>): Session {
  return sessions[0];
}
```

把结果弱化为 `Session | undefined` 是另一种全函数签名。

## `unknown` 优于 `any`

外部数据永远是 `unknown`。使用前先收窄。

```ts
// Don't
function handle(input: any) {
  return input.foo.bar;
}

// Do
function handle(input: unknown) {
  if (typeof input === "object" && input !== null && "foo" in input) {
    // narrowed; compiler verifies access
  }
}
```

外部来源包括 RPC 载荷、`JSON.parse`、`postMessage`、IPC、文件内容、环境变量、数据库结果。

## 先 schema 后手写守卫

在为外部数据逐属性手写类型守卫之前，先找仓库已有的运行时 schema 库和现有 schema。让同一个 schema 全权负责校验，并从中派生 TypeScript 类型。不要同时维护 schema、重复的 interface，以及可能彼此漂移的守卫。

```ts
import { z } from "zod";

const UserSchema = z.object({
  id: z.string().uuid(),
  role: z.enum(["admin", "member"]),
});

type User = z.infer<typeof UserSchema>;

function parseUser(input: unknown): User {
  return UserSchema.parse(input);
}
```

当失败是预期分支时使用 `safeParse`。若仓库使用其他 schema 库，则用其对应的推断辅助函数。不要为单个守卫新增 schema 依赖。本规则偏好代码库已经信任的 schema 体系。

## 禁止 `as` 断言

每一个 `as` 都是潜在的运行时崩溃。仅在类型系统已验证该主张之后才做断言。

```ts
import { z } from "zod";

// Don't
const user = data as User;

// Don't
function isUser(data: unknown): data is User {
  return typeof data === "object" && data !== null && "id" in data;
}

// Do
const userSchema = z.object({ id: z.string(), name: z.string() });
type User = z.infer<typeof userSchema>;

function parseUser(data: unknown): User {
  return userSchema.parse(data);
}
```

当类型先行时，用校验器所要证明的类型标注它。这样编译器会拒绝证明力不足的校验器。把下面对象中的 `name` 去掉，赋值就无法通过编译。

```ts
type User = { id: string; name: string };

const userSchema: z.ZodType<User> = z.object({ id: z.string(), name: z.string() });
```

从现有代码中重构掉 `as` 时，先弄清 TypeScript 为何无法推断：

- 缺少判别字段：补一个，改用可辨识联合。
- 源类型过宽（例如 `Record<string, unknown>`）：收窄它。
- 无类型边界：用拥有该形状的 schema 解析。仅在完全没有 schema 的地方新增一个。
- 确实无法表达：使用品牌类型或 `satisfies`。

## 收窄优先级

从最佳到最后的备选：

1. **可辨识联合 switch / if。** 编译器会自动收窄。
2. **`in` 运算符。** `"key" in obj` 收窄到包含该键的变体。
3. **`typeof` / `instanceof`。** 用于原始值和类实例。
4. **用户定义类型守卫。** 以上都不够用时。
5. **`as` 断言。** 仅在验证之后。

```ts
function area(s: Shape): number {
  if ("radius" in s) return Math.PI * s.radius ** 2; // narrowed to circle
  return s.width * s.height; // narrowed to rect
}
```

## 类型守卫

守卫必须真正验证其主张。说谎的守卫比 `as` 更糟。

```ts
function isCircle(s: Shape): s is Shape & { kind: "circle" } {
  return s.kind === "circle";
}
```

尽可能优先用判别字段收窄。

## 穷尽性

在 default 分支中，把该判别值赋给一个 `never` 类型的局部变量。

```ts
// Value-returning switch
function area(s: Shape): number {
  switch (s.kind) {
    case "circle":
      return Math.PI * s.radius ** 2;
    case "rect":
      return s.width * s.height;
    default: {
      const _exhaustive: never = s;
      return _exhaustive;
    }
  }
}

// Void switch
function handle(s: Shape): void {
  switch (s.kind) {
    case "circle":
      drawCircle(s);
      break;
    case "rect":
      drawRect(s);
      break;
    default: {
      const _exhaustive: never = s;
      void _exhaustive;
    }
  }
}
```

有返回值的 switch 用 return 风格，语句式 switch 用 void 风格。

## `satisfies` 优于 `as`

`satisfies` 在验证的同时不拓宽字面量类型。

```ts
// Don't. Widens, loses literal types.
const config = { theme: "dark", cols: 3 } as Config;

// Do. Validates AND preserves literal types.
const config = { theme: "dark", cols: 3 } satisfies Config;
// config.theme is "dark" (literal), not string
```

## 边界校验

在数据进入之处校验一次。内部代码信任类型。参见 **boundary-discipline** 原则技能。

- **线格式（Wire formats）**（proto、JSON-RPC）：解析时启用 `ignoreUnknownFields`，使向前兼容的变更不会破坏旧客户端。
- **持久化 JSON：** 带版本号的 blob，并在解析处包 try/catch。
- **不要重复校验**调用链深处的数据。

## 从 schema 派生类型

当 `.proto`、OpenAPI 规范、GraphQL schema 或数据库迁移已经定义了某种形状时，从生成的类型派生，而不是复制一份。

```ts
// Don't. Duplicate shape, drifts when the schema changes.
type CheckSummary = {
  totalCount: number;
  checks: { name: string; status: string }[];
};
function renderChecks(s: CheckSummary) {
  /* ... */
}

// Do. Derive from the generated schema type.
import type { ChecksMessage } from "<generated module>";
function renderChecks(s: Pick<ChecksMessage, "totalCount" | "checks">) {
  /* ... */
}
```

在编写新 interface 之前，先用 `Pick`、`Omit`、`Parameters`、`ReturnType`、`Awaited`、`typeof`。

## 对象参数

```ts
// Don't. Swap two args, still compiles.
openFile(uri, {
  startLineNumber: 10,
  startColumn: 1,
  endLineNumber: 10,
  endColumn: 1,
});

// Do. Order-independent, self-documenting.
openFile({
  uri,
  selection: {
    startLineNumber: 10,
    startColumn: 1,
    endLineNumber: 10,
    endColumn: 1,
  },
});
```

在热路径上跳过：逐帧渲染、分词器、解析器，以及任何分配开销敏感的紧密循环。
