"""Term 계열 쿼리 빌더.

정확한 값 매칭을 위한 term과 terms 쿼리를 생성합니다.
"""

from typing import Any, Dict, List, Optional


class TermQuery:
    """단일 값에 대한 정확한 일치 쿼리를 생성합니다.

    Elasticsearch term 쿼리에 대응합니다.
    분석되지 않은(not analyzed) 필드에서 정확한 값을 찾을 때 사용합니다.
    """

    @staticmethod
    def build(field: str, value: Any, boost: Optional[float] = None) -> Dict[str, Any]:
        """Term 쿼리 딕셔너리를 생성합니다.

        Args:
            field: 검색할 필드명.
            value: 검색할 정확한 값.
            boost: 쿼리 가중치 (선택).

        Returns:
            Elasticsearch term 쿼리 딕셔너리.
        """
        term_body: Dict[str, Any] = {"value": value}
        if boost is not None:
            term_body["boost"] = boost
        return {"term": {field: term_body}}


class TermsQuery:
    """여러 값에 대한 일치 쿼리를 생성합니다.

    Elasticsearch terms 쿼리에 대응합니다.
    주어진 값 목록 중 하나라도 일치하면 문서가 반환됩니다.
    """

    @staticmethod
    def build(field: str, values: List[Any], boost: Optional[float] = None) -> Dict[str, Any]:
        """Terms 쿼리 딕셔너리를 생성합니다.

        Args:
            field: 검색할 필드명.
            values: 검색할 값 목록.
            boost: 쿼리 가중치 (선택).

        Returns:
            Elasticsearch terms 쿼리 딕셔너리.
        """
        result: Dict[str, Any] = {"terms": {field: values}}
        if boost is not None:
            result["terms"]["boost"] = boost
        return result
