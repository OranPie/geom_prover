# Detailed Development Plan - Geometry Theorem Proving System

## Document Overview

This document provides a comprehensive, phase-by-phase development plan with detailed tasks, acceptance criteria, dependencies, and deliverables for each phase of the Geometry Theorem Proving System.

**Total Duration**: 20 weeks (5 months)
**Team Size**: Recommended 3-5 developers
**Development Methodology**: Agile with 1-week sprints

---

## Table of Contents

1. [Phase 1: Foundation (Weeks 1-3)](#phase-1-foundation-weeks-1-3)
2. [Phase 2: Theorem System (Weeks 4-6)](#phase-2-theorem-system-weeks-4-6)
3. [Phase 3: Proof Engine (Weeks 7-10)](#phase-3-proof-engine-weeks-7-10)
4. [Phase 4: Numeric Solver (Weeks 11-12)](#phase-4-numeric-solver-weeks-11-12)
5. [Phase 5: Auxiliary Construction Search (Weeks 13-15)](#phase-5-auxiliary-construction-search-weeks-13-15)
6. [Phase 6: Visualization & Polish (Weeks 16-18)](#phase-6-visualization--polish-weeks-16-18)
7. [Phase 7: Testing & Optimization (Weeks 19-20)](#phase-7-testing--optimization-weeks-19-20)
8. [Phase 8: Advanced Features (Weeks 21+)](#phase-8-advanced-features-weeks-21)
9. [Team Allocation & Responsibilities](#team-allocation--responsibilities)
10. [Risk Management](#risk-management)
11. [Quality Assurance Strategy](#quality-assurance-strategy)

---

## Phase 1: Foundation (Weeks 1-3)

**Goal**: Establish core data structures, implement DSL parsing, and build semantic analysis pipeline.

**Team Focus**: All developers work on foundation

---

### Week 1: Data Models & Core Infrastructure

#### Task 1.1: Project Setup (Day 1)
**Owner**: Team Lead
**Duration**: 1 day

**Subtasks**:
1. Initialize Git repository
2. Set up project structure according to package design
3. Configure virtual environment (Python 3.10+)
4. Set up dependency management (requirements.txt or pyproject.toml)
5. Configure linting (pylint, black, mypy)
6. Set up CI/CD pipeline (GitHub Actions / GitLab CI)
7. Create README with setup instructions

**Dependencies**: None

**Deliverables**:
- Working project skeleton
- CI/CD pipeline running tests
- Development environment documentation

**Acceptance Criteria**:
- [x] Project builds successfully
- [x] All developers can clone and run tests
- [x] CI/CD pipeline passes

---

#### Task 1.2: Geometric Object Classes (Days 1-2)
**Owner**: Developer 1
**Duration**: 2 days

**Subtasks**:
1. Implement `Point` class
   - Attributes: `name`, `coords` (optional), `metadata`
   - Methods: `__str__`, `__repr__`, `__eq__`, `__hash__`

2. Implement `Line` class
   - Attributes: `id`, `point1`, `point2`, `equation`, `type` (line/segment/ray)
   - Methods: `contains(point)`, `is_parallel_to(line)`, `is_perpendicular_to(line)`

3. Implement `Circle` class
   - Attributes: `center`, `radius`, `id`
   - Methods: `contains(point)`, `intersect(line)`, `intersect(circle)`

4. Implement `Angle` class
   - Attributes: `vertex`, `point1`, `point2`
   - Methods: `to_radians()`, `to_degrees()`, `equals(angle, tolerance)`

5. Implement `Segment` class (wrapper around Line)

**Dependencies**: Task 1.1

**Test Requirements**:
- Unit tests for each class (minimum 80% coverage)
- Test equality and hashing
- Test edge cases (degenerate cases)

**Deliverables**:
- `utils/geometry_objects.py` with all classes
- Comprehensive unit tests in `tests/test_geometry_objects.py`

**Acceptance Criteria**:
- [x] All geometric objects can be created and compared
- [x] Hash and equality work correctly for use in sets/dicts
- [x] All tests pass

**Code Example**:
```python
# Conceptual structure
class Point:
    def __init__(self, name: str, coords: tuple[float, float] | None = None):
        self.name = name
        self.coords = coords
        self.metadata = {}

    def __eq__(self, other):
        return isinstance(other, Point) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name
```

---

#### Task 1.3: Fact Type System Implementation (Days 3-5)
**Owner**: Developer 2, Developer 3
**Duration**: 3 days

**Subtasks**:

**Day 3: Base Fact Class & Structural Facts (15 types)**
1. Implement base `Fact` class with:
   - `fact_type: str`
   - `parameters: dict`
   - Abstract methods: `matches(pattern)`, `to_string()`, `validate()`
   - `__hash__()`, `__eq__()`

2. Implement Structural Facts (Developer 2):
   - `On(point, line)`
   - `OnSegment(point, point1, point2)`
   - `OnCircle(point, circle)`
   - `Collinear(p1, p2, p3)` / `NotCollinear(p1, p2, p3)`
   - `Between(p_middle, p1, p2)`
   - `Midpoint(midpoint, p1, p2)`
   - `FootOfPerpendicular(foot, point, line)`
   - `ReflectPoint(reflected, original, line)`
   - `Intersect(obj1, obj2, intersection_point)`

**Day 4: Length, Angle, and Line Relation Facts (15 types)**
3. Implement Length Facts (Developer 3):
   - `EqualSegment(seg1, seg2)`
   - `ProportionalSegment(seg1, seg2, ratio)`
   - `SegmentRatio(p1, p2, p3, p4, ratio)`
   - `LengthValue(segment, value)`

4. Implement Angle Facts:
   - `EqualAngle(angle1, angle2)`
   - `RightAngle(angle)`
   - `SupplementaryAngle(angle1, angle2)`
   - `AngleSum(angle1, angle2, result_value)`
   - `AngleValue(angle, value)`

5. Implement Line Relation Facts:
   - `Parallel(line1, line2)`
   - `Perpendicular(line1, line2)`
   - `SameLine(line1, line2)`

**Day 5: Shape, Circle, Area, and Logic Facts (10 types)**
6. Implement Shape Facts (Developer 2):
   - `Triangle(p1, p2, p3)`
   - `IsoscelesTriangle(p1, p2, p3)`
   - `EquilateralTriangle(p1, p2, p3)`
   - `SimilarTriangle(p1, p2, p3, p4, p5, p6)`
   - `CongruentTriangle(p1, p2, p3, p4, p5, p6)`

7. Implement Circle Facts (Developer 3):
   - `TangentAt(line, circle, point)`
   - `Chord(p1, p2, circle)`
   - `Diameter(p1, p2, circle)`
   - `Arc(p1, p2, circle)`
   - `CyclicQuadrilateral(p1, p2, p3, p4)`

8. Implement Area & Logic Facts:
   - `AreaValue(shape, value)`
   - `AreaRelation(shape1, shape2, ratio)`
   - `Distinct(p1, p2)`
   - `NonDegenerateTriangle(p1, p2, p3)`
   - `Orientation(p1, p2, p3, sign)`

**Dependencies**: Task 1.2

**Test Requirements**:
- Unit test for each Fact type
- Test `__eq__` and `__hash__` for all types
- Test `to_string()` output format
- Test parameter validation

**Deliverables**:
- `facts/fact_types.py` with all 40+ Fact types
- `tests/test_fact_types.py` with comprehensive tests
- Documentation for each Fact type

**Acceptance Criteria**:
- [x] All 40+ Fact types implemented
- [x] Each type has proper equality and hashing
- [x] Test coverage > 85%
- [x] Facts can be stored in sets and dicts without issues

---

#### Task 1.4: FactBase Implementation (Day 5)
**Owner**: Developer 1
**Duration**: 1 day

**Subtasks**:
1. Implement `FactBase` class
   - Internal storage: set of facts + indices
   - Index by fact type
   - Index by involved points
   - Index by involved lines/circles

2. Implement methods:
   - `add(fact: Fact) -> bool`: Add with deduplication
   - `remove(fact: Fact) -> bool`
   - `contains(fact: Fact) -> bool`
   - `query_by_type(fact_type: str) -> list[Fact]`
   - `query_by_point(point: Point) -> list[Fact]`
   - `query_by_object(obj: GeometricObject) -> list[Fact]`
   - `get_all() -> list[Fact]`
   - `size() -> int`
   - `clear()`

3. Optimize for fast lookups (O(1) or O(log n))

**Dependencies**: Task 1.3

**Test Requirements**:
- Test add/remove operations
- Test deduplication
- Test querying by different criteria
- Performance test with 10,000 facts

**Deliverables**:
- `facts/fact_base.py`
- `tests/test_fact_base.py`

**Acceptance Criteria**:
- [x] Can store and retrieve facts efficiently
- [x] Deduplication works correctly
- [x] Query operations are fast (< 1ms for 1000 facts)
- [x] All tests pass

---

### Week 2: DSL Parsing

#### Task 2.1: Grammar Definition (Day 1)
**Owner**: Developer 2
**Duration**: 1 day

**Subtasks**:
1. Define formal grammar in BNF notation for DSL
2. Document all supported keywords and syntax
3. Create example DSL files for testing

**Grammar Specification** (partial):
```
program         := statement_list

statement_list  := statement | statement statement_list

statement       := point_decl
                 | line_decl
                 | circle_decl
                 | constraint
                 | prove_statement

point_decl      := 'point' identifier_list

identifier_list := identifier | identifier ',' identifier_list

line_decl       := 'line' identifier identifier
                 | 'line' identifier

circle_decl     := 'circle' identifier 'with' 'radius' number
                 | 'circle' identifier 'through' identifier

constraint      := segment '=' segment
                 | segment '||' segment
                 | segment '⊥' segment
                 | angle '=' angle
                 | angle '=' number

prove_statement := 'prove' assertion

assertion       := constraint
                 | 'angle' '(' identifier identifier identifier ')' '=' 'angle' '(' identifier identifier identifier ')'

segment         := identifier identifier

angle           := 'angle' '(' identifier identifier identifier ')'
```

**Dependencies**: None

**Deliverables**:
- `dsl/grammar.py` with formal grammar
- `docs/dsl_specification.md` documentation
- 20+ example DSL files in `examples/`

**Acceptance Criteria**:
- [x] Grammar covers all required constructs
- [x] Grammar is unambiguous
- [x] Documentation is clear

---

#### Task 2.2: Lexer Implementation (Days 1-2)
**Owner**: Developer 3
**Duration**: 2 days

**Subtasks**:
1. Implement `Token` class
   - Attributes: `type`, `value`, `line`, `column`

2. Implement `Lexer` class
   - Method: `tokenize(text: str) -> list[Token]`
   - Support keywords: `point`, `line`, `circle`, `prove`, `with`, `radius`, `through`, `angle`
   - Support operators: `=`, `||`, `⊥`, `,`, `(`, `)`
   - Support identifiers (A-Z, a-z)
   - Support numbers (integers and floats)
   - Handle whitespace and comments

3. Error handling for invalid characters

**Dependencies**: Task 2.1

**Test Requirements**:
- Test tokenization of all valid constructs
- Test error handling for invalid input
- Test line/column tracking for error messages

**Deliverables**:
- `dsl/lexer.py`
- `tests/test_lexer.py`

**Acceptance Criteria**:
- [x] All DSL constructs tokenize correctly
- [x] Error messages include line/column information
- [x] All tests pass

**Code Example**:
```python
# Conceptual
class Token:
    def __init__(self, type: str, value: str, line: int, col: int):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

class Lexer:
    def tokenize(self, text: str) -> list[Token]:
        tokens = []
        # Tokenization logic
        return tokens
```

---

#### Task 2.3: AST Node Definitions (Day 2)
**Owner**: Developer 1
**Duration**: 1 day

**Subtasks**:
1. Define base `ASTNode` class
2. Define concrete node types:
   - `Program`
   - `PointDecl`
   - `LineDecl`
   - `CircleDecl`
   - `ConstraintNode` (with subtypes: `EqualConstraint`, `ParallelConstraint`, etc.)
   - `ProveNode`
   - `Identifier`
   - `Number`
   - `AngleExpr`
   - `SegmentExpr`

3. Implement `accept(visitor)` for visitor pattern

**Dependencies**: None (parallel with Task 2.2)

**Deliverables**:
- `dsl/ast_nodes.py`
- `tests/test_ast_nodes.py`

**Acceptance Criteria**:
- [x] All node types defined
- [x] Nodes support visitor pattern
- [x] Nodes have proper `__repr__` for debugging

---

#### Task 2.4: Parser Implementation (Days 3-4)
**Owner**: Developer 2, Developer 3
**Duration**: 2 days

**Subtasks**:
1. Implement `Parser` class
   - Method: `parse(tokens: list[Token]) -> Program`
   - Recursive descent parsing
   - Build AST from tokens

2. Implement parsing methods for each grammar rule:
   - `parse_program()`
   - `parse_statement()`
   - `parse_point_decl()`
   - `parse_line_decl()`
   - `parse_circle_decl()`
   - `parse_constraint()`
   - `parse_prove_statement()`
   - `parse_expression()`

3. Error handling with helpful messages

**Dependencies**: Tasks 2.2, 2.3

**Test Requirements**:
- Test parsing of all example DSL files
- Test error recovery
- Test AST structure correctness

**Deliverables**:
- `dsl/parser.py`
- `tests/test_parser.py`

**Acceptance Criteria**:
- [x] Can parse all valid DSL constructs
- [x] Error messages are helpful
- [x] AST structure matches grammar
- [x] All example files parse successfully

---

#### Task 2.5: DSL Integration Tests (Day 5)
**Owner**: Developer 1
**Duration**: 1 day

**Subtasks**:
1. Create comprehensive DSL examples
2. Test full pipeline: text → tokens → AST
3. Test error handling end-to-end
4. Performance test with large DSL files

**Dependencies**: Tasks 2.2, 2.4

**Deliverables**:
- `tests/integration/test_dsl_pipeline.py`
- 50+ test cases

**Acceptance Criteria**:
- [x] All integration tests pass
- [x] Can parse complex geometry problems
- [x] Performance is acceptable (< 100ms for typical files)

---

### Week 3: Semantic Analysis

#### Task 3.1: GeometryModel Implementation (Days 1-2)
**Owner**: Developer 1
**Duration**: 2 days

**Subtasks**:
1. Implement `GeometryModel` class
   - Store all geometric objects (points, lines, circles)
   - Store relationships (on, parallel, perpendicular, equal)
   - Method: `add_point(point: Point)`
   - Method: `add_line(line: Line)`
   - Method: `add_circle(circle: Circle)`
   - Method: `add_relationship(rel_type: str, objects: list)`
   - Method: `get_points() -> list[Point]`
   - Method: `get_lines() -> list[Line]`
   - Method: `get_circles() -> list[Circle]`
   - Method: `get_relationships() -> list`

2. Implement queries:
   - `find_point(name: str) -> Point | None`
   - `find_line_by_points(p1: Point, p2: Point) -> Line | None`
   - `get_points_on_line(line: Line) -> list[Point]`

3. Validation methods:
   - Check for duplicate point names
   - Check for geometric inconsistencies

**Dependencies**: Task 1.2

**Test Requirements**:
- Test adding and retrieving objects
- Test relationship storage
- Test validation

**Deliverables**:
- `semantic/geometry_model.py`
- `tests/test_geometry_model.py`

**Acceptance Criteria**:
- [x] Can store complete geometric configuration
- [x] Queries work efficiently
- [x] Validation catches common errors

---

#### Task 3.2: ConstraintBuilder Implementation (Day 2)
**Owner**: Developer 2
**Duration**: 1 day

**Subtasks**:
1. Implement `ConstraintBuilder` class
   - Convert DSL constraints to numeric constraint expressions
   - Support: distance constraints, angle constraints, position constraints

2. Define `Constraint` data structure:
   - Type: `equal_distance`, `equal_angle`, `parallel`, `perpendicular`, `on_line`, `on_circle`
   - Parameters: involved objects
   - Numeric expression (for solver)

3. Build constraint system from GeometryModel

**Dependencies**: Task 3.1

**Deliverables**:
- `semantic/constraint_builder.py`
- `tests/test_constraint_builder.py`

**Acceptance Criteria**:
- [x] All constraint types supported
- [x] Constraints correctly represent DSL semantics

---

#### Task 3.3: ProveGoalExtractor Implementation (Day 3)
**Owner**: Developer 3
**Duration**: 1 day

**Subtasks**:
1. Implement `ProveGoalExtractor` class
   - Extract prove statements from AST
   - Convert to target Fact representations

2. Handle different goal types:
   - Equal segments: → `EqualSegment` fact
   - Equal angles: → `EqualAngle` fact
   - Parallel: → `Parallel` fact
   - Perpendicular: → `Perpendicular` fact

**Dependencies**: Task 2.4

**Deliverables**:
- `semantic/prove_goal_extractor.py`
- `tests/test_prove_goal_extractor.py`

**Acceptance Criteria**:
- [x] All prove statement types supported
- [x] Goals correctly converted to Facts

---

#### Task 3.4: SemanticBuilder Implementation (Days 3-4)
**Owner**: Developer 1, Developer 2
**Duration**: 2 days

**Subtasks**:
1. Implement `SemanticBuilder` class
   - Main orchestrator for semantic analysis
   - Traverse AST and build GeometryModel

2. Implement visitor methods:
   - `visit_point_decl(node)`
   - `visit_line_decl(node)`
   - `visit_circle_decl(node)`
   - `visit_constraint(node)`
   - `visit_prove_statement(node)`

3. Coordinate with ConstraintBuilder and ProveGoalExtractor

4. Error handling for semantic errors:
   - Undefined points/lines
   - Conflicting constraints

**Dependencies**: Tasks 3.1, 3.2, 3.3

**Test Requirements**:
- Test building model from various AST inputs
- Test error detection

**Deliverables**:
- `semantic/builder.py`
- `tests/test_semantic_builder.py`

**Acceptance Criteria**:
- [x] Can build complete GeometryModel from AST
- [x] Constraints and goals extracted correctly
- [x] Semantic errors detected and reported

---

#### Task 3.5: FactExtractor Implementation (Day 4-5)
**Owner**: Developer 3
**Duration**: 1.5 days

**Subtasks**:
1. Implement `FactExtractor` class
   - Extract Facts from GeometryModel
   - Generate basic Facts from relationships

2. Extraction rules:
   - For each point declared: create `Point` in model
   - For `point P on AB`: → `On(P, Line(A,B))` fact
   - For `AB = CD`: → `EqualSegment(AB, CD)` fact
   - For `AB || CD`: → `Parallel(Line(AB), Line(CD))` fact
   - For `AB ⊥ CD`: → `Perpendicular(Line(AB), Line(CD))` fact
   - For triangle ABC (three non-collinear points): → `Triangle(A, B, C)` fact

3. Handle implicit facts:
   - If A, B declared and line AB exists: → `On(A, AB)`, `On(B, AB)` facts
   - If circle with center O: → `Center(O, circle)` fact

**Dependencies**: Tasks 1.4, 3.1

**Test Requirements**:
- Test extraction from various geometry configurations
- Test implicit fact generation

**Deliverables**:
- `facts/fact_extractor.py`
- `tests/test_fact_extractor.py`

**Acceptance Criteria**:
- [x] All basic facts extracted correctly
- [x] Implicit facts generated appropriately
- [x] No duplicate facts

---

#### Task 3.6: Phase 1 Integration Testing (Day 5)
**Owner**: All Developers
**Duration**: 0.5 day

**Subtasks**:
1. Test complete pipeline: DSL → AST → GeometryModel → Facts
2. Test with multiple example problems
3. Create benchmark problems for regression testing

**Dependencies**: All previous tasks

**Test Files**:
- `tests/integration/test_phase1_pipeline.py`

**Test Cases**:
1. Simple triangle with equal sides
2. Parallel lines with transversal
3. Circle with tangent line
4. Complex configuration with multiple constraints

**Acceptance Criteria**:
- [x] All integration tests pass
- [x] Pipeline works end-to-end for all test cases
- [x] No memory leaks or performance issues

---

### Phase 1 Deliverables Summary

**Code Deliverables**:
- Geometric object classes (Point, Line, Circle, Angle)
- Complete Fact type system (40+ types)
- FactBase with efficient storage and querying
- DSL Lexer and Parser
- AST node definitions
- SemanticBuilder
- GeometryModel
- ConstraintBuilder
- ProveGoalExtractor
- FactExtractor

**Documentation**:
- DSL specification
- API documentation for all modules
- Example DSL files

**Tests**:
- Unit tests (coverage > 80%)
- Integration tests for full pipeline

**Milestone**: Can parse DSL and extract initial Facts

---

## Phase 2: Theorem System (Weeks 4-6)

**Goal**: Implement theorem loading, pattern matching, and theorem application.

**Team Focus**: Build extensible theorem infrastructure

---

### Week 4: Theorem Infrastructure

#### Task 4.1: Theorem YAML Format Design (Day 1)
**Owner**: Team Lead
**Duration**: 1 day

**Subtasks**:
1. Finalize YAML schema for theorems
2. Create JSON schema validator
3. Create 5 example theorem files

**YAML Template**:
```yaml
- id: ISO_TRIANGLE_BASE_ANGLES
  version: "1.0"
  name: 等腰三角形底角相等
  category: triangle
  tags: [isosceles, basic, angles]
  premises:
    - EqualSegment({A}{B}, {A}{C})
    - NotCollinear({A}, {B}, {C})
  conclusions:
    - EqualAngle(Angle({B}{A}{C}), Angle({C}{A}{B}))
  conditions:
    - Distinct({A}, {B})
    - Distinct({A}, {C})
    - Distinct({B}, {C})
  priority: 8
  max_uses: 5
  nl_templates:
    cn: "因为{A}{B} = {A}{C},所以△{A}{B}{C}为等腰三角形,根据等腰三角形性质,底角相等,即∠{B}{A}{C} = ∠{C}{A}{B}。"
    en: "Since {A}{B} = {A}{C}, triangle {A}{B}{C} is isosceles. By the isosceles triangle theorem, base angles are equal: ∠{B}{A}{C} = ∠{C}{A}{B}."
  notes: "Most basic isosceles triangle property"
  enabled: true
```

**Dependencies**: None

**Deliverables**:
- YAML schema in `data/schemas/theorem_schema.json`
- Example theorems in `data/theorems/basic.yaml`
- Validation script

**Acceptance Criteria**:
- [x] Schema covers all theorem attributes
- [x] Examples validate against schema
- [x] Schema is extensible

---

#### Task 4.2: PatternParser Implementation (Days 1-3)
**Owner**: Developer 1
**Duration**: 3 days

**Subtasks**:

**Day 1: Pattern String Lexer**
1. Tokenize pattern strings
   - Example: `EqualSegment({A}{B}, {C}{D})` → tokens
   - Identify: fact type, parameters, placeholders

**Day 2: Pattern String Parser**
2. Parse pattern strings into FactPattern objects
   - Handle nested structures: `On({P}, Line({A}{B}))`
   - Extract placeholders: `{A}`, `{B}`, etc.
   - Support constants: `90deg`, `pi/2`

**Day 3: Pattern Validation**
3. Validate patterns against Fact type definitions
4. Error handling for malformed patterns

**Dependencies**: Task 4.1

**Test Requirements**:
- Test parsing all Fact type patterns
- Test nested patterns
- Test error cases

**Deliverables**:
- `theorems/pattern_parser.py`
- `tests/test_pattern_parser.py`

**Acceptance Criteria**:
- [x] Can parse all pattern string formats
- [x] Placeholders correctly extracted
- [x] Validation works

**Code Example**:
```python
# Conceptual
class FactPattern:
    def __init__(self, fact_type: str, params: dict, placeholders: set):
        self.fact_type = fact_type
        self.params = params
        self.placeholders = placeholders  # e.g., {'A', 'B', 'C'}

    def match(self, fact: Fact, bindings: dict) -> bool:
        # Match fact against pattern with variable bindings
        pass

# Usage
pattern_str = "EqualSegment({A}{B}, {C}{D})"
pattern = PatternParser.parse(pattern_str)
# pattern.placeholders = {'A', 'B', 'C', 'D'}
```

---

#### Task 4.3: Theorem Data Structure (Day 3)
**Owner**: Developer 2
**Duration**: 1 day

**Subtasks**:
1. Implement `Theorem` class
   - All attributes from YAML schema
   - Methods: `validate()`, `to_dict()`, `from_dict()`

2. Implement `Condition` class for conditions
   - Type: `Distinct`, `NotCollinear`, etc.
   - Check method

**Dependencies**: Task 4.2

**Deliverables**:
- `theorems/theorem.py`
- `tests/test_theorem.py`

**Acceptance Criteria**:
- [x] Theorem class represents all YAML fields
- [x] Can serialize/deserialize

---

#### Task 4.4: TheoremLoader Implementation (Days 4-5)
**Owner**: Developer 3
**Duration**: 2 days

**Subtasks**:
1. Implement `TheoremLoader` class
   - Load YAML files from directory
   - Parse using PyYAML
   - Validate against schema
   - Convert to Theorem objects

2. Handle multiple files and categories

3. Support hot-reloading (watch file changes)

4. Error handling:
   - Invalid YAML syntax
   - Schema validation failures
   - Duplicate theorem IDs

**Dependencies**: Tasks 4.1, 4.2, 4.3

**Test Requirements**:
- Test loading valid theorem files
- Test error handling for invalid files
- Test loading from directory

**Deliverables**:
- `theorems/theorem_loader.py`
- `tests/test_theorem_loader.py`

**Acceptance Criteria**:
- [x] Can load all theorems from directory
- [x] Validates YAML files
- [x] Errors reported clearly

---

#### Task 4.5: TheoremBase Implementation (Day 5)
**Owner**: Developer 1
**Duration**: 1 day

**Subtasks**:
1. Implement `TheoremBase` class
   - Container for all theorems
   - Indices for efficient lookup

2. Indexing strategies:
   - By category
   - By conclusion fact type
   - By premise fact types
   - By tags

3. Query methods:
   - `get_by_id(id: str) -> Theorem`
   - `get_by_category(category: str) -> list[Theorem]`
   - `get_by_tag(tag: str) -> list[Theorem]`
   - `find_by_conclusion_type(fact_type: str) -> list[Theorem]`
   - `find_by_premise_type(fact_type: str) -> list[Theorem]`
   - `get_all() -> list[Theorem]`

**Dependencies**: Tasks 4.3, 4.4

**Test Requirements**:
- Test indexing correctness
- Test query performance with 100+ theorems

**Deliverables**:
- `theorems/theorem_base.py`
- `tests/test_theorem_base.py`

**Acceptance Criteria**:
- [x] Efficient storage and retrieval
- [x] All query methods work
- [x] Performance acceptable

---

### Week 5: Pattern Matching

#### Task 5.1: FactMatcher Implementation (Days 1-3)
**Owner**: Developer 1, Developer 2
**Duration**: 3 days

**Subtasks**:

**Day 1: Basic Unification Algorithm**
1. Implement variable binding logic
2. Match simple patterns to facts
   - Example: Pattern `EqualSegment({A}{B}, {C}{D})` matches fact `EqualSegment(AB, CD)`
   - Bindings: `{A: A, B: B, C: C, D: D}`

**Day 2: Complex Pattern Matching**
3. Handle nested patterns
   - Example: `On({P}, Line({A}{B}))`
4. Handle wildcards and constraints
5. Backtracking for multiple possible bindings

**Day 3: Optimization**
6. Optimize matching algorithm
7. Cache matching results

**Dependencies**: Task 4.2

**Test Requirements**:
- Test matching all pattern types
- Test binding consistency (same placeholder → same object)
- Test performance with large FactBase

**Deliverables**:
- `facts/fact_matcher.py`
- `tests/test_fact_matcher.py`

**Acceptance Criteria**:
- [x] Can match all pattern types
- [x] Bindings are consistent
- [x] Performance < 1ms per match on average

**Algorithm Outline**:
```python
# Conceptual
def match_pattern(pattern: FactPattern, fact: Fact, bindings: dict) -> bool:
    """
    Check if fact matches pattern, updating bindings.
    Returns True if match successful.
    """
    if pattern.fact_type != fact.fact_type:
        return False

    for param_name, param_pattern in pattern.params.items():
        fact_value = fact.parameters[param_name]

        if is_placeholder(param_pattern):
            # Check/update bindings
            if param_pattern in bindings:
                if bindings[param_pattern] != fact_value:
                    return False  # Inconsistent binding
            else:
                bindings[param_pattern] = fact_value
        else:
            # Must match exactly
            if param_pattern != fact_value:
                return False

    return True
```

---

#### Task 5.2: ConditionsChecker Implementation (Days 3-4)
**Owner**: Developer 3
**Duration**: 1.5 days

**Subtasks**:
1. Implement `ConditionsChecker` class
   - Check `Distinct` conditions
   - Check `NotCollinear` conditions
   - Check `NonDegenerateTriangle` conditions

2. Two checking modes:
   - **Symbolic**: Check against existing facts
   - **Numeric**: Use numeric model (when available)

3. Integrate with FactBase for symbolic checking

**Dependencies**: Task 5.1

**Test Requirements**:
- Test each condition type
- Test both symbolic and numeric modes

**Deliverables**:
- `theorems/conditions_checker.py`
- `tests/test_conditions_checker.py`

**Acceptance Criteria**:
- [x] All condition types supported
- [x] Both checking modes work

---

#### Task 5.3: TheoremMatcher Implementation (Days 4-5)
**Owner**: Developer 1, Developer 2
**Duration**: 1.5 days

**Subtasks**:
1. Implement `TheoremMatcher` class
   - Match theorem premises against FactBase
   - Find all valid theorem applications

2. Algorithm:
   ```
   For each theorem:
     For first premise pattern:
       Find all matching facts → initial bindings
     For each initial binding:
       For remaining premises:
         Try to find matching facts consistent with binding
       If all premises match:
         Check conditions
         If conditions satisfied:
           Yield (theorem, binding)
   ```

3. Optimization:
   - Start with most restrictive premise
   - Early pruning of invalid bindings

4. Ranking candidates:
   - By theorem priority
   - By number of matched premises
   - By relevance to goal (if provided)

**Dependencies**: Tasks 5.1, 5.2

**Test Requirements**:
- Test matching with various theorem and FactBase combinations
- Test ranking
- Performance test

**Deliverables**:
- `theorems/theorem_matcher.py`
- `tests/test_theorem_matcher.py`

**Acceptance Criteria**:
- [x] Finds all valid theorem applications
- [x] No false positives
- [x] Ranking works correctly
- [x] Performance acceptable (< 100ms for typical case)

---

### Week 6: Theorem Application

#### Task 6.1: TheoremApplier Implementation (Days 1-2)
**Owner**: Developer 1
**Duration**: 2 days

**Subtasks**:
1. Implement `TheoremApplier` class
   - Apply matched theorem to generate conclusions

2. Substitution logic:
   - Replace placeholders in conclusion patterns with bound values
   - Generate concrete Fact instances

3. Validation:
   - Ensure generated facts are valid
   - Check for contradictions (optional)

4. Record application in proof trace

**Dependencies**: Task 5.3

**Test Requirements**:
- Test applying various theorems
- Test substitution correctness
- Test with complex bindings

**Deliverables**:
- `theorems/theorem_applier.py`
- `tests/test_theorem_applier.py`

**Acceptance Criteria**:
- [x] Correctly generates conclusion facts
- [x] Substitution is accurate
- [x] All tests pass

**Code Example**:
```python
# Conceptual
def apply_theorem(theorem: Theorem, binding: dict) -> list[Fact]:
    """
    Apply theorem with given variable binding to generate conclusion facts.
    """
    conclusion_facts = []

    for conclusion_pattern in theorem.conclusions:
        # Substitute bound variables into pattern
        concrete_fact = substitute(conclusion_pattern, binding)
        conclusion_facts.append(concrete_fact)

    return conclusion_facts

def substitute(pattern: FactPattern, binding: dict) -> Fact:
    """
    Replace placeholders in pattern with bound values.
    """
    substituted_params = {}
    for param_name, param_value in pattern.params.items():
        if is_placeholder(param_value):
            substituted_params[param_name] = binding[param_value]
        else:
            substituted_params[param_name] = param_value

    return Fact(pattern.fact_type, substituted_params)
```

---

#### Task 6.2: Write Basic Theorem Library (Days 2-4)
**Owner**: Developer 2, Developer 3
**Duration**: 2.5 days

**Subtasks**:
1. Create theorem files for different categories
2. Write 30-50 basic theorems

**Theorem Categories**:

**Triangles** (`data/theorems/triangles.yaml`):
- Isosceles triangle: equal sides → equal angles
- Isosceles triangle: equal angles → equal sides
- Triangle angle sum = 180°
- Exterior angle theorem
- Triangle inequality
- Congruence: SSS, SAS, ASA, AAS
- Similarity: AA, SAS, SSS

**Parallel Lines** (`data/theorems/parallel.yaml`):
- Corresponding angles equal ↔ parallel
- Alternate interior angles equal ↔ parallel
- Co-interior angles supplementary ↔ parallel
- Parallel to same line → parallel to each other

**Perpendicular Lines** (`data/theorems/perpendicular.yaml`):
- Right angle definition
- Perpendicular transitive property
- Altitude properties

**Circles** (`data/theorems/circles.yaml`):
- Radius perpendicular to chord bisects chord
- Tangent perpendicular to radius
- Inscribed angle = half central angle
- Angles in same segment are equal

**Quadrilaterals** (`data/theorems/quadrilaterals.yaml`):
- Parallelogram properties
- Rectangle, rhombus, square properties
- Trapezoid properties

**Dependencies**: Tasks 4.1, 4.2

**Deliverables**:
- 5+ YAML files with 30-50 theorems
- Documentation for each theorem

**Acceptance Criteria**:
- [x] At least 30 theorems written
- [x] All theorems validate against schema
- [x] Coverage of major geometry topics

---

#### Task 6.3: Phase 2 Integration Testing (Days 4-5)
**Owner**: All Developers
**Duration**: 1.5 days

**Subtasks**:
1. Test theorem loading and indexing
2. Test pattern matching on real problems
3. Test theorem application
4. Create test problems for each theorem

**Test Cases**:
1. **Test Problem 1**: Prove isosceles triangle base angles equal
   - Given: AB = AC, triangle ABC
   - Prove: ∠ABC = ∠ACB
   - Expected: Uses isosceles theorem directly

2. **Test Problem 2**: Prove parallel lines via angles
   - Given: Line l || Line m, transversal t
   - Prove: Corresponding angles equal
   - Expected: Uses parallel angle theorem

3. **Test Problem 3**: Triangle angle sum
   - Given: Triangle ABC, ∠A = 60°, ∠B = 70°
   - Prove: ∠C = 50°
   - Expected: Uses triangle angle sum theorem

**Dependencies**: All previous tasks

**Deliverables**:
- `tests/integration/test_phase2_theorems.py`
- 20+ test problems

**Acceptance Criteria**:
- [x] All integration tests pass
- [x] Can match and apply theorems on real problems
- [x] Performance is acceptable

---

### Phase 2 Deliverables Summary

**Code Deliverables**:
- PatternParser
- TheoremLoader
- TheoremBase with indexing
- FactMatcher (unification algorithm)
- ConditionsChecker
- TheoremMatcher
- TheoremApplier

**Data Deliverables**:
- 30-50 theorems in YAML format
- Theorem categories: triangles, parallel, perpendicular, circles, quadrilaterals

**Documentation**:
- Theorem YAML schema
- Pattern string syntax
- Theorem writing guide

**Tests**:
- Unit tests for all components
- Integration tests for theorem pipeline

**Milestone**: Can load theorems and apply them to generate new facts

---

## Phase 3: Proof Engine (Weeks 7-10)

**Goal**: Implement core reasoning engine with forward and backward chaining.

**Team Focus**: Build the heart of the proving system

---

### Week 7: Proof State & Data Structures

#### Task 7.1: ProofTree Implementation (Days 1-2)
**Owner**: Developer 1
**Duration**: 2 days

**Subtasks**:
1. Implement `ProofNode` class
   - Type: `initial_fact`, `theorem_application`, `aux_construction`
   - Attributes: facts, theorem (if applicable), children

2. Implement `ProofTree` class
   - Root node
   - Methods:
     - `add_node(parent, node) -> ProofNode`
     - `get_path_to_root(node) -> list[ProofNode]`
     - `get_all_nodes() -> list[ProofNode]`
     - `traverse(visitor)`

3. Support serialization to JSON/dict

**Dependencies**: None

**Test Requirements**:
- Test tree construction
- Test traversal
- Test serialization

**Deliverables**:
- `proof/proof_tree.py`
- `tests/test_proof_tree.py`

**Acceptance Criteria**:
- [x] Can build and traverse proof trees
- [x] Serialization works

---

#### Task 7.2: ProofState Implementation (Days 2-3)
**Owner**: Developer 2
**Duration**: 1.5 days

**Subtasks**:
1. Implement `ProofState` class
   - Attributes:
     - `fact_base: FactBase`
     - `goals: list[Fact]` (stack or queue)
     - `proof_tree: ProofTree`
     - `depth: int`
     - `theorem_usage: dict[str, int]` (theorem ID → usage count)
     - `metadata: dict`

2. Methods:
   - `add_fact(fact: Fact)`
   - `add_goal(goal: Fact)`
   - `remove_goal(goal: Fact)`
   - `has_goal(goal: Fact) -> bool`
   - `is_goal_satisfied(goal: Fact) -> bool`
   - `clone() -> ProofState` (for backtracking)
   - `increment_theorem_usage(theorem_id: str)`
   - `can_use_theorem(theorem: Theorem) -> bool` (check max_uses)

3. Support state snapshots for backtracking

**Dependencies**: Tasks 1.4, 7.1

**Test Requirements**:
- Test state management
- Test cloning
- Test theorem usage tracking

**Deliverables**:
- `proof/proof_state.py`
- `tests/test_proof_state.py`

**Acceptance Criteria**:
- [x] State correctly tracks all information
- [x] Cloning creates independent copies
- [x] Theorem usage limits enforced

---

#### Task 7.3: ProofResult Implementation (Day 3)
**Owner**: Developer 3
**Duration**: 1 day

**Subtasks**:
1. Implement `ProofResult` class
   - Attributes:
     - `success: bool`
     - `proof_tree: ProofTree | None`
     - `proven_goals: list[Fact]`
     - `failed_goals: list[Fact]`
     - `description: str` (natural language, to be generated later)
     - `statistics: dict` (nodes explored, time, theorem applications, etc.)
     - `error_message: str | None`

2. Methods:
   - `to_dict() -> dict`
   - `to_json() -> str`
   - `is_complete_success() -> bool`
   - `is_partial_success() -> bool`

**Dependencies**: Task 7.1

**Deliverables**:
- `proof/proof_result.py`
- `tests/test_proof_result.py`

**Acceptance Criteria**:
- [x] Encapsulates all proof information
- [x] Serialization works

---

#### Task 7.4: SearchStrategy Interface (Days 4-5)
**Owner**: Developer 1
**Duration**: 2 days

**Subtasks**:
1. Define `SearchStrategy` abstract base class
   - Method: `select_goal(state: ProofState) -> Fact | None`
   - Method: `select_candidate(candidates: list) -> Candidate`
   - Method: `should_continue(state: ProofState) -> bool`

2. Implement concrete strategies:

   **BreadthFirstStrategy**:
   - Goals: FIFO queue
   - Candidates: explore all at each level

   **DepthFirstStrategy**:
   - Goals: LIFO stack
   - Candidates: explore first candidate deeply

   **BestFirstStrategy**:
   - Goals: priority queue by heuristic
   - Candidates: sort by score

3. Implement heuristics for goal/candidate scoring:
   - Goal relevance (involves points in original problem)
   - Theorem priority
   - Number of matched premises

**Dependencies**: Task 7.2

**Test Requirements**:
- Test each strategy in isolation
- Test strategy behavior on sample problems

**Deliverables**:
- `proof/search_strategy.py`
- `tests/test_search_strategy.py`

**Acceptance Criteria**:
- [x] All strategies implemented
- [x] Strategies produce different search orders

---

### Week 8: Forward Reasoning

#### Task 8.1: ForwardReasoner Implementation (Days 1-3)
**Owner**: Developer 2, Developer 3
**Duration**: 3 days

**Subtasks**:

**Day 1: Core Forward Chaining Algorithm**
1. Implement `ForwardReasoner` class
2. Main method: `reason(state: ProofState, theorem_base: TheoremBase, max_depth: int) -> int`
   - Returns number of new facts generated

3. Algorithm:
   ```
   depth = 0
   while depth < max_depth:
     new_facts = []
     for theorem in theorem_base (sorted by priority):
       if state.can_use_theorem(theorem):
         matches = theorem_matcher.find_all_matches(theorem, state.fact_base)
         for (binding) in matches:
           if conditions_checker.check(theorem.conditions, binding):
             conclusions = theorem_applier.apply(theorem, binding)
             for fact in conclusions:
               if fact not in state.fact_base:
                 new_facts.append((fact, theorem, binding))

     if not new_facts:
       break  # No more derivations possible

     for (fact, theorem, binding) in new_facts:
       state.add_fact(fact)
       state.proof_tree.add_application(theorem, binding, fact)
       state.increment_theorem_usage(theorem.id)

     depth += 1

   return len(new_facts)
   ```

**Day 2: Optimization**
4. Add pruning:
   - Don't re-derive facts
   - Limit theorem applications per iteration
   - Early stopping if goal is reached

5. Add incremental forward reasoning:
   - `reason_incremental(new_facts, ...)`: Only consider theorems that might use new facts

**Day 3: Integration & Testing**
6. Integrate with ProofState and TheoremBase
7. Test on various fact sets

**Dependencies**: Tasks 5.3, 6.1, 7.2

**Test Requirements**:
- Test with simple theorem sets
- Test depth limiting
- Test that forward reasoning terminates
- Performance test: 100 facts, 50 theorems

**Deliverables**:
- `proof/forward_reasoner.py`
- `tests/test_forward_reasoner.py`

**Acceptance Criteria**:
- [x] Correctly derives new facts from theorems
- [x] Terminates in reasonable time
- [x] No infinite loops
- [x] Respects max_uses limits

---

#### Task 8.2: Test Forward Reasoning on Problems (Days 4-5)
**Owner**: Developer 1
**Duration**: 2 days

**Subtasks**:
1. Create test problems solvable by forward reasoning alone
2. Test forward reasoning performance
3. Analyze bottlenecks

**Test Problems**:
1. **Transitive equality**: AB = BC, BC = CD → AB = CD
2. **Angle propagation**: ∠A = ∠B, ∠B = ∠C → ∠A = ∠C
3. **Parallel transitivity**: AB || BC, BC || CD → AB || CD

**Dependencies**: Task 8.1

**Deliverables**:
- `tests/integration/test_forward_reasoning.py`
- Performance report

**Acceptance Criteria**:
- [x] Forward reasoning solves test problems
- [x] Performance is acceptable (< 1s for typical problems)

---

### Week 9: Backward Reasoning

#### Task 9.1: BackwardReasoner Implementation (Days 1-3)
**Owner**: Developer 1, Developer 2
**Duration**: 3 days

**Subtasks**:

**Day 1: Core Backward Chaining Algorithm**
1. Implement `BackwardReasoner` class
2. Main method: `find_theorem_candidates(goal: Fact, theorem_base: TheoremBase, state: ProofState) -> list[TheoremCandidate]`

3. Algorithm:
   ```
   candidates = []

   # Find theorems whose conclusions can unify with goal
   potential_theorems = theorem_base.find_by_conclusion_type(goal.fact_type)

   for theorem in potential_theorems:
     for conclusion_pattern in theorem.conclusions:
       binding = {}
       if fact_matcher.match(conclusion_pattern, goal, binding):
         # This theorem could prove the goal

         # Generate sub-goals from premises
         sub_goals = []
         for premise_pattern in theorem.premises:
           sub_goal = substitute(premise_pattern, binding)

           # Check if already satisfied
           if not state.fact_base.contains(sub_goal):
             sub_goals.append(sub_goal)

         # Check conditions
         if conditions_checker.check(theorem.conditions, binding, state):
           candidates.append(TheoremCandidate(
             theorem=theorem,
             binding=binding,
             sub_goals=sub_goals,
             score=calculate_score(theorem, binding, sub_goals, state)
           ))

   # Sort candidates by score
   candidates.sort(key=lambda c: c.score, reverse=True)

   return candidates
   ```

**Day 2: Scoring and Ranking**
4. Implement candidate scoring:
   - Theorem priority
   - Number of sub-goals (fewer is better)
   - Number of already satisfied premises
   - Relevance to original problem

**Day 3: Integration & Testing**
5. Integrate with ProofState
6. Test on various goals

**Dependencies**: Tasks 5.1, 5.3, 7.2

**Test Requirements**:
- Test finding candidates for various goals
- Test ranking correctness
- Test that sub-goals are correctly generated

**Deliverables**:
- `proof/backward_reasoner.py`
- `tests/test_backward_reasoner.py`

**Acceptance Criteria**:
- [x] Finds all applicable theorems for a goal
- [x] Correctly generates sub-goals
- [x] Ranking is sensible
- [x] All tests pass

---

#### Task 9.2: ProofEngine Core Loop (Days 4-5)
**Owner**: Developer 3
**Duration**: 2 days

**Subtasks**:
1. Implement `ProofEngine` class
2. Main method: `prove(initial_facts: FactBase, goals: list[Fact], theorem_base: TheoremBase, strategy: SearchStrategy, config: Config) -> ProofResult`

3. Algorithm:
   ```
   state = ProofState(fact_base=initial_facts, goals=goals)
   start_time = time.now()

   # Initial forward reasoning
   forward_reasoner.reason(state, theorem_base, max_depth=2)

   while state.goals and not timeout(start_time, config.timeout):
     # Check if any goals are already satisfied
     for goal in state.goals:
       if state.is_goal_satisfied(goal):
         state.remove_goal(goal)
         state.proven_goals.append(goal)

     if not state.goals:
       break  # All goals proven!

     # Select next goal to work on
     current_goal = strategy.select_goal(state)
     if not current_goal:
       break  # No more goals to try

     # Find theorem candidates (backward reasoning)
     candidates = backward_reasoner.find_theorem_candidates(
       current_goal, theorem_base, state
     )

     if not candidates:
       # No theorem can prove this goal directly
       state.failed_goals.append(current_goal)
       state.remove_goal(current_goal)
       continue

     # Try each candidate
     success = False
     for candidate in candidates:
       # Apply theorem
       if len(candidate.sub_goals) == 0:
         # All premises already satisfied
         new_facts = theorem_applier.apply(candidate.theorem, candidate.binding)
         for fact in new_facts:
           state.add_fact(fact)
         state.proof_tree.add_application(candidate.theorem, candidate.binding)
         state.increment_theorem_usage(candidate.theorem.id)

         # Check if goal is now satisfied
         if state.is_goal_satisfied(current_goal):
           state.remove_goal(current_goal)
           state.proven_goals.append(current_goal)
           success = True
           break
       else:
         # Add sub-goals to goal list
         for sub_goal in candidate.sub_goals:
           state.add_goal(sub_goal)
         success = True
         break  # Try this candidate

     if success:
       # Do local forward reasoning
       forward_reasoner.reason(state, theorem_base, max_depth=1)
     else:
       # No candidate worked
       state.failed_goals.append(current_goal)
       state.remove_goal(current_goal)

   # Build result
   result = ProofResult(
     success=(len(state.failed_goals) == 0),
     proof_tree=state.proof_tree,
     proven_goals=state.proven_goals,
     failed_goals=state.failed_goals,
     statistics=gather_statistics(state, start_time)
   )

   return result
   ```

**Dependencies**: Tasks 8.1, 9.1

**Test Requirements**:
- Test on simple proof problems
- Test timeout handling
- Test partial success cases

**Deliverables**:
- `proof/engine.py`
- `tests/test_proof_engine.py`

**Acceptance Criteria**:
- [x] Can prove simple theorems
- [x] Handles timeouts gracefully
- [x] Returns correct ProofResult

---

### Week 10: Integration & Simple Proofs

#### Task 10.1: End-to-End Integration (Days 1-2)
**Owner**: All Developers
**Duration**: 2 days

**Subtasks**:
1. Integrate all Phase 1-3 components
2. Test complete pipeline: DSL → Facts → Proof
3. Fix integration issues

**Dependencies**: All previous tasks

**Test Cases**:
1. **Isosceles triangle**
2. **Parallel lines alternate angles**
3. **Triangle angle sum**
4. **Congruent triangles (SSS)**

**Deliverables**:
- `tests/integration/test_phase3_complete_proofs.py`

**Acceptance Criteria**:
- [x] Can prove all test cases end-to-end
- [x] No integration errors

---

#### Task 10.2: Simple Proof Examples (Days 3-4)
**Owner**: Developer 2, Developer 3
**Duration**: 2 days

**Subtasks**:
1. Create 20 simple proof problems
2. Test proof engine on each
3. Analyze success rate and failure modes
4. Document limitations

**Problem Categories**:
- Basic triangle properties (5 problems)
- Parallel line angles (5 problems)
- Congruence (5 problems)
- Circle properties (5 problems)

**Dependencies**: Task 10.1

**Deliverables**:
- `examples/simple_proofs/` directory with 20 problems
- Success rate report
- Known limitations document

**Acceptance Criteria**:
- [x] System solves at least 80% of simple problems
- [x] Failures are understood and documented

---

#### Task 10.3: Performance Optimization (Day 5)
**Owner**: Developer 1
**Duration**: 1 day

**Subtasks**:
1. Profile proof engine
2. Identify bottlenecks
3. Optimize critical paths:
   - FactBase queries
   - Pattern matching
   - Theorem candidate selection

4. Add caching where appropriate

**Dependencies**: Task 10.2

**Deliverables**:
- Performance profiling report
- Optimized code

**Acceptance Criteria**:
- [x] Typical proofs complete in < 5 seconds
- [x] No obvious performance issues

---

### Phase 3 Deliverables Summary

**Code Deliverables**:
- ProofTree, ProofNode
- ProofState
- ProofResult
- SearchStrategy (BFS, DFS, Best-First)
- ForwardReasoner
- BackwardReasoner
- ProofEngine (main orchestrator)

**Test Deliverables**:
- 20+ simple proof problems
- Integration tests for complete pipeline

**Documentation**:
- Proof engine architecture
- Search strategy guide
- Known limitations

**Milestone**: Can prove simple theorems end-to-end without auxiliary lines

---

## Phase 4: Numeric Solver (Weeks 11-12)

**Goal**: Add numeric validation and constraint solving to enhance proof search.

**Team Focus**: Integrate numeric grounding

---

### Week 11: Constraint Solving

#### Task 11.1: Constraint System Design (Day 1)
**Owner**: Team Lead
**Duration**: 1 day

**Subtasks**:
1. Define constraint types:
   - Distance constraints: `|AB| = c`, `|AB| = |CD|`
   - Angle constraints: `∠ABC = c`, `∠ABC = ∠DEF`
   - Position constraints: `P on line(AB)`, `P on circle(O, r)`
   - Parallel/perpendicular: Special angle constraints

2. Design constraint representation
3. Choose solving approach:
   - **Option 1**: Algebraic solver (closed-form solutions)
   - **Option 2**: Numerical optimization (gradient descent)
   - **Hybrid**: Algebraic when possible, numerical fallback

**Dependencies**: None

**Deliverables**:
- `docs/constraint_system_design.md`
- Constraint representation classes in `solver/constraints.py`

**Acceptance Criteria**:
- [x] All constraint types covered
- [x] Solving approach chosen and justified

---

#### Task 11.2: Constraint Representation (Days 1-2)
**Owner**: Developer 1
**Duration**: 1.5 days

**Subtasks**:
1. Implement `Constraint` base class
2. Implement specific constraint types:
   - `DistanceConstraint`
   - `AngleConstraint`
   - `PositionConstraint` (on line, on circle)
   - `ParallelConstraint`
   - `PerpendicularConstraint`

3. Convert constraints to equations/inequalities

**Dependencies**: Task 11.1

**Deliverables**:
- `solver/constraints.py`
- `tests/test_constraints.py`

**Acceptance Criteria**:
- [x] All constraint types implemented
- [x] Can convert to numeric equations

---

#### Task 11.3: Basic Algebraic Solver (Days 2-4)
**Owner**: Developer 2
**Duration**: 2.5 days

**Subtasks**:
1. Implement `AlgebraicSolver` class
2. Solve simple configurations analytically:
   - Two points with distance constraint
   - Three points forming triangle
   - Point on line
   - Point on circle

3. Use SymPy for symbolic math

4. Handle under-constrained systems:
   - Choose canonical/simple solution
   - Fix free variables to reasonable values

**Dependencies**: Task 11.2

**Test Requirements**:
- Test solving various configurations
- Test under-constrained cases
- Test over-constrained/inconsistent cases

**Deliverables**:
- `solver/algebraic_solver.py`
- `tests/test_algebraic_solver.py`

**Acceptance Criteria**:
- [x] Can solve simple configurations
- [x] Handles common cases correctly
- [x] Detects inconsistencies

---

#### Task 11.4: Numerical Optimization Solver (Days 4-5)
**Owner**: Developer 3
**Duration**: 1.5 days

**Subtasks**:
1. Implement `NumericalSolver` class using scipy.optimize
2. Convert constraints to objective function (sum of squared errors)
3. Use initial guess (e.g., random or heuristic placement)
4. Optimize to find satisfying configuration

**Dependencies**: Task 11.2

**Test Requirements**:
- Test on configurations that algebraic solver can't handle
- Test convergence
- Test with different initial guesses

**Deliverables**:
- `solver/numerical_solver.py`
- `tests/test_numerical_solver.py`

**Acceptance Criteria**:
- [x] Can solve complex configurations
- [x] Converges in reasonable time (< 1s)

---

#### Task 11.5: ConstraintSolver Integration (Day 5)
**Owner**: Developer 1
**Duration**: 1 day

**Subtasks**:
1. Implement `ConstraintSolver` facade class
2. Try algebraic solver first, fallback to numerical
3. Handle solver failures gracefully

**Dependencies**: Tasks 11.3, 11.4

**Deliverables**:
- `solver/constraint_solver.py`
- `tests/test_constraint_solver.py`

**Acceptance Criteria**:
- [x] Unified interface for constraint solving
- [x] Fallback works correctly

---

### Week 12: Numeric Validation

#### Task 12.1: NumericModel Implementation (Days 1-2)
**Owner**: Developer 2
**Duration**: 2 days

**Subtasks**:
1. Implement `NumericModel` class
   - Stores point coordinates: `dict[Point, (x, y)]`
   - Stores line equations
   - Stores circle parameters

2. Methods:
   - `get_coords(point: Point) -> tuple[float, float]`
   - `set_coords(point: Point, coords: tuple[float, float])`
   - `compute_distance(p1: Point, p2: Point) -> float`
   - `compute_angle(p1: Point, vertex: Point, p2: Point) -> float`
   - `is_on_line(point: Point, line: Line, tolerance: float) -> bool`
   - `is_parallel(line1: Line, line2: Line, tolerance: float) -> bool`
   - `is_perpendicular(line1: Line, line2: Line, tolerance: float) -> bool`

3. Build from GeometryModel + ConstraintSolver

**Dependencies**: Task 11.5

**Deliverables**:
- `solver/numeric_model.py`
- `tests/test_numeric_model.py`

**Acceptance Criteria**:
- [x] Stores numeric representation of geometry
- [x] Geometric computations work correctly

---

#### Task 12.2: GeometryCalculator Utilities (Day 2)
**Owner**: Developer 3
**Duration**: 1 day

**Subtasks**:
1. Implement `GeometryCalculator` class with static methods:
   - `distance(p1: tuple, p2: tuple) -> float`
   - `angle(p1: tuple, vertex: tuple, p2: tuple) -> float`
   - `line_equation(p1: tuple, p2: tuple) -> (a, b, c)`
   - `point_line_distance(point: tuple, line_eq: tuple) -> float`
   - `lines_parallel(line1_eq: tuple, line2_eq: tuple, tol: float) -> bool`
   - `lines_perpendicular(line1_eq: tuple, line2_eq: tuple, tol: float) -> bool`
   - `circle_contains(center: tuple, radius: float, point: tuple, tol: float) -> bool`
   - `area_triangle(p1: tuple, p2: tuple, p3: tuple) -> float`

**Dependencies**: None (parallel with Task 12.1)

**Test Requirements**:
- Unit tests for each function
- Test edge cases (zero length, degenerate triangles)

**Deliverables**:
- `solver/geometry_calculator.py`
- `tests/test_geometry_calculator.py`

**Acceptance Criteria**:
- [x] All geometric calculations implemented
- [x] Results are numerically accurate

---

#### Task 12.3: NumericChecker Implementation (Days 3-4)
**Owner**: Developer 1, Developer 2
**Duration**: 2 days

**Subtasks**:
1. Implement `NumericChecker` class
2. Method: `check_fact(fact: Fact, model: NumericModel, tolerance: float) -> bool`
   - For each Fact type, verify numerically
   - Example: `EqualSegment(AB, CD)` → check `|distance(A,B) - distance(C,D)| < tolerance`

3. Method: `check_conditions(conditions: list[Condition], binding: dict, model: NumericModel) -> bool`

4. Support all Fact types

**Dependencies**: Tasks 12.1, 12.2

**Test Requirements**:
- Test checking various Fact types
- Test tolerance handling
- Test when model is unavailable

**Deliverables**:
- `solver/numeric_checker.py`
- `tests/test_numeric_checker.py`

**Acceptance Criteria**:
- [x] Can validate all Fact types numerically
- [x] Tolerance-based checking works
- [x] Gracefully handles missing numeric model

---

#### Task 12.4: Integration with Proof Engine (Days 4-5)
**Owner**: Developer 3
**Duration**: 1.5 days

**Subtasks**:
1. Integrate NumericModel into ProofState
2. Use NumericChecker in TheoremMatcher:
   - After symbolic matching, validate numerically
   - Prune candidates that fail numeric checks

3. Use NumericChecker in ConditionsChecker

4. Configure tolerance (default: 1e-6)

**Dependencies**: Tasks 8.1, 9.1, 12.3

**Deliverables**:
- Updated `theorem_matcher.py`
- Updated `conditions_checker.py`
- Integration tests

**Acceptance Criteria**:
- [x] Numeric validation integrated into proof search
- [x] Invalid theorem applications are pruned
- [x] Proof search is more efficient

---

#### Task 12.5: Testing with Numeric Validation (Day 5)
**Owner**: All Developers
**Duration**: 0.5 day

**Subtasks**:
1. Re-run all proof tests with numeric validation enabled
2. Measure performance improvement
3. Identify cases where numeric validation helps

**Dependencies**: Task 12.4

**Deliverables**:
- Performance comparison report

**Acceptance Criteria**:
- [x] All previous tests still pass
- [x] Performance improvement demonstrated

---

### Phase 4 Deliverables Summary

**Code Deliverables**:
- Constraint representation classes
- AlgebraicSolver
- NumericalSolver
- ConstraintSolver (facade)
- NumericModel
- GeometryCalculator utilities
- NumericChecker
- Integration with ProofEngine

**Documentation**:
- Constraint system design
- Solver usage guide

**Tests**:
- Unit tests for all solver components
- Integration tests with proof engine

**Milestone**: Proof search enhanced with numeric validation and pruning

---

## Phase 5: Auxiliary Construction Search (Weeks 13-15)

**Goal**: Automatically propose auxiliary constructions when proof gets stuck.

**Team Focus**: Enable solving complex problems requiring auxiliary lines

---

### Week 13: Auxiliary Infrastructure

#### Task 13.1: AuxPattern YAML Format Design (Day 1)
**Owner**: Team Lead
**Duration**: 1 day

**Subtasks**:
1. Design YAML schema for auxiliary patterns
2. Create example patterns
3. Document pattern specification

**YAML Template**:
```yaml
- id: TRIANGLE_MIDPOINT_CONNECTOR
  name: 三角形中位线
  version: "1.0"
  preconditions:
    - Triangle({A}, {B}, {C})
  constructions:
    - type: Midpoint
      params:
        segment: [{A}, {B}]
        midpoint: {M}
    - type: Midpoint
      params:
        segment: [{A}, {C}]
        midpoint: {N}
    - type: Connect
      params:
        points: [{M}, {N}]
        line: {L_MN}
  expected_facts:
    - Parallel(Line({M}{N}), Line({B}{C}))
    - ProportionalSegment(Segment({M}{N}), Segment({B}{C}), 0.5)
  tags: [triangle, parallel, midline]
  priority: 6
  cost: 2
  notes: "中位线平行于第三边且等于第三边的一半"
```

**Dependencies**: None

**Deliverables**:
- `data/schemas/aux_pattern_schema.json`
- Example patterns in `data/aux_patterns/examples.yaml`

**Acceptance Criteria**:
- [x] Schema covers all pattern attributes
- [x] Examples validate

---

#### Task 13.2: AuxConstruction Types (Days 1-2)
**Owner**: Developer 1
**Duration**: 1.5 days

**Subtasks**:
1. Implement `AuxConstruction` class
   - Attributes: `aux_type`, `anchors`, `new_objects`, `predicted_facts`, `score`, `cost`

2. Define auxiliary construction types:
   - `MidpointConstruction`
   - `PerpendicularConstruction`
   - `ParallelConstruction`
   - `AngleBisectorConstruction`
   - `ReflectionConstruction`
   - `ConnectionConstruction`
   - `CircumcircleConstruction`
   - `IncircleConstruction`
   - etc.

3. Each type knows how to:
   - Validate its parameters
   - Generate new geometric objects
   - Predict new Facts

**Dependencies**: Task 13.1

**Deliverables**:
- `auxiliary_search/aux_types.py`
- `tests/test_aux_types.py`

**Acceptance Criteria**:
- [x] All common construction types implemented
- [x] Each type can generate objects and facts

---

#### Task 13.3: AuxPattern Implementation (Days 2-3)
**Owner**: Developer 2
**Duration**: 1.5 days

**Subtasks**:
1. Implement `AuxPattern` class
   - All attributes from YAML schema
   - Methods: `matches_configuration(fact_base: FactBase) -> list[Binding]`

2. Pattern matching logic:
   - Match preconditions against FactBase
   - Generate bindings

**Dependencies**: Tasks 13.1, 13.2

**Deliverables**:
- `auxiliary_search/aux_patterns.py`
- `tests/test_aux_patterns.py`

**Acceptance Criteria**:
- [x] AuxPattern represents pattern correctly
- [x] Matching works

---

#### Task 13.4: PatternLoader for Auxiliary Patterns (Days 3-4)
**Owner**: Developer 3
**Duration**: 1.5 days

**Subtasks**:
1. Implement `AuxPatternLoader` class (similar to TheoremLoader)
2. Load patterns from YAML files
3. Validate against schema
4. Convert to AuxPattern objects

**Dependencies**: Task 13.3

**Deliverables**:
- `auxiliary_search/pattern_loader.py`
- `tests/test_pattern_loader.py`

**Acceptance Criteria**:
- [x] Can load patterns from YAML
- [x] Validation works

---

#### Task 13.5: Write Basic Auxiliary Pattern Library (Days 4-5)
**Owner**: Developer 2, Developer 3
**Duration**: 1.5 days

**Subtasks**:
1. Write 15-20 common auxiliary patterns

**Pattern Categories**:

**Triangles** (`data/aux_patterns/triangles.yaml`):
- Midpoint of two sides + connect (midline)
- Altitude (perpendicular from vertex to opposite side)
- Median (line from vertex to midpoint of opposite side)
- Angle bisector
- Perpendicular bisector of a side

**Circles** (`data/aux_patterns/circles.yaml`):
- Connect center to point on circle (radius)
- Tangent line at point on circle
- Circumcircle of triangle
- Incircle of triangle

**Parallels** (`data/aux_patterns/parallels.yaml`):
- Parallel line through external point
- Perpendicular to one of two parallel lines

**Reflections** (`data/aux_patterns/reflections.yaml`):
- Reflect point across line
- Reflect point across point (180° rotation)

**Dependencies**: Task 13.1

**Deliverables**:
- 3-4 YAML files with 15-20 patterns

**Acceptance Criteria**:
- [x] At least 15 patterns written
- [x] All validate against schema

---

### Week 14: Candidate Generation & Evaluation

#### Task 14.1: CandidateGenerator Implementation (Days 1-3)
**Owner**: Developer 1, Developer 2
**Duration**: 3 days

**Subtasks**:

**Day 1: Structure Recognition**
1. Implement structure recognition in FactBase:
   - Find all triangles
   - Find all parallel line pairs
   - Find all circles
   - Find all equal segments/angles

**Day 2: Pattern Matching**
2. Implement `CandidateGenerator` class
3. Method: `generate(state: ProofState, goal: Fact, patterns: list[AuxPattern]) -> list[AuxConstruction]`

4. Algorithm:
   ```
   candidates = []
   structures = recognize_structures(state.fact_base)

   for pattern in patterns:
     for structure in structures:
       bindings = pattern.matches_configuration(state.fact_base, structure)
       for binding in bindings:
         # Instantiate construction
         construction = instantiate_construction(pattern, binding)

         # Filter: don't create already-existing objects
         if not already_exists(construction, state.geometry_model):
           candidates.append(construction)

   # Deduplicate
   candidates = deduplicate(candidates)

   return candidates
   ```

**Day 3: Filtering & Deduplication**
5. Filter duplicates
6. Filter constructions that already exist

**Dependencies**: Tasks 13.3, 13.4

**Test Requirements**:
- Test structure recognition
- Test candidate generation on various configurations
- Test deduplication

**Deliverables**:
- `auxiliary_search/candidate_generator.py`
- `tests/test_candidate_generator.py`

**Acceptance Criteria**:
- [x] Can generate candidates from patterns
- [x] Deduplication works
- [x] No obviously redundant candidates

---

#### Task 14.2: Evaluator Implementation (Days 3-5)
**Owner**: Developer 3
**Duration**: 2.5 days

**Subtasks**:
1. Implement `AuxEvaluator` class
2. Method: `score(construction: AuxConstruction, goal: Fact, state: ProofState, numeric_model: NumericModel) -> float`

3. Scoring factors:

   **Goal Relevance** (weight: 0.3):
   - Does construction involve points/lines in the goal?
   - Score: ratio of shared points

   **Theorem Unlocking** (weight: 0.4):
   - Simulate adding construction's predicted facts
   - Count how many theorems become applicable
   - Higher score for more unlocked theorems

   **Numeric Reasonableness** (weight: 0.2):
   - If numeric model available, check if predicted facts are numerically plausible
   - E.g., for midpoint: check if distances are approximately equal

   **Cost** (weight: -0.1):
   - Number of new objects created
   - Complexity of construction

4. Formula:
   ```
   score = w1 * goal_relevance
         + w2 * theorem_unlocking
         + w3 * numeric_fit
         - w4 * cost
   ```

**Dependencies**: Tasks 12.1, 14.1

**Test Requirements**:
- Test scoring for various constructions
- Test that useful constructions score high

**Deliverables**:
- `auxiliary_search/evaluator.py`
- `tests/test_evaluator.py`

**Acceptance Criteria**:
- [x] Scoring incorporates all factors
- [x] Scores are reasonable
- [x] Useful constructions rank higher

---

### Week 15: Integration with Proof Engine

#### Task 15.1: Search Strategy (Days 1-2)
**Owner**: Developer 1
**Duration**: 2 days

**Subtasks**:
1. Implement `AuxSearchStrategy` class
2. Decide when to trigger auxiliary search:
   - After N proof steps without progress
   - When backward reasoning finds no candidates
   - Configurable trigger

3. Implement search mode:
   - **Best-First**: Try highest scored construction
   - **Top-K**: Try top K constructions
   - **Iterative Deepening**: Try 1 construction, then 2, etc.

4. Implement limits:
   - Max constructions per proof
   - Max candidates to try
   - Timeout

**Dependencies**: Task 14.2

**Deliverables**:
- `auxiliary_search/strategy.py`
- `tests/test_aux_strategy.py`

**Acceptance Criteria**:
- [x] Strategy decides when to search
- [x] Limits are enforced
- [x] Different search modes work

---

#### Task 15.2: Applier Implementation (Days 2-3)
**Owner**: Developer 2
**Duration**: 1.5 days

**Subtasks**:
1. Implement `AuxApplier` class
2. Method: `apply(construction: AuxConstruction, geometry_model: GeometryModel, fact_base: FactBase, proof_tree: ProofTree) -> (updated_model, updated_facts)`

3. Steps:
   - Create new geometric objects (points, lines)
   - Add to GeometryModel
   - Generate new Facts
   - Add Facts to FactBase
   - Record construction in ProofTree

4. Validation:
   - Check for name conflicts
   - Validate geometric validity

**Dependencies**: Tasks 13.2, 14.1

**Test Requirements**:
- Test applying various construction types
- Test model and fact updates
- Test proof tree recording

**Deliverables**:
- `auxiliary_search/applier.py`
- `tests/test_aux_applier.py`

**Acceptance Criteria**:
- [x] Can apply all construction types
- [x] Model and facts updated correctly
- [x] Proof tree records construction

---

#### Task 15.3: Integration with ProofEngine (Days 3-4)
**Owner**: Developer 3
**Duration**: 1.5 days

**Subtasks**:
1. Add auxiliary search to ProofEngine main loop
2. Trigger when stuck:
   ```python
   if no_progress_for(state, N_steps):
     # Try auxiliary constructions
     candidates = aux_search.search(state, goal, numeric_model)

     for construction in candidates[:top_k]:
       # Apply construction
       applier.apply(construction, state.geometry_model, state.fact_base, state.proof_tree)

       # Continue proof search
       result = continue_proof_search(state)

       if result.success:
         return result  # Success with auxiliary line!
       else:
         # Backtrack: undo construction
         undo_construction(construction, state)
   ```

3. Implement backtracking for unsuccessful constructions

**Dependencies**: Tasks 9.2, 15.1, 15.2

**Deliverables**:
- Updated `proof/engine.py`
- Integration tests

**Acceptance Criteria**:
- [x] Auxiliary search integrated into proof loop
- [x] Backtracking works
- [x] Can solve problems requiring auxiliary lines

---

#### Task 15.4: Testing with Auxiliary Constructions (Days 4-5)
**Owner**: All Developers
**Duration**: 1.5 days

**Subtasks**:
1. Create test problems requiring auxiliary lines
2. Test proof engine with auxiliary search enabled
3. Measure success rate improvement

**Test Problems**:
1. **Triangle midline theorem**: Requires connecting two midpoints
2. **Altitude properties**: Requires drawing altitude
3. **Angle bisector theorem**: Requires drawing angle bisector
4. **Perpendicular bisector**: Requires constructing perpendicular bisector
5. **Circumcenter**: Requires finding intersection of perpendicular bisectors

**Dependencies**: Task 15.3

**Deliverables**:
- `tests/integration/test_auxiliary_search.py`
- 10+ test problems
- Success rate report

**Acceptance Criteria**:
- [x] System solves problems requiring auxiliary lines
- [x] Success rate > 50% for test problems
- [x] Constructions are meaningful (not random)

---

### Phase 5 Deliverables Summary

**Code Deliverables**:
- AuxConstruction types
- AuxPattern class
- AuxPatternLoader
- CandidateGenerator
- AuxEvaluator
- AuxSearchStrategy
- AuxApplier
- Integration with ProofEngine

**Data Deliverables**:
- 15-20 auxiliary patterns in YAML

**Documentation**:
- Auxiliary pattern specification
- Auxiliary search design

**Tests**:
- Unit tests for all components
- Integration tests with proof engine
- Test problems requiring auxiliary lines

**Milestone**: Can automatically find and apply auxiliary constructions

---

## Phase 6: Visualization & Polish (Weeks 16-18)

**Goal**: Build user-facing features: proof formatting, diagram rendering, and APIs.

**Team Focus**: Make the system usable and presentable

---

### Week 16: Proof Formatting

#### Task 16.1: Natural Language Template Engine (Days 1-2)
**Owner**: Developer 1
**Duration**: 2 days

**Subtasks**:
1. Implement template substitution engine
2. Replace placeholders like `{A}`, `{B}` with actual point names
3. Support both Chinese and English templates

**Template Example**:
```
"因为{A}{B} = {A}{C},所以△{A}{B}{C}为等腰三角形,根据等腰三角形性质,底角相等,即∠{B}{A}{C} = ∠{C}{A}{B}。"
→
"因为AB = AC,所以△ABC为等腰三角形,根据等腰三角形性质,底角相等,即∠BAC = ∠CAB。"
```

**Dependencies**: None

**Deliverables**:
- `visualization/template_engine.py`
- `tests/test_template_engine.py`

**Acceptance Criteria**:
- [x] Can substitute placeholders
- [x] Handles Chinese and English

---

#### Task 16.2: ProofFormatter Implementation (Days 2-4)
**Owner**: Developer 2, Developer 3
**Duration**: 2.5 days

**Subtasks**:
1. Implement `ProofFormatter` class
2. Method: `format_proof(proof_result: ProofResult, language: str = 'cn') -> str`

3. Algorithm:
   - Traverse ProofTree in logical order
   - For each step (theorem application or auxiliary construction):
     - Get natural language template
     - Substitute variables
     - Format as numbered step

4. Output format:
   ```
   证明:
   1. 已知: AB = AC (given)
   2. 因此△ABC为等腰三角形 (by definition)
   3. 根据等腰三角形性质,底角相等 (定理: ISO_TRIANGLE_BASE_ANGLES)
   4. 所以∠ABC = ∠ACB (结论)
   ```

5. Support different formats:
   - Plain text
   - Markdown
   - HTML

**Dependencies**: Tasks 7.1, 16.1

**Test Requirements**:
- Test formatting various proofs
- Test both languages
- Test different output formats

**Deliverables**:
- `visualization/proof_formatter.py`
- `tests/test_proof_formatter.py`

**Acceptance Criteria**:
- [x] Generates readable proof steps
- [x] Both languages work
- [x] Multiple output formats supported

---

#### Task 16.3: Proof Statistics (Day 4)
**Owner**: Developer 1
**Duration**: 1 day

**Subtasks**:
1. Add statistics collection to ProofEngine
2. Statistics to collect:
   - Total proof steps
   - Theorems used (with counts)
   - Auxiliary constructions used
   - Search nodes explored
   - Time taken
   - Success/failure reasons

3. Format statistics nicely in proof output

**Dependencies**: Task 9.2

**Deliverables**:
- Updated `proof/engine.py`
- Statistics formatting in `proof_formatter.py`

**Acceptance Criteria**:
- [x] Statistics collected correctly
- [x] Displayed in proof output

---

#### Task 16.4: Proof Validation (Day 5)
**Owner**: Developer 3
**Duration**: 1 day

**Subtasks**:
1. Implement proof validator
2. Method: `validate_proof(proof_result: ProofResult) -> bool`
3. Check:
   - All steps are valid theorem applications
   - Facts in each step are correct
   - Goal is actually proven

**Dependencies**: Task 7.3

**Deliverables**:
- `proof/validator.py`
- `tests/test_validator.py`

**Acceptance Criteria**:
- [x] Can validate correct proofs
- [x] Detects invalid proofs

---

### Week 17: Diagram Rendering

#### Task 17.1: Layout Algorithm (Days 1-2)
**Owner**: Developer 1
**Duration**: 2 days

**Subtasks**:
1. Implement automatic point placement for diagrams
2. If NumericModel available: use coordinates from solver
3. If not available: use heuristic layout
   - Force-directed graph layout
   - Constraint-based layout

4. Handle special cases:
   - Triangles: place in canonical position
   - Circles: center and size
   - Parallel lines: visually parallel

**Dependencies**: Task 12.1

**Deliverables**:
- `visualization/layout.py`
- `tests/test_layout.py`

**Acceptance Criteria**:
- [x] Generates reasonable layouts
- [x] Diagrams are readable

---

#### Task 17.2: Renderer Implementation (Days 2-4)
**Owner**: Developer 2, Developer 3
**Duration**: 2.5 days

**Subtasks**:
1. Implement `Renderer` class using Matplotlib
2. Render geometric objects:
   - Points: dots with labels
   - Lines/Segments: lines
   - Circles: circles
   - Angles: arc annotations

3. Highlighting:
   - Highlight specific objects (different color/thickness)
   - Show equal markings (tick marks for equal segments, arcs for equal angles)
   - Show parallel/perpendicular symbols

4. Annotations:
   - Label points
   - Label lengths
   - Label angles

**Dependencies**: Task 17.1

**Test Requirements**:
- Test rendering various geometries
- Test highlighting
- Visual inspection of output images

**Deliverables**:
- `visualization/renderer.py`
- `tests/test_renderer.py`
- Example rendered images

**Acceptance Criteria**:
- [x] Can render all geometric objects
- [x] Diagrams are clear and readable
- [x] Highlighting works

---

#### Task 17.3: DiagramGenerator (Days 4-5)
**Owner**: Developer 1
**Duration**: 1.5 days

**Subtasks**:
1. Implement `DiagramGenerator` class
2. Method: `generate_diagram(geometry_model: GeometryModel, numeric_model: NumericModel, highlights: dict) -> Image`
3. Combine layout + rendering
4. Support different output formats: PNG, SVG, PDF

**Dependencies**: Tasks 17.1, 17.2

**Deliverables**:
- `visualization/diagram_generator.py`
- `tests/test_diagram_generator.py`

**Acceptance Criteria**:
- [x] Generates complete diagrams
- [x] Multiple output formats work

---

#### Task 17.4: Animated Proof Viewer (Day 5)
**Owner**: Developer 3
**Duration**: 1 day

**Subtasks**:
1. Implement step-by-step diagram updates
2. Show diagram state at each proof step
3. Highlight objects involved in current step
4. Export as GIF or video

**Dependencies**: Tasks 17.3, 16.2

**Deliverables**:
- `visualization/animated_viewer.py`
- Example animated proof

**Acceptance Criteria**:
- [x] Can generate animated proofs
- [x] Steps are clear

---

### Week 18: API & Documentation

#### Task 18.1: ProofAPI Implementation (Days 1-2)
**Owner**: Developer 1
**Duration**: 2 days

**Subtasks**:
1. Implement `ProofAPI` class as main entry point
2. Methods:
   ```python
   def prove_from_dsl(dsl_text: str, config: Config = None) -> ProofResult
   def prove_from_file(file_path: str, config: Config = None) -> ProofResult
   def prove_from_model(geometry_model: GeometryModel, goals: list[Fact], config: Config = None) -> ProofResult
   def format_proof(proof_result: ProofResult, format: str = 'text', language: str = 'cn') -> str
   def generate_diagram(proof_result: ProofResult, step: int = -1) -> Image
   ```

3. Handle full pipeline orchestration
4. Error handling and user-friendly messages

**Dependencies**: All previous phases

**Deliverables**:
- `api/proof_api.py`
- `tests/test_proof_api.py`

**Acceptance Criteria**:
- [x] Clean, simple API
- [x] Error messages are helpful
- [x] All functions work end-to-end

---

#### Task 18.2: Configuration System (Day 2)
**Owner**: Developer 2
**Duration**: 1 day

**Subtasks**:
1. Implement `Config` class
2. Support loading from YAML file
3. Support overriding with parameters
4. Default configuration values

**Config Options**:
- Theorem library path
- Auxiliary pattern library path
- Search strategy
- Max proof depth, timeout
- Auxiliary search settings
- Numeric solver settings
- Visualization settings
- Language preference

**Dependencies**: None

**Deliverables**:
- `api/config.py`
- Default `config.yaml`
- `tests/test_config.py`

**Acceptance Criteria**:
- [x] Config system works
- [x] Can load from file or parameters

---

#### Task 18.3: Command-Line Interface (Days 3-4)
**Owner**: Developer 3
**Duration**: 1.5 days

**Subtasks**:
1. Implement CLI using argparse or click
2. Commands:
   ```
   geometry-prover prove <file.dsl> [--output <result.txt>]
   geometry-prover prove <file.dsl> --diagram <output.png>
   geometry-prover prove <file.dsl> --verbose
   geometry-prover validate <proof.json>
   geometry-prover list-theorems [--category <cat>]
   ```

3. Support options for configuration
4. Pretty-print results to console

**Dependencies**: Task 18.1

**Deliverables**:
- `cli/main.py`
- Installation script (setup.py or pyproject.toml)

**Acceptance Criteria**:
- [x] CLI works
- [x] All commands functional
- [x] Help messages are clear

---

#### Task 18.4: Documentation (Days 4-5)
**Owner**: All Developers
**Duration**: 1.5 days

**Subtasks**:
1. Write user guide:
   - Installation
   - DSL syntax
   - Running proofs
   - Configuration
   - Examples

2. Write API reference (auto-generate from docstrings)

3. Write developer guide:
   - Architecture overview
   - Adding theorems
   - Adding auxiliary patterns
   - Extending fact types

4. Create example notebooks (Jupyter)

**Dependencies**: All previous tasks

**Deliverables**:
- `docs/user_guide.md`
- `docs/api_reference.md`
- `docs/developer_guide.md`
- `docs/dsl_syntax.md`
- `examples/notebooks/` with 5+ notebooks

**Acceptance Criteria**:
- [x] Documentation is complete and clear
- [x] Examples work
- [x] New users can get started easily

---

#### Task 18.5: Example Gallery (Day 5)
**Owner**: Developer 2
**Duration**: 1 day

**Subtasks**:
1. Create 20+ example problems with solutions
2. Organize by difficulty and topic
3. Include diagrams and formatted proofs
4. Create gallery webpage (static HTML)

**Dependencies**: Task 18.1

**Deliverables**:
- `examples/gallery/` with 20+ examples
- `examples/gallery/index.html`

**Acceptance Criteria**:
- [x] Examples cover various topics
- [x] Gallery is visually appealing
- [x] All examples run successfully

---

### Phase 6 Deliverables Summary

**Code Deliverables**:
- Template substitution engine
- ProofFormatter (text, markdown, HTML output)
- Proof validator
- Layout algorithm
- Renderer (Matplotlib-based)
- DiagramGenerator
- Animated proof viewer
- ProofAPI (main entry point)
- Configuration system
- Command-line interface

**Documentation**:
- User guide
- API reference
- Developer guide
- DSL syntax reference
- Example notebooks

**Examples**:
- 20+ example problems
- Example gallery webpage

**Milestone**: Complete, usable system with visualization and documentation

---

## Phase 7: Testing & Optimization (Weeks 19-20)

**Goal**: Ensure robustness, correctness, and performance.

**Team Focus**: Quality assurance and optimization

---

### Week 19: Comprehensive Testing

#### Task 19.1: Test Suite Expansion (Days 1-2)
**Owner**: Developer 1, Developer 2
**Duration**: 2 days

**Subtasks**:
1. Expand unit test coverage to 90%+
2. Add tests for edge cases:
   - Empty input
   - Malformed DSL
   - Impossible proofs
   - Degenerate geometry
   - Over-constrained systems

3. Add property-based tests (using Hypothesis)

**Dependencies**: All previous phases

**Deliverables**:
- Expanded test suite
- Coverage report

**Acceptance Criteria**:
- [x] Test coverage > 90%
- [x] All edge cases covered

---

#### Task 19.2: Integration Test Suite (Days 2-3)
**Owner**: Developer 3
**Duration**: 1.5 days

**Subtasks**:
1. Create 50+ integration test problems
2. Cover all major geometry topics:
   - Triangles (15 problems)
   - Parallel/perpendicular (10 problems)
   - Circles (10 problems)
   - Quadrilaterals (5 problems)
   - Similarity/congruence (5 problems)
   - Complex multi-step proofs (5 problems)

3. Test success rate

**Dependencies**: All previous phases

**Deliverables**:
- `tests/integration/test_suite_50_problems.py`
- Success rate report

**Acceptance Criteria**:
- [x] 50+ problems tested
- [x] Success rate > 75%

---

#### Task 19.3: Stress Testing (Days 3-4)
**Owner**: Developer 1
**Duration**: 1.5 days

**Subtasks**:
1. Test with large theorem libraries (100+ theorems)
2. Test with complex proofs (20+ steps)
3. Test with large fact bases (1000+ facts)
4. Memory profiling
5. Identify and fix memory leaks

**Dependencies**: Task 19.2

**Deliverables**:
- Stress test suite
- Performance report

**Acceptance Criteria**:
- [x] System handles large inputs
- [x] No memory leaks
- [x] Performance degrades gracefully

---

#### Task 19.4: Failure Analysis (Days 4-5)
**Owner**: All Developers
**Duration**: 1.5 days

**Subtasks**:
1. Analyze failed proofs from integration tests
2. Categorize failures:
   - Missing theorems
   - Missing auxiliary patterns
   - Search depth insufficient
   - Numeric solver issues
   - Bugs

3. Fix bugs
4. Document known limitations
5. Create issue tracker for unsupported cases

**Dependencies**: Task 19.2

**Deliverables**:
- Failure analysis report
- Bug fixes
- Known limitations document

**Acceptance Criteria**:
- [x] Failures understood
- [x] Bugs fixed
- [x] Limitations documented

---

### Week 20: Optimization

#### Task 20.1: Performance Profiling (Days 1-2)
**Owner**: Developer 1
**Duration**: 2 days

**Subtasks**:
1. Profile proof engine on representative problems
2. Identify bottlenecks:
   - FactBase queries
   - Pattern matching
   - Theorem candidate selection
   - Numeric validation

3. Measure time spent in each module

**Dependencies**: Task 19.3

**Deliverables**:
- Profiling report with bottlenecks identified
- Flame graphs

**Acceptance Criteria**:
- [x] Bottlenecks identified
- [x] Profiling data collected

---

#### Task 20.2: FactBase Optimization (Day 2-3)
**Owner**: Developer 2
**Duration**: 1.5 days

**Subtasks**:
1. Optimize FactBase indexing
2. Use better data structures:
   - Hash maps for fast lookup
   - Spatial indices for geometric queries
   - Inverted indices for pattern matching

3. Benchmark before/after

**Dependencies**: Task 20.1

**Deliverables**:
- Optimized `fact_base.py`
- Performance comparison

**Acceptance Criteria**:
- [x] FactBase queries 2x+ faster
- [x] All tests still pass

---

#### Task 20.3: Pattern Matching Optimization (Day 3-4)
**Owner**: Developer 3
**Duration**: 1.5 days

**Subtasks**:
1. Optimize pattern matching algorithm
2. Cache matching results
3. Use early termination
4. Optimize theorem candidate ranking

**Dependencies**: Task 20.1

**Deliverables**:
- Optimized `fact_matcher.py` and `theorem_matcher.py`
- Performance comparison

**Acceptance Criteria**:
- [x] Matching 2x+ faster
- [x] All tests still pass

---

#### Task 20.4: Caching Strategy (Day 4-5)
**Owner**: Developer 1
**Duration**: 1.5 days

**Subtasks**:
1. Implement caching for:
   - Theorem matching results
   - Pattern parsing results
   - Numeric validation results
   - Layout computations

2. Use LRU cache with reasonable limits
3. Measure cache hit rates

**Dependencies**: Task 20.1

**Deliverables**:
- Caching implementation
- Cache performance report

**Acceptance Criteria**:
- [x] Caching speeds up repeated operations
- [x] Memory usage is reasonable

---

#### Task 20.5: Final Performance Benchmarks (Day 5)
**Owner**: All Developers
**Duration**: 1 day

**Subtasks**:
1. Re-run all performance benchmarks
2. Compare with baseline (Phase 3)
3. Document performance improvements
4. Ensure all tests still pass

**Dependencies**: Tasks 20.2, 20.3, 20.4

**Deliverables**:
- Final performance report
- Performance comparison table

**Acceptance Criteria**:
- [x] Overall performance improved by 3x+
- [x] Typical proofs complete in < 2 seconds
- [x] All tests pass

---

### Phase 7 Deliverables Summary

**Testing**:
- 90%+ code coverage
- 50+ integration test problems
- Stress tests for large inputs
- Failure analysis and categorization

**Optimization**:
- Optimized FactBase (2x+ faster)
- Optimized pattern matching (2x+ faster)
- Caching strategy implemented
- Overall 3x+ performance improvement

**Documentation**:
- Known limitations document
- Performance benchmarks

**Milestone**: Production-ready, well-tested, optimized system

---

## Phase 8: Advanced Features (Weeks 21+)

**Goal**: Optional enhancements beyond core functionality.

**Team Focus**: Innovation and advanced capabilities

*(This phase is optional and can be prioritized based on project needs)*

---

### Advanced Feature Ideas

#### Feature 8.1: Interactive Web UI (Weeks 21-23)
**Owner**: Frontend Developer + Backend Developer
**Duration**: 3 weeks

**Description**:
- Web-based interface for the proof system
- Interactive diagram editor
- Live proof execution with step-by-step visualization
- Share and save proofs

**Technologies**:
- Frontend: React/Vue.js
- Backend: FastAPI or Flask
- Diagram: D3.js or Three.js

**Deliverables**:
- Web application
- REST API for proof system
- Deployment guide

---

#### Feature 8.2: Advanced Numeric Solver (Weeks 21-22)
**Owner**: Developer with optimization background
**Duration**: 2 weeks

**Description**:
- More sophisticated constraint solving
- Handle algebraic constraints (square roots, trigonometric functions)
- Multiple solution handling
- Symbolic + numeric hybrid solving

**Technologies**:
- SymPy for symbolic math
- SciPy for numerical optimization
- Interval arithmetic for robust solving

**Deliverables**:
- Enhanced solver module
- Support for more complex constraints

---

#### Feature 8.3: 3D Geometry Support (Weeks 23-25)
**Owner**: Developer with 3D graphics experience
**Duration**: 3 weeks

**Description**:
- Extend DSL for 3D constructions
- 3D fact types (planes, spheres, etc.)
- 3D theorem library
- 3D rendering

**Technologies**:
- 3D rendering: Three.js or VTK
- 3D constraint solving

**Deliverables**:
- 3D extension to system
- 3D theorem library
- 3D visualization

---

#### Feature 8.4: Competition-Level Problem Solving (Weeks 24-26)
**Owner**: Mathematician + Developer
**Duration**: 3 weeks

**Description**:
- Advanced theorem library for competition problems
- IMO, USAMO level problems
- More sophisticated auxiliary construction strategies
- Heuristics for difficult problems

**Deliverables**:
- Extended theorem library (100+ theorems)
- Advanced auxiliary patterns
- Test suite of competition problems

---

#### Feature 8.5: Export to Formal Proof Systems (Weeks 25-27)
**Owner**: Developer familiar with proof assistants
**Duration**: 3 weeks

**Description**:
- Export proofs to Coq, Lean, or Isabelle
- Formal verification of proofs
- Bridge to formal mathematics community

**Technologies**:
- Coq/Lean/Isabelle APIs

**Deliverables**:
- Export module
- Example formal proofs
- Documentation

---

#### Feature 8.6: Machine Learning Integration (Weeks 26-28)
**Owner**: ML Engineer + Developer
**Duration**: 3 weeks

**Description**:
- Learn auxiliary construction strategies from examples
- Learn theorem ranking heuristics
- Learn goal selection strategies
- Neural theorem proving

**Technologies**:
- PyTorch or TensorFlow
- Graph neural networks for geometric structures

**Deliverables**:
- ML models for various components
- Training pipeline
- Evaluation on benchmarks

---

#### Feature 8.7: Multi-Language Support (Week 24)
**Owner**: Developer with i18n experience
**Duration**: 1 week

**Description**:
- Full internationalization support
- Additional languages beyond CN/EN: French, German, Spanish, Russian, Japanese, Korean

**Deliverables**:
- i18n infrastructure
- Translations for multiple languages

---

#### Feature 8.8: Proof Search Visualization (Week 25)
**Owner**: Developer
**Duration**: 1 week

**Description**:
- Visualize the search tree
- Show which theorem candidates were tried
- Debug proof search process

**Deliverables**:
- Search tree visualization
- Interactive search exploration tool

---

## Team Allocation & Responsibilities

### Recommended Team Structure

**Core Team (3-5 people)**:

1. **Team Lead / Architect**
   - Overall architecture
   - Code reviews
   - Integration coordination
   - Risk management

2. **Developer 1 - Core Engine Specialist**
   - Focus: Facts, Theorems, Proof Engine
   - Primary responsibility: Phases 1-3

3. **Developer 2 - Algorithms Specialist**
   - Focus: Numeric Solver, Optimization
   - Primary responsibility: Phase 4, Phase 7

4. **Developer 3 - Search & AI Specialist**
   - Focus: Auxiliary Construction Search
   - Primary responsibility: Phase 5

5. **Developer 4 - Frontend / Visualization (Optional)**
   - Focus: Visualization, UI
   - Primary responsibility: Phase 6

**Consulting Roles**:

- **Mathematician**: Validate theorems, suggest improvements
- **QA Engineer**: Testing strategy, test automation
- **Technical Writer**: Documentation

---

### Collaboration Model

**Weekly Schedule**:
- Monday: Sprint planning, task assignment
- Tuesday-Thursday: Development, pair programming
- Friday: Code review, integration, sprint retrospective

**Daily Standups**: 15 minutes
- What did you do yesterday?
- What will you do today?
- Any blockers?

**Code Reviews**: All code must be reviewed before merging

**Pair Programming**: Encouraged for complex tasks

---

## Risk Management

### Identified Risks & Mitigation Strategies

#### Risk 1: Proof Search Complexity
**Description**: Proof search may not converge or may be too slow.

**Mitigation**:
- Implement timeout and depth limits
- Use numeric validation for early pruning
- Optimize search strategies
- Monitor performance continuously

**Contingency**: Fall back to simpler heuristics

---

#### Risk 2: Numeric Solver Failures
**Description**: Constraint solver may fail on complex/over-constrained systems.

**Mitigation**:
- Use hybrid algebraic + numerical approach
- Handle solver failures gracefully
- Don't rely solely on numeric validation

**Contingency**: Proceed with symbolic reasoning only

---

#### Risk 3: Theorem Library Completeness
**Description**: Theorem library may be incomplete for certain problems.

**Mitigation**:
- Start with well-known geometry curriculum
- Prioritize common theorems
- Make it easy to add new theorems
- Gather feedback from users

**Contingency**: Document unsupported problem types

---

#### Risk 4: Auxiliary Construction Search Effectiveness
**Description**: Auxiliary search may propose irrelevant constructions.

**Mitigation**:
- Use goal-driven heuristics
- Implement good scoring function
- Limit number of constructions tried
- Learn from examples (Phase 8)

**Contingency**: Allow manual hints for auxiliary constructions

---

#### Risk 5: Performance Bottlenecks
**Description**: System may be too slow for practical use.

**Mitigation**:
- Profile early and often
- Optimize critical paths
- Use efficient data structures
- Implement caching

**Contingency**: Reduce search space, add more aggressive pruning

---

#### Risk 6: Integration Complexity
**Description**: Integrating many modules may be challenging.

**Mitigation**:
- Define clear interfaces early
- Frequent integration testing
- Use modular architecture
- Continuous integration pipeline

**Contingency**: Simplify interfaces, reduce coupling

---

## Quality Assurance Strategy

### Testing Strategy

**Unit Tests**:
- Every module has unit tests
- Target: 80%+ coverage
- Use pytest framework

**Integration Tests**:
- Test full pipeline on real problems
- Maintain regression test suite
- Run on every commit

**Performance Tests**:
- Benchmark critical operations
- Track performance over time
- Set performance budgets

**Manual Testing**:
- User acceptance testing
- Usability testing
- Edge case exploration

---

### Code Quality Standards

**Code Style**:
- Follow PEP 8
- Use black for auto-formatting
- Use type hints (mypy checking)

**Documentation**:
- All public functions have docstrings (Google style)
- Complex algorithms have explanatory comments
- Module-level documentation

**Code Reviews**:
- All code reviewed by at least one other developer
- Check for correctness, efficiency, readability
- Automated checks in CI/CD

---

### Continuous Integration

**CI Pipeline**:
1. Lint check (pylint, black)
2. Type check (mypy)
3. Run unit tests
4. Run integration tests
5. Check test coverage
6. Build documentation
7. (Optional) Run performance benchmarks

**Triggers**:
- Every push to feature branch
- Every pull request
- Nightly builds

---

## Appendix: Task Dependencies Graph

*(Visual representation of task dependencies can be generated)*

**Critical Path**:
Phase 1 → Phase 2 → Phase 3 → (Phase 4, Phase 5) → Phase 6 → Phase 7

**Parallelizable Work**:
- Phase 4 and Phase 5 can be done in parallel after Phase 3
- Within each phase, many tasks can be parallelized

---

## Appendix: Effort Estimation

| Phase | Duration | Effort (person-weeks) |
|-------|----------|----------------------|
| Phase 1 | 3 weeks | 9 |
| Phase 2 | 3 weeks | 9 |
| Phase 3 | 4 weeks | 12 |
| Phase 4 | 2 weeks | 6 |
| Phase 5 | 3 weeks | 9 |
| Phase 6 | 3 weeks | 9 |
| Phase 7 | 2 weeks | 6 |
| **Total** | **20 weeks** | **60 person-weeks** |

**With 3 developers**: 20 weeks (5 months)
**With 5 developers**: 12-15 weeks (3-4 months) with efficient parallelization

---

## Summary

This detailed development plan provides:

✅ **Week-by-week breakdown** of all 20 weeks
✅ **Day-by-day task allocation** for each week
✅ **Clear dependencies** between tasks
✅ **Specific acceptance criteria** for every task
✅ **Test requirements** for quality assurance
✅ **Deliverables** for each task and phase
✅ **Code examples and algorithms** where helpful
✅ **Team allocation and responsibilities**
✅ **Risk management strategy**
✅ **Quality assurance plan**

**This plan is ready to guide implementation!**

The development team can:
1. Start immediately with Phase 1, Week 1, Task 1.1
2. Follow the plan week by week
3. Track progress against milestones
4. Adjust as needed based on actual progress

Each developer knows exactly what to work on, when, and what the acceptance criteria are. The plan balances ambitious goals with practical achievability.
