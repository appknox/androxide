"""``androguard.util`` stand-ins."""


def set_log(level: str) -> None:
    """androguard's ``set_log(level)`` configures loguru for androguard's own
    logging. androxide logs nothing, so this does nothing."""
    return None
