"""query/compound/dis_max.py에 대한 단위 테스트.

DisMaxQuery가 올바른 Elasticsearch dis_max 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.compound.dis_max import DisMaxQuery


class TestDisMaxQuery:
    """DisMaxQuery 테스트."""

    def test_dis_max_basic(self):
        """기본 DisMax 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        q1 = {"match": {"title": {"query": "검색어"}}}
        q2 = {"match": {"body": {"query": "검색어"}}}
        result = DisMaxQuery.build(queries=[q1, q2])
        expected = {
            "dis_max": {
                "queries": [
                    {"match": {"title": {"query": "검색어"}}},
                    {"match": {"body": {"query": "검색어"}}},
                ]
            }
        }
        assert result == expected

    def test_dis_max_with_tie_breaker(self):
        """tie_breaker 옵션이 포함된 DisMax 쿼리가 올바르게 생성되는지 확인합니다."""
        q1 = {"match": {"title": {"query": "foo"}}}
        q2 = {"match": {"body": {"query": "foo"}}}
        result = DisMaxQuery.build(queries=[q1, q2], tie_breaker=0.7)
        expected = {
            "dis_max": {
                "queries": [
                    {"match": {"title": {"query": "foo"}}},
                    {"match": {"body": {"query": "foo"}}},
                ],
                "tie_breaker": 0.7,
            }
        }
        assert result == expected

    def test_dis_max_with_boost(self):
        """boost 옵션이 포함된 DisMax 쿼리가 올바르게 생성되는지 확인합니다."""
        q1 = {"term": {"status": {"value": "active"}}}
        q2 = {"term": {"type": {"value": "post"}}}
        result = DisMaxQuery.build(queries=[q1, q2], boost=1.2)
        expected = {
            "dis_max": {
                "queries": [
                    {"term": {"status": {"value": "active"}}},
                    {"term": {"type": {"value": "post"}}},
                ],
                "boost": 1.2,
            }
        }
        assert result == expected

    def test_dis_max_all_options(self):
        """tie_breaker와 boost 모두 포함된 DisMax 쿼리가 올바르게 생성되는지 확인합니다."""
        q1 = {"match": {"title": {"query": "검색"}}}
        q2 = {"match": {"content": {"query": "검색"}}}
        result = DisMaxQuery.build(queries=[q1, q2], tie_breaker=0.3, boost=1.5)
        expected = {
            "dis_max": {
                "queries": [
                    {"match": {"title": {"query": "검색"}}},
                    {"match": {"content": {"query": "검색"}}},
                ],
                "tie_breaker": 0.3,
                "boost": 1.5,
            }
        }
        assert result == expected

    def test_dis_max_single_query(self):
        """단일 쿼리로 DisMax를 생성할 수 있는지 확인합니다."""
        q = {"match": {"title": {"query": "foo"}}}
        result = DisMaxQuery.build(queries=[q])
        expected = {
            "dis_max": {
                "queries": [{"match": {"title": {"query": "foo"}}}]
            }
        }
        assert result == expected

    def test_dis_max_without_tie_breaker_has_no_key(self):
        """tie_breaker를 지정하지 않으면 결과에 키가 없는지 확인합니다."""
        q = {"match": {"title": {"query": "foo"}}}
        result = DisMaxQuery.build(queries=[q])
        assert "tie_breaker" not in result["dis_max"]

    def test_dis_max_without_boost_has_no_key(self):
        """boost를 지정하지 않으면 결과에 키가 없는지 확인합니다."""
        q = {"match": {"title": {"query": "foo"}}}
        result = DisMaxQuery.build(queries=[q])
        assert "boost" not in result["dis_max"]

    def test_dis_max_structure(self):
        """DisMax 쿼리 결과의 구조가 올바른지 확인합니다."""
        q = {"match": {"title": {"query": "foo"}}}
        result = DisMaxQuery.build(queries=[q])
        assert "dis_max" in result
        assert "queries" in result["dis_max"]
        assert isinstance(result["dis_max"]["queries"], list)
