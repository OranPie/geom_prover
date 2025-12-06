"""
Facts module for the geometry prover.

This module provides the complete fact type system - the foundation of geometric knowledge representation.
"""

from geometry_prover.facts.fact_base import FactBase
from geometry_prover.facts.fact_types import (
    # Base
    Fact,
    FACT_TYPES,
    get_fact_class,

    # Structural Facts
    On,
    OnSegment,
    OnCircle,
    Collinear,
    NotCollinear,
    Between,
    Midpoint,
    FootOfPerpendicular,
    ReflectPoint,
    Intersect,

    # Length/Ratio Facts
    EqualSegment,
    ProportionalSegment,
    SegmentRatio,
    LengthValue,

    # Angle Facts
    EqualAngle,
    RightAngle,
    SupplementaryAngle,
    AngleSum,
    AngleValue,

    # Line Relation Facts
    Parallel,
    Perpendicular,
    SameLine,

    # Shape Facts
    Triangle,
    IsoscelesTriangle,
    EquilateralTriangle,
    SimilarTriangle,
    CongruentTriangle,

    # Circle Facts
    TangentAt,
    Chord,
    Diameter,
    Arc,
    CyclicQuadrilateral,

    # Area Facts
    AreaValue,
    AreaRelation,

    # Logic Facts
    Distinct,
    NonDegenerateTriangle,
    Orientation,
)

__all__ = [
    "FactBase",
    "Fact",
    "FACT_TYPES",
    "get_fact_class",
    "On",
    "OnSegment",
    "OnCircle",
    "Collinear",
    "NotCollinear",
    "Between",
    "Midpoint",
    "FootOfPerpendicular",
    "ReflectPoint",
    "Intersect",
    "EqualSegment",
    "ProportionalSegment",
    "SegmentRatio",
    "LengthValue",
    "EqualAngle",
    "RightAngle",
    "SupplementaryAngle",
    "AngleSum",
    "AngleValue",
    "Parallel",
    "Perpendicular",
    "SameLine",
    "Triangle",
    "IsoscelesTriangle",
    "EquilateralTriangle",
    "SimilarTriangle",
    "CongruentTriangle",
    "TangentAt",
    "Chord",
    "Diameter",
    "Arc",
    "CyclicQuadrilateral",
    "AreaValue",
    "AreaRelation",
    "Distinct",
    "NonDegenerateTriangle",
    "Orientation",
]
