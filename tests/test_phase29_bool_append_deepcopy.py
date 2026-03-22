"""Phase 29 테스트 — BoolQueryBuilder 조건 append deepcopy 검증.

각 절(must/should/must_not/filter)에 추가한 condition dict를
외부에서 수정해도 빌더 내부 상태가 오염되지 않음을 확인합니다.
"""

import pytest
from elastic_query_builder.query.compound.bool_query import BoolQueryBuilder


class TestAddMustDeepCopy:
    """add_must: 외부 condition 수정 시 빌더 내부 불변 검증."""

    def test_modify_original_does_not_affect_builder(self):
        condition = {"term": {"status": {"value": "active"}}}
        builder = BoolQueryBuilder().add_must(condition)

        condition["term"]["status"]["value"] = "inactive"

        result = builder.build()
        assert result["bool"]["must"][0]["term"]["status"]["value"] == "active"

    def test_nested_modification_isolation(self):
        inner = {"value": "original"}
        condition = {"term": {"field": inner}}
        builder = BoolQueryBuilder().add_must(condition)

        inner["value"] = "modified"

        result = builder.build()
        assert result["bool"]["must"][0]["term"]["field"]["value"] == "original"


class TestAddShouldDeepCopy:
    """add_should: 외부 condition 수정 시 빌더 내부 불변 검증."""

    def test_modify_original_does_not_affect_builder(self):
        condition = {"match": {"title": {"query": "hello"}}}
        builder = BoolQueryBuilder().add_should(condition)

        condition["match"]["title"]["query"] = "changed"

        result = builder.build()
        assert result["bool"]["should"][0]["match"]["title"]["query"] == "hello"


class TestAddMustNotDeepCopy:
    """add_must_not: 외부 condition 수정 시 빌더 내부 불변 검증."""

    def test_modify_original_does_not_affect_builder(self):
        condition = {"term": {"status": {"value": "deleted"}}}
        builder = BoolQueryBuilder().add_must_not(condition)

        condition["term"]["status"]["value"] = "active"

        result = builder.build()
        assert result["bool"]["must_not"][0]["term"]["status"]["value"] == "deleted"


class TestAddFilterDeepCopy:
    """add_filter: 외부 condition 수정 시 빌더 내부 불변 검증."""

    def test_modify_original_does_not_affect_builder(self):
        condition = {"range": {"age": {"gte": 18}}}
        builder = BoolQueryBuilder().add_filter(condition)

        condition["range"]["age"]["gte"] = 99

        result = builder.build()
        assert result["bool"]["filter"][0]["range"]["age"]["gte"] == 18
