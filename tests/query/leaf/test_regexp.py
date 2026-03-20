"""query/leaf/regexp.py에 대한 단위 테스트.

RegexpQuery가 올바른 Elasticsearch 정규 표현식 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.regexp import RegexpQuery


class TestRegexpQuery:
    """RegexpQuery 테스트."""

    def test_regexp_query_basic(self):
        """기본 Regexp 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = RegexpQuery.build("name", "test.*")
        expected = {"regexp": {"name": {"value": "test.*"}}}
        assert result == expected

    def test_regexp_query_with_flags(self):
        """flags 옵션이 포함된 Regexp 쿼리가 올바르게 생성되는지 확인합니다."""
        result = RegexpQuery.build("name", "test.*", flags="ALL")
        expected = {"regexp": {"name": {"value": "test.*", "flags": "ALL"}}}
        assert result == expected

    def test_regexp_query_with_max_determinized_states(self):
        """max_determinized_states 옵션이 포함된 Regexp 쿼리가 올바르게 생성되는지 확인합니다."""
        result = RegexpQuery.build("name", "test.*", max_determinized_states=10000)
        expected = {
            "regexp": {
                "name": {
                    "value": "test.*",
                    "max_determinized_states": 10000,
                }
            }
        }
        assert result == expected

    def test_regexp_query_with_boost(self):
        """boost 옵션이 포함된 Regexp 쿼리가 올바르게 생성되는지 확인합니다."""
        result = RegexpQuery.build("name", "test.*", boost=1.5)
        expected = {"regexp": {"name": {"value": "test.*", "boost": 1.5}}}
        assert result == expected

    def test_regexp_query_with_all_options(self):
        """모든 옵션을 사용한 Regexp 쿼리가 올바르게 생성되는지 확인합니다."""
        result = RegexpQuery.build(
            "name", "test.*",
            flags="COMPLEMENT|INTERVAL",
            max_determinized_states=20000,
            boost=2.0,
            case_insensitive=True,
        )
        expected = {
            "regexp": {
                "name": {
                    "value": "test.*",
                    "flags": "COMPLEMENT|INTERVAL",
                    "max_determinized_states": 20000,
                    "boost": 2.0,
                    "case_insensitive": True,
                }
            }
        }
        assert result == expected

    def test_regexp_query_none_options_excluded(self):
        """None인 옵션은 결과에 포함되지 않는지 확인합니다."""
        result = RegexpQuery.build("name", "test.*")
        body = result["regexp"]["name"]
        assert "value" in body
        assert "flags" not in body
        assert "max_determinized_states" not in body
        assert "boost" not in body
        assert "case_insensitive" not in body
