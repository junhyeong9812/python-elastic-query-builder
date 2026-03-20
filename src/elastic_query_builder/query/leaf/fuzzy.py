"""Fuzzy 쿼리 빌더.

유사한 용어를 찾기 위한 퍼지 검색 쿼리를 생성합니다.
"""

from typing import Any, Dict, Optional


class FuzzyQuery:
    """퍼지 매칭 쿼리를 생성합니다.

    Elasticsearch fuzzy 쿼리에 대응합니다.
    편집 거리(edit distance)를 기반으로 유사한 용어를 검색합니다.
    """

    @staticmethod
    def build(
        field: str,
        value: str,
        fuzziness: Optional[Any] = None,
        prefix_length: Optional[int] = None,
        max_expansions: Optional[int] = None,
        transpositions: Optional[bool] = None,
        boost: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Fuzzy 쿼리 딕셔너리를 생성합니다.

        Args:
            field: 검색할 필드명.
            value: 검색할 값.
            fuzziness: 허용할 편집 거리 (선택). 숫자 또는 "AUTO".
            prefix_length: 퍼지 매칭 시작 전 일치해야 하는 접두사 길이 (선택).
            max_expansions: 최대 확장 수 (선택).
            transpositions: 인접 문자 전치 허용 여부 (선택).
            boost: 쿼리 가중치 (선택).

        Returns:
            Elasticsearch fuzzy 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"value": value}
        if fuzziness is not None:
            body["fuzziness"] = fuzziness
        if prefix_length is not None:
            body["prefix_length"] = prefix_length
        if max_expansions is not None:
            body["max_expansions"] = max_expansions
        if transpositions is not None:
            body["transpositions"] = transpositions
        if boost is not None:
            body["boost"] = boost
        return {"fuzzy": {field: body}}
