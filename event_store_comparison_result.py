from enum import Enum, auto

class ComparisonResult(str, Enum):
    EQUAL = "EQUAL"
    OLDER = "OLDER"
    NEWER = "NEWER"
    DIVERGING = "DIVERGING"
    OLDER_OR_DIVERGING = "OLDER_OR_DIVERGING"
