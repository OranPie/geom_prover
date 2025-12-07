"""
Automatic construction of composite objects from components.

Uses GeometryModel's get_or_create_* methods to build missing objects
when theorems specify derived_from relationships.

From the auxiliary system plan:
- Enables automatic extraction of points from Lines/Segments/Angles
- Enables automatic construction of composites from component points
- Processes derived_from metadata during pattern matching
"""

from typing import List, Dict, Optional
from geometry_prover.utils import Point, Line, Segment, Angle
from geometry_prover.theorems.theorem import Theorem


class AuxiliaryConstructor:
    """
    Constructs missing geometric objects based on derived_from metadata.

    When a theorem variable has derived_from: [?A, ?B], this class:
    1. Checks if components (?A, ?B) are bound
    2. Constructs the composite object (e.g., Line(?A, ?B))
    3. Adds it to the binding

    Alternatively, if a composite is bound, it extracts the components.
    """

    def __init__(self):
        """Initialize auxiliary constructor."""
        pass

    def augment_binding(self, binding, theorem: Theorem):
        """
        Augment binding with constructed objects based on derived_from.

        For each variable with derived_from:
        - If components are bound, construct the composite
        - If composite is bound, extract the components

        Args:
            binding: Current variable binding (Binding instance)
            theorem: Theorem with variable metadata

        Returns:
            Augmented binding with constructed/extracted objects
        """
        # Import Binding here to avoid circular import
        from geometry_prover.theorems.matcher import Binding

        augmented = Binding()

        # Copy existing bindings
        for var, value in binding.bindings.items():
            augmented.bind(var, value)

        # Process each variable with derived_from
        for variable in theorem.variables:
            if not variable.derived_from:
                continue

            var_name = variable.name
            components = variable.derived_from

            # Case 1: Components are bound → construct composite
            if all(augmented.get(c) for c in components):
                if not augmented.get(var_name):
                    composite = self._construct_composite(
                        variable.type,
                        [augmented.get(c) for c in components]
                    )
                    if composite is not None:
                        augmented.bind(var_name, composite)

            # Case 2: Composite is bound → extract components
            elif augmented.get(var_name):
                composite = augmented.get(var_name)
                extracted = self._extract_components(composite, variable.type)

                if extracted and len(extracted) == len(components):
                    for i, component_var in enumerate(components):
                        if not augmented.get(component_var):
                            augmented.bind(component_var, extracted[i])

        return augmented

    def _construct_composite(self, obj_type: str, components: List) -> Optional[object]:
        """
        Construct a composite object from components.

        Args:
            obj_type: Type of object to construct ("line", "segment", "angle", "triangle")
            components: List of component objects (e.g., points)

        Returns:
            Constructed composite object, or None if construction fails
        """
        try:
            if obj_type == "line":
                if len(components) >= 2:
                    if components[0] == components[1]:
                        return None  # Degenerate line
                    return Line(components[0], components[1])
            elif obj_type == "segment":
                if len(components) >= 2:
                    if components[0] == components[1]:
                        return None  # Degenerate segment
                    return Segment(components[0], components[1])
            elif obj_type == "angle":
                if len(components) >= 3:
                    a, b, c = components[:3]
                    if a == b or b == c or a == c:
                        return None  # Degenerate angle
                    return Angle(components[0], components[1], components[2])
            elif obj_type == "triangle":
                # Triangle is not a geometric object, it's a fact
                # Return tuple of points for now
                if len(components) >= 3:
                    first_three = components[:3]
                    if len(set(first_three)) < 3:
                        return None  # Degenerate triangle
                    return tuple(first_three)
        except Exception as e:
            # If construction fails, return None
            # This allows matching to continue without the constructed object
            return None

        return None

    def _extract_components(self, obj, obj_type: str) -> Optional[List]:
        """
        Extract components from a composite object.

        Args:
            obj: Composite object (Line, Segment, Angle, etc.)
            obj_type: Expected type of the object

        Returns:
            List of component objects, or None if extraction fails
        """
        try:
            if obj_type == "line" and isinstance(obj, Line):
                return [obj.point1, obj.point2]
            elif obj_type == "segment" and isinstance(obj, Segment):
                return [obj.point1, obj.point2]
            elif obj_type == "angle" and isinstance(obj, Angle):
                return [obj.point1, obj.vertex, obj.point2]
            elif obj_type == "triangle" and isinstance(obj, tuple):
                return list(obj)
        except Exception:
            # If extraction fails, return None
            return None

        return None
