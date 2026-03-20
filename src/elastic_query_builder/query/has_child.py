"""HasChild 쿼리 빌더.

부모-자식 관계에서 자식 문서를 기준으로 부모 문서를 검색하는 쿼리를 생성합니다.
"""

from typing import Any, Dict, Optional


class HasChildQuery:
    """자식 문서 기반 부모 문서 검색 쿼리를 생성합니다.

    Elasticsearch has_child 쿼리에 대응합니다.
    join 필드로 매핑된 부모-자식 관계에서 자식 문서 조건에 맞는
    부모 문서를 검색할 때 사용합니다.
    """

    @staticmethod
    def build(
        type: str,
        query: Dict[str, Any],
        score_mode: Optional[str] = None,
        min_children: Optional[int] = None,
        max_children: Optional[int] = None,
        ignore_unmapped: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """HasChild 쿼리 딕셔너리를 생성합니다.

        Args:
            type: 자식 문서의 타입 이름.
            query: 자식 문서에서 실행할 쿼리 딕셔너리.
            score_mode: 점수 계산 방식 (선택). "avg", "max", "min", "sum", "none".
            min_children: 최소 매칭 자식 문서 수 (선택).
            max_children: 최대 매칭 자식 문서 수 (선택).
            ignore_unmapped: 매핑되지 않은 필드 무시 여부 (선택).

        Returns:
            Elasticsearch has_child 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"type": type, "query": query}
        if score_mode is not None:
            body["score_mode"] = score_mode
        if min_children is not None:
            body["min_children"] = min_children
        if max_children is not None:
            body["max_children"] = max_children
        if ignore_unmapped is not None:
            body["ignore_unmapped"] = ignore_unmapped
        return {"has_child": body}
