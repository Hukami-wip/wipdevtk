from enum import Enum


class ModeMetaClass(type):
    def __eq__(self, __o: object) -> bool:
        return self.clseq(__o)

    def __repr__(self) -> str:
        return self.clsrepr()

    def __str__(self):
        return self.clsstr()


class MODE(metaclass=ModeMetaClass):
    CURRENT = None

    @classmethod
    def set(cls, mode):
        if cls.CURRENT is None:
            cls.CURRENT = ModeType.normalize(mode)

    @classmethod
    def clseq(cls, __o: object) -> bool:
        return cls.CURRENT == __o

    @classmethod
    def clsrepr(cls) -> str:
        return repr(cls.CURRENT)

    @classmethod
    def clsstr(cls):
        if cls.CURRENT is not None:
            return str(cls.CURRENT.value)
        else:
            return "NO MODE"

    @classmethod
    def reset(cls):
        """
        Never use this function !
        (except for testing purpose)
        """
        cls.CURRENT = None


class ModeType(Enum):
    DEV = "DEVELOPMENT"
    TEST = "TEST"
    DEBUG = "DEBUG"
    PROD = "PRODUCTION"
    PROFILE = "PROFILE"

    @staticmethod
    def normalize(launching_mode: str):
        if launching_mode in list(ModeType):
            return launching_mode

        mode_string = launching_mode.strip().lower()
        if mode_string in ["prod", "production"]:
            return ModeType.PROD

        elif mode_string in ["debug", "bug"]:
            return ModeType.DEBUG

        elif mode_string in ["test", "testing"]:
            return ModeType.TEST

        elif mode_string in ["dev", "develop", "development", "developement"]:
            return ModeType.DEV

        elif mode_string in ["futur", "future"]:
            return ModeType.FUTURE

        elif mode_string in ["profile", "profiling", "prof"]:
            return ModeType.PROFILE

        else:
            raise ValueError(
                f"Launching MODE {launching_mode} doesn't exist\n"
                f"Existing one are: {list(ModeType)}"
            )


DEV = ModeType.DEV
TEST = ModeType.TEST
DEBUG = ModeType.DEBUG
PROD = ModeType.PROD
PROFILE = ModeType.PROFILE
