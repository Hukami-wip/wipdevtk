from abc import ABC, abstractmethod

from wipdevtk.dev import log
from wipdevtk.exceptions import handle_exception
from wipdevtk.meta import AbstractSingletonConnector


class Connector(ABC, metaclass=AbstractSingletonConnector):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def is_alive(self):
        raise NotImplementedError

    def check_connection(self):
        try:
            if not self.is_alive():
                log(f"{self.__class__.__name__} {self.name} attempt to reconnect...")
                self.connect()
            return True
        except Exception as exception:
            handle_exception(exception, no_raise=True)
            return False

    # @staticmethod
    # def ensure_connection(func):
    #     @wraps(func)
    #     def wrapper(self, *args, **kwargs):
    #         if self.check_connection():
    #             return func(self, *args, **kwargs)
    #         else:
    #             raise SystemException(f"{self.__class__.__name__} connection failed")

    #     return wrapper
