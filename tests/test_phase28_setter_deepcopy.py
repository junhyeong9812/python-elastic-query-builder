"""Phase 28 테스트 — QueryBuilder setter deepcopy 검증.

각 setter 메서드에 전달한 dict/list를 외부에서 수정해도
빌더 내부 상태가 오염되지 않음을 확인합니다.
"""

import pytest
from elastic_query_builder import QueryBuilder


class TestSetHighlightDeepCopy:
    """set_highlight: 외부 dict 수정 시 빌더 내부 불변 검증."""

    def test_modify_original_does_not_affect_builder(self):
        highlight = {"fields": {"title": {}}}
        builder = QueryBuilder().set_highlight(highlight)

        highlight["fields"]["title"]["fragment_size"] = 100
        highlight["fields"]["body"] = {}

        result = builder.build()
        assert "fragment_size" not in result["highlight"]["fields"]["title"]
        assert "body" not in result["highlight"]["fields"]

    def test_nested_dict_independence(self):
        inner = {"fragment_size": 150}
        highlight = {"fields": {"title": inner}}
        builder = QueryBuilder().set_highlight(highlight)

        inner["fragment_size"] = 999

        result = builder.build()
        assert result["highlight"]["fields"]["title"]["fragment_size"] == 150


class TestSetPostFilterDeepCopy:
    """set_post_filter: 외부 dict 수정 시 빌더 내부 불변 검증."""

    def test_modify_original_does_not_affect_builder(self):
        filter_query = {"term": {"status": {"value": "active"}}}
        builder = QueryBuilder().set_post_filter(filter_query)

        filter_query["term"]["status"]["value"] = "inactive"

        result = builder.build()
        assert result["post_filter"]["term"]["status"]["value"] == "active"


class TestSetSuggestDeepCopy:
    """set_suggest: 외부 dict 수정 시 빌더 내부 불변 검증."""

    def test_modify_original_does_not_affect_builder(self):
        suggest = {"my-suggest": {"text": "hello", "term": {"field": "title"}}}
        builder = QueryBuilder().set_suggest(suggest)

        suggest["my-suggest"]["text"] = "changed"

        result = builder.build()
        assert result["suggest"]["my-suggest"]["text"] == "hello"


class TestAddSuggestDeepCopy:
    """add_suggest: 외부 dict 수정 시 빌더 내부 불변 검증."""

    def test_modify_original_does_not_affect_builder(self):
        suggest_body = {"text": "hello", "term": {"field": "title"}}
        builder = QueryBuilder().add_suggest("my-suggest", suggest_body)

        suggest_body["text"] = "changed"

        result = builder.build()
        assert result["suggest"]["my-suggest"]["text"] == "hello"


class TestSetKnnFilterDeepCopy:
    """set_knn: filter 파라미터의 외부 수정 시 빌더 내부 불변 검증."""

    def test_modify_filter_does_not_affect_builder(self):
        knn_filter = {"term": {"status": "published"}}
        builder = QueryBuilder().set_knn(
            field="embedding", query_vector=[1.0, 2.0], k=10,
            num_candidates=100, filter=knn_filter
        )

        knn_filter["term"]["status"] = "draft"

        result = builder.build()
        assert result["knn"]["filter"]["term"]["status"] == "published"


class TestSetCollapseInnerHitsDeepCopy:
    """set_collapse: inner_hits 파라미터의 외부 수정 시 빌더 내부 불변 검증."""

    def test_modify_inner_hits_does_not_affect_builder(self):
        inner_hits = {"name": "latest", "size": 3}
        builder = QueryBuilder().set_collapse(field="user", inner_hits=inner_hits)

        inner_hits["size"] = 999

        result = builder.build()
        assert result["collapse"]["inner_hits"]["size"] == 3


class TestAddRescoreDeepCopy:
    """add_rescore: 외부 dict 수정 시 빌더 내부 불변 검증."""

    def test_modify_original_does_not_affect_builder(self):
        rescore = {
            "window_size": 50,
            "query": {"rescore_query": {"match_phrase": {"title": "test"}}}
        }
        builder = QueryBuilder().add_rescore(rescore)

        rescore["window_size"] = 999

        result = builder.build()
        assert result["rescore"][0]["window_size"] == 50


class TestSetScriptFieldsDeepCopy:
    """set_script_fields: 외부 dict 수정 시 빌더 내부 불변 검증."""

    def test_modify_original_does_not_affect_builder(self):
        script_fields = {
            "my_field": {"script": {"source": "doc['price'].value * 2"}}
        }
        builder = QueryBuilder().set_script_fields(script_fields)

        script_fields["my_field"]["script"]["source"] = "changed"

        result = builder.build()
        assert result["script_fields"]["my_field"]["script"]["source"] == "doc['price'].value * 2"
