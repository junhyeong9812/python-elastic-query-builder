"""HasParent 쿼리 빌더.

부모-자식 관계에서 부모 문서를 기준으로 자식 문서를 검색하는 쿼리를 생성합니다.
"""

from typing import Any, Dict, Optional


class HasParentQuery:
    """부모 문서 기반 자식 문서 검색 쿼리를 생성합니다.

    Elasticsearch has_parent 쿼리에 대응합니다.
    join 필드로 매핑된 부모-자식 관계에서 부모 문서 조건에 맞는
    자식 문서를 검색할 때 사용합니다.
    """

    @staticmethod
    def build(
        parent_type: str,
        query: Dict[str, Any],
        score: Optional[bool] = None,
        ignore_unmapped: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """HasParent 쿼리 딕셔너리를 생성합니다.

        Args:
            parent_type: 부모 문서의 타입 이름.
            query: 부모 문서에서 실행할 쿼리 딕셔너리.
            score: 부모 문서의 점수를 자식 문서에 전파할지 여부 (선택).
            ignore_unmapped: 매핑되지 않은 필드 무시 여부 (선택).

        Returns:
            Elasticsearch has_parent 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"parent_type": parent_type, "query": query}
        if score is not None:
            body["score"] = score
        if ignore_unmapped is not None:
            body["ignore_unmapped"] = ignore_unmapped
        return {"has_parent": body}
