"""aggregation/bucket/terms.py에 대한 단위 테스트.

TermsAggregation이 올바른 Elasticsearch terms 집계 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.aggregation.bucket.terms import TermsAggregation


class TestTermsAggregation:
    """TermsAggregation 테스트."""

    def test_terms_agg_basic(self):
        """기본 terms 집계가 올바른 구조를 생성하는지 확인합니다."""
        result = TermsAggregation.build("status")
        expected = {"terms": {"field": "status"}}
        assert result == expected

    def test_terms_agg_with_size(self):
        """size 옵션이 포함된 terms 집계가 올바르게 생성되는지 확인합니다."""
        result = TermsAggregation.build("status", size=10)
        expected = {"terms": {"field": "status", "size": 10}}
        assert result == expected

    def test_terms_agg_with_order(self):
        """order 옵션이 포함된 terms 집계가 올바르게 생성되는지 확인합니다."""
        result = TermsAggregation.build("status", order={"_count": "desc"})
        expected = {"terms": {"field": "status", "order": {"_count": "desc"}}}
        assert result == expected

    def test_terms_agg_with_min_doc_count(self):
        """min_doc_count 옵션이 포함된 terms 집계가 올바르게 생성되는지 확인합니다."""
        result = TermsAggregation.build("status", min_doc_count=5)
        expected = {"terms": {"field": "status", "min_doc_count": 5}}
        assert result == expected

    def test_terms_agg_with_missing(self):
        """missing 옵션이 포함된 terms 집계가 올바르게 생성되는지 확인합니다."""
        result = TermsAggregation.build("status", missing="N/A")
        expected = {"terms": {"field": "status", "missing": "N/A"}}
        assert result == expected

    def test_terms_agg_with_include_exclude(self):
        """include/exclude 옵션이 포함된 terms 집계가 올바르게 생성되는지 확인합니다."""
        result = TermsAggregation.build("status", include="pattern*", exclude="other*")
        expected = {
            "terms": {
                "field": "status",
                "include": "pattern*",
                "exclude": "other*",
            }
        }
        assert result == expected

    def test_terms_agg_all_options(self):
        """모든 옵션이 포함된 terms 집계가 올바르게 생성되는지 확인합니다."""
        result = TermsAggregation.build(
            "status",
            size=10,
            order={"_count": "desc"},
            min_doc_count=5,
            missing="N/A",
            include="pattern*",
            exclude="other*",
        )
        expected = {
            "terms": {
                "field": "status",
                "size": 10,
                "order": {"_count": "desc"},
                "min_doc_count": 5,
                "missing": "N/A",
                "include": "pattern*",
                "exclude": "other*",
            }
        }
        assert result == expected

    def test_terms_agg_without_optional_has_no_keys(self):
        """선택 옵션을 지정하지 않으면 결과에 해당 키가 없는지 확인합니다."""
        result = TermsAggregation.build("status")
        terms_body = result["terms"]
        assert "size" not in terms_body
        assert "order" not in terms_body
        assert "min_doc_count" not in terms_body
        assert "missing" not in terms_body
        assert "include" not in terms_body
        assert "exclude" not in terms_body

    def test_terms_agg_structure(self):
        """terms 집계 결과의 구조가 올바른지 확인합니다."""
        result = TermsAggregation.build("status")
        assert "terms" in result
        assert "field" in result["terms"]
        assert result["terms"]["field"] == "status"
