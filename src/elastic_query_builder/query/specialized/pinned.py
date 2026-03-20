"""pinned 쿼리 빌더.

Elasticsearch의 pinned 쿼리를 생성합니다.
특정 문서를 검색 결과 상단에 고정합니다.
"""

from typing import Any, Dict, List, Optional


class PinnedQuery:
    """pinned 쿼리 빌더."""

    @staticmethod
    def build(
        ids: List[str],
        organic: Dict[str, Any],
        boost: Optional[float] = None,
    ) -> Dict[str, Any]:
        """pinned 쿼리 딕셔너리를 생성합니다.

        Args:
            ids: 상단에 고정할 문서 ID 목록.
            organic: 나머지 결과를 위한 쿼리.
            boost: 부스트 값.

        Returns:
            pinned 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"ids": ids, "organic": organic}
        if boost is not None:
            body["boost"] = boost
        return {"pinned": body}
