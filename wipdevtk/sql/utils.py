from __future__ import annotations

from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String
from sqlalchemy.dialects.mssql import (
    BIGINT,
    BINARY,
    BIT,
    CHAR,
    DATETIME,
    DATETIME2,
    DECIMAL,
    FLOAT,
    INTEGER,
    JSON,
    NCHAR,
    NUMERIC,
    NVARCHAR,
    SMALLDATETIME,
    SMALLINT,
    TINYINT,
    VARBINARY,
    VARCHAR,
)
from sqlalchemy.orm import Session

from wipdevtk.exceptions import handle_exception
from wipdevtk.interfaces.connectors.sql_connector import SQLConnector


class SessionAccess:
    def __set__(self, obj, value):
        type(obj).session = value

    def __get__(self, obj, objtype):
        if obj is not None:
            return getattr(obj, "session")
        else:
            return getattr(objtype, "session")


def get_session():
    return Session(SQLConnector().engine)


def _session(func):
    def handle_session_exception(
        cls, *args, exception: Exception, counter: int, session: Session, **kwargs
    ):
        handle_exception(
            exception=exception,
            no_raise=True,
        )

        session.rollback()
        session.close()
        raise

    def call_with_session(cls, *args, counter: int = 1, **kwargs):
        if "session" not in kwargs.keys():
            with get_session() as session:
                try:
                    return_func = func(cls, session=session, *args, **kwargs)
                    session.commit()
                    session.close()
                except Exception as e:
                    return_func = handle_session_exception(
                        cls,
                        *args,
                        exception=e,
                        counter=counter,
                        session=session,
                        **kwargs,
                    )
        else:
            try:
                return_func = func(cls, *args, **kwargs)
            except Exception as e:
                return_func = handle_session_exception(
                    cls, *args, exception=e, counter=counter, **kwargs
                )
        return return_func

    return call_with_session


def sqlalchemy_to_python_type(sqlalchemy_type):
    # BINARY
    # BIT
    # DATE
    # DATETIME2
    # DATETIMEOFFSET
    # NTEXT
    # SMALLDATETIME
    # TEXT
    # TIME
    # TIMESTAMP
    # UNIQUEIDENTIFIER
    # VARBINARY
    if isinstance(sqlalchemy_type, (Integer, INTEGER, BIGINT, SMALLINT, TINYINT)):
        return int
    elif isinstance(sqlalchemy_type, (Float, DECIMAL, FLOAT, NUMERIC)):
        return float
    elif isinstance(sqlalchemy_type, (String, CHAR, NCHAR, VARCHAR, NVARCHAR, JSON)):
        return str
    elif isinstance(sqlalchemy_type, (DateTime, DATETIME, DATETIME2, SMALLDATETIME)):
        return None
    elif isinstance(sqlalchemy_type, Date):
        return None
    elif isinstance(sqlalchemy_type, (Boolean, BIT)):
        return bool
    elif isinstance(sqlalchemy_type, (VARBINARY, BINARY)):
        return bytes
    else:
        raise ValueError(
            f"The maping for the column type {sqlalchemy_type} is not implemented yet."
        )


def none_as_value(type):
    class NoneAsValueType(type):
        __none_as_value__ = True

    return NoneAsValueType


def non_updatable(_type):
    class NonUpdatable(_type):
        __is_non_updatable__ = True

    return NonUpdatable


def alembic_render_non_updatable(type_, obj, autogen_context):
    """
    Alembic renderer utility for NonUpdatable types.

    This function should be used as a render_item in Alembic's env.py
    to properly render NonUpdatable wrapped types as their underlying types.

    Args:
        type_: The SQLAlchemy type being rendered
        obj: The column object
        autogen_context: Alembic's autogeneration context

    Returns:
        str: The rendered type string, or False to use default rendering
    """
    # Check if this is a NonUpdatable type by looking for the marker attribute
    if hasattr(type_, "__is_non_updatable__") and type_.__is_non_updatable__:
        # Get the underlying type from the MRO (Method Resolution Order)
        for base in type_.__mro__[1:]:
            if base.__name__ != "NonUpdatable" and hasattr(base, "__module__"):
                module = base.__module__

                # Handle SQLAlchemy core types
                if module == "sqlalchemy" or module.startswith("sqlalchemy.sql"):
                    type_name = base.__name__

                    # Check if this has timezone parameter (for DateTime types)
                    if (
                        hasattr(obj, "type")
                        and hasattr(obj.type, "timezone")
                        and obj.type.timezone
                    ):
                        return f"sa.{type_name}(timezone=True)"
                    else:
                        return f"sa.{type_name}()"

                # Handle other SQLAlchemy types
                elif module.startswith("sqlalchemy"):
                    return f"sa.{base.__name__}()"

        # Fallback: if we can't determine the base type, use DateTime
        return "sa.DateTime(timezone=True)"

    # Return False to use default rendering for other types
    return False
