"""Nested 쿼리 빌더.

중첩(nested) 타입 필드 내부의 문서를 검색하는 쿼리를 생성합니다.
"""

from typing import Any, Dict, Optional


class NestedQuery:
    """중첩 타입 필드 검색 쿼리를 생성합니다.

    Elasticsearch nested 쿼리에 대응합니다.
    nested 타입으로 매핑된 필드 내부의 객체를 독립적으로 검색할 때 사용합니다.
    """

    @staticmethod
    def build(
        path: str,
        query: Dict[str, Any],
        score_mode: Optional[str] = None,
        ignore_unmapped: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Nested 쿼리 딕셔너리를 생성합니다.

        Args:
            path: 중첩 필드의 경로.
            query: 중첩 필드 내부에서 실행할 쿼리 딕셔너리.
            score_mode: 점수 계산 방식 (선택). "avg", "max", "min", "sum", "none".
            ignore_unmapped: 매핑되지 않은 필드 무시 여부 (선택).

        Returns:
            Elasticsearch nested 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"path": path, "query": query}
        if score_mode is not None:
            body["score_mode"] = score_mode
        if ignore_unmapped is not None:
            body["ignore_unmapped"] = ignore_unmapped
        return {"nested": body}
