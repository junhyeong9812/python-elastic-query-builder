"""HasChildQuery 테스트."""

import pytest
from elastic_query_builder.query.has_child import HasChildQuery


class TestHasChildQuery:
    """HasChildQuery.build 메서드 테스트."""

    def test_basic(self):
        """필수 파라미터만으로 has_child 쿼리를 생성한다."""
        result = HasChildQuery.build(
            type="child_doc",
            query={"match": {"title": "test"}},
        )
        assert result == {
            "has_child": {
                "type": "child_doc",
                "query": {"match": {"title": "test"}},
            }
        }

    def test_score_mode(self):
        """score_mode 옵션을 포함한 has_child 쿼리를 생성한다."""
        result = HasChildQuery.build(
            type="child_doc",
            query={"match_all": {}},
            score_mode="avg",
        )
        assert result["has_child"]["score_mode"] == "avg"

    def test_min_children(self):
        """min_children 옵션을 포함한 has_child 쿼리를 생성한다."""
        result = HasChildQuery.build(
            type="child_doc",
            query={"match_all": {}},
            min_children=2,
        )
        assert result["has_child"]["min_children"] == 2

    def test_max_children(self):
        """max_children 옵션을 포함한 has_child 쿼리를 생성한다."""
        result = HasChildQuery.build(
            type="child_doc",
            query={"match_all": {}},
            max_children=10,
        )
        assert result["has_child"]["max_children"] == 10

    def test_ignore_unmapped(self):
        """ignore_unmapped 옵션을 포함한 has_child 쿼리를 생성한다."""
        result = HasChildQuery.build(
            type="child_doc",
            query={"match_all": {}},
            ignore_unmapped=True,
        )
        assert result["has_child"]["ignore_unmapped"] is True

    def test_all_options(self):
        """모든 옵션을 포함한 has_child 쿼리를 생성한다."""
        result = HasChildQuery.build(
            type="child_doc",
            query={"term": {"status": "active"}},
            score_mode="max",
            min_children=1,
            max_children=5,
            ignore_unmapped=False,
        )
        assert result == {
            "has_child": {
                "type": "child_doc",
                "query": {"term": {"status": "active"}},
                "score_mode": "max",
                "min_children": 1,
                "max_children": 5,
                "ignore_unmapped": False,
            }
        }

    def test_no_optional_keys(self):
        """선택 파라미터를 생략하면 해당 키가 결과에 포함되지 않는다."""
        result = HasChildQuery.build(
            type="answer",
            query={"match": {"body": "elasticsearch"}},
        )
        body = result["has_child"]
        assert "score_mode" not in body
        assert "min_children" not in body
        assert "max_children" not in body
        assert "ignore_unmapped" not in body
