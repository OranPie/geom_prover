"""Custom exceptions for geometry_prover."""


class GeometryProverError(Exception):
    """Base exception for all geometry prover errors."""

    pass


class DSLParseError(GeometryProverError):
    """Raised when DSL parsing fails."""

    def __init__(self, message: str, line: int = None, column: int = None):
        self.line = line
        self.column = column
        if line is not None and column is not None:
            super().__init__(f"{message} (line {line}, column {column})")
        else:
            super().__init__(message)


class SemanticError(GeometryProverError):
    """Raised when semantic analysis fails."""

    pass


class TheoremNotFoundError(GeometryProverError):
    """Raised when a referenced theorem is not found."""

    pass


class ProofTimeoutError(GeometryProverError):
    """Raised when proof search exceeds timeout."""

    pass


class NumericSolverError(GeometryProverError):
    """Raised when numeric constraint solving fails."""

    pass


class InvalidFactError(GeometryProverError):
    """Raised when an invalid fact is created."""

    pass


class InvalidConstructionError(GeometryProverError):
    """Raised when an invalid geometric construction is attempted."""

    pass
