"""function_score 쿼리 빌더.

Elasticsearch의 function_score 쿼리를 생성합니다.
문서의 점수를 커스텀 함수로 조정할 수 있습니다.
"""

from typing import Any, Dict, List, Optional


class FunctionScoreQuery:
    """function_score 쿼리를 생성하는 정적 빌더."""

    @staticmethod
    def build(query: Dict[str, Any], functions: Optional[List[Dict[str, Any]]] = None,
              score_mode: Optional[str] = None, boost_mode: Optional[str] = None,
              max_boost: Optional[float] = None, boost: Optional[float] = None,
              min_score: Optional[float] = None) -> Dict[str, Any]:
        """function_score 쿼리를 생성합니다.

        Args:
            query: 기본 쿼리.
            functions: 점수 함수 목록.
            score_mode: 함수 점수 결합 방식.
            boost_mode: 쿼리 점수와 함수 점수 결합 방식.
            max_boost: 최대 부스트 값.
            boost: 쿼리 부스트 값.
            min_score: 최소 점수 임계값.

        Returns:
            function_score 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"query": query}
        if functions is not None:
            body["functions"] = functions
        if score_mode is not None:
            body["score_mode"] = score_mode
        if boost_mode is not None:
            body["boost_mode"] = boost_mode
        if max_boost is not None:
            body["max_boost"] = max_boost
        if boost is not None:
            body["boost"] = boost
        if min_score is not None:
            body["min_score"] = min_score
        return {"function_score": body}
