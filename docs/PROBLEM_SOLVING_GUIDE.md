# 如何用 Geometry Prover 求解一道几何题

下面用一套可直接运行的流程，演示如何把几何题描述成 DSL、解析成事实，再用定理库推理出结论。示例基于仓库自带的 SSS 三边相等三角形证明流程（`examples/week8_examples/complex_triangle_congruence.py`）。

## 1. 准备环境

```bash
pip install -e .
# 在项目根目录执行示例时，确保 Python 能找到本地包
export PYTHONPATH=.
```

## 2. 用 DSL 写出题目

```text
Point A, B, C, D, E, F
Triangle ABC
Triangle DEF
AB = DE
BC = EF
CA = FD
```

这段 DSL 表示两个三角形以及三对对应边相等，为后续 SSS 推导做准备。

## 3. 解析 DSL 并生成初始事实

```python
from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.parser import Parser
from geometry_prover.semantic.fact_extractor import FactExtractor
from geometry_prover.facts.fact_types import Triangle

problem = """
Point A, B, C, D, E, F
Triangle ABC
Triangle DEF
AB = DE
BC = EF
CA = FD
"""

# 1) 词法/语法解析
tokens = Lexer(problem).tokenize()
ast = Parser(tokens).parse()

# 2) 抽取几何模型
model = FactExtractor().extract_from_program(ast)

# 3) 准备推理用的事实（DSL 里的约束 + 显式三角形事实）
triangle_facts = [
    Triangle(model.points["A"], model.points["B"], model.points["C"]),
    Triangle(model.points["D"], model.points["E"], model.points["F"]),
]
initial_facts = model.constraints + triangle_facts
```

## 4. 加载定理库

```python
from pathlib import Path
from geometry_prover.theorems.engine import TheoremEngine

theorem_dir = Path("geometry_prover/data/theorems")
engine = TheoremEngine()
engine.load_library(str(theorem_dir))
```

## 5. 选择推理器并运行

这里使用正向推理（ForwardReasoner）。若需要目标驱动可以改用 BackwardReasoner，或者双向 BidirectionalReasoner。

```python
from geometry_prover.proof.forward_reasoner import ForwardReasoner

reasoner = ForwardReasoner(engine)
result = reasoner.reason(initial_facts, max_depth=10, max_facts=200)
```

## 6. 查看结论与推理轨迹

`ProofResult` 会记录推导出的事实、使用的定理次数等信息。可通过证明树筛选出想要的结论。

```python
from geometry_prover.facts.fact_types import CongruentTriangle, SimilarTriangle

# 汇总所有派生事实
all_nodes = result.proof_tree.get_all_nodes() if result.proof_tree else []
derived_facts = [fact for node in all_nodes for fact in node.facts]

congruent = [f for f in derived_facts if isinstance(f, CongruentTriangle)]
similar = [f for f in derived_facts if isinstance(f, SimilarTriangle)]

print("推理统计:", result.statistics)
print("是否得出全等:", bool(congruent))
print("是否得出相似:", bool(similar))
```

运行完整示例：

```bash
python examples/week8_examples/complex_triangle_congruence.py
```

你会在输出里看到 SSS 推出三角形全等，随后自动得到相似关系，并附带定理使用次数与派生事实数量。

## 7. 更多例子：事实展开演示

如果想直观看到“给定条件 → 自动派生事实”的过程，可以运行事实展开示例：

```bash
python examples/week8_examples/fact_expansion_walkthrough.py
```

这个例子只用一个等腰三角形的 DSL 描述（`AB = AC`），先打印初始约束，再展示推理后得到的所有事实，按类型分组，包括：

- `IsoscelesTriangle`（从两边相等推导出等腰三角形）
- `EqualAngle`（等腰三角形的底角相等）

你可以把 DSL 内容改成自己的题目，复用同样的流程快速查看系统能自动扩展出的事实。进一步组合定理库或提高 `max_depth`、`max_facts` 参数，就能探索更复杂的结论。
