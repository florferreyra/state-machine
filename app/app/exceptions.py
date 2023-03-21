"""Module to handle custom exceptions"""


class InvalidTransition(Exception):
    """Moving from a state to another is not possible."""
    pass


class AbortTransition(Exception):
    """Changing state should be aborted"""
    pass
