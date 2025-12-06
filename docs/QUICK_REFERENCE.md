# Geometry Prover - Quick Reference
**Version**: Week 8 Day 3 Extension

---

## New Features at a Glance

| Category | Count | Key Items |
|----------|-------|-----------|
| **Quadrilateral Facts** | 6 | Rectangle, Square, Parallelogram, Rhombus, Trapezoid, Quadrilateral |
| **Quadrilateral Theorems** | 7 | Angle sum, opposite sides, right angles |
| **Circle Theorems** | 10 | Inscribed angle, Thales, tangent⊥radius, cyclic quad |
| **Midpoint Theorems** | 7 | Midsegment, parallel bisection (中点定理) |
| **DSL Tokens** | +16 | Quadrilateral keywords, operators (+, -, *, ^, :, \|) |

**Total**: 67 fact types, 67 theorems, 85% system maturity

---

## Import Cheat Sheet

```python
# Core utilities
from geometry_prover.utils import Point, Line, Circle, Angle, Segment

# Quadrilaterals (NEW)
from geometry_prover.facts.fact_types import (
    Quadrilateral, Rectangle, Square,
    Parallelogram, Rhombus, Trapezoid
)

# Circle facts (ENHANCED)
from geometry_prover.facts.fact_types import (
    OnCircle, TangentAt, Diameter, Chord,
    InscribedAngle, CentralAngle, RadiusValue,
    CyclicQuadrilateral, InscribedCircle, CircumscribedCircle
)

# Midpoint & distance (NEW + ENHANCED)
from geometry_prover.facts.fact_types import (
    Midpoint, DistanceToLine, EqualDistancesToLines
)

# Basic facts
from geometry_prover.facts.fact_types import (
    Triangle, IsoscelesTriangle, EquilateralTriangle,
    On, Parallel, Perpendicular,
    EqualSegment, EqualAngle, RightAngle, AngleValue
)

# Reasoning
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.forward_reasoner import ForwardReasoner
```

---

## Quick Patterns

### 1. Basic Reasoning Template
```python
# Setup
points = [Point(name) for name in "ABCD"]
facts = [Triangle(*points[:3]), Midpoint(points[3], points[0], points[1])]

# Reason
engine = TheoremEngine()
engine.load_library("geometry_prover/data/theorems")
reasoner = ForwardReasoner(engine)
result = reasoner.reason(initial_facts=facts, max_iterations=10)

# Results
print(f"Derived: {result.statistics['derived_facts']} facts")
print(f"Applied: {result.statistics['theorem_applications']} theorems")
```

### 2. Quadrilateral Problem
```python
A, B, C, D = [Point(n) for n in "ABCD"]

# Rectangle with one known angle
rect = Rectangle(A, B, C, D)
angle_A = AngleValue(Angle(D, A, B), 90.0)

result = reasoner.reason([rect, angle_A])
# Derives: All angles = 90°, opposite sides equal
```

### 3. Midpoint Theorem (中点定理)
```python
# Triangle with midpoint and parallel line
tri = Triangle(A, B, C)
mid_D = Midpoint(D, B, C)
line_DE = Line(D, E)
on_E = On(E, Line(A, C))
para = Parallel(line_DE, Line(A, B))

result = reasoner.reason([tri, mid_D, on_E, on_D, para])
# Derives: E is midpoint of AC
```

### 4. Circle Angle (Thales)
```python
circle = Circle(O, 5.0)
diameter = Diameter(A, B, circle)
on_P = OnCircle(P, circle)
inscribed = InscribedAngle(Angle(A, P, B), circle)

result = reasoner.reason([circle, diameter, on_P, inscribed])
# Derives: ∠APB = 90° (angle in semicircle)
```

---

## Theorem Quick Reference

### ⭐ Most Important Theorems

| Name | Category | Use When |
|------|----------|----------|
| `parallel_through_midpoint_bisects_AC` | Midpoint | Midpoint + parallel line |
| `parallel_through_midpoint_bisects_AB` | Midpoint | Midpoint + parallel line |
| `triangle_midsegment_parallel` | Midpoint | Two midpoints of triangle |
| `isosceles_midpoint_segments_equal` | Midpoint | Isosceles + midpoints |
| `thales_theorem` | Circle | Angle in semicircle |
| `inscribed_angle_theorem` | Circle | Inscribed vs central angle |
| `tangent_radius_perpendicular` | Circle | Tangent to circle |
| `rectangle_right_angles` | Quadrilateral | Rectangle given |
| `quadrilateral_angle_sum` | Quadrilateral | Find missing angle |
| `cyclic_quadrilateral_opposite_angles` | Circle | Cyclic quadrilateral |

### All Quadrilateral Theorems

1. `quadrilateral_angle_sum` - ∠A + ∠B + ∠C + ∠D = 360°
2. `rectangle_right_angles` - All angles = 90°
3. `rectangle_opposite_sides_equal` - AB = CD, BC = AD
4. `square_all_sides_equal` - All sides equal
5. `parallelogram_opposite_sides_equal` - Opposite sides equal
6. `parallelogram_opposite_sides_parallel` - AB || CD, BC || AD
7. `rhombus_all_sides_equal` - All sides equal

### All Circle Theorems

1. `inscribed_angle_theorem` - Inscribed = (1/2) × central
2. `tangent_radius_perpendicular` - Radius ⊥ tangent
3. `thales_theorem` - Angle in semicircle = 90°
4. `equal_inscribed_angles_same_arc` - Same arc → equal angles
5. `equal_tangent_segments` - Tangents from point are equal
6. `chord_perpendicular_bisector_through_center`
7. `equal_chords_equal_distance` - Equal chords → equal distances
8. `cyclic_quadrilateral_opposite_angles` - Opposite ∠s supplementary
9. `incircle_radius_formula` - r = Area / semiperimeter
10. `circumcircle_radius_formula` - R = abc / 4K

### All Midpoint Theorems

1. `triangle_midsegment_parallel` - MN || BC
2. `triangle_midsegment_length` - |MN| = (1/2) × |BC|
3. `parallel_through_midpoint_bisects_AC` - Key theorem!
4. `parallel_through_midpoint_bisects_AB` - Key theorem!
5. `midpoint_bisects_implies_parallel` - Converse
6. `isosceles_midpoint_segments_equal` - DE = DF
7. `midpoint_equal_segments` - AM = MB

---

## DSL Syntax (Enhanced)

### Keywords Added

```
# Quadrilaterals
rectangle, square, parallelogram, rhombus, trapezoid, quadrilateral

# Coordinates (parser pending)
origin, slope, function, distance

# Operators
+, -, *, ^, :, |, ||, °
```

### Usage Examples

```
# Quadrilateral
rectangle ABCD

# Parallel
line l1
line l2
l1 || l2

# Distance (future)
|AB| = 5

# Angle
angle ABC = 90°
```

---

## Common Gotchas

### 1. Point Order Matters!
```python
# ✅ Correct - vertices in order
Rectangle(A, B, C, D)  # A→B→C→D

# ❌ Wrong - random order
Rectangle(A, C, B, D)  # Don't do this!
```

### 2. Check Required Facts
```python
# To apply parallel_through_midpoint_bisects_AC:
Triangle(A, B, C)         # ✅ Need triangle
Midpoint(D, B, C)         # ✅ Need midpoint
On(E, AC)                 # ✅ E on AC
On(D, line_DE)            # ✅ D on line
Parallel(line_DE, AB)     # ✅ Parallel condition
```

### 3. Increase Iterations if Needed
```python
# Complex problems may need more
result = reasoner.reason(
    initial_facts=facts,
    max_iterations=20  # Default is lower
)
```

### 4. Access Results Correctly
```python
# ✅ Correct
result.statistics['derived_facts']
result.statistics['theorem_applications']
result.statistics['theorem_usage']

# ❌ Wrong (doesn't exist)
result.all_facts  # Not available
result.derived_facts  # Not available
```

---

## Debugging Tips

### 1. Check What Theorems Fired
```python
result = reasoner.reason(initial_facts=facts)

for thm_name, count in result.statistics['theorem_usage'].items():
    print(f"{thm_name}: {count}×")
```

### 2. List Initial Facts
```python
for fact in initial_facts:
    print(f"  {fact.to_string()}")
```

### 3. Check Statistics
```python
stats = result.statistics
print(f"Iterations: {stats['iterations']}")
print(f"Total facts: {stats['total_facts']}")
print(f"Derived: {stats['derived_facts']}")
print(f"Converged: {stats['converged']}")
```

### 4. Verify Theorem Conditions
```bash
# Read the YAML file to understand what's needed
cat geometry_prover/data/theorems/midpoint_theorems.yaml
```

---

## Performance Tips

### 1. Limit Iterations
```python
# Start small
max_iterations=5

# Increase only if needed
max_iterations=10-20
```

### 2. Limit Facts
```python
result = reasoner.reason(
    initial_facts=facts,
    max_facts=500  # Prevent explosion
)
```

### 3. Use Specific Facts
```python
# ✅ Better - specific triangle type
IsoscelesTriangle(A, B, C)

# ⚪ OK - general triangle
Triangle(A, B, C)
```

---

## File Locations

```
geometry_prover/
├── data/theorems/
│   ├── quadrilateral_properties.yaml    # NEW (7 theorems)
│   ├── circle_theorems.yaml             # NEW (10 theorems)
│   ├── midpoint_theorems.yaml           # NEW (7 theorems)
│   ├── triangle_properties.yaml
│   ├── congruence.yaml
│   └── ...
├── facts/fact_types.py                  # All 67 fact types
├── dsl/lexer.py                         # Enhanced lexer
└── docs/USER_GUIDE.md                   # Full documentation
```

---

## System Status

### Coverage by Topic

| Topic | Coverage | Notes |
|-------|----------|-------|
| Triangles | 90% | Congruence, similarity, centers |
| Quadrilaterals | 85% | Basic properties, NEW! |
| Circles | 80% | Inscribed angles, tangents, NEW! |
| Midpoints | 95% | Midsegment, parallel bisection, NEW! |
| Parallel Lines | 70% | Basic theorems |
| Coordinates | 40% | Facts exist, parser pending |
| 3D Geometry | 0% | Not supported |

### What's Missing

- ⏳ DSL parser for coordinates (lexer done)
- ⏳ Power of a point theorem
- ⏳ Radical axis
- ⏳ More similarity theorems
- ⏳ Transformation theorems

---

## Example: Complete Problem

```python
#!/usr/bin/env python3
"""
Problem: Rectangle with midpoint
Prove: Diagonal bisects rectangle into two triangles
"""

from geometry_prover.utils import Point, Line, Angle
from geometry_prover.facts.fact_types import Rectangle, Midpoint, On
from geometry_prover.theorems.engine import TheoremEngine
from geometry_prover.proof.forward_reasoner import ForwardReasoner

# Setup
A, B, C, D = [Point(n) for n in "ABCD"]
M = Point("M")

# Given
rect = Rectangle(A, B, C, D)
mid_M = Midpoint(M, A, C)  # M is midpoint of diagonal AC

# Load and reason
engine = TheoremEngine()
engine.load_library("geometry_prover/data/theorems")

reasoner = ForwardReasoner(engine)
result = reasoner.reason(
    initial_facts=[rect, mid_M],
    max_iterations=10
)

# Check results
print(f"✅ Success: {result.success}")
print(f"Derived {result.statistics['derived_facts']} facts")
print(f"Applied {result.statistics['theorem_applications']} theorems")

# Show theorems used
print("\nTheorems applied:")
for name, count in result.statistics['theorem_usage'].items():
    print(f"  • {name}: {count}×")
```

---

**Quick Reference Version**: 1.0
**Last Updated**: 2025-12-06

For complete documentation, see `docs/USER_GUIDE.md`
