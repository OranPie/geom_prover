下面这一份就是你要的 **「最后的总结文档 / all-in-one 导引」**：
专门汇总了：

1. ✅ 定理文件格式完整规范（可扩展、可维护）
2. ✅ Fact 类型体系的完整清单（分层分类）
3. ✅ Proof Engine 的完整搜索流程 + 时序图（文字版 UML）

全篇是**设计与规范**，不写实现代码，可直接用于指导多人协作实现。

---

# 0. 总览：系统三大层

1. **Fact 层**

   * 用统一的形式表示几何事实：如“点在直线上”“两角相等”“三点共线”等。
   * 这是“逻辑原子”。

2. **Theorem 层**

   * 由外部文件（YAML/JSON 等）描述：

     * 前提是一些 Fact 模式
     * 结论是一些 Fact 模式
     * 附加条件 & 自然语言模板
   * 完全可扩展：新增/修改定理不用动核心代码。

3. **Proof Engine 层**

   * 接收：初始 Fact 集合 + 定理库 + 目标 Fact（prove）
   * 做：带剪枝的搜索与推理（前向/后向/混合）
   * 输出：Proof（证明树） + Description（叙述）

---

# 1. 定理文件格式完整规范（Theorem File Format）

这里以 **YAML** 为示例格式（概念同样可移植到 JSON / 自定义 DSL）。
每条定理是一个独立条目；一个文件中可以有多条定理。

## 1.1 顶层字段列表

每条定理条目的字段建议如下：

* `id`：string，定理的唯一标识

* `version`：string，定理版本（便于升级）

* `name`：string，人类可读名称（中文可）

* `category`：string，分类标签（如 `triangle`, `circle`, `parallel`, `similarity`）

* `tags`：list[string]，额外标签（竞赛级/常用等）

* `premises`：list[FactPatternString]，前提模式

* `conclusions`：list[FactPatternString]，结论模式

* `conditions`：list[ConditionString]，其他逻辑条件（非直接 Fact）

* `priority`：int，推理优先级（用于搜索排序）

* `max_uses`：int，可选；在一次证明中最多使用多少次（防止无限循环）

* `nl_templates`：

  * `cn`: string，自然语言中文模板
  * `en`: string，可选英文模板

* `notes`：string，备注/说明

* `enabled`：bool，是否启用

一个完整条目结构：

```yaml
- id: ISO_TRIANGLE_1
  version: "1.0"
  name: 等腰三角形底角相等
  category: triangle
  tags: [isosceles, basic]
  premises:
    - EqualSegment({A}{B}, {A}{C})
    - NotCollinear({A}, {B}, {C})
  conclusions:
    - EqualAngle(Angle({B}{A}{C}), Angle({C}{A}{B}))
  conditions: []
  priority: 5
  max_uses: 3
  nl_templates:
    cn: "已知{A}{B} = {A}{C}且A,B,C不共线，则三角形{A}{B}{C}为等腰三角形，∠BAC = ∠ACB。"
    en: "If AB = AC and A,B,C are non-collinear, then triangle ABC is isosceles and ∠BAC = ∠ACB."
  notes: "最基础的等腰三角形性质。"
  enabled: true
```

> 注意：这不是“程序代码”，而是**数据格式规范**。

---

## 1.2 Fact Pattern 字符串语法规范

`premises` 与 `conclusions` 中每一项是一个 **Fact 模式字符串**，对应 Fact 类型体系中的一种类型。

基础规则：

1. **Fact 名在前，括号内是参数**

   * `EqualSegment({A}{B}, {C}{D})`
   * `On({P}, Line({A}{B}))`

2. **参数中使用 `{X}` 表示“模式变量”**

   * `{A}`、`{B}`、`{P}` 等在匹配时会绑定到实际点名。

3. **复合对象**

   * 线段：`{A}{B}` 表示 Segment(A,B)
   * 角：`Angle({A}{B}{C})` 表示 ∠ABC
   * 直线：`Line({A}{B})`
   * 圆：`Circle({O}, {R})` 或简化 `Circle({O}, r)`

4. **允许常数**

   * 如：`AngleValue(Angle({A}{B}{C}), 90deg)`
   * 或：`AngleValue(Angle({A}{B}{C}), pi/2)`

### 常见模式示例

* 比如“平行线内错角相等”：

```yaml
- id: PARALLEL_ALT_ANGLE
  name: 平行线内错角相等
  category: parallel
  premises:
    - Parallel(Line({A}{B}), Line({C}{D}))
    - On({E}, Line({A}{B}))
    - On({F}, Line({C}{D}))
    - Intersect(Line({E}{F}), Line({A}{B}), {X})
    - Intersect(Line({E}{F}), Line({C}{D}), {Y})
  conclusions:
    - EqualAngle(Angle({E}{X}{A}), Angle({F}{Y}{C}))
  ...
```

---

## 1.3 Conditions 字段语法规范

`conditions` 中描述那些不直接表达为 Fact，但需要检查的逻辑条件，例如：

* 不重合：`Distinct({A}, {B})`
* 不共线：`NotCollinear({A}, {B}, {C})`（也可以是 Fact）
* 非退化：`NonDegenerateTriangle({A}, {B}, {C})`

约定：

* conditions 是对模式变量的额外约束
* 在匹配定理时，Fact 匹配成功后，再对 conditions 进行检查
* 检查方式可以：

  * 依据已有 Fact（例如已存在 NotCollinear(A,B,C)）
  * 或用数值模型做辅助判断（如三点几乎共线则判为 false）

形如：

```yaml
conditions:
  - Distinct({A}, {B})
  - Distinct({A}, {C})
  - Distinct({B}, {C})
```

---

## 1.4 优先级与使用次数

* `priority`：越大表示越优先尝试
* `max_uses`：防止某些定理在循环结构中被反复使用，造成搜索爆炸：

策略示例：

* 基本几何事实：priority 高，例如 10
* 复杂相似三角形：priority 中等 5
* 高阶定理（如特殊构造）：priority 较低 1–3

Proof Engine 在搜索时，会按优先级排序定理。

---

## 1.5 定理扩展流程建议

1. 先识别需要的 **Fact 类型**
2. 若 Fact 类型不存在 → 在 Fact Type 系统中新增
3. 用模式写定理文件
4. 为定理写：

   * 简明中文描述（nl_templates.cn）
   * 单元测试几何配置（在 tests/ 里）
5. 保证新定理不会与现有定理产生明显循环

---

# 2. Fact 类型体系完整清单（推荐版本）

下面给出一个较为“覆盖广但不疯狂”的 Fact 类型体系，你可以在此基础上删减或扩展。

## 2.1 几何对象关系类（结构型 Fact）

1. `On(P, Line(A,B))`

   * 点 P 在直线 AB 上。
   * 来源：

     * DSL `point P on AB`

2. `OnSegment(P, A, B)`

   * P 在线段 AB 上（介于 A,B 之间）。

3. `OnCircle(P, Circle(O,R))`

   * P 在以 O 为圆心、半径 R 的圆上。

4. `Center(O, Circle(O,R))`

   * O 是圆的圆心。

5. `Radius(O, P)`

   * OP 为某圆的半径（可与 Circle 结合）。

6. `Collinear(A, B, C)` / `NotCollinear(A, B, C)`

   * A,B,C 共线/不共线。

7. `Between(B, A, C)`

   * B 在 A、C 之间。

8. `Midpoint(M, A, B)`

   * M 是 AB 的中点。

9. `FootOfPerpendicular(F, P, Line(A,B))`

   * F 是 P 到直线 AB 的垂足。

10. `ReflectPoint(P', P, Line(A,B))`

    * P' 是点 P 关于直线 AB 的对称点。

11. `Intersect(L1, L2, P)`

    * 直线/线段 L1 与 L2 相交于点 P。

---

## 2.2 长度/比例相关 Fact

12. `EqualSegment(Segment(A,B), Segment(C,D))`

    * AB = CD。

13. `ProportionalSegment(Segment(A,B), Segment(C,D), k)`

    * |AB| = k * |CD|。

14. `SegmentRatio(A, B, C, D, r)`

    * |AB| / |CD| = r。

15. `LengthValue(Segment(A,B), v)`

    * |AB| = v（数值）。

---

## 2.3 角度相关 Fact

16. `EqualAngle(Angle(A,B,C), Angle(D,E,F))`

    * ∠ABC = ∠DEF。

17. `RightAngle(Angle(A,B,C))`

    * ∠ABC = 90°。

18. `SupplementaryAngle(Angle1, Angle2)`

    * 两角互补。

19. `AngleSum(Angle1, Angle2, k)`

    * Angle1 + Angle2 = k° 或 k rad。

20. `AngleValue(Angle(A,B,C), v)`

    * ∠ABC = v。

---

## 2.4 直线间关系

21. `Parallel(Line(A,B), Line(C,D))`

    * AB ∥ CD。

22. `Perpendicular(Line(A,B), Line(C,D))`

    * AB ⟂ CD。

23. `SameLine(Line(A,B), Line(C,D))`

    * 两线是同一条直线。

---

## 2.5 三角形/多边形形态 Fact

24. `Triangle(A,B,C)`

    * 标记：A,B,C 构成三角形（不共线）。

25. `IsoscelesTriangle(A,B,C)`

    * △ABC 为等腰三角形（通常指 AB=AC 或其他约定）。

26. `EquilateralTriangle(A,B,C)`

    * △ABC 为正三角形。

27. `SimilarTriangle(A,B,C, D,E,F)`

    * △ABC ~ △DEF。

28. `CongruentTriangle(A,B,C, D,E,F)`

    * △ABC ≅ △DEF。

29. `AreaValue(Triangle(A,B,C), v)`

    * 面积为 v。

> 注：相似/全等可以是高阶 Fact，由定理推导产生；甚至可以只在定理库内用模式表达（不一定当普通 Fact 用）。

---

## 2.6 圆相关 Fact

30. `TangentAt(Line(A,B), Circle(O,R), P)`

    * 直线 AB 在点 P 与圆 O,R 相切。

31. `Chord(A,B, Circle(O,R))`

    * AB 是该圆的弦。

32. `Diameter(A,B, Circle(O,R))`

    * AB 是直径。

33. `Arc(A,B, Circle(O,R))`

    * 圆弧 AB。

34. `CyclicQuadrilateral(A,B,C,D)`

    * 四边形 ABCD 内接于一个圆（所有点共圆）。

---

## 2.7 面积/数值关系 Fact

35. `AreaRelation(Triangle(A,B,C), Triangle(D,E,F), ratio)`

    * 面积比 = ratio。

36. `AreaSum(Shape1, Shape2, Shape3)`

    * 面积关系（可进一步细化）。

37. `NumericConstraint(expr, relation, value)`

    * 通用数值约束（如 sin(∠ABC) * |AB| = ...），主要用于连接优化/数值求解。

---

## 2.8 逻辑辅助类 Fact（用于定理 conditions 或证明判断）

38. `Distinct(P, Q)`

    * P ≠ Q。

39. `NonDegenerateTriangle(A,B,C)`

    * 三点不共线且边长非零。

40. `Orientation(A,B,C, sign)`

    * 有向面积符号，可用来区分凸/凹等。

> 这部分可以视具体需求选择保留或仅作为 conditions，而不进入普通 FactBase。

---

# 3. Proof Engine 完整搜索流程时序图（文字版）

## 3.1 主要参与者（对象）

* `Client/UI`：调用方
* `API.ProofAPI`：对外统一入口
* `DSL.Parser`：解析 DSL
* `SemanticBuilder`：从 AST 到 GeometryModel + ProveGoals
* `FactExtractor`：从模型中提取初始 Fact
* `TheoremBase`：定理库（从文件加载）
* `ProofEngine`：证明引擎（引擎核心）

  * 内部有：

    * `ProofState`
    * `ForwardReasoner`
    * `BackwardReasoner`
    * `NumericChecker`
* `Solver.NumericModel`：数值解模型（用于检验）

---

## 3.2 全局流程概览（从 DSL 到 Proof）

用文字序列表达类似 UML 时序图：

```text
Client/UI
  │
  │ 1. 提交 DSL 脚本（含 prove 语句）
  ▼
API.ProofAPI
  │
  │ 2. 调用 DSL.Parser 解析代码
  ▼
DSL.Parser
  │
  │ 3. 返回 AST
  ▼
SemanticBuilder
  │
  │ 4. 从 AST 构建：
  │    - GeometryModel
  │    - Constraints（数值约束）
  │    - ProveGoals（目标Fact描述）
  ▼
FactExtractor
  │
  │ 5. 基于 GeometryModel & DSL约束 提取基础 Facts
  ▼
TheoremBase
  │
  │ 6. 加载定理库（若尚未加载）
  ▼
Solver.NumericModel (可选)
  │
  │ 7. 使用 Constraints 做一次数值求解，得到 NumericModel
  │    - 若数值解失败，则 ProofEngine 不使用数值剪枝，只做纯推理
  ▼
ProofEngine
  │
  │ 8. 对每个 ProveGoal 启动证明：
  │    - 初始化 ProofState：
  │        - fact_base = 初始Facts
  │        - goals = [目标Fact]
  │        - proof_tree = 空
  │
  │ 9. 进入主循环：
  │    while goals 非空且未超时/超深度：
  │       - 取出当前goal
  │       - 调用 BackwardReasoner 找定理候选
  │       - 对每个候选定理：
  │           a) 模式匹配（TheoremPattern ↔ fact_base 或 future facts）
  │           b) 检查 conditions（利用 fact_base 和 NumericChecker）
  │           c) 若条件满足 → 产生一个“应用计划”
  │       - 对“应用计划”排序（根据 priority、匹配数量、数值合理性）
  │       - 逐个尝试应用：
  │           d) 应用定理：产生新Facts + 新goals（若是分解式）
  │           e) 更新 fact_base + proof_tree + goals
  │           f) 调用 ForwardReasoner 做一次局部前向推理扩展
  │           g) 检查：目标Fact是否已经在fact_base中成立？
  │               - 成立 → 本goal证明成功；记录path
  │               - 不成立 → 继续
  │
  │ 10. 若 goals 全部证明成功 → 构建 ProofResult(success)
  │     若某些 goals 无法证明 → ProofResult(partial/failed)
  ▼
Proof.Description
  │
  │ 11. 将 proof_tree 用 nl_templates 格式化成证明步骤说明
  ▼
API.ProofAPI
  │
  │ 12. 返回 ProofResult（含结构化 Proof + Description）给 Client/UI
  ▼
Client/UI
  │
  │ 13. UI 渲染：证明步骤 + 几何图的高亮展示
```

---

## 3.3 ProofEngine 内部逻辑关键点（更细一点）

### A. BackwardReasoner（后向推理）流程

对于当前 `goal`：

1. 在 TheoremBase 中找所有**结论模式**可能统一到该 goal 的定理。
2. 对每条候选定理：

   * 做模式变量到实际目标对象的初步绑定。
   * 由定理的前提模式生成一组“子目标”（sub-goals）。
3. 将 `(定理, 绑定, 子目标)` 作为一种“证明扩展候选”。

### B. ForwardReasoner（前向推理）流程

在 fact_base 更新后：

1. 遍历定理库，寻找前提全部可由现有 Facts 匹配的定理。
2. 产生新的 Conclusion Facts，加入 fact_base。
3. 限制前向推理的深度和次数，避免爆炸。

### C. NumericChecker（数值剪枝）

在两处被调用：

1. **在匹配定理前提后**：

   * 检查数值上是否非常不合理（例如被判平行的两线，夹角数值上明显 > 10°）。
   * 若不合理 → 直接剪枝，不尝试该候选。

2. **在生成新的 Conclusion Fact 时**：

   * 检查新 Fact 是否与 NumericModel 相冲突（如 EqualSegment，但数值上差很多）
   * 若冲突 → 放弃该推理路径（回溯）。

---

# 4. 最后总结：如何用这套设计来“搭建完整系统”

**如果你现在开始实现，推荐的路线：**

1. **先实现 Fact 类型体系（fact_types + fact_base）**

   * 把本文件中的 Fact list 做成真正的数据结构
   * 确保 FactBase 支持：添加、去重、按类型/点查询

2. **然后实现定理文件加载 + 模式匹配（theorem 模块）**

   * 确定统一的 theorem YAML 格式
   * 写几条基础定理试运行（内错角、等腰三角形、内角和）
   * 实现模式字符串解析 & 参数绑定

3. **实现 DSL → GeometryModel → Fact 的链路（dsl + semantic_builder + fact_extractor）**

   * 先支持简单几何构造（point, line, on, circle）
   * 能生成初始 Fact 集合

4. **实现 ProofEngine 的最小闭环**

   * 不用数值先：只做 Fact+Theorem 的纯逻辑证明
   * 从一个简单例子开始：

     * “已知 AB = AC, A,B,C 不共线，prove ∠ABC = ∠BCA”

5. **再加入 Solver & NumericModel，做数值剪枝增强**

   * 增强稳定性和效率
   * 对复杂场景减少搜索爆炸

6. **逐步扩充定理库 & Fact 类型**

   * 用 `data/theorems/` 做版本化管理
   * 可按 topic（triangle, circle, similarity, …）拆文件

7. **最后加入 UI 与可视化**

   * 渲染证明树
   * 高亮涉及的点、线、角
   * 支持中文叙述的展开/折叠

---

如果你之后想继续深入某一块（比如：

* 自动辅助线搜索的策略怎么跟 ProofEngine 集成，
* 或者把定理模式语法做成 “类 mini-DSL 的 BNF 规范”，

你可以直接点名“展开 XXX”，我就基于这份 all-in-one 导引继续往下细化。

