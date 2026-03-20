"""aggregation/metric/top_hits.py에 대한 단위 테스트.

TopHitsAggregation이 올바른 Elasticsearch top_hits 집계 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.aggregation.metric.top_hits import TopHitsAggregation


class TestTopHitsAggregation:
    """TopHitsAggregation 테스트."""

    def test_top_hits_basic(self):
        """기본 top_hits 집계가 올바른 구조를 생성하는지 확인합니다."""
        result = TopHitsAggregation.build()
        expected = {"top_hits": {}}
        assert result == expected

    def test_top_hits_with_size(self):
        """size 옵션이 포함된 top_hits 집계가 올바르게 생성되는지 확인합니다."""
        result = TopHitsAggregation.build(size=5)
        expected = {"top_hits": {"size": 5}}
        assert result == expected

    def test_top_hits_with_sort(self):
        """sort 옵션이 포함된 top_hits 집계가 올바르게 생성되는지 확인합니다."""
        result = TopHitsAggregation.build(sort=[{"date": {"order": "desc"}}])
        expected = {
            "top_hits": {
                "sort": [{"date": {"order": "desc"}}],
            }
        }
        assert result == expected

    def test_top_hits_with_source(self):
        """_source 옵션이 포함된 top_hits 집계가 올바르게 생성되는지 확인합니다."""
        result = TopHitsAggregation.build(_source=["title", "date"])
        expected = {
            "top_hits": {
                "_source": ["title", "date"],
            }
        }
        assert result == expected

    def test_top_hits_with_source_bool(self):
        """_source에 bool 값을 사용한 top_hits 집계가 올바르게 생성되는지 확인합니다."""
        result = TopHitsAggregation.build(_source=False)
        expected = {"top_hits": {"_source": False}}
        assert result == expected

    def test_top_hits_all_options(self):
        """모든 옵션이 포함된 top_hits 집계가 올바르게 생성되는지 확인합니다."""
        result = TopHitsAggregation.build(
            size=3,
            sort=[{"score": {"order": "desc"}}, {"date": {"order": "asc"}}],
            _source=["title", "date", "score"],
        )
        expected = {
            "top_hits": {
                "size": 3,
                "sort": [
                    {"score": {"order": "desc"}},
                    {"date": {"order": "asc"}},
                ],
                "_source": ["title", "date", "score"],
            }
        }
        assert result == expected

    def test_top_hits_without_optional_has_no_keys(self):
        """선택 옵션을 지정하지 않으면 결과에 해당 키가 없는지 확인합니다."""
        result = TopHitsAggregation.build()
        body = result["top_hits"]
        assert "size" not in body
        assert "sort" not in body
        assert "_source" not in body

    def test_top_hits_structure(self):
        """top_hits 집계 결과의 구조가 올바른지 확인합니다."""
        result = TopHitsAggregation.build(size=1)
        assert "top_hits" in result
        assert isinstance(result["top_hits"], dict)
        assert result["top_hits"]["size"] == 1
