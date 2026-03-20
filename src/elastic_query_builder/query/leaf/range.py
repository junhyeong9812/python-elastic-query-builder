"""Range 쿼리 빌더.

숫자, 날짜 등의 범위 검색을 위한 range 쿼리를 생성합니다.
"""

from typing import Any, Dict, Optional


class RangeQuery:
    """범위 검색 쿼리를 생성합니다.

    Elasticsearch range 쿼리에 대응합니다.
    숫자, 날짜, IP 주소 등의 범위를 지정하여 문서를 검색합니다.
    """

    @staticmethod
    def build(
        field: str,
        gte: Optional[Any] = None,
        lte: Optional[Any] = None,
        gt: Optional[Any] = None,
        lt: Optional[Any] = None,
        format: Optional[str] = None,
        boost: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Range 쿼리 딕셔너리를 생성합니다.

        Args:
            field: 검색할 필드명.
            gte: 이상 (greater than or equal). 이 값 포함.
            lte: 이하 (less than or equal). 이 값 포함.
            gt: 초과 (greater than). 이 값 미포함.
            lt: 미만 (less than). 이 값 미포함.
            format: 날짜 포맷 (선택). 예: "yyyy-MM-dd".
            boost: 쿼리 가중치 (선택).

        Returns:
            Elasticsearch range 쿼리 딕셔너리.
        """
        range_body: Dict[str, Any] = {}
        if gte is not None:
            range_body["gte"] = gte
        if lte is not None:
            range_body["lte"] = lte
        if gt is not None:
            range_body["gt"] = gt
        if lt is not None:
            range_body["lt"] = lt
        if format is not None:
            range_body["format"] = format
        if boost is not None:
            range_body["boost"] = boost
        return {"range": {field: range_body}}
