# Geometry Theorem Proving System

An automated geometry theorem proving system with hybrid symbolic-numeric reasoning and automatic auxiliary construction search.

## Features

- **DSL for Geometry Construction**: Intuitive domain-specific language for defining geometric problems
- **Fact-Based Knowledge Representation**: 40+ geometric fact types
- **Extensible Theorem Library**: YAML-based theorem definitions (no code changes needed)
- **Hybrid Reasoning**: Combines symbolic logic with numeric validation
- **Automatic Auxiliary Lines**: Automatically proposes helpful constructions
- **Proof Visualization**: Generate diagrams and step-by-step explanations
- **Multi-Language Support**: Chinese and English

## Installation

### From Source

```bash
git clone https://github.com/yourusername/geometry-prover.git
cd geometry-prover
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

### Example DSL Input

```
point A, B, C
triangle ABC
AB = AC
prove angle(ABC) = angle(ACB)
```

### Python API

```python
from geometry_prover import ProofAPI

api = ProofAPI()
result = api.prove_from_dsl("""
    point A, B, C
    triangle ABC
    AB = AC
    prove angle(ABC) = angle(ACB)
""")

if result.success:
    print("Proof found!")
    print(result.description)
else:
    print("Could not prove the theorem")
```

### Command Line

```bash
geometry-prover prove problem.dsl --output proof.txt
geometry-prover prove problem.dsl --diagram proof.png
```

## Project Status

**Current Phase**: Phase 1 - Foundation (Week 1)

- [x] Project setup
- [ ] Geometric object classes
- [ ] Fact type system (40+ types)
- [ ] FactBase implementation
- [ ] DSL parsing
- [ ] Semantic analysis

See [DETAILED_DEVELOPMENT_PLAN.md](DETAILED_DEVELOPMENT_PLAN.md) for full roadmap.

## Architecture

The system consists of three main layers:

1. **Data Layer**: Facts, Geometry Model, Proof Tree
2. **Application Layer**: DSL Parser, Semantic Builder, Proof Engine, Auxiliary Search, Solver
3. **Interface Layer**: API, CLI, Visualization

See [PACKAGE_DESIGN_PLAN.md](PACKAGE_DESIGN_PLAN.md) for detailed architecture.

## Documentation

- [Package Design Plan](PACKAGE_DESIGN_PLAN.md)
- [Detailed Development Plan](DETAILED_DEVELOPMENT_PLAN.md)
- [User Guide](docs/user_guide.md) *(coming soon)*
- [API Reference](docs/api_reference.md) *(coming soon)*
- [DSL Syntax](docs/dsl_syntax.md) *(coming soon)*
- [Problem Solving Guide](docs/PROBLEM_SOLVING_GUIDE.md) — step-by-step walkthrough for solving a geometry problem with the DSL and reasoners

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=geometry_prover --cov-report=html

# Run specific test module
pytest tests/test_facts/test_fact_types.py
```

## Code Quality

```bash
# Format code
black geometry_prover tests

# Lint
pylint geometry_prover

# Type check
mypy geometry_prover
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Development Team

- Team Lead / Architect
- Developer 1 - Core Engine
- Developer 2 - Algorithms
- Developer 3 - Search & AI

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

Based on research in automated theorem proving and geometry education.

## Roadmap

### Phase 1: Foundation (Weeks 1-3) - **In Progress**
- Core data structures
- DSL parsing
- Semantic analysis

### Phase 2: Theorem System (Weeks 4-6)
- Theorem loading
- Pattern matching
- 30-50 basic theorems

### Phase 3: Proof Engine (Weeks 7-10)
- Forward reasoning
- Backward reasoning
- Simple proofs

### Phase 4: Numeric Solver (Weeks 11-12)
- Constraint solving
- Numeric validation

### Phase 5: Auxiliary Search (Weeks 13-15)
- Automatic auxiliary constructions

### Phase 6: Visualization (Weeks 16-18)
- Proof formatting
- Diagram rendering
- Documentation

### Phase 7: Testing & Optimization (Weeks 19-20)
- Comprehensive testing
- Performance optimization

### Phase 8: Advanced Features (Weeks 21+)
- Web UI
- 3D geometry
- ML integration

## Contact

- GitHub Issues: https://github.com/yourusername/geometry-prover/issues
- Email: dev@example.com
