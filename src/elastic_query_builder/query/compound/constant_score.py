"""ConstantScore 쿼리 빌더.

필터 조건에 일치하는 모든 문서에 동일한 점수를 부여하는 쿼리를 생성합니다.
"""

from typing import Any, Dict, Optional


class ConstantScoreQuery:
    """Constant Score 쿼리를 생성합니다.

    Elasticsearch constant_score 쿼리에 대응합니다.
    필터 조건에 일치하는 모든 문서에 동일한 점수(boost 값)를 부여합니다.
    """

    @staticmethod
    def build(
        filter: Dict[str, Any],
        boost: Optional[float] = None,
    ) -> Dict[str, Any]:
        """ConstantScore 쿼리 딕셔너리를 생성합니다.

        Args:
            filter: 필터 쿼리 딕셔너리.
            boost: 일치하는 문서에 부여할 점수 (선택).

        Returns:
            Elasticsearch constant_score 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"filter": filter}
        if boost is not None:
            body["boost"] = boost
        return {"constant_score": body}
