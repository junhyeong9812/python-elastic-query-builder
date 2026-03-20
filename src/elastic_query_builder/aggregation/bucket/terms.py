"""Terms 집계 빌더.

필드 값별로 문서를 그룹화하는 bucket 집계를 생성합니다.
"""

from typing import Any, Dict, Optional


class TermsAggregation:
    """Terms bucket 집계를 생성합니다.

    Elasticsearch terms aggregation에 대응합니다.
    지정한 필드의 고유 값별로 문서를 그룹화합니다.
    """

    @staticmethod
    def build(
        field: str,
        size: Optional[int] = None,
        order: Optional[Dict[str, str]] = None,
        min_doc_count: Optional[int] = None,
        missing: Optional[Any] = None,
        include: Optional[str] = None,
        exclude: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Terms 집계 딕셔너리를 생성합니다.

        Args:
            field: 집계할 필드명.
            size: 반환할 버킷 수 (선택).
            order: 버킷 정렬 기준 (선택). 예: {"_count": "desc"}.
            min_doc_count: 최소 문서 수 (선택).
            missing: 필드 값이 없는 문서에 대한 대체 값 (선택).
            include: 포함할 값 패턴 (선택).
            exclude: 제외할 값 패턴 (선택).

        Returns:
            Elasticsearch terms 집계 딕셔너리.
        """
        body: Dict[str, Any] = {"field": field}
        if size is not None:
            body["size"] = size
        if order is not None:
            body["order"] = order
        if min_doc_count is not None:
            body["min_doc_count"] = min_doc_count
        if missing is not None:
            body["missing"] = missing
        if include is not None:
            body["include"] = include
        if exclude is not None:
            body["exclude"] = exclude
        return {"terms": body}
