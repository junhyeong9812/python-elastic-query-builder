from enum import Enum

"""Elasticsearch 쿼리 빌더에서 사용하는 열거형 정의.

모든 열거형은 str을 상속하여 문자열로 직접 사용할 수 있습니다.
"""

class SortOrder(str, Enum):
    """정렬 방향을 나타내는 열거형."""

    ASC = "asc"
    DESC = "desc"


class SortMissing(str, Enum):
    """정렬 시 누락된 값의 위치를 지정하는 열거형."""

    FIRST = "_first"
    LAST = "_last"


class BoolClause(str, Enum):
    """Bool 쿼리의 절(clause) 종류를 나타내는 열거형."""

    MUST = "must"
    SHOULD = "should"
    MUST_NOT = "must_not"
    FILTER = "filter"


class MultiMatchType(str, Enum):
    """multi_match 쿼리의 타입을 나타내는 열거형."""

    BEST_FIELDS = "best_fields"
    MOST_FIELDS = "most_fields"
    CROSS_FIELDS = "cross_fields"
    PHRASE = "phrase"
    PHRASE_PREFIX = "phrase_prefix"
    BOOL_PREFIX = "bool_prefix"


class FunctionScoreMode(str, Enum):
    """function_score 쿼리의 score_mode를 나타내는 열거형."""

    MULTIPLY = "multiply"
    SUM = "sum"
    AVG = "avg"
    FIRST = "first"
    MAX = "max"
    MIN = "min"


class FunctionBoostMode(str, Enum):
    """function_score 쿼리의 boost_mode를 나타내는 열거형."""

    MULTIPLY = "multiply"
    REPLACE = "replace"
    SUM = "sum"
    AVG = "avg"
    MAX = "max"
    MIN = "min"