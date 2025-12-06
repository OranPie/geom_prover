# Geometry Prover Data Directory

This directory contains theorem definitions, schemas, and other data files used by the geometry theorem prover.

## Directory Structure

```
data/
├── theorems/           # Theorem definitions in YAML format
│   ├── basic_theorems.yaml       # Core geometric theorems
│   ├── example_theorems.yaml     # Example/template theorems
│   └── advanced_theorems.yaml    # Advanced theorems (Week 5-6)
│
├── schemas/            # YAML schemas and validation
│   └── theorem_schema.yaml       # Schema for theorem YAML files
│
└── aux_patterns/       # Auxiliary construction patterns (Week 13-15)
```

## Theorem File Format

Theorems are defined in YAML format with the following structure:

```yaml
theorems:
  - name: "theorem_name"
    category: "category_name"
    description: "Human-readable description"
    
    conditions:
      - type: "FactType"
        parameter1: "?variable1"
        parameter2: "?variable2"
    
    conclusions:
      - type: "FactType"
        parameter1: "?variable1"
        parameter2: "?variable2"
    
    variables:
      - name: "?variable1"
        type: "point|line|segment|angle|circle"
        description: "Optional description"
        derived_from: ["?parent1", "?parent2"]  # Optional
```

## Pattern Variables

Variables in theorems use the `?` prefix (e.g., `?A`, `?ABC`) to indicate pattern variables that will be bound during matching.

## Example

See `theorems/example_theorems.yaml` for complete examples.
