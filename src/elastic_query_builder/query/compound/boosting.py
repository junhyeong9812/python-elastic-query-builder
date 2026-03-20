"""Boosting 쿼리 빌더.

positive 쿼리에 일치하는 문서의 점수를 negative 쿼리 조건에 따라 감소시키는 쿼리를 생성합니다.
"""

from typing import Any, Dict


class BoostingQuery:
    """Boosting 쿼리를 생성합니다.

    Elasticsearch boosting 쿼리에 대응합니다.
    positive 쿼리에 일치하는 문서 중, negative 쿼리에도 일치하는 문서의
    점수를 negative_boost 비율만큼 감소시킵니다.
    """

    @staticmethod
    def build(
        positive: Dict[str, Any],
        negative: Dict[str, Any],
        negative_boost: float,
    ) -> Dict[str, Any]:
        """Boosting 쿼리 딕셔너리를 생성합니다.

        Args:
            positive: 문서가 반드시 일치해야 하는 쿼리 딕셔너리.
            negative: 일치하는 문서의 점수를 감소시킬 쿼리 딕셔너리.
            negative_boost: negative 쿼리에 일치하는 문서의 점수 감소 비율. 0.0~1.0.

        Returns:
            Elasticsearch boosting 쿼리 딕셔너리.
        """
        return {"boosting": {
            "positive": positive,
            "negative": negative,
            "negative_boost": negative_boost,
        }}
