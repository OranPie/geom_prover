"""
Tests for FactBase container.

Tests from DETAILED_DEVELOPMENT_PLAN.md:
Phase 1, Week 1, Task 1.4 - Test Requirements:
- Test add/remove operations
- Test deduplication
- Test querying by different criteria
- Performance test with 10,000 facts
"""

import pytest
import time
from geometry_prover.facts import (
    FactBase, On, Triangle, EqualSegment, Parallel, Perpendicular,
    OnCircle, Midpoint, RightAngle, IsoscelesTriangle, EqualAngle
)
from geometry_prover.utils import Point, Line, Circle, Angle, Segment


class TestFactBaseBasics:
    """Test basic FactBase operations."""

    def test_factbase_creation(self):
        """Test creating an empty FactBase."""
        fb = FactBase()
        assert fb.size() == 0
        assert len(fb) == 0
        assert fb.get_all() == []

    def test_add_fact(self):
        """Test adding a fact."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')
        line = Line(A, B)
        fact = On(C, line)

        result = fb.add(fact)
        assert result is True
        assert fb.size() == 1
        assert fact in fb

    def test_add_duplicate_fact(self):
        """Test that duplicate facts are not added."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')
        fact = Triangle(A, B, C)

        result1 = fb.add(fact)
        result2 = fb.add(fact)

        assert result1 is True
        assert result2 is False
        assert fb.size() == 1

    def test_contains(self):
        """Test checking if fact exists."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')
        fact1 = Triangle(A, B, C)
        fact2 = Triangle(A, B, Point('D'))

        fb.add(fact1)

        assert fb.contains(fact1)
        assert fact1 in fb
        assert not fb.contains(fact2)
        assert fact2 not in fb

    def test_remove_fact(self):
        """Test removing a fact."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')
        fact = Triangle(A, B, C)

        fb.add(fact)
        assert fb.size() == 1

        result = fb.remove(fact)
        assert result is True
        assert fb.size() == 0
        assert fact not in fb

    def test_remove_nonexistent_fact(self):
        """Test removing a fact that doesn't exist."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')
        fact = Triangle(A, B, C)

        result = fb.remove(fact)
        assert result is False

    def test_clear(self):
        """Test clearing all facts."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')

        fb.add(Triangle(A, B, C))
        fb.add(On(A, Line(B, C)))
        assert fb.size() == 2

        fb.clear()
        assert fb.size() == 0
        assert fb.get_all() == []


class TestFactBaseQueries:
    """Test FactBase query operations."""

    def test_query_by_type(self):
        """Test querying facts by type."""
        fb = FactBase()
        A, B, C, D = Point('A'), Point('B'), Point('C'), Point('D')

        # Add various facts
        fb.add(Triangle(A, B, C))
        fb.add(Triangle(B, C, D))
        fb.add(On(A, Line(B, C)))

        triangles = fb.query_by_type('Triangle')
        on_facts = fb.query_by_type('On')

        assert len(triangles) == 2
        assert len(on_facts) == 1

    def test_query_by_point(self):
        """Test querying facts by point."""
        fb = FactBase()
        A, B, C, D = Point('A'), Point('B'), Point('C'), Point('D')

        fb.add(Triangle(A, B, C))
        fb.add(On(A, Line(B, D)))
        fb.add(Triangle(B, C, D))

        facts_with_A = fb.query_by_point(A)
        facts_with_B = fb.query_by_point(B)

        assert len(facts_with_A) == 2  # Triangle and On
        assert len(facts_with_B) == 3  # All three facts

    def test_query_by_line(self):
        """Test querying facts by line."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')
        line1 = Line(A, B)
        line2 = Line(B, C)

        fb.add(On(C, line1))
        fb.add(Parallel(line1, line2))

        facts_with_line1 = fb.query_by_line(line1)
        assert len(facts_with_line1) == 2

    def test_query_by_circle(self):
        """Test querying facts by circle."""
        fb = FactBase()
        O, A, B = Point('O'), Point('A'), Point('B')
        circle = Circle(O, radius=5.0)

        fb.add(OnCircle(A, circle))
        fb.add(OnCircle(B, circle))

        facts_with_circle = fb.query_by_circle(circle)
        assert len(facts_with_circle) == 2

    def test_query_by_multiple_points(self):
        """Test querying facts involving multiple specific points."""
        fb = FactBase()
        A, B, C, D = Point('A'), Point('B'), Point('C'), Point('D')

        fb.add(Triangle(A, B, C))
        fb.add(Triangle(A, B, D))
        fb.add(On(A, Line(B, C)))

        # Facts involving both A and B and C
        facts_ABC = fb.query_by_points({A, B, C})
        assert len(facts_ABC) == 2  # Triangle(A,B,C) and On(A, line(B,C))

        # Facts involving A, B, and D
        facts_ABD = fb.query_by_points({A, B, D})
        assert len(facts_ABD) == 1  # Only Triangle(A,B,D)

    def test_get_all_types(self):
        """Test getting all fact types."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')

        fb.add(Triangle(A, B, C))
        fb.add(On(A, Line(B, C)))
        fb.add(IsoscelesTriangle(A, B, C))

        types = fb.get_all_types()
        assert 'Triangle' in types
        assert 'On' in types
        assert 'IsoscelesTriangle' in types
        assert len(types) == 3


class TestFactBaseIndexing:
    """Test FactBase indexing and deduplication."""

    def test_deduplication_same_fact(self):
        """Test that identical facts are deduplicated."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')

        fact1 = Triangle(A, B, C)
        fact2 = Triangle(A, B, C)  # Same fact

        fb.add(fact1)
        fb.add(fact2)

        assert fb.size() == 1

    def test_deduplication_equivalent_segments(self):
        """Test deduplication of equivalent segment facts."""
        fb = FactBase()
        A, B, C, D = Point('A'), Point('B'), Point('C'), Point('D')

        seg1 = Segment(A, B)
        seg2 = Segment(C, D)
        seg3 = Segment(A, B)  # Same as seg1

        fact1 = EqualSegment(seg1, seg2)
        fact2 = EqualSegment(seg3, seg2)  # Equivalent to fact1

        fb.add(fact1)
        fb.add(fact2)

        assert fb.size() == 1

    def test_point_index_updated(self):
        """Test that point index is properly updated."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')
        fact = Triangle(A, B, C)

        fb.add(fact)

        # All three points should be in index
        assert len(fb.query_by_point(A)) == 1
        assert len(fb.query_by_point(B)) == 1
        assert len(fb.query_by_point(C)) == 1

        # Remove and check index updated
        fb.remove(fact)
        assert len(fb.query_by_point(A)) == 0

    def test_type_index_updated(self):
        """Test that type index is properly updated."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')

        fact1 = Triangle(A, B, C)
        fact2 = Triangle(A, B, Point('D'))

        fb.add(fact1)
        fb.add(fact2)
        assert len(fb.query_by_type('Triangle')) == 2

        fb.remove(fact1)
        assert len(fb.query_by_type('Triangle')) == 1


class TestFactBasePerformance:
    """Test FactBase performance with large numbers of facts."""

    def test_performance_add_1000_facts(self):
        """Test adding 1000 facts."""
        fb = FactBase()
        facts = []

        # Create 1000 different triangle facts
        for i in range(1000):
            A = Point(f'A{i}')
            B = Point(f'B{i}')
            C = Point(f'C{i}')
            facts.append(Triangle(A, B, C))

        start_time = time.time()
        for fact in facts:
            fb.add(fact)
        elapsed = time.time() - start_time

        assert fb.size() == 1000
        assert elapsed < 1.0  # Should complete in under 1 second
        print(f"  Added 1000 facts in {elapsed:.3f}s")

    def test_performance_query_by_type(self):
        """Test query performance with 1000 facts."""
        fb = FactBase()

        # Add 500 triangles and 500 on-facts
        for i in range(500):
            A = Point(f'A{i}')
            B = Point(f'B{i}')
            C = Point(f'C{i}')
            fb.add(Triangle(A, B, C))
            fb.add(On(A, Line(B, C)))

        start_time = time.time()
        triangles = fb.query_by_type('Triangle')
        elapsed = time.time() - start_time

        assert len(triangles) == 500
        assert elapsed < 0.001  # Should be < 1ms
        print(f"  Query by type in {elapsed*1000:.3f}ms")

    def test_performance_query_by_point(self):
        """Test point query performance."""
        fb = FactBase()
        A = Point('A')

        # Create 100 facts involving point A
        for i in range(100):
            B = Point(f'B{i}')
            C = Point(f'C{i}')
            fb.add(Triangle(A, B, C))

        start_time = time.time()
        facts_with_A = fb.query_by_point(A)
        elapsed = time.time() - start_time

        assert len(facts_with_A) == 100
        assert elapsed < 0.001  # Should be < 1ms
        print(f"  Query by point in {elapsed*1000:.3f}ms")


class TestFactBaseStringRepresentation:
    """Test string representations of FactBase."""

    def test_repr_empty(self):
        """Test repr of empty FactBase."""
        fb = FactBase()
        assert repr(fb) == "FactBase(size=0, types=0)"

    def test_repr_with_facts(self):
        """Test repr with facts."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')
        fb.add(Triangle(A, B, C))

        assert "size=1" in repr(fb)
        assert "types=1" in repr(fb)

    def test_str_empty(self):
        """Test str of empty FactBase."""
        fb = FactBase()
        assert str(fb) == "FactBase(empty)"

    def test_str_with_facts(self):
        """Test str with facts."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')
        fb.add(Triangle(A, B, C))
        fb.add(On(A, Line(B, C)))

        s = str(fb)
        assert "2 facts" in s
        assert "Triangle:1" in s
        assert "On:1" in s


class TestFactBaseStats:
    """Test FactBase statistics."""

    def test_stats_empty(self):
        """Test stats of empty FactBase."""
        fb = FactBase()
        stats = fb.stats()

        assert stats['total_facts'] == 0
        assert stats['fact_types'] == 0
        assert stats['indexed_points'] == 0

    def test_stats_with_facts(self):
        """Test stats with facts."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')
        O = Point('O')
        circle = Circle(O, radius=5.0)

        fb.add(Triangle(A, B, C))
        fb.add(On(A, Line(B, C)))
        fb.add(OnCircle(A, circle))

        stats = fb.stats()

        assert stats['total_facts'] == 3
        assert stats['fact_types'] == 3
        assert stats['indexed_points'] >= 3  # At least A, B, C
        assert stats['indexed_circles'] == 1
        assert stats['type_distribution']['Triangle'] == 1
        assert stats['type_distribution']['On'] == 1


class TestFactBaseEdgeCases:
    """Test edge cases and special scenarios."""

    def test_add_multiple_fact_types(self):
        """Test adding various fact types."""
        fb = FactBase()
        A, B, C, D = Point('A'), Point('B'), Point('C'), Point('D')
        line1 = Line(A, B)
        line2 = Line(C, D)

        fb.add(Triangle(A, B, C))
        fb.add(On(D, line1))
        fb.add(Parallel(line1, line2))
        fb.add(EqualSegment(Segment(A, B), Segment(C, D)))
        fb.add(RightAngle(Angle(A, B, C)))

        assert fb.size() == 5
        assert len(fb.get_all_types()) == 5

    def test_query_nonexistent_type(self):
        """Test querying for a fact type that doesn't exist."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')
        fb.add(Triangle(A, B, C))

        result = fb.query_by_type('NonExistentType')
        assert result == []

    def test_query_nonexistent_point(self):
        """Test querying for a point that doesn't exist."""
        fb = FactBase()
        A, B, C = Point('A'), Point('B'), Point('C')
        fb.add(Triangle(A, B, C))

        D = Point('D')
        result = fb.query_by_point(D)
        assert result == []

    def test_empty_points_query(self):
        """Test querying with empty point set."""
        fb = FactBase()
        result = fb.query_by_points(set())
        assert result == []


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
