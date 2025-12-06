# Geometry Theorem Proving System - Package Design Plan

## Document Overview

This document provides a comprehensive package design plan for implementing a geometry theorem proving system based on the specifications in INTRO.md and AUX.md. This is a **design-only document** - no implementation code, suitable for guiding multi-developer collaboration.

---

## Table of Contents

1. [System Architecture Overview](#1-system-architecture-overview)
2. [Package Structure](#2-package-structure)
3. [Core Module Designs](#3-core-module-designs)
4. [Data Models and Type System](#4-data-models-and-type-system)
5. [Module Interactions and Data Flow](#5-module-interactions-and-data-flow)
6. [Implementation Roadmap](#6-implementation-roadmap)
7. [Extensibility and Configuration](#7-extensibility-and-configuration)

---

## 1. System Architecture Overview

### 1.1 Three-Layer Architecture

The system is organized into three main layers:

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface Layer                 │
│              (CLI, Web UI, API Endpoints)               │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  DSL Parser  │→ │   Semantic   │→ │    Proof     │  │
│  │              │  │   Builder    │  │   Engine     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                           │                  │          │
│                           ▼                  ▼          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Numeric    │  │   Auxiliary  │  │   Theorem    │  │
│  │   Solver     │  │   Search     │  │    Base      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                      Data Layer                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│   │  Fact Base   │  │   Geometry   │  │  Proof Tree  │ │
│   │              │  │    Model     │  │              │ │
│   └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Key Design Principles

1. **Separation of Concerns**: Each layer has clear responsibilities
2. **Extensibility**: Theorems and auxiliary patterns are externally configurable
3. **Modularity**: Independent modules with well-defined interfaces
4. **Data-Driven**: Theorems and patterns defined in YAML/JSON, not hardcoded
5. **Hybrid Reasoning**: Combines symbolic logic with numeric validation

---

## 2. Package Structure

```
geometry_prover/
│
├── __init__.py
├── __version__.py
│
├── api/                          # Public API Layer
│   ├── __init__.py
│   ├── proof_api.py              # Main entry point for proving
│   ├── visualization_api.py       # API for rendering/visualization
│   └── config.py                  # Configuration management
│
├── dsl/                          # DSL Parsing Layer
│   ├── __init__.py
│   ├── lexer.py                  # Tokenization
│   ├── parser.py                 # Syntax analysis
│   ├── ast_nodes.py              # AST node definitions
│   └── grammar.py                # Grammar rules specification
│
├── semantic/                     # Semantic Analysis Layer
│   ├── __init__.py
│   ├── builder.py                # SemanticBuilder: AST → Model
│   ├── geometry_model.py         # GeometryModel class
│   ├── constraint_builder.py     # Build numeric constraints
│   └── prove_goal_extractor.py   # Extract prove goals from AST
│
├── facts/                        # Fact System Layer
│   ├── __init__.py
│   ├── fact_base.py              # FactBase container
│   ├── fact_types.py             # All 40 Fact type definitions
│   ├── fact_extractor.py         # Extract facts from GeometryModel
│   ├── fact_matcher.py           # Pattern matching for facts
│   └── fact_serializer.py        # Serialization utilities
│
├── theorems/                     # Theorem Management Layer
│   ├── __init__.py
│   ├── theorem_base.py           # TheoremBase class
│   ├── theorem_loader.py         # Load theorems from YAML/JSON
│   ├── theorem_matcher.py        # Match theorem patterns to facts
│   ├── theorem_applier.py        # Apply theorem to generate new facts
│   ├── pattern_parser.py         # Parse fact pattern strings
│   └── conditions_checker.py     # Check theorem conditions
│
├── proof/                        # Proof Engine Layer
│   ├── __init__.py
│   ├── engine.py                 # ProofEngine main class
│   ├── proof_state.py            # ProofState representation
│   ├── proof_tree.py             # ProofTree structure
│   ├── forward_reasoner.py       # Forward reasoning strategy
│   ├── backward_reasoner.py      # Backward reasoning strategy
│   ├── search_strategy.py        # Search strategies (BFS/DFS/Best-First)
│   └── proof_result.py           # ProofResult representation
│
├── auxiliary_search/             # Auxiliary Construction Search
│   ├── __init__.py
│   ├── aux_types.py              # AuxConstruction type definitions
│   ├── aux_patterns.py           # AuxPattern class
│   ├── pattern_loader.py         # Load patterns from YAML
│   ├── candidate_generator.py    # Generate AuxConstruction candidates
│   ├── evaluator.py              # Score and evaluate candidates
│   ├── strategy.py               # Search strategy for aux constructions
│   └── applier.py                # Apply constructions to model
│
├── solver/                       # Numeric Solver Layer
│   ├── __init__.py
│   ├── numeric_model.py          # NumericModel class
│   ├── constraint_solver.py      # Solve numeric constraints
│   ├── numeric_checker.py        # Numeric validation/pruning
│   └── geometry_calculator.py    # Geometric calculations
│
├── visualization/                # Visualization Layer
│   ├── __init__.py
│   ├── renderer.py               # Render geometry figures
│   ├── proof_formatter.py        # Format proof steps as text
│   ├── diagram_generator.py      # Generate diagrams
│   └── interactive_viewer.py     # Interactive proof viewer
│
├── utils/                        # Utilities
│   ├── __init__.py
│   ├── logging.py                # Logging utilities
│   ├── validation.py             # Input validation
│   ├── exceptions.py             # Custom exceptions
│   └── geometry_utils.py         # Geometric utility functions
│
├── data/                         # External Data Files
│   ├── theorems/                 # Theorem definitions
│   │   ├── triangles.yaml
│   │   ├── circles.yaml
│   │   ├── parallel.yaml
│   │   ├── similarity.yaml
│   │   └── ...
│   │
│   └── aux_patterns/             # Auxiliary construction patterns
│       ├── triangles.yaml
│       ├── circles.yaml
│       ├── parallels.yaml
│       └── ...
│
└── tests/                        # Test Suite
    ├── __init__.py
    ├── test_dsl/
    ├── test_facts/
    ├── test_theorems/
    ├── test_proof/
    ├── test_auxiliary/
    ├── test_solver/
    └── integration/
```

---

## 3. Core Module Designs

### 3.1 DSL Module (`dsl/`)

#### Purpose
Parse user-written geometry construction scripts into an Abstract Syntax Tree (AST).

#### Key Components

**3.1.1 Lexer (`lexer.py`)**
- Tokenize input DSL text
- Support keywords: `point`, `line`, `circle`, `on`, `parallel`, `perpendicular`, `prove`, etc.
- Handle identifiers, numbers, operators, and symbols

**3.1.2 Parser (`parser.py`)**
- Build AST from token stream
- Support grammar rules for:
  - Point declarations: `point A, B, C`
  - Line declarations: `line AB`
  - Constraints: `AB = AC`, `AB || CD`, `AB ⊥ CD`
  - Circle declarations: `circle O with radius r`
  - Prove statements: `prove angle(ABC) = angle(ACB)`

**3.1.3 AST Nodes (`ast_nodes.py`)**
- Define node types for all DSL constructs
- Base class: `ASTNode`
- Concrete types: `PointDecl`, `LineDecl`, `CircleDecl`, `ConstraintNode`, `ProveNode`, etc.

**3.1.4 Grammar (`grammar.py`)**
- Formal grammar specification (BNF-like)
- Can be extended without modifying parser core

#### Public Interface
```python
# Example API (conceptual)
Parser.parse(dsl_text: str) -> AST
```

---

### 3.2 Semantic Module (`semantic/`)

#### Purpose
Transform AST into a concrete GeometryModel with geometric objects and constraints.

#### Key Components

**3.2.1 SemanticBuilder (`builder.py`)**
- Main class orchestrating semantic analysis
- Traverse AST and build:
  - `GeometryModel`: Contains all geometric objects
  - Numeric constraints: For solver
  - Prove goals: What needs to be proven

**3.2.2 GeometryModel (`geometry_model.py`)**
- Stores geometric objects:
  - Points: name, symbolic representation
  - Lines: defined by two points or equation
  - Circles: center + radius
  - Angles: three points
  - Segments: two points
- Stores relationships:
  - `on` relations: point on line/circle
  - Parallel/perpendicular relations
  - Equal length/angle relations

**3.2.3 ConstraintBuilder (`constraint_builder.py`)**
- Convert symbolic constraints to numeric constraint expressions
- Generate constraint system for numeric solver
- Handle:
  - Distance constraints: `|AB| = |CD|`
  - Angle constraints: `∠ABC = 90°`
  - Positional constraints: `P on line(AB)`

**3.2.4 ProveGoalExtractor (`prove_goal_extractor.py`)**
- Extract prove statements from AST
- Convert to target Fact representations
- Support multiple prove goals per script

#### Public Interface
```python
# Conceptual API
SemanticBuilder.build(ast: AST) -> (GeometryModel, Constraints, ProveGoals)
```

---

### 3.3 Facts Module (`facts/`)

#### Purpose
Implement the Fact type system - the "logical atoms" of geometric knowledge.

#### Key Components

**3.3.1 Fact Types (`fact_types.py`)**
- Define all 40 Fact types from the specification
- Organized into categories:
  - Structural: `On`, `OnSegment`, `OnCircle`, `Collinear`, `Between`, `Midpoint`, etc.
  - Length/Ratio: `EqualSegment`, `ProportionalSegment`, `LengthValue`, etc.
  - Angle: `EqualAngle`, `RightAngle`, `SupplementaryAngle`, `AngleValue`, etc.
  - Line Relations: `Parallel`, `Perpendicular`, `SameLine`
  - Triangle/Polygon: `Triangle`, `IsoscelesTriangle`, `SimilarTriangle`, `CongruentTriangle`, etc.
  - Circle: `TangentAt`, `Chord`, `Diameter`, `CyclicQuadrilateral`, etc.
  - Area: `AreaValue`, `AreaRelation`
  - Logic: `Distinct`, `NonDegenerateTriangle`, `Orientation`

**Base Fact Class Structure:**
```python
# Conceptual
class Fact:
    fact_type: str
    parameters: dict

    def matches(pattern: FactPattern) -> bool
    def to_string() -> str
    def __hash__() / __eq__()  # For deduplication
```

**3.3.2 FactBase (`fact_base.py`)**
- Container for all known facts
- Operations:
  - Add fact (with deduplication)
  - Query by type
  - Query by involved points/objects
  - Pattern matching
- Indexing for efficient lookup
- Support incremental updates

**3.3.3 FactExtractor (`fact_extractor.py`)**
- Extract initial facts from GeometryModel
- Generate basic facts from:
  - Point declarations
  - `on` relationships
  - Explicit constraints (parallel, perpendicular, equal)
  - Triangle/circle definitions

**3.3.4 FactMatcher (`fact_matcher.py`)**
- Match fact patterns (from theorems) against concrete facts
- Perform variable binding
- Handle wildcards and parameterized patterns
- Unification algorithm

**3.3.5 FactSerializer (`fact_serializer.py`)**
- Serialize/deserialize facts for storage or transmission
- Support JSON and internal representations

#### Public Interface
```python
# Conceptual API
FactBase.add(fact: Fact)
FactBase.query(fact_type: str, **filters) -> list[Fact]
FactBase.match_pattern(pattern: FactPattern) -> list[Binding]
```

---

### 3.4 Theorems Module (`theorems/`)

#### Purpose
Manage theorem library, load from external files, and match/apply theorems.

#### Key Components

**3.4.1 TheoremBase (`theorem_base.py`)**
- Container for all loaded theorems
- Operations:
  - Load theorems from YAML files
  - Query by category/tag
  - Find theorems by conclusion pattern
  - Find theorems by premise pattern
- Indexing by categories and patterns

**3.4.2 TheoremLoader (`theorem_loader.py`)**
- Load theorems from YAML/JSON files
- Parse theorem definitions:
  - `id`, `version`, `name`, `category`, `tags`
  - `premises`: list of FactPattern strings
  - `conclusions`: list of FactPattern strings
  - `conditions`: additional logic conditions
  - `priority`, `max_uses`
  - `nl_templates`: natural language templates
  - `enabled`: whether theorem is active
- Validate theorem structure
- Support hot-reloading for development

**Theorem Data Structure:**
```python
# Conceptual
class Theorem:
    id: str
    version: str
    name: str
    category: str
    tags: list[str]
    premises: list[FactPattern]
    conclusions: list[FactPattern]
    conditions: list[Condition]
    priority: int
    max_uses: int
    nl_templates: dict[str, str]  # 'cn', 'en'
    enabled: bool
```

**3.4.3 PatternParser (`pattern_parser.py`)**
- Parse fact pattern strings from theorem files
- Syntax:
  - `EqualSegment({A}{B}, {C}{D})`
  - `On({P}, Line({A}{B}))`
  - `Angle({A}{B}{C})`
  - Support for constants: `AngleValue(Angle({A}{B}{C}), 90deg)`
- Build FactPattern objects with placeholders

**3.4.4 TheoremMatcher (`theorem_matcher.py`)**
- Match theorem premises against FactBase
- Perform variable binding and unification
- Find all valid theorem applications
- Rank candidates by:
  - Priority
  - Number of matched premises
  - Relevance to goal

**3.4.5 TheoremApplier (`theorem_applier.py`)**
- Apply matched theorem to generate new conclusions
- Substitute bound variables into conclusion patterns
- Generate new Fact instances
- Update ProofTree with application record

**3.4.6 ConditionsChecker (`conditions_checker.py`)**
- Check additional conditions (non-Fact constraints)
- Handle:
  - `Distinct({A}, {B})`: check points are different
  - `NotCollinear({A}, {B}, {C})`: check non-collinearity
  - Can use numeric model for validation
  - Can check against existing facts

#### Public Interface
```python
# Conceptual API
TheoremBase.load_from_directory(path: str)
TheoremBase.find_by_conclusion(pattern: FactPattern) -> list[Theorem]
TheoremMatcher.match(theorem: Theorem, fact_base: FactBase) -> list[Binding]
TheoremApplier.apply(theorem: Theorem, binding: Binding) -> list[Fact]
```

---

### 3.5 Proof Module (`proof/`)

#### Purpose
Core reasoning engine that searches for proofs using theorems.

#### Key Components

**3.5.1 ProofEngine (`engine.py`)**
- Main orchestrator for proof search
- Implements hybrid reasoning:
  - Backward reasoning: goal-driven
  - Forward reasoning: fact-driven
  - Numeric validation: prune invalid paths
- Algorithm outline:
  ```
  1. Initialize ProofState with initial facts and goals
  2. While goals remain and not timeout/depth limit:
     a. Select a goal (prioritized)
     b. Use BackwardReasoner to find applicable theorems
     c. For each candidate theorem:
        - Check conditions
        - Apply theorem
        - Generate sub-goals (if any)
        - Use ForwardReasoner to expand facts
        - Check if goal is satisfied
     d. Update ProofState and ProofTree
     e. If stuck, trigger AuxiliarySearch
  3. Return ProofResult (success/partial/failed)
  ```

**3.5.2 ProofState (`proof_state.py`)**
- Represents current state during proof search
- Contains:
  - `fact_base`: current FactBase
  - `goals`: list of remaining goals (Fact to prove)
  - `proof_tree`: record of reasoning steps
  - `depth`: current search depth
  - `theorem_usage`: track theorem application counts
- Support state cloning for backtracking

**3.5.3 ProofTree (`proof_tree.py`)**
- Tree structure recording the proof
- Nodes represent:
  - Theorem applications
  - Fact derivations
  - Auxiliary constructions
- Edges represent dependencies
- Can be serialized for visualization

**3.5.4 ForwardReasoner (`forward_reasoner.py`)**
- Forward chaining: derive new facts from existing facts
- Algorithm:
  ```
  1. For each theorem in TheoremBase:
     2. Try to match all premises against current FactBase
     3. If all premises match and conditions hold:
        4. Apply theorem to generate conclusions
        5. Add new facts to FactBase
     6. Limit depth to prevent explosion
  ```
- Can be triggered after each new fact addition
- Uses priority to control exploration

**3.5.5 BackwardReasoner (`backward_reasoner.py`)**
- Backward chaining: work from goal to premises
- Algorithm:
  ```
  1. Given a goal Fact G:
     2. Find all theorems whose conclusions can unify with G
     3. For each theorem T:
        4. Bind variables from conclusion to goal
        5. Generate sub-goals from premises (with bindings)
        6. Return (T, sub-goals) as candidates
  ```
- Returns candidates ranked by priority

**3.5.6 SearchStrategy (`search_strategy.py`)**
- Define search strategies:
  - **Depth-First Search (DFS)**: deep exploration
  - **Breadth-First Search (BFS)**: level-by-level
  - **Best-First Search**: prioritize by heuristic
  - **Iterative Deepening**: gradually increase depth
- Configurable timeout and depth limits
- Support for backtracking

**3.5.7 ProofResult (`proof_result.py`)**
- Encapsulates proof result
- Contains:
  - `success`: bool
  - `proof_tree`: ProofTree (if successful)
  - `proven_goals`: list of successfully proven goals
  - `failed_goals`: list of unproven goals
  - `description`: natural language proof steps
  - `statistics`: search stats (nodes explored, time, etc.)

#### Public Interface
```python
# Conceptual API
ProofEngine(theorem_base, numeric_model).prove(
    initial_facts: FactBase,
    goals: list[Fact],
    strategy: SearchStrategy
) -> ProofResult
```

---

### 3.6 Auxiliary Search Module (`auxiliary_search/`)

#### Purpose
Automatically propose auxiliary constructions (lines, midpoints, perpendiculars, etc.) when proof gets stuck.

#### Key Components

**3.6.1 AuxTypes (`aux_types.py`)**
- Define auxiliary construction types:
  - `Midpoint`: midpoint of a segment
  - `Perpendicular`: perpendicular from point to line
  - `Parallel`: parallel line through point
  - `AngleBisector`: angle bisector
  - `Reflect`: reflected point across line
  - `Connect`: connect two points
  - `Circumcircle`: circumcircle of triangle
  - `Incircle`: incircle of triangle
  - etc.

**AuxConstruction Structure:**
```python
# Conceptual
class AuxConstruction:
    aux_type: str  # e.g., 'midpoint', 'perpendicular'
    anchors: dict  # Existing points/lines it depends on
    new_objects: list  # New points/lines to be created
    predicted_facts: list[Fact]  # Expected new facts
    score: float  # Evaluation score
    cost: float  # Search cost
```

**3.6.2 AuxPatterns (`aux_patterns.py`)**
- Define auxiliary construction patterns
- Similar to theorems but for constructions

**AuxPattern Structure:**
```python
# Conceptual
class AuxPattern:
    id: str
    name: str
    preconditions: list[FactPattern]  # When to apply
    constructions: list[AuxConstruction]  # What to construct
    expected_facts: list[FactPattern]  # What facts will be generated
    tags: list[str]  # e.g., ['triangle', 'similarity']
    priority: int
```

**3.6.3 PatternLoader (`pattern_loader.py`)**
- Load auxiliary patterns from YAML files
- Similar structure to theorem files
- Example pattern:
  ```yaml
  - id: TRIANGLE_MIDSEGMENT
    name: 三角形中位线
    preconditions:
      - Triangle({A}, {B}, {C})
    constructions:
      - type: Midpoint
        params: {M: midpoint of {A}{B}}
      - type: Midpoint
        params: {N: midpoint of {A}{C}}
      - type: Connect
        params: {line: {M}{N}}
    expected_facts:
      - Parallel(Line({M}{N}), Line({B}{C}))
      - EqualRatio(Segment({M}{N}), Segment({B}{C}), 0.5)
    tags: [triangle, parallel, midline]
    priority: 5
  ```

**3.6.4 CandidateGenerator (`candidate_generator.py`)**
- Generate auxiliary construction candidates
- Algorithm:
  ```
  1. Analyze current FactBase for geometric structures
     (triangles, parallel lines, circles, etc.)
  2. For each structure, match against AuxPatterns
  3. For matched patterns:
     a. Bind pattern variables to actual objects
     b. Instantiate AuxConstruction
     c. Filter duplicates (already exist)
  4. Return list of candidates
  ```
- Pattern-driven: use AuxPatterns
- Goal-driven: consider what goal needs
- Theorem-driven: consider missing theorem premises

**3.6.5 Evaluator (`evaluator.py`)**
- Score auxiliary construction candidates
- Scoring factors:
  1. **Goal Relevance**: Does it involve points/lines in the goal?
  2. **Theorem Unlocking**: How many theorems become applicable?
  3. **Numeric Reasonableness**: Does numeric model support it?
  4. **Cost**: How complex is the construction?
- Formula: `score = w1*relevance + w2*theorem_unlock + w3*numeric_fit - w4*cost`
- Uses NumericModel for validation

**3.6.6 Strategy (`strategy.py`)**
- Define auxiliary construction search strategy
- When to trigger:
  - After N failed proof attempts
  - When goal is not progressing
  - At specific depth in proof tree
- How to search:
  - **Iterative Deepening**: Try 1 construction, then 2, etc.
  - **Best-First**: Always pick highest scored candidate
  - **Backtracking**: Undo unsuccessful constructions
- Limits:
  - Max constructions per proof
  - Max candidates to try
  - Timeout

**3.6.7 Applier (`applier.py`)**
- Apply selected auxiliary construction to the system
- Operations:
  1. Create new geometric objects (points, lines)
  2. Update GeometryModel
  3. Generate new Facts
  4. Add to FactBase
  5. Record in ProofTree as a construction step
  6. Update NumericModel if needed
- Ensure construction is geometrically valid

#### Integration with Proof Engine
- ProofEngine calls AuxiliarySearch when stuck
- AuxiliarySearch returns top-K constructions
- ProofEngine tries each construction and continues reasoning
- If successful, construction is kept; otherwise backtrack

#### Public Interface
```python
# Conceptual API
AuxiliarySearch(aux_patterns, evaluator).search(
    proof_state: ProofState,
    goal: Fact,
    numeric_model: NumericModel
) -> list[AuxConstruction]

Applier.apply(
    aux_construction: AuxConstruction,
    geometry_model: GeometryModel,
    fact_base: FactBase
) -> (updated_model, updated_facts)
```

---

### 3.7 Solver Module (`solver/`)

#### Purpose
Provide numeric validation and constraint solving to guide and prune proof search.

#### Key Components

**3.7.1 NumericModel (`numeric_model.py`)**
- Stores numeric coordinates for all geometric objects
- Obtained by solving constraints from GeometryModel
- Provides:
  - Point coordinates: `(x, y)` for each point
  - Line equations
  - Distances, angles, areas
- Used for:
  - Checking fact validity numerically
  - Pruning impossible theorem applications
  - Evaluating auxiliary constructions

**3.7.2 ConstraintSolver (`constraint_solver.py`)**
- Solve geometric constraint systems
- Input: Constraints from ConstraintBuilder
- Output: NumericModel (point coordinates)
- Approaches:
  - **Algebraic solver**: closed-form solutions
  - **Numerical optimization**: gradient descent, Newton's method
  - **Constraint satisfaction**: backtracking, local search
- Handle:
  - Over-constrained systems (inconsistent)
  - Under-constrained systems (multiple solutions)
- May fail for complex/degenerate cases

**3.7.3 NumericChecker (`numeric_checker.py`)**
- Validate facts and theorem applications numerically
- Used in two places:
  1. **After theorem matching**: Check if premises are numerically consistent
     - E.g., claimed parallel but angle > 10°
  2. **Before adding new facts**: Check if new fact is consistent with numeric model
     - E.g., claimed equal segments but lengths differ significantly
- Tolerance-based checking
- Returns: `valid`, `invalid`, or `uncertain` (if numeric model unavailable)

**3.7.4 GeometryCalculator (`geometry_calculator.py`)**
- Utility functions for geometric calculations:
  - Distance between points
  - Angle between lines
  - Area of triangle/polygon
  - Intersection of lines/circles
  - Perpendicular distance
  - Parallel/perpendicular checks
- Used by NumericChecker and Evaluator

#### Public Interface
```python
# Conceptual API
ConstraintSolver.solve(constraints: Constraints) -> NumericModel
NumericChecker.check_fact(fact: Fact, model: NumericModel) -> bool
NumericChecker.check_conditions(conditions, binding, model) -> bool
```

---

### 3.8 Visualization Module (`visualization/`)

#### Purpose
Render proofs, diagrams, and interactive visualizations.

#### Key Components

**3.8.1 Renderer (`renderer.py`)**
- Render geometric figures
- Support multiple backends:
  - Matplotlib (static images)
  - SVG (web-compatible)
  - Interactive canvas (for UI)
- Highlight specific objects/relations
- Animate proof steps

**3.8.2 ProofFormatter (`proof_formatter.py`)**
- Format proof steps as readable text
- Use natural language templates from theorems
- Support multiple languages (CN, EN)
- Generate step-by-step explanations:
  ```
  Step 1: 已知 AB = AC (given)
  Step 2: 三角形 ABC 为等腰三角形 (by definition)
  Step 3: 因此 ∠ABC = ∠ACB (等腰三角形底角相等)
  ```

**3.8.3 DiagramGenerator (`diagram_generator.py`)**
- Automatically generate diagrams from GeometryModel
- Layout algorithm for point placement
- Use NumericModel for coordinates
- Annotate with labels, measurements

**3.8.4 InteractiveViewer (`interactive_viewer.py`)**
- Interactive proof exploration
- Features:
  - Step through proof tree
  - Highlight corresponding diagram elements
  - Show/hide intermediate steps
  - Filter by theorem category

---

### 3.9 API Module (`api/`)

#### Purpose
Provide clean public interface for external use.

#### Key Components

**3.9.1 ProofAPI (`proof_api.py`)**
- Main entry point for proving
- High-level functions:
  ```python
  # Conceptual
  def prove_from_dsl(dsl_text: str, config: Config) -> ProofResult
  def prove_from_model(model: GeometryModel, goals, config) -> ProofResult
  def verify_proof(proof: ProofResult) -> bool
  ```
- Handle full pipeline: DSL → Parse → Semantic → Prove → Format

**3.9.2 VisualizationAPI (`visualization_api.py`)**
- API for rendering and visualization
- Functions:
  ```python
  # Conceptual
  def render_diagram(model: GeometryModel, format='png') -> bytes
  def render_proof(proof_result: ProofResult, lang='cn') -> str
  def generate_interactive_view(proof_result: ProofResult) -> HTML
  ```

**3.9.3 Config (`config.py`)**
- Configuration management
- Settings:
  - Theorem library path
  - Auxiliary pattern library path
  - Search strategy and limits
  - Timeout settings
  - Numeric solver options
  - Visualization preferences
  - Language preference

---

### 3.10 Utils Module (`utils/`)

#### Purpose
Common utilities used across modules.

#### Key Components

**3.10.1 Logging (`logging.py`)**
- Structured logging
- Log levels: DEBUG, INFO, WARN, ERROR
- Log proof search progress, theorem applications, etc.

**3.10.2 Validation (`validation.py`)**
- Input validation utilities
- Validate DSL syntax
- Validate theorem file format
- Validate configuration

**3.10.3 Exceptions (`exceptions.py`)**
- Define custom exceptions:
  - `DSLParseError`
  - `SemanticError`
  - `TheoremNotFoundError`
  - `ProofTimeoutError`
  - `NumericSolverError`
  - etc.

**3.10.4 GeometryUtils (`geometry_utils.py`)**
- Utility functions for geometry
- Point, line, circle operations
- Transformations (rotation, reflection)

---

## 4. Data Models and Type System

### 4.1 Core Data Types

#### 4.1.1 Geometric Objects

**Point**
- `name`: string identifier
- `coords`: optional (x, y) from numeric model
- `dependencies`: how it was constructed

**Line**
- `id`: unique identifier
- `points`: two defining points OR
- `equation`: ax + by + c = 0
- `type`: 'line' | 'segment' | 'ray'

**Circle**
- `center`: Point
- `radius`: float or symbolic expression
- `id`: unique identifier

**Angle**
- `vertex`: Point (middle point)
- `point1`, `point2`: two other points
- Represents ∠(point1, vertex, point2)

**Segment**
- `point1`, `point2`: endpoints
- Equivalent to Line with type='segment'

#### 4.1.2 Fact Type Hierarchy

All Fact types inherit from base `Fact` class:

```
Fact (base)
├── StructuralFact
│   ├── On
│   ├── OnSegment
│   ├── OnCircle
│   ├── Collinear
│   ├── NotCollinear
│   ├── Between
│   ├── Midpoint
│   ├── FootOfPerpendicular
│   ├── ReflectPoint
│   └── Intersect
├── LengthFact
│   ├── EqualSegment
│   ├── ProportionalSegment
│   ├── SegmentRatio
│   └── LengthValue
├── AngleFact
│   ├── EqualAngle
│   ├── RightAngle
│   ├── SupplementaryAngle
│   ├── AngleSum
│   └── AngleValue
├── LineRelationFact
│   ├── Parallel
│   ├── Perpendicular
│   └── SameLine
├── ShapeFact
│   ├── Triangle
│   ├── IsoscelesTriangle
│   ├── EquilateralTriangle
│   ├── SimilarTriangle
│   ├── CongruentTriangle
│   └── AreaValue
├── CircleFact
│   ├── TangentAt
│   ├── Chord
│   ├── Diameter
│   ├── Arc
│   └── CyclicQuadrilateral
├── AreaFact
│   ├── AreaRelation
│   ├── AreaSum
│   └── NumericConstraint
└── LogicFact
    ├── Distinct
    ├── NonDegenerateTriangle
    └── Orientation
```

Each Fact type has:
- Type identifier
- Parameters (points, lines, values)
- Hash and equality methods
- String representation
- Pattern matching capability

### 4.2 Theorem Data Model

```python
# Conceptual structure
Theorem {
    id: str
    version: str
    name: str
    category: str
    tags: list[str]
    premises: list[FactPattern]
    conclusions: list[FactPattern]
    conditions: list[Condition]
    priority: int
    max_uses: int
    nl_templates: {
        'cn': str,
        'en': str
    }
    notes: str
    enabled: bool
}
```

**FactPattern**: A Fact with placeholders
- Example: `EqualSegment({A}{B}, {C}{D})`
- Placeholders: `{A}`, `{B}`, `{C}`, `{D}`
- Can match multiple concrete facts

**Condition**: Additional constraint
- Example: `Distinct({A}, {B})`
- Checked during theorem application

### 4.3 Auxiliary Construction Data Model

```python
# Conceptual structure
AuxConstruction {
    aux_type: str  # 'midpoint', 'perpendicular', etc.
    anchors: dict  # Existing objects
    new_objects: list  # What will be created
    predicted_facts: list[Fact]
    score: float
    cost: float
}

AuxPattern {
    id: str
    name: str
    preconditions: list[FactPattern]
    constructions: list[AuxConstruction]
    expected_facts: list[FactPattern]
    tags: list[str]
    priority: int
}
```

### 4.4 Proof Data Model

```python
# Conceptual structure
ProofTree {
    root: ProofNode
    nodes: list[ProofNode]
    edges: list[ProofEdge]
}

ProofNode {
    type: 'theorem_application' | 'aux_construction' | 'initial_fact'
    facts: list[Fact]  # Facts at this node
    theorem: Theorem (if type='theorem_application')
    aux: AuxConstruction (if type='aux_construction')
    children: list[ProofNode]
}

ProofResult {
    success: bool
    proof_tree: ProofTree
    proven_goals: list[Fact]
    failed_goals: list[Fact]
    description: str  # Natural language
    statistics: dict
}
```

---

## 5. Module Interactions and Data Flow

### 5.1 Complete Data Flow (DSL to Proof)

```
┌──────────────┐
│  User Input  │
│  (DSL Text)  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  DSL Parser  │  ──→ AST
└──────┬───────┘
       │
       ▼
┌─────────────────┐
│ SemanticBuilder │  ──→ GeometryModel + Constraints + ProveGoals
└──────┬──────────┘
       │
       ├─────────────────────────────┐
       │                             │
       ▼                             ▼
┌──────────────┐            ┌────────────────┐
│FactExtractor │            │ ConstraintSolver│
└──────┬───────┘            └───────┬─────────┘
       │                            │
       │ initial Facts              │ NumericModel
       │                            │
       └──────────┬─────────────────┘
                  │
                  ▼
          ┌───────────────┐
          │  ProofEngine  │
          └───────┬───────┘
                  │
      ┌───────────┼───────────┐
      │           │           │
      ▼           ▼           ▼
┌──────────┐ ┌─────────┐ ┌─────────────────┐
│Backward  │ │Forward  │ │AuxiliarySearch  │
│Reasoner  │ │Reasoner │ │(when stuck)     │
└────┬─────┘ └────┬────┘ └────────┬────────┘
     │            │               │
     └────────────┼───────────────┘
                  │
            uses TheoremBase
            uses NumericChecker
                  │
                  ▼
          ┌───────────────┐
          │  ProofResult  │
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │ ProofFormatter│  ──→ Natural Language Description
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │  Renderer     │  ──→ Visual Diagram
          └───────────────┘
```

### 5.2 Key Interaction Patterns

#### 5.2.1 Theorem Matching Flow
```
FactBase + Goal
    │
    ▼
BackwardReasoner
    │ query theorems by conclusion
    ▼
TheoremBase
    │ return candidate theorems
    ▼
TheoremMatcher
    │ match premises to facts
    ▼
ConditionsChecker
    │ check extra conditions
    ▼
NumericChecker (optional)
    │ validate numerically
    ▼
Return: list of (Theorem, Binding, SubGoals)
```

#### 5.2.2 Auxiliary Construction Flow
```
ProofEngine (stuck)
    │
    ▼
AuxiliarySearch.strategy
    │ trigger auxiliary search
    ▼
CandidateGenerator
    │ generate candidates
    ▼
Evaluator
    │ score candidates
    ▼
Select top-K candidates
    │
    ▼
For each candidate:
    │
    ▼
Applier.apply(aux_construction)
    │ update GeometryModel
    │ update FactBase
    ▼
ProofEngine.continue_search()
    │
    ▼
Success? ──yes──→ Keep construction
    │
    no
    │
    ▼
Backtrack, try next candidate
```

#### 5.2.3 Numeric Validation Flow
```
Constraints from DSL
    │
    ▼
ConstraintSolver.solve()
    │
    ▼
NumericModel (coordinates)
    │
    └──→ Used by:
         │
         ├─→ NumericChecker (validate facts)
         │
         ├─→ Evaluator (score aux constructions)
         │
         └─→ Renderer (draw diagram)
```

---

## 6. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-3)
**Goal**: Build core data structures and basic parsing

1. **Week 1: Data Models**
   - Implement Fact type hierarchy (all 40 types)
   - Implement FactBase with basic operations
   - Implement geometric object classes (Point, Line, Circle, etc.)
   - Unit tests for data models

2. **Week 2: DSL Parsing**
   - Implement Lexer
   - Implement Parser
   - Define AST node types
   - Support basic geometry constructions
   - Unit tests for parser

3. **Week 3: Semantic Building**
   - Implement SemanticBuilder
   - Implement GeometryModel
   - Implement FactExtractor
   - Integration tests: DSL → GeometryModel → Facts

**Milestone 1**: Can parse DSL and extract basic facts

---

### Phase 2: Theorem System (Weeks 4-6)
**Goal**: Load and apply theorems

4. **Week 4: Theorem Infrastructure**
   - Design theorem YAML format
   - Implement TheoremLoader
   - Implement PatternParser
   - Implement TheoremBase
   - Write 5-10 basic theorems (triangles, parallel lines)

5. **Week 5: Pattern Matching**
   - Implement FactMatcher (pattern matching & unification)
   - Implement TheoremMatcher
   - Implement ConditionsChecker
   - Unit tests for matching

6. **Week 6: Theorem Application**
   - Implement TheoremApplier
   - Test theorem application on simple cases
   - Expand theorem library to 20-30 theorems

**Milestone 2**: Can match and apply theorems to generate new facts

---

### Phase 3: Proof Engine (Weeks 7-10)
**Goal**: Implement core reasoning

7. **Week 7: Proof State & Tree**
   - Implement ProofState
   - Implement ProofTree
   - Implement ProofResult

8. **Week 8: Forward Reasoning**
   - Implement ForwardReasoner
   - Test forward chaining
   - Control explosion with depth limits

9. **Week 9: Backward Reasoning**
   - Implement BackwardReasoner
   - Implement goal-driven search
   - Test on simple proofs

10. **Week 10: Proof Engine Integration**
    - Implement ProofEngine main loop
    - Implement SearchStrategy (BFS, DFS, Best-First)
    - Integration tests: complete simple proofs
    - Example: "Prove isosceles triangle has equal base angles"

**Milestone 3**: Can prove simple theorems without auxiliary lines

---

### Phase 4: Numeric Solver (Weeks 11-12)
**Goal**: Add numeric validation and pruning

11. **Week 11: Constraint Solving**
    - Implement ConstraintBuilder
    - Implement ConstraintSolver (basic algebraic solver)
    - Implement NumericModel
    - Test on simple configurations

12. **Week 12: Numeric Checking**
    - Implement NumericChecker
    - Integrate with ProofEngine for pruning
    - Implement GeometryCalculator utilities
    - Test improved efficiency

**Milestone 4**: Proof search enhanced with numeric validation

---

### Phase 5: Auxiliary Construction Search (Weeks 13-15)
**Goal**: Automatic auxiliary line generation

13. **Week 13: Auxiliary Infrastructure**
    - Design AuxPattern YAML format
    - Implement AuxTypes
    - Implement AuxPatterns
    - Implement PatternLoader
    - Write 10-15 common patterns (midpoint, perpendicular, etc.)

14. **Week 14: Candidate Generation & Evaluation**
    - Implement CandidateGenerator
    - Implement Evaluator (scoring)
    - Test candidate generation

15. **Week 15: Integration with Proof Engine**
    - Implement Strategy (when to trigger)
    - Implement Applier
    - Integrate with ProofEngine
    - Test on problems requiring auxiliary lines

**Milestone 5**: Can automatically find auxiliary constructions

---

### Phase 6: Visualization & Polish (Weeks 16-18)
**Goal**: User-facing features

16. **Week 16: Proof Formatting**
    - Implement ProofFormatter
    - Use nl_templates for descriptions
    - Generate step-by-step proofs in CN/EN

17. **Week 17: Visualization**
    - Implement Renderer (Matplotlib backend)
    - Implement DiagramGenerator
    - Render proofs with highlighted steps

18. **Week 18: API & Documentation**
    - Implement ProofAPI and VisualizationAPI
    - Write user documentation
    - Write developer documentation
    - Create example notebooks/scripts

**Milestone 6**: Complete system with visualization

---

### Phase 7: Testing & Optimization (Weeks 19-20)
**Goal**: Robustness and performance

19. **Week 19: Comprehensive Testing**
    - Integration tests for full pipeline
    - Test on 50+ geometry problems
    - Edge case testing (degenerate cases, impossible proofs)
    - Stress testing (complex proofs)

20. **Week 20: Optimization**
    - Profile performance bottlenecks
    - Optimize FactBase indexing
    - Optimize theorem matching
    - Optimize search strategies
    - Add caching where appropriate

**Milestone 7**: Production-ready system

---

### Phase 8: Advanced Features (Weeks 21+)
**Optional enhancements**

- Interactive web UI
- More sophisticated numeric solver (handle algebraic constraints)
- Support for 3D geometry
- Competition-level theorem library
- Export to formal proof systems (Coq, Lean)
- Multi-language support (more than CN/EN)

---

## 7. Extensibility and Configuration

### 7.1 Theorem Extensibility

**Adding New Theorems**:
1. No code changes required
2. Create new YAML file in `data/theorems/`
3. Follow theorem format specification
4. System auto-loads on startup or hot-reload

**Theorem File Example**:
```yaml
- id: ANGLE_BISECTOR_THEOREM
  version: "1.0"
  name: 角平分线定理
  category: triangle
  tags: [angle_bisector, ratio]
  premises:
    - Triangle({A}, {B}, {C})
    - AngleBisector({D}, {A}, {B}, {C})
    - On({D}, Line({B}{C}))
  conclusions:
    - SegmentRatio({B}{D}, {D}{C}, {A}{B}, {A}{C})
  conditions:
    - Distinct({B}, {D})
    - Distinct({D}, {C})
  priority: 6
  max_uses: 2
  nl_templates:
    cn: "根据角平分线定理,{A}{D}平分∠{B}{A}{C},因此{B}{D}/{D}{C}={A}{B}/{A}{C}。"
    en: "By angle bisector theorem, {A}{D} bisects ∠{B}{A}{C}, so {B}{D}/{D}{C}={A}{B}/{A}{C}."
  enabled: true
```

### 7.2 Auxiliary Pattern Extensibility

**Adding New Auxiliary Patterns**:
1. Create YAML file in `data/aux_patterns/`
2. Define preconditions, constructions, expected facts
3. System auto-loads

**Pattern File Example**:
```yaml
- id: ALTITUDE_CONSTRUCTION
  name: 作高线
  preconditions:
    - Triangle({A}, {B}, {C})
  constructions:
    - type: Perpendicular
      from_point: {A}
      to_line: Line({B}{C})
      foot_point: {H}
  expected_facts:
    - Perpendicular(Line({A}{H}), Line({B}{C}))
    - On({H}, Line({B}{C}))
  tags: [triangle, altitude, perpendicular]
  priority: 5
  notes: "高线是三角形的重要辅助线"
```

### 7.3 Fact Type Extensibility

**Adding New Fact Types**:
1. Define new class in `facts/fact_types.py`
2. Inherit from base `Fact` class
3. Implement required methods:
   - `__init__`
   - `matches(pattern)`
   - `to_string()`
   - `__hash__`, `__eq__`
4. Register in Fact type registry
5. Update pattern parser if needed

### 7.4 Configuration System

**Config File** (`config.yaml`):
```yaml
# Paths
theorem_library: "data/theorems/"
aux_pattern_library: "data/aux_patterns/"

# Proof Engine Settings
proof:
  strategy: "best_first"  # bfs, dfs, best_first, iterative_deepening
  max_depth: 50
  timeout_seconds: 60
  max_theorem_uses: 100
  enable_forward_reasoning: true
  forward_reasoning_depth: 2

# Auxiliary Construction Settings
auxiliary:
  enabled: true
  trigger_after_steps: 20
  max_constructions: 3
  max_candidates: 10
  strategy: "best_first"

# Numeric Solver Settings
numeric:
  enabled: true
  solver_type: "algebraic"  # algebraic, optimization
  tolerance: 1e-6
  max_iterations: 1000

# Visualization Settings
visualization:
  default_format: "png"
  dpi: 300
  language: "cn"  # cn, en

# Logging
logging:
  level: "INFO"  # DEBUG, INFO, WARN, ERROR
  log_file: "geometry_prover.log"
```

### 7.5 Plugin System (Future)

Design for future plugin support:
- Custom Fact types
- Custom theorem matching strategies
- Custom search heuristics
- Custom visualization backends

---

## 8. Summary and Next Steps

### 8.1 What This Design Provides

This package design plan provides:

1. **Complete Architecture**: All modules, classes, and interactions defined
2. **Clear Responsibilities**: Each module has a specific purpose
3. **Extensibility**: Theorems and patterns are data, not code
4. **Scalability**: Can handle large theorem libraries and complex proofs
5. **Hybrid Reasoning**: Combines logic with numeric validation
6. **Auxiliary Automation**: Automatically proposes constructions
7. **Implementation Roadmap**: Step-by-step development plan (20 weeks)

### 8.2 Key Design Decisions

1. **Fact-based representation**: All geometric knowledge as Facts
2. **External theorem definitions**: YAML-based, easily extensible
3. **Hybrid search**: Forward + Backward + Auxiliary
4. **Numeric grounding**: Use numeric model for validation
5. **Pattern-driven auxiliary search**: Configurable construction patterns
6. **Modular architecture**: Clean separation of concerns

### 8.3 Next Steps for Implementation

To start implementing:

1. **Set up project structure**: Create directories per package design
2. **Define data models first**: Fact types, geometric objects
3. **Implement DSL parser**: Get basic input working
4. **Build small theorem library**: 10-20 basic theorems
5. **Implement basic proof engine**: Forward/backward reasoning
6. **Test on simple problems**: Validate design with real examples
7. **Iterate and expand**: Add more features incrementally

### 8.4 Success Metrics

The system is successful when it can:

- Parse complex geometry problems from DSL
- Prove 80%+ of high school geometry theorems
- Automatically find auxiliary constructions for 50%+ of problems that need them
- Generate human-readable proof explanations
- Complete proofs within reasonable time (< 1 minute for typical problems)
- Handle degenerate and edge cases gracefully

---

## Appendix: Example Usage Scenario

**Input DSL**:
```
point A, B, C
Triangle ABC
AB = AC
prove angle(ABC) = angle(ACB)
```

**System Flow**:
1. DSL Parser: Parse to AST
2. SemanticBuilder: Build GeometryModel with triangle ABC, constraint AB=AC
3. FactExtractor: Generate Facts: `Triangle(A,B,C)`, `EqualSegment(AB, AC)`
4. ConstraintSolver: Solve to get NumericModel (coordinates)
5. ProofEngine: Start proving goal `EqualAngle(∠ABC, ∠ACB)`
6. BackwardReasoner: Find theorem "Isosceles triangle base angles equal"
7. TheoremMatcher: Match premises `EqualSegment({A}{B}, {A}{C})` to facts
8. TheoremApplier: Apply theorem, generate conclusion `EqualAngle(∠ABC, ∠ACB)`
9. ProofResult: Success!
10. ProofFormatter: Generate description: "已知AB=AC,因此△ABC为等腰三角形,根据等腰三角形性质,底角相等,所以∠ABC=∠ACB。"
11. Renderer: Draw diagram with highlighted equal sides and angles

**Output**:
- Proof: Success
- Steps: 3 steps (given → isosceles → base angles equal)
- Description: Natural language proof
- Diagram: Visual representation

---

This concludes the comprehensive package design plan. The design is ready for implementation by a development team. Each module can be developed independently and integrated incrementally following the roadmap.
