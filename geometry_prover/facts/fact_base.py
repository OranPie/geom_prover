"""
FactBase - Container for storing and querying geometric facts.

The FactBase provides efficient storage and retrieval of facts with:
- Automatic deduplication
- Multiple indices for fast queries
- O(1) lookup by type
- O(1) lookup by point
- Support for large fact sets (1000+ facts)
"""

from typing import Optional, Set, List
from collections import defaultdict
from geometry_prover.facts.fact_types import Fact
from geometry_prover.utils import Point, Line, Circle


class FactBase:
    """
    Container for storing and querying geometric facts.

    Features:
    - Automatic deduplication using set
    - Index by fact type for fast queries
    - Index by involved points for spatial queries
    - Index by geometric objects (lines, circles)
    - Efficient add/remove/query operations

    Attributes:
        _facts: Set of all facts (for deduplication)
        _by_type: Index mapping fact type to set of facts
        _by_point: Index mapping point to set of facts involving that point
        _by_line: Index mapping line to set of facts involving that line
        _by_circle: Index mapping circle to set of facts involving that circle
    """

    def __init__(self):
        """Initialize an empty FactBase."""
        self._facts: Set[Fact] = set()
        self._by_type: dict[str, Set[Fact]] = defaultdict(set)
        self._by_point: dict[Point, Set[Fact]] = defaultdict(set)
        self._by_line: dict[Line, Set[Fact]] = defaultdict(set)
        self._by_circle: dict[Circle, Set[Fact]] = defaultdict(set)

    def add(self, fact: Fact) -> bool:
        """
        Add a fact to the FactBase.

        Args:
            fact: The fact to add

        Returns:
            True if the fact was added (new), False if it already existed

        Examples:
            >>> fb = FactBase()
            >>> fact = On(Point('A'), Line(Point('B'), Point('C')))
            >>> fb.add(fact)
            True
            >>> fb.add(fact)  # Adding again
            False
        """
        if fact in self._facts:
            return False

        # Add to main set
        self._facts.add(fact)

        # Add to type index
        self._by_type[fact.fact_type].add(fact)

        # Add to point index
        for point in fact.get_involved_points():
            self._by_point[point].add(fact)

        # Add to object indices
        self._index_objects(fact)

        return True

    def _index_objects(self, fact: Fact) -> None:
        """Index facts by geometric objects (lines, circles)."""
        # Check parameters for lines and circles
        for param_value in fact.parameters.values():
            if isinstance(param_value, Line):
                self._by_line[param_value].add(fact)
            elif isinstance(param_value, Circle):
                self._by_circle[param_value].add(fact)
            elif isinstance(param_value, list):
                # Handle lists of objects
                for item in param_value:
                    if isinstance(item, Line):
                        self._by_line[item].add(fact)
                    elif isinstance(item, Circle):
                        self._by_circle[item].add(fact)

    def remove(self, fact: Fact) -> bool:
        """
        Remove a fact from the FactBase.

        Args:
            fact: The fact to remove

        Returns:
            True if the fact was removed, False if it didn't exist

        Examples:
            >>> fb = FactBase()
            >>> fact = On(Point('A'), Line(Point('B'), Point('C')))
            >>> fb.add(fact)
            True
            >>> fb.remove(fact)
            True
            >>> fb.remove(fact)
            False
        """
        if fact not in self._facts:
            return False

        # Remove from main set
        self._facts.discard(fact)

        # Remove from type index
        self._by_type[fact.fact_type].discard(fact)

        # Remove from point index
        for point in fact.get_involved_points():
            self._by_point[point].discard(fact)

        # Remove from object indices
        self._deindex_objects(fact)

        return True

    def _deindex_objects(self, fact: Fact) -> None:
        """Remove fact from object indices."""
        for param_value in fact.parameters.values():
            if isinstance(param_value, Line):
                self._by_line[param_value].discard(fact)
            elif isinstance(param_value, Circle):
                self._by_circle[param_value].discard(fact)
            elif isinstance(param_value, list):
                for item in param_value:
                    if isinstance(item, Line):
                        self._by_line[item].discard(fact)
                    elif isinstance(item, Circle):
                        self._by_circle[item].discard(fact)

    def contains(self, fact: Fact) -> bool:
        """
        Check if a fact exists in the FactBase.

        Args:
            fact: The fact to check

        Returns:
            True if the fact exists, False otherwise

        Examples:
            >>> fb = FactBase()
            >>> fact = Triangle(Point('A'), Point('B'), Point('C'))
            >>> fb.contains(fact)
            False
            >>> fb.add(fact)
            True
            >>> fb.contains(fact)
            True
        """
        return fact in self._facts

    def query_by_type(self, fact_type: str) -> List[Fact]:
        """
        Query facts by fact type.

        Args:
            fact_type: The type of facts to retrieve (e.g., "On", "EqualSegment")

        Returns:
            List of facts of the specified type

        Time Complexity: O(1) to get the set, O(n) to convert to list where n is result size

        Examples:
            >>> fb = FactBase()
            >>> fb.add(On(Point('A'), Line(Point('B'), Point('C'))))
            >>> fb.add(On(Point('D'), Line(Point('E'), Point('F'))))
            >>> len(fb.query_by_type('On'))
            2
        """
        return list(self._by_type.get(fact_type, set()))

    def query_by_point(self, point: Point) -> List[Fact]:
        """
        Query facts involving a specific point.

        Args:
            point: The point to search for

        Returns:
            List of facts involving the specified point

        Time Complexity: O(1) to get the set, O(n) to convert to list

        Examples:
            >>> fb = FactBase()
            >>> A = Point('A')
            >>> B = Point('B')
            >>> C = Point('C')
            >>> fb.add(Triangle(A, B, C))
            >>> fb.add(On(A, Line(B, C)))
            >>> len(fb.query_by_point(A))
            2
        """
        return list(self._by_point.get(point, set()))

    def query_by_line(self, line: Line) -> List[Fact]:
        """
        Query facts involving a specific line.

        Args:
            line: The line to search for

        Returns:
            List of facts involving the specified line

        Examples:
            >>> fb = FactBase()
            >>> line = Line(Point('A'), Point('B'))
            >>> fb.add(On(Point('C'), line))
            >>> len(fb.query_by_line(line))
            1
        """
        return list(self._by_line.get(line, set()))

    def query_by_circle(self, circle: Circle) -> List[Fact]:
        """
        Query facts involving a specific circle.

        Args:
            circle: The circle to search for

        Returns:
            List of facts involving the specified circle

        Examples:
            >>> fb = FactBase()
            >>> circle = Circle(Point('O'), radius=5.0)
            >>> fb.add(OnCircle(Point('A'), circle))
            >>> len(fb.query_by_circle(circle))
            1
        """
        return list(self._by_circle.get(circle, set()))

    def query_by_points(self, points: Set[Point]) -> List[Fact]:
        """
        Query facts involving ALL of the specified points.

        Args:
            points: Set of points to match

        Returns:
            List of facts that involve all specified points

        Examples:
            >>> fb = FactBase()
            >>> A, B, C = Point('A'), Point('B'), Point('C')
            >>> fb.add(Triangle(A, B, C))
            >>> fb.add(On(A, Line(B, C)))
            >>> len(fb.query_by_points({A, B, C}))
            1  # Only Triangle involves all three
        """
        if not points:
            return []

        # Start with facts from the first point (usually smallest set)
        result_set = set(self._by_point.get(next(iter(points)), set()))

        # Intersect with facts from other points
        for point in points:
            result_set &= self._by_point.get(point, set())

        return list(result_set)

    def get_all(self) -> List[Fact]:
        """
        Get all facts in the FactBase.

        Returns:
            List of all facts

        Examples:
            >>> fb = FactBase()
            >>> fb.add(Triangle(Point('A'), Point('B'), Point('C')))
            >>> len(fb.get_all())
            1
        """
        return list(self._facts)

    def get_all_types(self) -> List[str]:
        """
        Get list of all fact types currently in the FactBase.

        Returns:
            List of fact type names

        Examples:
            >>> fb = FactBase()
            >>> fb.add(On(Point('A'), Line(Point('B'), Point('C'))))
            >>> fb.add(Triangle(Point('D'), Point('E'), Point('F')))
            >>> sorted(fb.get_all_types())
            ['On', 'Triangle']
        """
        return [fact_type for fact_type in self._by_type.keys() if self._by_type[fact_type]]

    def size(self) -> int:
        """
        Get the number of facts in the FactBase.

        Returns:
            Number of facts

        Examples:
            >>> fb = FactBase()
            >>> fb.size()
            0
            >>> fb.add(Triangle(Point('A'), Point('B'), Point('C')))
            >>> fb.size()
            1
        """
        return len(self._facts)

    def clear(self) -> None:
        """
        Remove all facts from the FactBase.

        Examples:
            >>> fb = FactBase()
            >>> fb.add(Triangle(Point('A'), Point('B'), Point('C')))
            >>> fb.size()
            1
            >>> fb.clear()
            >>> fb.size()
            0
        """
        self._facts.clear()
        self._by_type.clear()
        self._by_point.clear()
        self._by_line.clear()
        self._by_circle.clear()

    def __len__(self) -> int:
        """
        Get the number of facts (supports len(fact_base)).

        Returns:
            Number of facts
        """
        return len(self._facts)

    def __contains__(self, fact: Fact) -> bool:
        """
        Check if a fact is in the FactBase (supports 'in' operator).

        Args:
            fact: The fact to check

        Returns:
            True if fact is in FactBase, False otherwise
        """
        return fact in self._facts

    def __repr__(self) -> str:
        """String representation of FactBase."""
        return f"FactBase(size={self.size()}, types={len(self.get_all_types())})"

    def __str__(self) -> str:
        """Human-readable string representation."""
        if self.size() == 0:
            return "FactBase(empty)"

        type_counts = {fact_type: len(facts) for fact_type, facts in self._by_type.items() if facts}
        type_summary = ", ".join(f"{t}:{c}" for t, c in sorted(type_counts.items()))
        return f"FactBase({self.size()} facts: {type_summary})"

    def stats(self) -> dict:
        """
        Get statistics about the FactBase.

        Returns:
            Dictionary with statistics:
            - total_facts: Total number of facts
            - fact_types: Number of different fact types
            - indexed_points: Number of points in index
            - indexed_lines: Number of lines in index
            - indexed_circles: Number of circles in index
            - type_distribution: Dict of fact counts by type

        Examples:
            >>> fb = FactBase()
            >>> fb.add(Triangle(Point('A'), Point('B'), Point('C')))
            >>> stats = fb.stats()
            >>> stats['total_facts']
            1
        """
        return {
            'total_facts': self.size(),
            'fact_types': len(self.get_all_types()),
            'indexed_points': len([p for p in self._by_point if self._by_point[p]]),
            'indexed_lines': len([l for l in self._by_line if self._by_line[l]]),
            'indexed_circles': len([c for c in self._by_circle if self._by_circle[c]]),
            'type_distribution': {
                fact_type: len(facts)
                for fact_type, facts in self._by_type.items()
                if facts
            }
        }
