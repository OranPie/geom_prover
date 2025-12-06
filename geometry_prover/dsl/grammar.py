# Geometry DSL Grammar Specification

**Version**: 1.0
**Date**: 2025-12-04
**Status**: Draft

---

## Overview

The Geometry DSL is a domain-specific language for describing geometric constructions, constraints, and proof goals. It is designed to be:

- **Intuitive**: Natural syntax close to mathematical notation
- **Concise**: Minimal boilerplate
- **Extensible**: Easy to add new constructs
- **Unambiguous**: Clear parsing rules

---

## Formal Grammar (BNF)

```bnf
<program>           ::= <statement_list>

<statement_list>    ::= <statement> | <statement> <statement_list>

<statement>         ::= <point_decl>
                      | <line_decl>
                      | <circle_decl>
                      | <triangle_decl>
                      | <constraint>
                      | <prove_statement>
                      | <comment>

<comment>           ::= "#" <text> <newline>

<point_decl>        ::= "point" <identifier_list>

<identifier_list>   ::= <identifier>
                      | <identifier> "," <identifier_list>

<line_decl>         ::= "line" <identifier> <identifier>
                      | "line" <identifier>

<triangle_decl>     ::= "triangle" <identifier> <identifier> <identifier>

<circle_decl>       ::= "circle" <identifier> "with" "radius" <number>
                      | "circle" <identifier> "with" "center" <identifier> "radius" <number>
                      | "circle" <identifier> "through" <identifier>

<constraint>        ::= <segment> "=" <segment>
                      | <segment> "||" <segment>
                      | <segment> "⊥" <segment>
                      | <segment> "//" <segment>
                      | <angle> "=" <angle>
                      | <angle> "=" <number>
                      | <identifier> "on" <segment>
                      | <identifier> "on" <identifier>

<prove_statement>   ::= "prove" <assertion>

<assertion>         ::= <constraint>
                      | "angle" "(" <identifier> <identifier> <identifier> ")" "=" "angle" "(" <identifier> <identifier> <identifier> ")"
                      | <segment> "=" <segment>

<segment>           ::= <identifier> <identifier>
                      | <identifier>

<angle>             ::= "angle" "(" <identifier> <identifier> <identifier> ")"
                      | "∠" <identifier> <identifier> <identifier>

<identifier>        ::= <letter> | <letter> <alphanum>

<alphanum>          ::= <letter> | <digit> | <alphanum>

<letter>            ::= "A".."Z" | "a".."z"

<digit>             ::= "0".."9"

<number>            ::= <integer> | <float>

<integer>           ::= <digit> | <digit> <integer>

<float>             ::= <integer> "." <integer>
```

---

## Keywords

### Declarations
- `point` - Declare points
- `line` - Declare lines
- `circle` - Declare circles
- `triangle` - Declare triangles

### Constraints
- `on` - Point on line/circle
- `with` - Modifier for specifications
- `center` - Circle center
- `radius` - Circle radius
- `through` - Circle through points

### Operators
- `=` - Equality
- `||` or `//` - Parallel
- `⊥` - Perpendicular (can also use `perp`)
- `angle` or `∠` - Angle notation

### Proof
- `prove` - Proof goal statement

### Comments
- `#` - Single-line comment

---

## Syntax Examples

### Point Declarations
```
point A
point A, B, C
point P, Q, R, S
```

### Line Declarations
```
line AB          # Line through points A and B
line l           # Named line
```

### Triangle Declarations
```
triangle ABC     # Triangle with vertices A, B, C
```

### Circle Declarations
```
circle O with radius 5
circle C with center O radius 3
circle O through A
```

### Constraints

#### Equality
```
AB = AC          # Segment AB equals segment AC
angle(ABC) = angle(DEF)
∠ABC = 90
```

#### Parallel/Perpendicular
```
AB || CD         # AB parallel to CD
AB // CD         # Alternative parallel syntax
AB ⊥ CD          # AB perpendicular to CD
```

#### Incidence
```
P on AB          # Point P on line AB
A on circle O    # Point A on circle O
```

### Prove Statements
```
prove AB = CD
prove AB || CD
prove angle(ABC) = angle(DEF)
prove ∠ABC = ∠ACB
```

### Comments
```
# This is a comment
point A, B, C    # Vertices of triangle
```

---

## Complete Example Programs

### Example 1: Isosceles Triangle
```
# Isosceles triangle with equal base angles
point A, B, C
triangle ABC
AB = AC
prove angle(ABC) = angle(ACB)
```

### Example 2: Parallel Lines
```
# Parallel lines with transversal
point A, B, C, D, E, F
line AB
line CD
line EF
AB || CD
E on AB
F on CD
prove angle(AEF) = angle(CFE)
```

### Example 3: Circle Properties
```
# Circle with tangent
point O, A, B, P
circle O with radius 5
A on circle O
B on circle O
line AB
P on AB
OP ⊥ AB
prove P is midpoint of AB
```

### Example 4: Right Triangle
```
# Right triangle with altitude
point A, B, C, H
triangle ABC
∠ABC = 90
H on AC
BH ⊥ AC
prove AB² + BC² = AC²
```

### Example 5: Complex Construction
```
# Triangle with multiple properties
point A, B, C, D, E, F
triangle ABC

# Equal sides
AB = AC

# Point D is midpoint of BC
D on BC
BD = DC

# E is foot of perpendicular from A to BC
E on BC
AE ⊥ BC

# Prove D and E are the same point
prove D = E
```

---

## Operator Precedence

1. Parentheses `()`
2. Geometric objects (segments, angles)
3. Relations (`=`, `||`, `⊥`)
4. Logical operators (future: `and`, `or`)

---

## Reserved Words

```
point, line, circle, triangle
on, with, center, radius, through
angle
prove
parallel, perpendicular
midpoint, bisector
and, or, not (reserved for future use)
```

---

## Lexical Rules

### Identifiers
- Start with letter (A-Z, a-z)
- Followed by letters, digits, or underscore
- Case-sensitive
- Examples: `A`, `B1`, `point_P`, `center_O`

### Numbers
- Integers: `0`, `1`, `42`, `100`
- Floats: `3.14`, `0.5`, `90.0`
- Scientific notation (future): `1.5e-3`

### Whitespace
- Spaces, tabs, newlines
- Used to separate tokens
- Multiple whitespace treated as single separator

### Comments
- Single-line: `# comment text`
- Multi-line (future): `/* comment */`

---

## Semantic Rules

### Point Naming
- Points typically use uppercase letters: `A`, `B`, `C`, `P`, `Q`
- Can use subscripts in identifiers: `P1`, `P2`

### Line Naming
- Lines named by two points: `AB` (line through A and B)
- Or single identifier: `l`, `m`, `line1`

### Implicit Constructions
- Writing `AB` implicitly references line/segment through points A and B
- Triangle declaration implicitly creates three segments

### Uniqueness
- Points must be declared before use
- Lines referenced by points must have those points declared
- Circles must have defined centers

---

## Error Handling

### Syntax Errors
- Unexpected token
- Missing required keyword
- Malformed expression
- Unclosed parenthesis

### Semantic Errors
- Undefined point/line reference
- Duplicate declarations
- Contradictory constraints
- Impossible geometric configurations

---

## Future Extensions

### Planned Features
- Variable declarations: `let x = length(AB)`
- Arithmetic expressions: `AB = 2 * CD`
- Conditional statements: `if AB = AC then ...`
- Macros/functions: `define isosceles(A, B, C) = ...`
- Angle arithmetic: `∠ABC + ∠BCD = 180`
- Vector notation: `vec(AB) + vec(BC) = vec(AC)`

### Advanced Constructs
- Polygons: `polygon ABCDEF`
- Constructions: `construct perpendicular from A to BC`
- Loci: `locus of points P where distance(P, A) = distance(P, B)`
- Transformations: `reflect A across BC`, `rotate P around O by 90`

---

## Design Rationale

### Why This Syntax?

1. **Familiar to Mathematicians**: Uses standard notation (AB for segments, ∠ABC for angles)
2. **Minimal Punctuation**: Reduces visual noise
3. **Natural Word Order**: "point A on line BC" reads naturally
4. **Unambiguous Parsing**: No operator precedence conflicts
5. **Easy to Type**: Common ASCII characters (except ∠, which has ASCII alternative)

### Design Decisions

- **Implicit Line Creation**: Writing `AB` creates implicit line reference
- **Keyword-Based**: Clear statement types (`point`, `line`, `prove`)
- **Constraint-Based**: Express properties as constraints, not imperative commands
- **Declarative Style**: Describe what is true, not how to construct

---

## Comparison with Other Systems

### vs. Euclidean Geometry Language (EGL)
- Our DSL: More concise, less verbose
- EGL: More explicit construction steps

### vs. GeoGebra Script
- Our DSL: Focused on proofs, not interactive
- GeoGebra: GUI-oriented, more imperative

### vs. Ott Geometry Language
- Our DSL: Simpler syntax, fewer constructs
- Ott: More formal, logic-based

---

## Implementation Notes

### Parser Strategy
- **Recursive Descent**: Top-down parsing
- **LL(1) Grammar**: One token lookahead sufficient
- **Error Recovery**: Synchronization at statement boundaries

### AST Design
- Each statement type has corresponding AST node
- Preserve source location (line, column) for error messages
- Support visitor pattern for traversal

### Lexer Requirements
- Handle Unicode symbols (∠, ⊥, ||)
- Track line and column numbers
- Support both `//` (parallel) and `#` (comment)

---

## Testing Strategy

### Test Categories
1. **Syntax Tests**: Valid/invalid programs
2. **Lexer Tests**: Token recognition
3. **Parser Tests**: AST construction
4. **Semantic Tests**: Meaningful programs
5. **Error Tests**: Helpful error messages

### Test Coverage Goals
- All grammar productions covered
- All keywords tested
- All operators tested
- Edge cases (empty file, single statement, etc.)

---

*End of Grammar Specification*
