"""TopHits 집계 빌더.

각 버킷 내 상위 문서를 반환하는 metric 집계를 생성합니다.
"""

from typing import Any, Dict, List, Optional, Union


class TopHitsAggregation:
    """TopHits metric 집계를 생성합니다.

    Elasticsearch top_hits aggregation에 대응합니다.
    bucket 집계 내부에서 사용하여 각 그룹의 상위 문서를 가져옵니다.
    """

    @staticmethod
    def build(
        size: Optional[int] = None,
        sort: Optional[List[Dict[str, Any]]] = None,
        _source: Optional[Union[bool, List[str]]] = None,
    ) -> Dict[str, Any]:
        """TopHits 집계 딕셔너리를 생성합니다.

        Args:
            size: 반환할 상위 문서 수 (선택).
            sort: 정렬 기준 목록 (선택). 예: [{"date": {"order": "desc"}}].
            _source: 반환할 필드 목록 또는 소스 포함 여부 (선택).

        Returns:
            Elasticsearch top_hits 집계 딕셔너리.
        """
        body: Dict[str, Any] = {}
        if size is not None:
            body["size"] = size
        if sort is not None:
            body["sort"] = sort
        if _source is not None:
            body["_source"] = _source
        return {"top_hits": body}
