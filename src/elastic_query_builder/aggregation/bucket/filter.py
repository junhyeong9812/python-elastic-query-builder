"""Filter / Filters 집계 빌더.

단일 또는 다중 필터 조건으로 문서를 그룹화하는 bucket 집계를 생성합니다.
"""

from typing import Any, Dict, Optional


class FilterAggregation:
    """Filter bucket 집계를 생성합니다.

    Elasticsearch filter aggregation에 대응합니다.
    단일 필터 조건에 매칭되는 문서만을 대상으로 집계합니다.
    """

    @staticmethod
    def build(filter_query: Dict[str, Any]) -> Dict[str, Any]:
        """Filter 집계 딕셔너리를 생성합니다.

        Args:
            filter_query: 필터로 사용할 쿼리 딕셔너리.

        Returns:
            Elasticsearch filter 집계 딕셔너리.
        """
        return {"filter": filter_query}


class FiltersAggregation:
    """Filters bucket 집계를 생성합니다.

    Elasticsearch filters aggregation에 대응합니다.
    이름이 지정된 여러 필터 조건으로 문서를 그룹화합니다.
    """

    @staticmethod
    def build(
        filters: Dict[str, Dict[str, Any]],
        other_bucket: Optional[bool] = None,
        other_bucket_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Filters 집계 딕셔너리를 생성합니다.

        Args:
            filters: 이름-쿼리 매핑 딕셔너리.
            other_bucket: 나머지 문서를 위한 버킷 생성 여부 (선택).
            other_bucket_key: other_bucket의 키 이름 (선택).

        Returns:
            Elasticsearch filters 집계 딕셔너리.
        """
        body: Dict[str, Any] = {"filters": filters}
        if other_bucket is not None:
            body["other_bucket"] = other_bucket
        if other_bucket_key is not None:
            body["other_bucket_key"] = other_bucket_key
        return {"filters": body}
