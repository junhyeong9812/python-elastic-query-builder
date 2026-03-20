"""QueryBuilder 추가 기능 테스트 (collapse, search_after, rescore)."""
import pytest
from elastic_query_builder.builder import QueryBuilder


class TestQueryBuilderCollapse:
    def test_set_collapse_basic(self):
        result = QueryBuilder().set_collapse("user").build()
        assert result["collapse"] == {"field": "user"}

    def test_set_collapse_with_inner_hits(self):
        result = QueryBuilder().set_collapse("user", inner_hits={"name": "last_tweets", "size": 5}).build()
        assert result["collapse"]["inner_hits"] == {"name": "last_tweets", "size": 5}

    def test_set_collapse_with_max_concurrent(self):
        result = QueryBuilder().set_collapse("user", max_concurrent_group_searches=4).build()
        assert result["collapse"]["max_concurrent_group_searches"] == 4

    def test_no_collapse_when_not_set(self):
        assert "collapse" not in QueryBuilder().build()

    def test_set_collapse_returns_self(self):
        builder = QueryBuilder()
        assert builder.set_collapse("field") is builder


class TestQueryBuilderSearchAfter:
    def test_set_search_after(self):
        result = QueryBuilder().set_search_after([1630000000, "doc_id_123"]).build()
        assert result["search_after"] == [1630000000, "doc_id_123"]

    def test_no_search_after_when_not_set(self):
        assert "search_after" not in QueryBuilder().build()

    def test_set_search_after_returns_self(self):
        builder = QueryBuilder()
        assert builder.set_search_after([]) is builder


class TestQueryBuilderRescore:
    def test_add_rescore(self):
        rescore = {"window_size": 100, "query": {"rescore_query": {"match_phrase": {"title": {"query": "test"}}}}}
        result = QueryBuilder().add_rescore(rescore).build()
        assert result["rescore"] == [rescore]

    def test_add_multiple_rescores(self):
        r1 = {"window_size": 100, "query": {"rescore_query": {"match": {"title": {"query": "a"}}}}}
        r2 = {"window_size": 200, "query": {"rescore_query": {"match": {"content": {"query": "b"}}}}}
        result = QueryBuilder().add_rescore(r1).add_rescore(r2).build()
        assert len(result["rescore"]) == 2

    def test_set_rescore(self):
        rescores = [{"window_size": 50, "query": {"rescore_query": {"match_all": {}}}}]
        result = QueryBuilder().set_rescore(rescores).build()
        assert result["rescore"] == rescores

    def test_no_rescore_when_not_set(self):
        assert "rescore" not in QueryBuilder().build()

    def test_add_rescore_returns_self(self):
        builder = QueryBuilder()
        assert builder.add_rescore({}) is builder
