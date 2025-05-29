import traceback
from types import TracebackType

from pydevtk.dev.mode import DEBUG, MODE


def handle_exception(
    exception: Exception,
    no_raise=False,
    log_prefix: str = "",
    log_suffix: str = "",
    show_traceback: bool = False,
    traceback_to_use: TracebackType = None,
    **kwargs,
):
    """
    Helper function to facilitate exception handling and logging.
    Args:
        exception            (Exception) : Exception to be handled
        no_raise                  (bool) : Raise or not, an error for the exception
        log_prefix                 (str) : Prefix to be added to the exception message
        log_suffix                 (str) : Suffix to be added to the exception message
        traceback_to_use (TracebackType) : Traceback to be used
    """
    if exception.args:
        exception_message = exception.args[0]
        original_message = exception.args[0]
    else:
        exception_message = ""
        original_message = ""

    if isinstance(exception, KeyError):
        exception_message = f"Key Error for key: {str(exception)}"

    # Handle traceback logic
    traceback_to_use = kwargs.get("traceback_to_use")

    if show_traceback or (MODE == DEBUG):
        if traceback_to_use is None:
            traceback_string = "".join(
                traceback.format_list(traceback.extract_stack()[:-1])
            )
        else:
            assert isinstance(traceback_to_use, TracebackType)
            traceback_string = "".join(traceback.format_tb(traceback_to_use))

        exception_message = (
            "Traceback (most recent call last):\n"
            + traceback_string
            + f"\n[{type(exception).__name__}] "
            + exception_message
        )

    exception_message_list = [
        str(log_prefix),
        str(exception_message),
        str(log_suffix),
    ]

    exception_message_list = [msg for msg in exception_message_list if msg != ""]
    exception_message = "\n".join(exception_message_list)

    has_new_message = exception_message != original_message

    has_kwargs = len(kwargs) > 0

    reinitialize = has_kwargs or has_new_message

    if reinitialize:
        if "traceback_to_use" not in kwargs.keys():
            kwargs["traceback_to_use"] = exception.__traceback__
        exception = type(exception)(exception_message, **kwargs)

    if no_raise:
        pass
    else:
        raise exception
