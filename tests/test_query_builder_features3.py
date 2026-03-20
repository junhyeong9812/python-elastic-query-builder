"""QueryBuilder 추가 기능 테스트 (indices_boost, explain, script_fields, fields, stored_fields)."""
import pytest
from elastic_query_builder.builder import QueryBuilder


class TestQueryBuilderIndicesBoost:
    def test_add_indices_boost(self):
        result = QueryBuilder().add_indices_boost("index1", 1.5).add_indices_boost("index2", 0.8).build()
        assert result["indices_boost"] == [{"index1": 1.5}, {"index2": 0.8}]

    def test_no_indices_boost_when_not_set(self):
        assert "indices_boost" not in QueryBuilder().build()

    def test_add_indices_boost_returns_self(self):
        builder = QueryBuilder()
        assert builder.add_indices_boost("idx", 1.0) is builder


class TestQueryBuilderExplain:
    def test_set_explain_true(self):
        result = QueryBuilder().set_explain(True).build()
        assert result["explain"] is True

    def test_set_explain_false(self):
        result = QueryBuilder().set_explain(False).build()
        assert result["explain"] is False

    def test_no_explain_when_not_set(self):
        assert "explain" not in QueryBuilder().build()

    def test_set_explain_returns_self(self):
        builder = QueryBuilder()
        assert builder.set_explain(True) is builder


class TestQueryBuilderScriptFields:
    def test_set_script_fields(self):
        sf = {"test_field": {"script": {"source": "doc['price'].value * 2"}}}
        result = QueryBuilder().set_script_fields(sf).build()
        assert result["script_fields"] == sf

    def test_add_script_field(self):
        result = (
            QueryBuilder()
            .add_script_field("doubled_price", {"source": "doc['price'].value * 2"})
            .add_script_field("tax", {"source": "doc['price'].value * 0.1"})
            .build()
        )
        assert "doubled_price" in result["script_fields"]
        assert "tax" in result["script_fields"]

    def test_no_script_fields_when_not_set(self):
        assert "script_fields" not in QueryBuilder().build()

    def test_add_script_field_returns_self(self):
        builder = QueryBuilder()
        assert builder.add_script_field("name", {"source": "1"}) is builder


class TestQueryBuilderFields:
    def test_set_fields(self):
        result = QueryBuilder().set_fields(["title", {"field": "date", "format": "epoch_millis"}]).build()
        assert result["fields"] == ["title", {"field": "date", "format": "epoch_millis"}]

    def test_no_fields_when_not_set(self):
        assert "fields" not in QueryBuilder().build()

    def test_set_fields_returns_self(self):
        builder = QueryBuilder()
        assert builder.set_fields([]) is builder


class TestQueryBuilderStoredFields:
    def test_set_stored_fields(self):
        result = QueryBuilder().set_stored_fields(["title", "date"]).build()
        assert result["stored_fields"] == ["title", "date"]

    def test_no_stored_fields_when_not_set(self):
        assert "stored_fields" not in QueryBuilder().build()

    def test_set_stored_fields_returns_self(self):
        builder = QueryBuilder()
        assert builder.set_stored_fields([]) is builder
