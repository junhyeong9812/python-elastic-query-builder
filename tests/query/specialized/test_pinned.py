"""query/specialized/pinned.py에 대한 단위 테스트.

PinnedQuery가 올바른 Elasticsearch pinned 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.specialized.pinned import PinnedQuery


class TestPinnedQuery:
    """PinnedQuery 테스트."""

    def test_basic(self):
        """기본 pinned 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = PinnedQuery.build(
            ids=["1", "2", "3"],
            organic={"match": {"title": "검색"}},
        )
        expected = {
            "pinned": {
                "ids": ["1", "2", "3"],
                "organic": {"match": {"title": "검색"}},
            }
        }
        assert result == expected

    def test_with_boost(self):
        """boost 옵션이 올바르게 설정되는지 확인합니다."""
        result = PinnedQuery.build(
            ids=["doc1"],
            organic={"match_all": {}},
            boost=1.5,
        )
        assert result["pinned"]["boost"] == 1.5

    def test_single_id(self):
        """단일 ID로 pinned 쿼리를 생성할 수 있는지 확인합니다."""
        result = PinnedQuery.build(
            ids=["42"],
            organic={"term": {"status": "published"}},
        )
        assert result["pinned"]["ids"] == ["42"]
        assert result["pinned"]["organic"] == {"term": {"status": "published"}}

    def test_optional_params_not_included_when_none(self):
        """None인 선택적 파라미터가 결과에 포함되지 않는지 확인합니다."""
        result = PinnedQuery.build(
            ids=["1"],
            organic={"match_all": {}},
        )
        assert "boost" not in result["pinned"]
