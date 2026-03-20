"""PercolateQuery에 대한 단위 테스트."""

import pytest
from elastic_query_builder.query.specialized.percolate import PercolateQuery


class TestPercolateQuery:
    """PercolateQuery 빌드 테스트."""

    def test_build_with_document(self):
        """document를 지정하여 percolate 쿼리를 생성할 수 있는지 확인합니다."""
        result = PercolateQuery.build(
            "query", document={"message": "A new bonsai tree in the office"}
        )
        assert result == {
            "percolate": {
                "field": "query",
                "document": {"message": "A new bonsai tree in the office"},
            }
        }

    def test_build_with_index_and_id(self):
        """index와 id를 지정하여 percolate 쿼리를 생성할 수 있는지 확인합니다."""
        result = PercolateQuery.build("query", index="my-index", id="1")
        assert result == {
            "percolate": {
                "field": "query",
                "index": "my-index",
                "id": "1",
            }
        }

    def test_build_with_documents(self):
        """documents 목록을 지정하여 percolate 쿼리를 생성할 수 있는지 확인합니다."""
        docs = [{"message": "doc1"}, {"message": "doc2"}]
        result = PercolateQuery.build("query", documents=docs)
        assert result == {
            "percolate": {
                "field": "query",
                "documents": docs,
            }
        }

    def test_build_with_boost(self):
        """boost 옵션을 지정할 수 있는지 확인합니다."""
        result = PercolateQuery.build(
            "query", document={"message": "test"}, boost=1.5
        )
        assert result["percolate"]["boost"] == 1.5

    def test_build_no_optional(self):
        """field만 지정하면 선택 옵션이 없는지 확인합니다."""
        result = PercolateQuery.build("query")
        assert result == {"percolate": {"field": "query"}}
        body = result["percolate"]
        assert "document" not in body
        assert "documents" not in body
        assert "index" not in body
        assert "id" not in body
        assert "boost" not in body
