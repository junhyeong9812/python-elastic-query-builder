"""IDs 쿼리 빌더.

문서 ID 목록을 기반으로 검색하는 쿼리를 생성합니다.
"""

from typing import Any, Dict, List


class IdsQuery:
    """문서 ID 기반 검색 쿼리를 생성합니다.

    Elasticsearch ids 쿼리에 대응합니다.
    _id 필드의 값을 기반으로 문서를 검색합니다.
    """

    @staticmethod
    def build(values: List[str]) -> Dict[str, Any]:
        """IDs 쿼리 딕셔너리를 생성합니다.

        Args:
            values: 검색할 문서 ID 목록.

        Returns:
            Elasticsearch ids 쿼리 딕셔너리.
        """
        return {"ids": {"values": values}}
