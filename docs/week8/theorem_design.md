# Week 8 Theorem Design Document

**Date**: 2025-12-06
**Goal**: Expand theorem library from 13 to 28+ theorems
**Status**: Day 1 - Planning & Design

---

## Executive Summary

Week 8 will add 15+ new theorems across three major categories to enable solving complex geometry problems involving triangles, parallel line angles, and triangle congruence.

**Current State**: 13 theorems (equality, parallel, basic angles)
**Target State**: 28+ theorems (adding triangles, congruence, advanced angles)

---

## Existing Fact Types (Already Available!)

Good news: The geometry_prover already has comprehensive fact types defined in `fact_types.py`:

### Triangle Facts
- ✅ `Triangle(p1, p2, p3)` - Triangle with three vertices
- ✅ `IsoscelesTriangle(p1, p2, p3)` - Isosceles triangle
- ✅ `EquilateralTriangle(p1, p2, p3)` - Equilateral triangle
- ✅ `CongruentTriangle(p1,p2,p3, p4,p5,p6)` - Triangle congruence
- ✅ `SimilarTriangle(p1,p2,p3, p4,p5,p6)` - Triangle similarity
- ✅ `NonDegenerateTriangle(p1, p2, p3)` - Valid triangle
- ✅ `RightAngle(angle)` - 90° angle

### Angle Facts
- ✅ `EqualAngle(angle1, angle2)` - Angle equality
- ✅ `AngleSum(angle1, angle2, value)` - Angle sum
- ✅ `AngleValue(angle, value)` - Angle measurement
- ✅ `SupplementaryAngle(angle1, angle2)` - Supplementary angles

### Line/Segment Facts
- ✅ `Parallel(line1, line2)` - Parallel lines
- ✅ `Perpendicular(line1, line2)` - Perpendicular lines
- ✅ `EqualSegment(seg1, seg2)` - Segment equality
- ✅ `On(point, line)` - Point on line
- ✅ `Collinear(p1, p2, p3)` - Collinear points

**Conclusion**: No new fact types needed! Can proceed directly to theorem creation.

---

## New Theorems to Create (15 theorems)

### Category 1: Triangle Properties (5 theorems)

#### 1. Triangle Angle Sum
**Name**: `triangle_angle_sum`
**Category**: `triangle_properties`

**Conditions**:
```yaml
- type: Triangle
  point1: ?A
  point2: ?B
  point3: ?C
```

**Conclusions**:
```yaml
- type: AngleSum
  angle1: ?ABC  # Angle at B
  angle2: ?BCA  # Angle at C
  value: ?angle_180_minus_CAB  # Special handling needed
```

**Challenge**: Requires numeric angle addition (180° = ∠A + ∠B + ∠C)
**Solution**: Defer to Phase 4 (Numeric Solver) OR create simpler versions

#### 2. Exterior Angle Theorem
**Name**: `exterior_angle_theorem`
**Category**: `triangle_properties`

**Description**: An exterior angle of a triangle equals the sum of the two non-adjacent interior angles

**Conditions**:
```yaml
- type: Triangle
  point1: ?A
  point2: ?B
  point3: ?C
- type: Collinear  # D is on extension of BC
  point1: ?B
  point2: ?C
  point3: ?D
```

**Conclusions**:
```yaml
- type: EqualAngle
  angle1: ?ACD  # Exterior angle
  angle2: ?sum_of_A_and_B  # Sum of remote interior angles
```

**Challenge**: Requires angle addition
**Solution**: Create simplified version OR defer

#### 3. Isosceles Triangle - Converse
**Name**: `isosceles_converse`
**Category**: `triangle_properties`

**Description**: If base angles are equal, then the triangle is isosceles

**Conditions**:
```yaml
- type: Triangle
  point1: ?A
  point2: ?B
  point3: ?C
- type: EqualAngle
  angle1: ?ABC
  angle2: ?ACB
```

**Conclusions**:
```yaml
- type: EqualSegment
  segment1: ?AB
  segment2: ?AC
- type: IsoscelesTriangle
  point1: ?A
  point2: ?B
  point3: ?C
```

**Status**: ✅ Can implement immediately

#### 4. Equilateral Triangle Properties
**Name**: `equilateral_all_angles_equal`
**Category**: `triangle_properties`

**Conditions**:
```yaml
- type: EquilateralTriangle
  point1: ?A
  point2: ?B
  point3: ?C
```

**Conclusions**:
```yaml
- type: EqualAngle
  angle1: ?ABC
  angle2: ?BCA
- type: EqualAngle
  angle1: ?ABC
  angle2: ?CAB
```

**Status**: ✅ Can implement immediately

#### 5. Right Triangle - Pythagorean (Symbolic)
**Name**: `right_triangle_sides`
**Category**: `triangle_properties`

**Description**: In right triangle, relationship between sides

**Conditions**:
```yaml
- type: Triangle
  point1: ?A
  point2: ?B
  point3: ?C
- type: RightAngle
  angle: ?ABC  # Right angle at B
```

**Conclusions**:
```yaml
- type: PythagoreanRelation
  hypotenuse: ?AC
  leg1: ?AB
  leg2: ?BC
```

**Status**: ✅ Already exists in example_theorems.yaml
**Action**: Move to main theorem library

---

### Category 2: Parallel Lines & Angles (5 theorems)

#### 6. Alternate Interior Angles
**Name**: `alternate_interior_angles`
**Category**: `parallel_angles`

**Description**: When two parallel lines are cut by a transversal, alternate interior angles are equal

**Conditions**:
```yaml
- type: Parallel
  line1: ?AB
  line2: ?CD
- type: On
  point: ?P
  line: ?EF  # Transversal
- type: On
  point: ?Q
  line: ?EF  # Transversal
- type: On
  point: ?P
  line: ?AB
- type: On
  point: ?Q
  line: ?CD
```

**Conclusions**:
```yaml
- type: EqualAngle
  angle1: ?EPA  # Alternate interior angle 1
  angle2: ?FQD  # Alternate interior angle 2
```

**Challenge**: Complex geometry with transversal
**Status**: ⚠️ Requires careful pattern design

#### 7. Corresponding Angles
**Name**: `corresponding_angles`
**Category**: `parallel_angles`

**Description**: When parallel lines cut by transversal, corresponding angles are equal

**Status**: ⚠️ Similar complexity to alternate interior

#### 8. Consecutive Interior Angles (Supplementary)
**Name**: `consecutive_interior_supplementary`
**Category**: `parallel_angles`

**Description**: Consecutive interior angles are supplementary (sum to 180°)

**Conditions**:
```yaml
- type: Parallel
  line1: ?AB
  line2: ?CD
# ... transversal conditions
```

**Conclusions**:
```yaml
- type: SupplementaryAngle
  angle1: ?angle1
  angle2: ?angle2
```

**Status**: ✅ Can implement with SupplementaryAngle fact

#### 9-10. Additional Parallel Theorems
- Perpendicular transversal theorem
- Parallel through point theorem

---

### Category 3: Triangle Congruence (5 theorems)

#### 11. SSS Congruence
**Name**: `sss_congruence`
**Category**: `congruence`

**Description**: Side-Side-Side congruence

**Conditions**:
```yaml
- type: Triangle
  point1: ?A
  point2: ?B
  point3: ?C
- type: Triangle
  point1: ?D
  point2: ?E
  point3: ?F
- type: EqualSegment
  segment1: ?AB
  segment2: ?DE
- type: EqualSegment
  segment1: ?BC
  segment2: ?EF
- type: EqualSegment
  segment1: ?CA
  segment2: ?FD
```

**Conclusions**:
```yaml
- type: CongruentTriangle
  p1: ?A
  p2: ?B
  p3: ?C
  p4: ?D
  p5: ?E
  p6: ?F
```

**Status**: ✅ Can implement immediately

#### 12. SAS Congruence
**Name**: `sas_congruence`
**Category**: `congruence`

**Description**: Side-Angle-Side congruence

**Conditions**:
```yaml
- type: EqualSegment
  segment1: ?AB
  segment2: ?DE
- type: EqualAngle
  angle1: ?ABC
  angle2: ?DEF
- type: EqualSegment
  segment1: ?BC
  segment2: ?EF
```

**Conclusions**:
```yaml
- type: CongruentTriangle
  p1: ?A
  p2: ?B
  p3: ?C
  p4: ?D
  p5: ?E
  p6: ?F
```

**Status**: ✅ Can implement immediately

#### 13. ASA Congruence
**Name**: `asa_congruence`
**Category**: `congruence`

**Description**: Angle-Side-Angle congruence

**Status**: ✅ Can implement immediately

#### 14. AAS Congruence
**Name**: `aas_congruence`
**Category**: `congruence`

**Description**: Angle-Angle-Side congruence

**Status**: ✅ Can implement immediately

#### 15. HL Congruence (Right Triangles)
**Name**: `hl_congruence`
**Category**: `congruence`

**Description**: Hypotenuse-Leg congruence for right triangles

**Conditions**:
```yaml
- type: RightAngle
  angle: ?ABC
- type: RightAngle
  angle: ?DEF
- type: EqualSegment
  segment1: ?AC  # Hypotenuse
  segment2: ?DF  # Hypotenuse
- type: EqualSegment
  segment1: ?AB  # Leg
  segment2: ?DE  # Leg
```

**Conclusions**:
```yaml
- type: CongruentTriangle
  p1: ?A
  p2: ?B
  p3: ?C
  p4: ?D
  p5: ?E
  p6: ?F
```

**Status**: ✅ Can implement immediately

---

## Implementation Priority

### Phase 1: Easy Wins (Day 2) - 6 theorems
Can implement immediately without numeric solver:

1. ✅ `isosceles_converse` - Base angles equal → sides equal
2. ✅ `equilateral_all_angles_equal` - All angles in equilateral triangle
3. ✅ `sss_congruence` - Side-Side-Side
4. ✅ `sas_congruence` - Side-Angle-Side
5. ✅ `asa_congruence` - Angle-Side-Angle
6. ✅ `aas_congruence` - Angle-Angle-Side

### Phase 2: Moderate Complexity (Day 3) - 4 theorems
Require careful pattern design:

7. ✅ `hl_congruence` - Hypotenuse-Leg
8. ⚠️ `consecutive_interior_supplementary` - Supplementary angles
9. ⚠️ `vertical_angles_extended` - Extended vertical angle theorems
10. ✅ `congruence_implies_equal_parts` - If triangles congruent, parts equal

### Phase 3: Complex (Day 4) - 5 theorems
Require transversal patterns:

11. ⚠️ `alternate_interior_angles` - Needs transversal pattern
12. ⚠️ `corresponding_angles` - Needs transversal pattern
13. ⚠️ `perpendicular_transversal` - Perpendicular relationships
14. ✅ `similar_triangles_aa` - Angle-Angle similarity
15. ✅ `congruent_implies_similar` - Congruence → similarity

### Phase 4: Deferred (Needs Numeric Solver)
Cannot implement without numeric computation:

- ❌ `triangle_angle_sum` - Requires 180° = ∠A + ∠B + ∠C
- ❌ `exterior_angle_theorem` - Requires angle addition
- ❌ Pythagorean theorem (numeric version)

---

## Theorem File Organization

```
geometry_prover/data/theorems/
├── core_theorems.yaml          # Existing (13 theorems)
├── example_theorems.yaml       # Existing (3 theorems)
└── week8/
    ├── triangle_properties.yaml  # 4-5 theorems
    ├── congruence.yaml          # 6 theorems
    ├── parallel_angles.yaml     # 3-4 theorems (simplified)
    └── similarity.yaml          # 2 theorems
```

---

## Success Metrics

### Target for Week 8
- **Theorems**: 13 → 24+ (add 11-15 new)
- **Categories**: 5 → 8
- **Examples**: 13 → 18-20
- **Fact Types Used**: 8 → 15+

### Must Have (Minimum Viable)
- ✅ 5 congruence theorems (SSS, SAS, ASA, AAS, HL)
- ✅ 2-3 triangle property theorems
- ✅ 2-3 simplified parallel angle theorems

### Nice to Have
- ✅ Similarity theorems
- ✅ Extended triangle properties
- ⚠️ Full parallel angle theorems with transversal

### Deferred to Future
- ❌ Numeric angle sum theorems (need numeric solver)
- ❌ Area-based theorems
- ❌ Circle theorems

---

## Next Steps (Day 2)

1. ✅ Create `triangle_properties.yaml` with:
   - isosceles_converse
   - equilateral_all_angles_equal

2. ✅ Create `congruence.yaml` with all 6 congruence theorems

3. ✅ Test new theorems with existing examples

4. ✅ Update theorem loader to include week8 directory

---

*Design Document Created: 2025-12-06*
*Status: Ready to implement*
*Next: Create theorem YAML files*
