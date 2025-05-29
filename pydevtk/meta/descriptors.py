"""
Descriptor utilities for advanced attribute access patterns.

This module contains descriptor classes that provide specialized behavior
for attribute access, method calls, and property management.
"""

from typing import Any, Type


class MethodCallAccess:
    """
    This descriptor to access different method implementations between
    class and instance through the same interface.

    When accessed from an instance, returns obj.instance_{name}
    When accessed from a class, returns cls.class_{name}

    This is useful for creating unified interfaces that behave differently
    based on whether they're called from a class or an instance.
    """

    def __init__(self, name: str):
        """
        Initialize the descriptor with a method name.

        Args:
            name: The base name for the methods (without instance_/class_ prefix)
        """
        self.name = name

    def __get__(self, obj: Any, objtype: Type = None) -> Any:
        """
        Descriptor getter that routes to different methods based on access context.

        Args:
            obj: The instance accessing the descriptor (None for class access)
            objtype: The class type

        Returns:
            The result of calling either instance_{name} or class_{name}
        """
        if obj is not None:
            return getattr(obj, f"instance_{self.name}")
        else:
            return getattr(objtype, f"class_{self.name}")
