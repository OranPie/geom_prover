# Geometry Prover Examples

This directory contains comprehensive examples demonstrating the complete Week 1-6 pipeline of the geometry theorem prover.

## Overview

The examples show the complete workflow:
1. **DSL Parsing** (Week 1) - Parse geometry problems written in domain-specific language
2. **Semantic Extraction** (Week 2-3) - Extract geometric objects and facts
3. **Theorem Loading** (Week 4) - Load and prepare theorem library
4. **Proof Infrastructure** (Week 5) - Set up proof trees and search strategies
5. **Automated Reasoning** (Week 6) - Apply forward, backward, or bidirectional reasoning

## Examples

### Example 1: Simple Symmetry Proof
**File:** `example_01_simple_symmetry.py`

**Complexity:** Basic
**Concepts:** DSL parsing, semantic extraction, single theorem application

**Problem:**
```
Given: AB = CD
Prove: CD = AB
```

**Demonstrates:**
- Complete pipeline from DSL to proof
- Bidirectional reasoning
- Symmetry theorem application
- Statistics tracking

**Run:**
```bash
cd /Users/yanyige/workspace2
PYTHONPATH=/Users/yanyige/workspace2:$PYTHONPATH python3 examples/example_01_simple_symmetry.py
```

---

### Example 2: Transitivity Chain
**File:** `example_02_transitivity.py`

**Complexity:** Intermediate
**Concepts:** Multi-step proof, comparing reasoning strategies

**Problem:**
```
Given: AB = CD, CD = EF
Prove: AB = EF
```

**Demonstrates:**
- Transitivity theorem application
- Comparison of three reasoning approaches:
  - Forward reasoning
  - Backward reasoning
  - Bidirectional reasoning
- Performance metrics
- Strategy effectiveness comparison

**Run:**
```bash
cd /Users/yanyige/workspace2
PYTHONPATH=/Users/yanyige/workspace2:$PYTHONPATH python3 examples/example_02_transitivity.py
```

---

### Example 3: Isosceles Triangle
**File:** `example_03_isosceles_triangle.py`

**Complexity:** Advanced
**Concepts:** Complex geometric objects, exploratory reasoning

**Problem:**
```
Triangle ABC where AB = AC
Explore all derivable facts
```

**Demonstrates:**
- Working with triangles and complex objects
- Forward reasoning for exploration
- Automatic fact derivation
- Proof tree construction
- Theorem library integration

**Run:**
```bash
cd /Users/yanyige/workspace2
PYTHONPATH=/Users/yanyige/workspace2:$PYTHONPATH python3 examples/example_03_isosceles_triangle.py
```

---

### Example 4: Detailed Proof Steps
**File:** `example_04_detailed_proof.py`

**Complexity:** Educational
**Concepts:** Step-by-step proof visualization

**Problem:**
```
Given: AB = CD
Prove: CD = AB (with detailed steps)
```

**Demonstrates:**
- Detailed proof tree visualization
- Step-by-step theorem applications
- Variable binding display
- Human-readable proof generation
- Educational proof presentation

**Run:**
```bash
cd /Users/yanyige/workspace2
PYTHONPATH=/Users/yanyige/workspace2:$PYTHONPATH python3 examples/example_04_detailed_proof.py
```

---

---

## Week 7 Examples - Extended Validation

**Directory:** `week7_examples/`

Week 7 adds 8 additional examples (Examples 6-13) that thoroughly validate the reasoning engines across different theorem categories:

- **Equality Examples** (3): Multi-step segment/angle equality, mixed reasoning
- **Parallel Lines** (1): Parallel transitivity chains
- **Angle Properties** (2): Vertical angles, isosceles triangles
- **Advanced** (2): Combined multi-category reasoning, deep proof chains

See `week7_examples/README.md` for detailed documentation.

**Run Week 7 examples:**
```bash
cd /Users/yanyige/workspace2
./examples/week7_examples/run_all_week7_examples.sh
```

**Test Week 7 examples:**
```bash
cd /Users/yanyige/workspace2
PYTHONPATH=/Users/yanyige/workspace2:$PYTHONPATH python3 -m pytest examples/week7_examples/test_week7_examples.py -v
```

---

## Running All Examples

To run all main examples (1-5) sequentially:

```bash
cd /Users/yanyige/workspace2
for example in examples/example_*.py; do
    echo "========================================="
    echo "Running: $example"
    echo "========================================="
    PYTHONPATH=/Users/yanyige/workspace2:$PYTHONPATH python3 "$example"
    echo ""
    echo "Press Enter to continue..."
    read
done
```

Or run the provided script:
```bash
cd /Users/yanyige/workspace2
./examples/run_all_examples.sh
```

**Run ALL examples (main + Week 7):**
```bash
# Main examples (1-5)
./examples/run_all_examples.sh

# Week 7 examples (6-13)
./examples/week7_examples/run_all_week7_examples.sh
```

## Example Output Structure

Each example follows this structure:

1. **Problem Description** - DSL representation of the geometry problem
2. **Parsing** - Lexical analysis and AST construction
3. **Semantic Extraction** - Fact and object extraction
4. **Theorem Loading** - Loading relevant theorems
5. **Proof Execution** - Running the automated prover
6. **Results** - Success/failure, statistics, proof tree
7. **Analysis** - Performance metrics and insights

## Understanding the Output

### Success Indicators
- ✓ indicates successful operation
- ✗ indicates failure
- ⚠ indicates warning or fallback

### Key Metrics
- **Iterations**: Number of reasoning cycles
- **Forward/Backward steps**: Steps in each direction (bidirectional only)
- **Total facts**: Facts in final state
- **Derived facts**: Newly discovered facts
- **Theorem applications**: How many times theorems were applied
- **Time (ms)**: Execution time in milliseconds

### Theorem Usage
Shows which theorems were applied and how many times:
- `equality_symmetry`: X = Y → Y = X
- `equality_transitivity`: X = Y, Y = Z → X = Z
- `angle_equality_symmetry`: ∠ABC = ∠DEF → ∠DEF = ∠ABC
- etc.

## Educational Value

These examples are designed to:
1. **Teach** the complete pipeline from problem to proof
2. **Demonstrate** different reasoning strategies
3. **Compare** performance of different approaches
4. **Visualize** proof construction process
5. **Provide** templates for new problems

## Extending Examples

To create your own example:

1. Define a geometry problem in DSL
2. Parse using Lexer and Parser
3. Extract semantics using FactExtractor
4. Load theorems using TheoremEngine
5. Define goals
6. Run reasoner (Forward, Backward, or Bidirectional)
7. Analyze results

Example template:
```python
from geometry_prover.dsl.lexer import Lexer
from geometry_prover.dsl.parser import Parser
from geometry_prover.semantic.fact_extractor import FactExtractor
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.bidirectional_reasoner import BidirectionalReasoner

# Your DSL problem
problem = """
Point A, B, C
# Your constraints here
"""

# Parse and extract
ast = Parser(Lexer(problem).tokenize()).parse()
model = FactExtractor().extract_from_program(ast)
facts = model.constraints

# Define goals
goals = [...]  # Your goals here

# Load theorems and prove
engine = TheoremEngine()
engine.load_library("geometry_prover/data/theorems")

reasoner = BidirectionalReasoner(engine)
result = reasoner.prove(facts, goals, max_depth=20)

print(f"Success: {result.success}")
```

## Troubleshooting

### Theorem Library Not Found
If you see "⚠ Theorem library not found", ensure:
- You're running from the correct directory
- The path `geometry_prover/data/theorems/` exists
- Theorem files are present

### Import Errors
Ensure PYTHONPATH is set:
```bash
export PYTHONPATH=/Users/yanyige/workspace2:$PYTHONPATH
```

### Slow Performance
For large problems:
- Reduce `max_depth` parameter
- Reduce `max_iterations` parameter
- Use forward reasoning for exploration only
- Use backward reasoning for specific goals

## Further Reading

- See `tests/test_integration_week1_6.py` for more integration examples
- See `DETAILED_DEVELOPMENT_PLAN.md` for architecture details
- See individual module README files for component documentation
- See `docs/` directory for comprehensive documentation

## Contributing

To add new examples:
1. Create `example_XX_description.py`
2. Follow the existing format
3. Add entry to this README
4. Test with `pytest examples/`
5. Submit PR with clear description

---

**Note:** These examples demonstrate the production-ready Week 1-6 implementation of the geometry theorem prover with 557 passing tests and 84% code coverage.
