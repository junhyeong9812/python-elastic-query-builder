"""query/compound/constant_score.py에 대한 단위 테스트.

ConstantScoreQuery가 올바른 Elasticsearch constant_score 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.compound.constant_score import ConstantScoreQuery


class TestConstantScoreQuery:
    """ConstantScoreQuery 테스트."""

    def test_constant_score_basic(self):
        """기본 ConstantScore 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        filter_query = {"term": {"status": {"value": "active"}}}
        result = ConstantScoreQuery.build(filter=filter_query)
        expected = {
            "constant_score": {
                "filter": {"term": {"status": {"value": "active"}}}
            }
        }
        assert result == expected

    def test_constant_score_with_boost(self):
        """boost 옵션이 포함된 ConstantScore 쿼리가 올바르게 생성되는지 확인합니다."""
        filter_query = {"term": {"status": {"value": "published"}}}
        result = ConstantScoreQuery.build(filter=filter_query, boost=1.2)
        expected = {
            "constant_score": {
                "filter": {"term": {"status": {"value": "published"}}},
                "boost": 1.2,
            }
        }
        assert result == expected

    def test_constant_score_without_boost_has_no_key(self):
        """boost를 지정하지 않으면 결과에 키가 없는지 확인합니다."""
        filter_query = {"term": {"status": {"value": "active"}}}
        result = ConstantScoreQuery.build(filter=filter_query)
        assert "boost" not in result["constant_score"]

    def test_constant_score_structure(self):
        """ConstantScore 쿼리 결과의 구조가 올바른지 확인합니다."""
        filter_query = {"match_all": {}}
        result = ConstantScoreQuery.build(filter=filter_query)
        assert "constant_score" in result
        assert "filter" in result["constant_score"]
        assert isinstance(result["constant_score"]["filter"], dict)
