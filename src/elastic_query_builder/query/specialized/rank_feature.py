"""rank_feature 쿼리 빌더.

Elasticsearch의 rank_feature 쿼리를 생성합니다.
rank_feature 또는 rank_features 필드의 값을 사용하여 문서 점수를 계산합니다.
"""

from typing import Any, Dict, Optional


class RankFeatureQuery:
    """rank_feature 쿼리 빌더."""

    @staticmethod
    def build(
        field: str,
        boost: Optional[float] = None,
        saturation: Optional[Dict[str, Any]] = None,
        log: Optional[Dict[str, Any]] = None,
        sigmoid: Optional[Dict[str, Any]] = None,
        linear: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """rank_feature 쿼리 딕셔너리를 생성합니다.

        Args:
            field: rank_feature 필드명.
            boost: 부스트 값.
            saturation: saturation 함수 설정.
            log: log 함수 설정.
            sigmoid: sigmoid 함수 설정.
            linear: linear 함수 설정.

        Returns:
            rank_feature 쿼리 딕셔너리.
        """
        body: Dict[str, Any] = {"field": field}
        if boost is not None:
            body["boost"] = boost
        if saturation is not None:
            body["saturation"] = saturation
        if log is not None:
            body["log"] = log
        if sigmoid is not None:
            body["sigmoid"] = sigmoid
        if linear is not None:
            body["linear"] = linear
        return {"rank_feature": body}
