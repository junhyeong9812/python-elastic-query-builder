"""HasParentQuery 테스트."""

import pytest
from elastic_query_builder.query.has_parent import HasParentQuery


class TestHasParentQuery:
    """HasParentQuery.build 메서드 테스트."""

    def test_basic(self):
        """필수 파라미터만으로 has_parent 쿼리를 생성한다."""
        result = HasParentQuery.build(
            parent_type="parent_doc",
            query={"match": {"title": "test"}},
        )
        assert result == {
            "has_parent": {
                "parent_type": "parent_doc",
                "query": {"match": {"title": "test"}},
            }
        }

    def test_score(self):
        """score 옵션을 포함한 has_parent 쿼리를 생성한다."""
        result = HasParentQuery.build(
            parent_type="parent_doc",
            query={"match_all": {}},
            score=True,
        )
        assert result["has_parent"]["score"] is True

    def test_ignore_unmapped(self):
        """ignore_unmapped 옵션을 포함한 has_parent 쿼리를 생성한다."""
        result = HasParentQuery.build(
            parent_type="parent_doc",
            query={"match_all": {}},
            ignore_unmapped=True,
        )
        assert result["has_parent"]["ignore_unmapped"] is True

    def test_all_options(self):
        """모든 옵션을 포함한 has_parent 쿼리를 생성한다."""
        result = HasParentQuery.build(
            parent_type="question",
            query={"term": {"status": "published"}},
            score=False,
            ignore_unmapped=True,
        )
        assert result == {
            "has_parent": {
                "parent_type": "question",
                "query": {"term": {"status": "published"}},
                "score": False,
                "ignore_unmapped": True,
            }
        }

    def test_no_optional_keys(self):
        """선택 파라미터를 생략하면 해당 키가 결과에 포함되지 않는다."""
        result = HasParentQuery.build(
            parent_type="question",
            query={"match": {"body": "elasticsearch"}},
        )
        body = result["has_parent"]
        assert "score" not in body
        assert "ignore_unmapped" not in body
