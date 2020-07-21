from enum import Enum


class ExchangeType(Enum):
    """Defines all possible exchange types
    """

    DIRECT = "direct"
    """direct exchange"""

    FANOUT = "fanout"
    """fanout exchange"""

    TOPIC = "topic"
    """topic exchange"""

    HEADERS = "headers"
    """headers exchange"""
