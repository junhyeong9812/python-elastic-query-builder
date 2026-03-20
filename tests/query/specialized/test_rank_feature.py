"""query/specialized/rank_feature.py에 대한 단위 테스트.

RankFeatureQuery가 올바른 Elasticsearch rank_feature 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.specialized.rank_feature import RankFeatureQuery


class TestRankFeatureQuery:
    """RankFeatureQuery 테스트."""

    def test_basic(self):
        """기본 rank_feature 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = RankFeatureQuery.build(field="pagerank")
        expected = {"rank_feature": {"field": "pagerank"}}
        assert result == expected

    def test_with_boost(self):
        """boost 옵션이 올바르게 설정되는지 확인합니다."""
        result = RankFeatureQuery.build(field="pagerank", boost=2.0)
        assert result["rank_feature"]["boost"] == 2.0

    def test_with_saturation(self):
        """saturation 함수가 올바르게 설정되는지 확인합니다."""
        result = RankFeatureQuery.build(
            field="pagerank",
            saturation={"pivot": 8},
        )
        assert result["rank_feature"]["saturation"] == {"pivot": 8}

    def test_with_log(self):
        """log 함수가 올바르게 설정되는지 확인합니다."""
        result = RankFeatureQuery.build(
            field="pagerank",
            log={"scaling_factor": 4},
        )
        assert result["rank_feature"]["log"] == {"scaling_factor": 4}

    def test_with_sigmoid(self):
        """sigmoid 함수가 올바르게 설정되는지 확인합니다."""
        result = RankFeatureQuery.build(
            field="pagerank",
            sigmoid={"pivot": 7, "exponent": 0.6},
        )
        assert result["rank_feature"]["sigmoid"] == {"pivot": 7, "exponent": 0.6}

    def test_with_linear(self):
        """linear 함수가 올바르게 설정되는지 확인합니다."""
        result = RankFeatureQuery.build(
            field="pagerank",
            linear={},
        )
        assert result["rank_feature"]["linear"] == {}

    def test_optional_params_not_included_when_none(self):
        """None인 선택적 파라미터가 결과에 포함되지 않는지 확인합니다."""
        result = RankFeatureQuery.build(field="pagerank")
        body = result["rank_feature"]
        assert "boost" not in body
        assert "saturation" not in body
        assert "log" not in body
        assert "sigmoid" not in body
        assert "linear" not in body
