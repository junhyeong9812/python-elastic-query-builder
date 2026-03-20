"""Range 집계 빌더.

사용자 정의 범위 구간별로 문서를 그룹화하는 bucket 집계를 생성합니다.
"""

from typing import Any, Dict, List, Optional


class RangeAggregation:
    """Range bucket 집계를 생성합니다.

    Elasticsearch range aggregation에 대응합니다.
    사용자가 정의한 범위 구간별로 문서를 그룹화합니다.
    """

    @staticmethod
    def build(
        field: str,
        ranges: List[Dict[str, Any]],
        keyed: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Range 집계 딕셔너리를 생성합니다.

        Args:
            field: 집계할 필드명.
            ranges: 범위 구간 목록. 예: [{"to": 100}, {"from": 100, "to": 200}].
            keyed: 결과를 키 기반으로 반환할지 여부 (선택).

        Returns:
            Elasticsearch range 집계 딕셔너리.
        """
        body: Dict[str, Any] = {"field": field, "ranges": ranges}
        if keyed is not None:
            body["keyed"] = keyed
        return {"range": body}
