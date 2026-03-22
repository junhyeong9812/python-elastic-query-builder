"""Phase 30 테스트 — BoolQueryBuilder merge() deepcopy 검증.

merge 후 원본 빌더의 조건을 수정해도
병합 대상 빌더에 영향이 없음을 확인합니다.
"""

import pytest
from elastic_query_builder.query.compound.bool_query import BoolQueryBuilder


class TestMergeDeepCopy:
    """merge(): 원본 수정이 병합 대상에 영향 없음 검증."""

    def test_modify_source_after_merge_does_not_affect_target(self):
        source = BoolQueryBuilder()
        source.add_must({"term": {"status": {"value": "active"}}})
        source.add_should({"match": {"title": {"query": "hello"}}})
        source.add_must_not({"term": {"deleted": {"value": True}}})
        source.add_filter({"range": {"age": {"gte": 18}}})

        target = BoolQueryBuilder()
        target.merge(source)

        # source의 내부 상태에 직접 접근하여 수정
        source._must[0]["term"]["status"]["value"] = "changed"
        source._should[0]["match"]["title"]["query"] = "changed"
        source._must_not[0]["term"]["deleted"]["value"] = False
        source._filter[0]["range"]["age"]["gte"] = 999

        result = target.build()
        assert result["bool"]["must"][0]["term"]["status"]["value"] == "active"
        assert result["bool"]["should"][0]["match"]["title"]["query"] == "hello"
        assert result["bool"]["must_not"][0]["term"]["deleted"]["value"] is True
        assert result["bool"]["filter"][0]["range"]["age"]["gte"] == 18

    def test_modify_target_after_merge_does_not_affect_source(self):
        source = BoolQueryBuilder()
        source.add_must({"term": {"status": {"value": "active"}}})

        target = BoolQueryBuilder()
        target.merge(source)

        # target의 내부 상태 수정
        target._must[0]["term"]["status"]["value"] = "modified"

        source_result = source.build()
        assert source_result["bool"]["must"][0]["term"]["status"]["value"] == "active"


class TestMergeMustDeepCopy:
    """merge_must(): 원본 수정이 병합 대상에 영향 없음 검증."""

    def test_modify_source_after_merge_must_does_not_affect_target(self):
        source = BoolQueryBuilder()
        source.add_must({"term": {"field": {"value": "original"}}})

        target = BoolQueryBuilder()
        target.merge_must(source)

        source._must[0]["term"]["field"]["value"] = "changed"

        result = target.build()
        assert result["bool"]["must"][0]["term"]["field"]["value"] == "original"


class TestMergeShouldDeepCopy:
    """merge_should(): 원본 수정이 병합 대상에 영향 없음 검증."""

    def test_modify_source_after_merge_should_does_not_affect_target(self):
        source = BoolQueryBuilder()
        source.add_should({"match": {"title": {"query": "original"}}})

        target = BoolQueryBuilder()
        target.merge_should(source)

        source._should[0]["match"]["title"]["query"] = "changed"

        result = target.build()
        assert result["bool"]["should"][0]["match"]["title"]["query"] == "original"
