"""
Theorem system for geometric reasoning.

This module provides theorem representation, pattern matching, and
automated reasoning capabilities for the geometry theorem prover.

Components:
- pattern.py: Pattern matching data structures
- theorem.py: Theorem representation
- loader.py: YAML theorem loading
- library.py: Theorem library management
- matcher.py: Pattern matching engine
- unification.py: Variable unification
"""

__all__ = [
    'Pattern',
    'Theorem',
    'TheoremLibrary',
    'PatternMatcher',
]
