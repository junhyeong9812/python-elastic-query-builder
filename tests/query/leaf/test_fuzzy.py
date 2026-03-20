"""query/leaf/fuzzy.py에 대한 단위 테스트.

FuzzyQuery가 올바른 Elasticsearch 퍼지 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.fuzzy import FuzzyQuery


class TestFuzzyQuery:
    """FuzzyQuery 테스트."""

    def test_fuzzy_query_basic(self):
        """기본 Fuzzy 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = FuzzyQuery.build("name", "test")
        expected = {"fuzzy": {"name": {"value": "test"}}}
        assert result == expected

    def test_fuzzy_query_with_fuzziness_auto(self):
        """fuzziness AUTO 옵션이 포함된 Fuzzy 쿼리가 올바르게 생성되는지 확인합니다."""
        result = FuzzyQuery.build("name", "test", fuzziness="AUTO")
        expected = {"fuzzy": {"name": {"value": "test", "fuzziness": "AUTO"}}}
        assert result == expected

    def test_fuzzy_query_with_fuzziness_number(self):
        """fuzziness 숫자 옵션이 포함된 Fuzzy 쿼리가 올바르게 생성되는지 확인합니다."""
        result = FuzzyQuery.build("name", "test", fuzziness=2)
        expected = {"fuzzy": {"name": {"value": "test", "fuzziness": 2}}}
        assert result == expected

    def test_fuzzy_query_with_prefix_length(self):
        """prefix_length 옵션이 포함된 Fuzzy 쿼리가 올바르게 생성되는지 확인합니다."""
        result = FuzzyQuery.build("name", "test", prefix_length=2)
        expected = {"fuzzy": {"name": {"value": "test", "prefix_length": 2}}}
        assert result == expected

    def test_fuzzy_query_with_max_expansions(self):
        """max_expansions 옵션이 포함된 Fuzzy 쿼리가 올바르게 생성되는지 확인합니다."""
        result = FuzzyQuery.build("name", "test", max_expansions=50)
        expected = {"fuzzy": {"name": {"value": "test", "max_expansions": 50}}}
        assert result == expected

    def test_fuzzy_query_with_transpositions(self):
        """transpositions 옵션이 포함된 Fuzzy 쿼리가 올바르게 생성되는지 확인합니다."""
        result = FuzzyQuery.build("name", "test", transpositions=False)
        expected = {"fuzzy": {"name": {"value": "test", "transpositions": False}}}
        assert result == expected

    def test_fuzzy_query_with_boost(self):
        """boost 옵션이 포함된 Fuzzy 쿼리가 올바르게 생성되는지 확인합니다."""
        result = FuzzyQuery.build("name", "test", boost=1.5)
        expected = {"fuzzy": {"name": {"value": "test", "boost": 1.5}}}
        assert result == expected

    def test_fuzzy_query_with_all_options(self):
        """모든 옵션을 사용한 Fuzzy 쿼리가 올바르게 생성되는지 확인합니다."""
        result = FuzzyQuery.build(
            "name", "test",
            fuzziness="AUTO",
            prefix_length=1,
            max_expansions=100,
            transpositions=True,
            boost=2.0,
        )
        expected = {
            "fuzzy": {
                "name": {
                    "value": "test",
                    "fuzziness": "AUTO",
                    "prefix_length": 1,
                    "max_expansions": 100,
                    "transpositions": True,
                    "boost": 2.0,
                }
            }
        }
        assert result == expected

    def test_fuzzy_query_none_options_excluded(self):
        """None인 옵션은 결과에 포함되지 않는지 확인합니다."""
        result = FuzzyQuery.build("name", "test")
        body = result["fuzzy"]["name"]
        assert "value" in body
        assert "fuzziness" not in body
        assert "prefix_length" not in body
        assert "max_expansions" not in body
        assert "transpositions" not in body
        assert "boost" not in body
