"""Nested 집계 빌더.

중첩(nested) 타입 필드 내부에서 집계를 수행하는 bucket 집계를 생성합니다.
"""

from typing import Any, Dict


class NestedAggregation:
    """Nested bucket 집계를 생성합니다.

    Elasticsearch nested aggregation에 대응합니다.
    nested 타입으로 매핑된 필드 내부의 객체를 대상으로 집계를 수행합니다.
    """

    @staticmethod
    def build(path: str) -> Dict[str, Any]:
        """Nested 집계 딕셔너리를 생성합니다.

        Args:
            path: 중첩 필드의 경로.

        Returns:
            Elasticsearch nested 집계 딕셔너리.
        """
        return {"nested": {"path": path}}
