"""QueryBuilder 추가 기능 테스트 (highlight, post_filter, suggest)."""
import pytest
from elastic_query_builder.builder import QueryBuilder


class TestQueryBuilderHighlight:
    def test_set_highlight(self):
        result = QueryBuilder().set_highlight({"fields": {"title": {}}}).build()
        assert result["highlight"] == {"fields": {"title": {}}}

    def test_add_highlight_field(self):
        result = QueryBuilder().add_highlight_field("title").add_highlight_field("content", {"fragment_size": 150}).build()
        assert result["highlight"]["fields"]["title"] == {}
        assert result["highlight"]["fields"]["content"] == {"fragment_size": 150}

    def test_set_highlight_with_options(self):
        result = QueryBuilder().set_highlight({
            "pre_tags": ["<em>"], "post_tags": ["</em>"],
            "fields": {"title": {"number_of_fragments": 3}}
        }).build()
        assert result["highlight"]["pre_tags"] == ["<em>"]

    def test_no_highlight_when_not_set(self):
        assert "highlight" not in QueryBuilder().build()

    def test_add_highlight_field_returns_self(self):
        builder = QueryBuilder()
        assert builder.add_highlight_field("field") is builder


class TestQueryBuilderPostFilter:
    def test_set_post_filter(self):
        result = QueryBuilder().set_post_filter({"term": {"color": {"value": "red"}}}).build()
        assert result["post_filter"] == {"term": {"color": {"value": "red"}}}

    def test_no_post_filter_when_not_set(self):
        assert "post_filter" not in QueryBuilder().build()

    def test_set_post_filter_returns_self(self):
        builder = QueryBuilder()
        assert builder.set_post_filter({}) is builder


class TestQueryBuilderSuggest:
    def test_set_suggest(self):
        suggest = {"my-suggest": {"text": "test", "term": {"field": "title"}}}
        result = QueryBuilder().set_suggest(suggest).build()
        assert result["suggest"] == suggest

    def test_add_suggest(self):
        result = (
            QueryBuilder()
            .add_suggest("title-suggest", {"text": "test", "term": {"field": "title"}})
            .add_suggest("tag-suggest", {"text": "test", "term": {"field": "tags"}})
            .build()
        )
        assert "title-suggest" in result["suggest"]
        assert "tag-suggest" in result["suggest"]

    def test_no_suggest_when_not_set(self):
        assert "suggest" not in QueryBuilder().build()

    def test_add_suggest_returns_self(self):
        builder = QueryBuilder()
        assert builder.add_suggest("name", {}) is builder
