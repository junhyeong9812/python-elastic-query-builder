"""Exists 쿼리 빌더.

특정 필드가 존재하는 문서를 검색하는 쿼리를 생성합니다.
"""

from typing import Any, Dict


class ExistsQuery:
    """필드 존재 여부 검색 쿼리를 생성합니다.

    Elasticsearch exists 쿼리에 대응합니다.
    지정한 필드에 null이 아닌 값이 있는 문서를 반환합니다.
    """

    @staticmethod
    def build(field: str) -> Dict[str, Any]:
        """Exists 쿼리 딕셔너리를 생성합니다.

        Args:
            field: 존재 여부를 확인할 필드명.

        Returns:
            Elasticsearch exists 쿼리 딕셔너리.
        """
        return {"exists": {"field": field}}
