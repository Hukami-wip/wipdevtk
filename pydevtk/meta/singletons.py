from abc import ABCMeta
from typing import Any


class Singleton(type):
    """
    A singleton metaclass implementation that ensures a class has only one instance and
    provides a global point of access to it.
    """

    _instances: "dict[Any, Any]" = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwds)
        return cls._instances[cls]


class NamedSingleton(type):
    """
    A singleton metaclass implementation that allows a single class to have multiple
    named instances and provides a global point of access to them.
    """

    _instances: "dict[Any, dict[str, Any]]" = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if "name" not in kwds.keys():
            name = cls.__name__
        else:
            name = kwds["name"]

        if cls not in cls._instances:
            cls._instances[cls] = {}
            cls._instances[cls][name] = super(NamedSingleton, cls).__call__(
                *args, **kwds
            )

        else:
            if name not in cls._instances[cls].keys():
                cls._instances[cls][name] = super(NamedSingleton, cls).__call__(
                    *args, **kwds
                )

        return cls._instances[cls][name]


class AbstractSingleton(ABCMeta, Singleton): ...


class AbstractNamedSingleton(ABCMeta, NamedSingleton): ...
