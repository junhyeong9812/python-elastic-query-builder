"""Regexp 쿼리 빌더.

정규 표현식 기반 검색 쿼리를 생성합니다.
"""

from typing import Any, Dict, Optional


class RegexpQuery:
    """정규 표현식 매칭 쿼리를 생성합니다.

    Elasticsearch regexp 쿼리에 대응합니다.
    정규 표현식 패턴과 일치하는 용어를 검색합니다.
    """

    @staticmethod
    def build(
        field: str,
        value: str,
        flags: Optional[str] = None,
        max_determinized_states: Optional[int] = None,
        boost: Optional[float] = None,
        case_insensitive: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Regexp 쿼리 딕셔너리를 생성합니다.

        Args:
            field: 검색할 필드명.
            value: 정규 표현식 패턴.
            flags: 정규 표현식 플래그 (선택).
            max_determinized_states: 최대 결정화 상태 수 (선택).
            boost: 쿼리 가중치 (선택).
            case_insensitive: 대소문자 무시 여부 (선택).

        Returns:
            Elasticsearch regexp 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"value": value}
        if flags is not None:
            body["flags"] = flags
        if max_determinized_states is not None:
            body["max_determinized_states"] = max_determinized_states
        if boost is not None:
            body["boost"] = boost
        if case_insensitive is not None:
            body["case_insensitive"] = case_insensitive
        return {"regexp": {field: body}}
