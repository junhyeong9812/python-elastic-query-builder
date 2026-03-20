"""script_score 쿼리 빌더.

Elasticsearch의 script_score 쿼리를 생성합니다.
스크립트를 사용하여 문서 점수를 커스터마이징합니다.
"""

from typing import Any, Dict, Optional


class ScriptScoreQuery:
    """script_score 쿼리 빌더."""

    @staticmethod
    def build(
        query: Dict[str, Any],
        script: Dict[str, Any],
        boost: Optional[float] = None,
        min_score: Optional[float] = None,
    ) -> Dict[str, Any]:
        """script_score 쿼리 딕셔너리를 생성합니다.

        Args:
            query: 내부 쿼리.
            script: 점수 계산 스크립트.
            boost: 부스트 값.
            min_score: 최소 점수.

        Returns:
            script_score 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"query": query, "script": script}
        if boost is not None:
            body["boost"] = boost
        if min_score is not None:
            body["min_score"] = min_score
        return {"script_score": body}
