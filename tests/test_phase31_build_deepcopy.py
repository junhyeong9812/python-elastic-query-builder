"""Phase 31 테스트 — build() 반환값 deepcopy 검증.

build() 결과를 외부에서 수정해도 빌더 내부 상태가 오염되지 않고,
연속 build() 호출 시 동일 결과가 반환됨을 확인합니다.
"""

import pytest
from elastic_query_builder import QueryBuilder
from elastic_query_builder.query.compound.bool_query import BoolQueryBuilder
from elastic_query_builder.aggregation.aggregation_builder import AggregationBuilder


class TestQueryBuilderBuildDeepCopy:
    """QueryBuilder.build() 결과 수정이 빌더에 영향 없음 검증."""

    def test_modify_highlight_in_result_does_not_affect_builder(self):
        builder = QueryBuilder().set_highlight({"fields": {"title": {}}})
        result1 = builder.build()
        result1["highlight"]["fields"]["title"]["fragment_size"] = 100
        result1["highlight"]["fields"]["injected"] = {}

        result2 = builder.build()
        assert "fragment_size" not in result2["highlight"]["fields"]["title"]
        assert "injected" not in result2["highlight"]["fields"]

    def test_modify_query_in_result_does_not_affect_builder(self):
        builder = QueryBuilder().set_query({"match": {"title": "test"}})
        result1 = builder.build()
        result1["query"]["match"]["title"] = "modified"

        result2 = builder.build()
        assert result2["query"]["match"]["title"] == "test"

    def test_modify_knn_in_result_does_not_affect_builder(self):
        builder = QueryBuilder().set_knn(
            field="embedding", query_vector=[1.0, 2.0], k=10, num_candidates=100
        )
        result1 = builder.build()
        result1["knn"]["k"] = 999

        result2 = builder.build()
        assert result2["knn"]["k"] == 10

    def test_modify_suggest_in_result_does_not_affect_builder(self):
        builder = QueryBuilder().add_suggest("my-suggest", {
            "text": "hello", "term": {"field": "title"}
        })
        result1 = builder.build()
        result1["suggest"]["my-suggest"]["text"] = "changed"

        result2 = builder.build()
        assert result2["suggest"]["my-suggest"]["text"] == "hello"

    def test_modify_post_filter_in_result_does_not_affect_builder(self):
        builder = QueryBuilder().set_post_filter({"term": {"status": "active"}})
        result1 = builder.build()
        result1["post_filter"]["term"]["status"] = "changed"

        result2 = builder.build()
        assert result2["post_filter"]["term"]["status"] == "active"

    def test_modify_collapse_in_result_does_not_affect_builder(self):
        builder = QueryBuilder().set_collapse(field="user", inner_hits={"name": "latest", "size": 3})
        result1 = builder.build()
        result1["collapse"]["inner_hits"]["size"] = 999

        result2 = builder.build()
        assert result2["collapse"]["inner_hits"]["size"] == 3

    def test_modify_rescore_in_result_does_not_affect_builder(self):
        builder = QueryBuilder().add_rescore({"window_size": 50})
        result1 = builder.build()
        result1["rescore"][0]["window_size"] = 999

        result2 = builder.build()
        assert result2["rescore"][0]["window_size"] == 50

    def test_modify_script_fields_in_result_does_not_affect_builder(self):
        builder = QueryBuilder().set_script_fields({
            "my_field": {"script": {"source": "doc['price'].value"}}
        })
        result1 = builder.build()
        result1["script_fields"]["my_field"]["script"]["source"] = "changed"

        result2 = builder.build()
        assert result2["script_fields"]["my_field"]["script"]["source"] == "doc['price'].value"

    def test_consecutive_builds_return_equal_results(self):
        builder = (
            QueryBuilder()
            .add_must(QueryBuilder.Term.build("status", "active"))
            .set_highlight({"fields": {"title": {}}})
            .set_size(10)
            .add_rescore({"window_size": 50})
        )

        result1 = builder.build()
        result2 = builder.build()
        assert result1 == result2
        assert result1 is not result2


class TestBoolQueryBuilderBuildDeepCopy:
    """BoolQueryBuilder.build() 결과 수정이 빌더에 영향 없음 검증."""

    def test_modify_must_in_result_does_not_affect_builder(self):
        builder = BoolQueryBuilder()
        builder.add_must({"term": {"status": {"value": "active"}}})

        result1 = builder.build()
        result1["bool"]["must"][0]["term"]["status"]["value"] = "modified"

        result2 = builder.build()
        assert result2["bool"]["must"][0]["term"]["status"]["value"] == "active"

    def test_modify_should_in_result_does_not_affect_builder(self):
        builder = BoolQueryBuilder()
        builder.add_should({"match": {"title": {"query": "hello"}}})

        result1 = builder.build()
        result1["bool"]["should"][0]["match"]["title"]["query"] = "modified"

        result2 = builder.build()
        assert result2["bool"]["should"][0]["match"]["title"]["query"] == "hello"

    def test_append_to_result_list_does_not_affect_builder(self):
        builder = BoolQueryBuilder()
        builder.add_must({"term": {"status": {"value": "active"}}})

        result1 = builder.build()
        result1["bool"]["must"].append({"term": {"extra": {"value": "injected"}}})

        result2 = builder.build()
        assert len(result2["bool"]["must"]) == 1


class TestAggregationBuilderBuildDeepCopy:
    """AggregationBuilder.build() 결과 수정이 빌더에 영향 없음 검증."""

    def test_modify_agg_in_result_does_not_affect_builder(self):
        builder = AggregationBuilder()
        builder.add_terms("status_agg", "status", size=10)

        result1 = builder.build()
        result1["status_agg"]["terms"]["size"] = 999

        result2 = builder.build()
        assert result2["status_agg"]["terms"]["size"] == 10
