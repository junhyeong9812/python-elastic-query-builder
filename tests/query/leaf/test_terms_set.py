"""query/leaf/terms_set.py에 대한 단위 테스트.

TermsSetQuery가 올바른 Elasticsearch 쿼리 딕셔너리를 생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.leaf.terms_set import TermsSetQuery


class TestTermsSetQuery:
    """TermsSetQuery 테스트."""

    def test_terms_set_with_minimum_should_match_field(self):
        """minimum_should_match_field를 사용한 terms_set 쿼리를 확인합니다."""
        result = TermsSetQuery.build(
            "programming_languages", ["python", "java", "go"],
            minimum_should_match_field="required_matches",
        )
        expected = {
            "terms_set": {
                "programming_languages": {
                    "terms": ["python", "java", "go"],
                    "minimum_should_match_field": "required_matches",
                }
            }
        }
        assert result == expected

    def test_terms_set_with_minimum_should_match_script(self):
        """minimum_should_match_script를 사용한 terms_set 쿼리를 확인합니다."""
        script = {"source": "Math.min(params.num_terms, doc['required_matches'].value)"}
        result = TermsSetQuery.build(
            "programming_languages", ["python", "java"],
            minimum_should_match_script=script,
        )
        expected = {
            "terms_set": {
                "programming_languages": {
                    "terms": ["python", "java"],
                    "minimum_should_match_script": script,
                }
            }
        }
        assert result == expected

    def test_terms_set_without_minimum_should_match(self):
        """minimum_should_match 없이 terms_set 쿼리를 확인합니다."""
        result = TermsSetQuery.build("tags", ["elastic", "search"])
        expected = {
            "terms_set": {
                "tags": {
                    "terms": ["elastic", "search"],
                }
            }
        }
        assert result == expected

    def test_terms_set_with_boost(self):
        """boost가 포함된 terms_set 쿼리를 확인합니다."""
        result = TermsSetQuery.build(
            "tags", ["elastic"], minimum_should_match_field="required", boost=1.5,
        )
        body = result["terms_set"]["tags"]
        assert body["boost"] == 1.5
        assert body["terms"] == ["elastic"]
        assert body["minimum_should_match_field"] == "required"

    def test_terms_set_none_options_excluded(self):
        """None인 옵션은 결과에 포함되지 않는지 확인합니다."""
        result = TermsSetQuery.build("tags", ["a", "b"])
        body = result["terms_set"]["tags"]
        assert "terms" in body
        assert "minimum_should_match_field" not in body
        assert "minimum_should_match_script" not in body
        assert "boost" not in body

    def test_terms_set_structure_validation(self):
        """terms_set 쿼리의 최상위 구조가 올바른지 확인합니다."""
        result = TermsSetQuery.build("field", [1, 2, 3])
        assert "terms_set" in result
        assert "field" in result["terms_set"]
        assert result["terms_set"]["field"]["terms"] == [1, 2, 3]
