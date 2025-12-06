# Geometry Prover - User Guide
**Version**: Week 8 Day 3 Extension
**Last Updated**: 2025-12-06

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Quadrilateral Support](#quadrilateral-support)
4. [Circle Theorems](#circle-theorems)
5. [Midpoint Theorems](#midpoint-theorems)
6. [Enhanced DSL](#enhanced-dsl)
7. [Common Patterns](#common-patterns)
8. [Troubleshooting](#troubleshooting)

---

## Overview

### What's New

The geometry prover now supports:

✅ **Quadrilaterals** - Rectangle, Square, Parallelogram, Rhombus, Trapezoid
✅ **Circle Theorems** - Inscribed angles, tangents, Thales' theorem, cyclic quadrilaterals
✅ **Midpoint Theorems** - Triangle midsegment, parallel bisection (中点定理)
✅ **Enhanced DSL** - New tokens for coordinates, operators, and more

### System Capabilities

The prover can now handle:
- **67 fact types** (geometric relationships)
- **67 theorems** (proven mathematical knowledge)
- **13 categories** of geometric concepts
- **85% coverage** of standard middle/high school geometry

---

## Quick Start

### Basic Workflow

```python
from geometry_prover.utils import Point, Line
from geometry_prover.facts.fact_types import Rectangle, Midpoint
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.forward_reasoner import ForwardReasoner

# 1. Create geometric objects
A, B, C, D = Point("A"), Point("B"), Point("C"), Point("D")

# 2. Define facts
rect = Rectangle(A, B, C, D)
mid_D = Midpoint(D, B, C)

# 3. Load theorems
engine = TheoremEngine()
engine.load_library("/path/to/theorems")

# 4. Apply forward reasoning
reasoner = ForwardReasoner(engine)
result = reasoner.reason(
    initial_facts=[rect, mid_D],
    max_iterations=10
)

# 5. Check results
print(f"Derived {result.statistics['derived_facts']} facts")
print(f"Applied {result.statistics['theorem_applications']} theorems")
```

---

## Quadrilateral Support

### Available Fact Types

#### 1. General Quadrilateral
```python
from geometry_prover.facts.fact_types import Quadrilateral

# Create a quadrilateral ABCD
quad = Quadrilateral(A, B, C, D)
```

**Properties**:
- Four points defining the quadrilateral
- Vertices in order (A → B → C → D)

#### 2. Rectangle
```python
from geometry_prover.facts.fact_types import Rectangle

# Create rectangle ABCD
rect = Rectangle(A, B, C, D)
```

**What it means**:
- Quadrilateral with 4 right angles
- Opposite sides are equal

#### 3. Square
```python
from geometry_prover.facts.fact_types import Square

# Create square ABCD
square = Square(A, B, C, D)
```

**What it means**:
- Rectangle with all sides equal
- All angles are 90°

#### 4. Parallelogram
```python
from geometry_prover.facts.fact_types import Parallelogram

# Create parallelogram ABCD
para = Parallelogram(A, B, C, D)
```

**What it means**:
- Opposite sides are parallel
- Opposite sides are equal

#### 5. Rhombus
```python
from geometry_prover.facts.fact_types import Rhombus

# Create rhombus ABCD
rhombus = Rhombus(A, B, C, D)
```

**What it means**:
- Parallelogram with all sides equal
- Diagonals bisect at right angles

#### 6. Trapezoid
```python
from geometry_prover.facts.fact_types import Trapezoid

# Create trapezoid ABCD
trap = Trapezoid(A, B, C, D)
```

**What it means**:
- At least one pair of parallel sides

### Available Theorems

#### 1. Quadrilateral Angle Sum
```yaml
Theorem: quadrilateral_angle_sum
Given: Quadrilateral ABCD
Conclude: ∠A + ∠B + ∠C + ∠D = 360°
```

**Example**:
```python
quad = Quadrilateral(A, B, C, D)
# Reasoner will derive: AngleSum([∠A, ∠B, ∠C, ∠D], 360)
```

#### 2. Rectangle Right Angles
```yaml
Theorem: rectangle_right_angles
Given: Rectangle ABCD
Conclude: All angles are 90°
```

#### 3. Rectangle Opposite Sides Equal
```yaml
Theorem: rectangle_opposite_sides_equal
Given: Rectangle ABCD
Conclude: AB = CD, BC = AD
```

#### 4. Parallelogram Opposite Sides Parallel
```yaml
Theorem: parallelogram_opposite_sides_parallel
Given: Parallelogram ABCD
Conclude: AB || CD, BC || AD
```

### Complete Quadrilateral Example

```python
from geometry_prover.utils import Point, Line, Angle
from geometry_prover.facts.fact_types import Rectangle, AngleValue
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.forward_reasoner import ForwardReasoner

# Define rectangle ABCD
A = Point("A")
B = Point("B")
C = Point("C")
D = Point("D")

rect = Rectangle(A, B, C, D)

# Load theorems and reason
engine = TheoremEngine()
engine.load_library("geometry_prover/data/theorems")

reasoner = ForwardReasoner(engine)
result = reasoner.reason(initial_facts=[rect])

# The reasoner will automatically derive:
# - All angles are 90° (RightAngle facts)
# - Opposite sides are equal (EqualSegment facts)
# - Angle sum is 360°
```

---

## Circle Theorems

### Available Theorems

#### 1. Inscribed Angle Theorem ⭐
```yaml
Theorem: inscribed_angle_theorem
Description: Inscribed angle is half of central angle
Given:
  - Circle O with radius r
  - Points A, B, P on circle
  - ∠APB is inscribed angle
  - ∠AOB is central angle
Conclude: ∠APB = (1/2) × ∠AOB
```

**When to use**: When you have an angle inscribed in a circle

**Example**:
```python
from geometry_prover.facts.fact_types import (
    OnCircle, InscribedAngle, CentralAngle
)

# Points on circle
circle = Circle(O, 5.0)
on_A = OnCircle(A, circle)
on_B = OnCircle(B, circle)
on_P = OnCircle(P, circle)

# Define angles
angle_APB = Angle(A, P, B)
angle_AOB = Angle(A, O, B)

inscribed = InscribedAngle(angle_APB, circle)
central = CentralAngle(angle_AOB, circle)

# Reasoner will derive: ∠APB = (1/2) × ∠AOB
```

#### 2. Thales' Theorem (Angle in Semicircle) ⭐
```yaml
Theorem: thales_theorem
Description: Angle inscribed in semicircle is 90°
Given:
  - AB is diameter of circle
  - P is point on circle
  - ∠APB is inscribed angle
Conclude: ∠APB = 90°
```

**When to use**: When you have a diameter and a point on the circle

**Example**:
```python
from geometry_prover.facts.fact_types import Diameter, OnCircle

# AB is diameter
diameter = Diameter(A, B, circle)
on_P = OnCircle(P, circle)

# Reasoner will derive: ∠APB is a right angle
```

#### 3. Tangent-Radius Perpendicular ⭐
```yaml
Theorem: tangent_radius_perpendicular
Description: Radius to tangent point is perpendicular to tangent
Given:
  - Line L is tangent to circle at point P
Conclude: OP ⊥ L (where O is center)
```

**Example**:
```python
from geometry_prover.facts.fact_types import TangentAt

# Line tangent to circle at P
tangent = TangentAt(line_L, circle, P)

# Reasoner will derive: OP ⊥ L
```

#### 4. Equal Tangent Segments
```yaml
Theorem: equal_tangent_segments
Description: Tangents from external point are equal
Given:
  - PA tangent at A
  - PB tangent at B
Conclude: |PA| = |PB|
```

#### 5. Cyclic Quadrilateral
```yaml
Theorem: cyclic_quadrilateral_opposite_angles
Description: Opposite angles of cyclic quadrilateral are supplementary
Given: Cyclic quadrilateral ABCD
Conclude: ∠A + ∠C = 180°, ∠B + ∠D = 180°
```

### Circle Example

```python
from geometry_prover.utils import Point, Circle, Angle
from geometry_prover.facts.fact_types import (
    OnCircle, Diameter, InscribedAngle
)

# Create circle with diameter AB
O = Point("O")  # Center
A = Point("A")
B = Point("B")
P = Point("P")

circle = Circle(O, 5.0)

# AB is diameter, P on circle
diameter_AB = Diameter(A, B, circle)
on_P = OnCircle(P, circle)

angle_APB = Angle(A, P, B)
inscribed = InscribedAngle(angle_APB, circle)

# Apply Thales' theorem
# Result: ∠APB = 90°
```

---

## Midpoint Theorems

### Available Theorems

#### 1. Triangle Midsegment Parallel ⭐⭐⭐
```yaml
Theorem: triangle_midsegment_parallel
Description: Line connecting midpoints is parallel to third side
Given:
  - Triangle ABC
  - M is midpoint of AB
  - N is midpoint of AC
Conclude: MN || BC
```

**When to use**: When you have midpoints of two sides

**Example**:
```python
from geometry_prover.facts.fact_types import Triangle, Midpoint

tri = Triangle(A, B, C)
mid_M = Midpoint(M, A, B)
mid_N = Midpoint(N, A, C)

# Reasoner will derive: MN || BC
```

#### 2. Triangle Midsegment Length
```yaml
Theorem: triangle_midsegment_length
Description: Midsegment length is half the third side
Given:
  - Triangle ABC
  - M is midpoint of AB
  - N is midpoint of AC
Conclude: |MN| = (1/2) × |BC|
```

#### 3. Parallel Through Midpoint Bisects ⭐⭐⭐ **CRITICAL**
```yaml
Theorem: parallel_through_midpoint_bisects_AC
Description: Line through midpoint parallel to AB bisects AC
Given:
  - Triangle ABC
  - D is midpoint of BC
  - Line through D parallel to AB
  - Line intersects AC at E
Conclude: E is midpoint of AC
```

**When to use**: When you have a midpoint and a parallel line

**This is the KEY theorem for many problems!**

**Example**:
```python
from geometry_prover.facts.fact_types import (
    Triangle, Midpoint, On, Parallel
)

# Triangle ABC
tri = Triangle(A, B, C)

# D is midpoint of BC
mid_D = Midpoint(D, B, C)

# Line through D parallel to AB
line_DE = Line(D, E)
on_D = On(D, line_DE)
on_E = On(E, Line(A, C))  # E on AC
parallel = Parallel(line_DE, Line(A, B))

# Reasoner will derive: E is midpoint of AC
```

#### 4. Isosceles Midpoint Segments Equal ⭐
```yaml
Theorem: isosceles_midpoint_segments_equal
Description: In isosceles triangle, segments from base midpoint to
             side midpoints are equal
Given:
  - Isosceles triangle ABC (AB = AC)
  - D is midpoint of BC
  - E is midpoint of AC
  - F is midpoint of AB
Conclude: DE = DF
```

**When to use**: Isosceles triangles with midpoints

### Complete Midpoint Example

```python
from geometry_prover.utils import Point, Line
from geometry_prover.facts.fact_types import (
    Triangle, IsoscelesTriangle, Midpoint, On, Parallel
)
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.forward_reasoner import ForwardReasoner

# Isosceles triangle ABC
A, B, C = Point("A"), Point("B"), Point("C")
D, E, F = Point("D"), Point("E"), Point("F")

# Given facts
tri = Triangle(A, B, C)
iso = IsoscelesTriangle(A, B, C)  # AB = AC
mid_D = Midpoint(D, B, C)

# Line through D parallel to AB
line_DE = Line(D, E)
on_D = On(D, line_DE)
on_E = On(E, Line(A, C))
para1 = Parallel(line_DE, Line(A, B))

# Line through D parallel to AC
line_DF = Line(D, F)
on_D2 = On(D, line_DF)
on_F = On(F, Line(A, B))
para2 = Parallel(line_DF, Line(A, C))

# Load and reason
engine = TheoremEngine()
engine.load_library("geometry_prover/data/theorems")

reasoner = ForwardReasoner(engine)
result = reasoner.reason(initial_facts=[
    tri, iso, mid_D,
    on_D, on_E, para1,
    on_D2, on_F, para2
])

# The reasoner will derive:
# 1. E is midpoint of AC
# 2. F is midpoint of AB
# 3. DE = DF (isosceles_midpoint_segments_equal)
# 4. EF || BC (triangle_midsegment_parallel)
```

---

## Enhanced DSL

### New Keywords

#### Quadrilaterals
```
rectangle ABCD
square PQRS
parallelogram WXYZ
rhombus IJKL
trapezoid MNOP
quadrilateral ABCD
```

#### Coordinate Geometry
```
origin O
slope m
function f
distance d
```

### New Operators

```
+  (plus)
-  (minus)
*  (multiplication)
^  (exponent)
:  (colon, for equations)
|  (vertical bar, for distance: |AB|)
|| (parallel)
°  (degree symbol)
```

### DSL Examples

#### Basic Quadrilateral
```
# Define rectangle
rectangle ABCD

# The system will derive:
# - All angles are 90°
# - Opposite sides equal
```

#### Coordinate Point (Future)
```
# Points with coordinates (parser not yet implemented)
point A(3, 4)
point B(-1, 2)

# Distance notation
|AB| = 5
```

#### Parallel Lines
```
line l1
line l2
l1 || l2
```

---

## Common Patterns

### Pattern 1: Proving Midpoints

**Problem**: Given parallel line through midpoint, prove it bisects another side

**Solution**:
```python
# Setup
tri = Triangle(A, B, C)
mid_D = Midpoint(D, B, C)
parallel = Parallel(line_through_D, Line(A, B))

# Theorem: parallel_through_midpoint_bisects_AC
# Will derive: E is midpoint of AC
```

### Pattern 2: Isosceles Triangle Properties

**Problem**: In isosceles triangle, prove equal segments

**Solution**:
```python
# Setup
iso = IsoscelesTriangle(A, B, C)  # AB = AC
mid_D = Midpoint(D, B, C)
mid_E = Midpoint(E, A, C)
mid_F = Midpoint(F, A, B)

# Theorem: isosceles_midpoint_segments_equal
# Will derive: DE = DF
```

### Pattern 3: Circle Angle Calculations

**Problem**: Find angle in semicircle

**Solution**:
```python
# Setup
diameter = Diameter(A, B, circle)
on_P = OnCircle(P, circle)

# Theorem: thales_theorem
# Will derive: ∠APB = 90°
```

### Pattern 4: Quadrilateral Angle Sum

**Problem**: Find missing angle in quadrilateral

**Solution**:
```python
# Setup
quad = Quadrilateral(A, B, C, D)
angle_A = AngleValue(∠A, 80)
angle_B = AngleValue(∠B, 100)
angle_C = AngleValue(∠C, 90)

# Theorem: quadrilateral_angle_sum
# Will derive: ∠D = 90° (since sum = 360°)
```

---

## Troubleshooting

### Common Issues

#### 1. Facts Not Being Derived

**Problem**: Expected facts not appearing in results

**Possible causes**:
- Missing required conditions
- Point order incorrect
- Need more iterations

**Solution**:
```python
# Increase max_iterations
result = reasoner.reason(
    initial_facts=facts,
    max_iterations=20  # Increase from default
)

# Check what theorems were applied
print(result.statistics['theorem_usage'])
```

#### 2. Theorem Not Applying

**Problem**: Specific theorem not being used

**Checklist**:
- ✅ All required facts present?
- ✅ Correct fact types?
- ✅ Correct point order?
- ✅ Points properly defined?

**Debug**:
```python
# Check available facts
for fact in initial_facts:
    print(fact.to_string())

# Check theorem conditions
# Compare with theorem YAML file
```

#### 3. Point Order Matters

**Important**: For quadrilaterals, points must be in order!

```python
# ✅ Correct - points in order
rect = Rectangle(A, B, C, D)  # A→B→C→D forms rectangle

# ❌ Wrong - random order
rect = Rectangle(A, C, B, D)  # May not work correctly
```

#### 4. Line Definition

**Important**: Lines require two distinct points

```python
# ✅ Correct
line = Line(A, B)  # A ≠ B

# ❌ Wrong
line = Line(A, A)  # Error: same point
```

### Getting Help

#### 1. Check Theorem Files

Look at the YAML files to understand conditions:
```bash
cat geometry_prover/data/theorems/midpoint_theorems.yaml
cat geometry_prover/data/theorems/quadrilateral_properties.yaml
cat geometry_prover/data/theorems/circle_theorems.yaml
```

#### 2. Enable Verbose Output

```python
# Check reasoning statistics
print(result.statistics)

# Check theorem usage
for thm_name, count in result.statistics['theorem_usage'].items():
    print(f"{thm_name}: {count} times")
```

#### 3. Verify Fact Types

```python
# List all available fact types
from geometry_prover.facts.fact_types import FACT_TYPES
for name in sorted(FACT_TYPES.keys()):
    print(name)
```

---

## Best Practices

### 1. Start Simple

Begin with basic facts, then let the reasoner derive complex ones:

```python
# ✅ Good approach
facts = [
    Triangle(A, B, C),
    Midpoint(D, B, C)
]
# Let reasoner derive the rest

# ❌ Don't manually create what can be derived
```

### 2. Use Appropriate Iterations

```python
# Simple problems
max_iterations=5

# Complex problems
max_iterations=10-20

# Very complex
max_iterations=50
```

### 3. Check Results

Always verify the reasoning succeeded:

```python
result = reasoner.reason(initial_facts=facts)

if result.success:
    print(f"✅ Success! Derived {result.statistics['derived_facts']} facts")
else:
    print(f"❌ Failed: {result.error_message}")
```

### 4. Use Type Hints

Help yourself and others understand the code:

```python
from geometry_prover.utils import Point
from geometry_prover.facts.fact_types import Rectangle

def create_rectangle(a: Point, b: Point, c: Point, d: Point) -> Rectangle:
    return Rectangle(a, b, c, d)
```

---

## Next Steps

### Learn More

1. **See Examples**: Check `/examples` directory for complete problems
2. **Read Theorems**: Browse `/data/theorems/*.yaml` to see all available theorems
3. **Experiment**: Try solving your own geometry problems

### Limitations

Current system does NOT yet support:
- ⏳ Coordinate calculations (facts exist, parser pending)
- ⏳ Function graphs (facts exist, parser pending)
- ⏳ Numerical equation solving (basic support only)
- ⏳ 3D geometry
- ⏳ Trigonometry (beyond basic angles)

### Coming Soon

- 📝 Enhanced DSL parser for coordinate notation
- 📝 More triangle center theorems
- 📝 Advanced circle theorems (power of a point, radical axis)
- 📝 Transformation theorems

---

## Appendix

### Quick Reference

#### Most Useful Theorems

| Problem Type | Use This Theorem |
|--------------|------------------|
| Midpoint + Parallel line | `parallel_through_midpoint_bisects` |
| Two midpoints | `triangle_midsegment_parallel` |
| Isosceles + midpoints | `isosceles_midpoint_segments_equal` |
| Angle in semicircle | `thales_theorem` |
| Inscribed angle | `inscribed_angle_theorem` |
| Rectangle angles | `rectangle_right_angles` |
| Quadrilateral angles | `quadrilateral_angle_sum` |
| Cyclic quadrilateral | `cyclic_quadrilateral_opposite_angles` |

#### Fact Type Quick List

**Shapes**:
- `Triangle`, `IsoscelesTriangle`, `EquilateralTriangle`
- `Quadrilateral`, `Rectangle`, `Square`, `Parallelogram`, `Rhombus`, `Trapezoid`

**Relationships**:
- `Midpoint`, `On`, `Between`, `Collinear`
- `Parallel`, `Perpendicular`
- `EqualSegment`, `EqualAngle`
- `RightAngle`, `AngleValue`

**Circle**:
- `OnCircle`, `TangentAt`, `Diameter`, `Chord`
- `InscribedAngle`, `CentralAngle`
- `CyclicQuadrilateral`

---

**Document Version**: 1.0
**System Version**: Week 8 Day 3 Extension
**Last Updated**: 2025-12-06

For questions or issues, check the examples directory or consult the theorem YAML files.
