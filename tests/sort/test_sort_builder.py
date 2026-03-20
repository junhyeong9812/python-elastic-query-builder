"""sort/sort_builder.py에 대한 단위 테스트.

SortBuilder가 다양한 정렬 조건을 올바르게 조합하고,
최종 Elasticsearch sort 배열을 생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.sort.sort_builder import SortBuilder
from elastic_query_builder.core.enums import SortOrder, SortMissing


class TestSortBuilderBasic:
    """SortBuilder 기본 동작 테스트."""

    def test_empty_sort(self):
        """빈 SortBuilder가 빈 배열을 생성하는지 확인합니다."""
        builder = SortBuilder()
        result = builder.build()
        assert result == []

    def test_is_empty_when_new(self):
        """새로 생성된 SortBuilder가 비어 있는지 확인합니다."""
        builder = SortBuilder()
        assert builder.is_empty() is True

    def test_is_empty_after_add(self):
        """정렬 조건을 추가한 후 is_empty가 False를 반환하는지 확인합니다."""
        builder = SortBuilder()
        builder.add("date")
        assert builder.is_empty() is False


class TestSortBuilderAdd:
    """SortBuilder.add 테스트."""

    def test_add_basic(self):
        """필드명만 지정하여 기본 정렬을 추가할 수 있는지 확인합니다."""
        builder = SortBuilder()
        builder.add("date")
        result = builder.build()
        expected = [{"date": {}}]
        assert result == expected

    def test_add_with_order_desc(self):
        """order 옵션을 지정하여 내림차순 정렬을 추가할 수 있는지 확인합니다."""
        builder = SortBuilder()
        builder.add("date", order=SortOrder.DESC)
        result = builder.build()
        expected = [{"date": {"order": "desc"}}]
        assert result == expected

    def test_add_with_order_asc(self):
        """order 옵션을 지정하여 오름차순 정렬을 추가할 수 있는지 확인합니다."""
        builder = SortBuilder()
        builder.add("date", order=SortOrder.ASC)
        result = builder.build()
        expected = [{"date": {"order": "asc"}}]
        assert result == expected

    def test_add_with_missing_last(self):
        """missing 옵션을 _last로 지정할 수 있는지 확인합니다."""
        builder = SortBuilder()
        builder.add("name", missing=SortMissing.LAST)
        result = builder.build()
        expected = [{"name": {"missing": "_last"}}]
        assert result == expected

    def test_add_with_missing_first(self):
        """missing 옵션을 _first로 지정할 수 있는지 확인합니다."""
        builder = SortBuilder()
        builder.add("name", missing=SortMissing.FIRST)
        result = builder.build()
        expected = [{"name": {"missing": "_first"}}]
        assert result == expected

    def test_add_with_mode(self):
        """mode 옵션을 지정할 수 있는지 확인합니다."""
        builder = SortBuilder()
        builder.add("price", mode="avg")
        result = builder.build()
        expected = [{"price": {"mode": "avg"}}]
        assert result == expected

    def test_add_with_mode_min(self):
        """mode 옵션을 min으로 지정할 수 있는지 확인합니다."""
        builder = SortBuilder()
        builder.add("scores", mode="min")
        result = builder.build()
        expected = [{"scores": {"mode": "min"}}]
        assert result == expected

    def test_add_all_options(self):
        """order, missing, mode 옵션을 모두 지정할 수 있는지 확인합니다."""
        builder = SortBuilder()
        builder.add("price", order=SortOrder.DESC, missing=SortMissing.LAST, mode="avg")
        result = builder.build()
        expected = [{"price": {"order": "desc", "missing": "_last", "mode": "avg"}}]
        assert result == expected

    def test_add_without_optional_has_empty_body(self):
        """선택 옵션을 지정하지 않으면 body가 빈 딕셔너리인지 확인합니다."""
        builder = SortBuilder()
        builder.add("date")
        result = builder.build()
        assert result[0]["date"] == {}
        assert "order" not in result[0]["date"]
        assert "missing" not in result[0]["date"]
        assert "mode" not in result[0]["date"]


class TestSortBuilderAddScore:
    """SortBuilder.add_score 테스트."""

    def test_add_score(self):
        """_score 정렬을 추가할 수 있는지 확인합니다."""
        builder = SortBuilder()
        builder.add_score()
        result = builder.build()
        expected = [{"_score": {}}]
        assert result == expected

    def test_add_score_with_order_asc(self):
        """_score 정렬에 order를 지정할 수 있는지 확인합니다."""
        builder = SortBuilder()
        builder.add_score(order=SortOrder.ASC)
        result = builder.build()
        expected = [{"_score": {"order": "asc"}}]
        assert result == expected

    def test_add_score_with_order_desc(self):
        """_score 정렬에 desc order를 지정할 수 있는지 확인합니다."""
        builder = SortBuilder()
        builder.add_score(order=SortOrder.DESC)
        result = builder.build()
        expected = [{"_score": {"order": "desc"}}]
        assert result == expected

    def test_add_score_without_order_has_empty_body(self):
        """order를 지정하지 않은 _score 정렬의 body가 빈 딕셔너리인지 확인합니다."""
        builder = SortBuilder()
        builder.add_score()
        result = builder.build()
        assert result[0]["_score"] == {}


class TestSortBuilderAddScript:
    """SortBuilder.add_script 테스트."""

    def test_add_script(self):
        """스크립트 기반 정렬을 추가할 수 있는지 확인합니다."""
        builder = SortBuilder()
        script = {"source": "doc['price'].value * 2", "lang": "painless"}
        builder.add_script(script, order=SortOrder.DESC)
        result = builder.build()
        expected = [{
            "_script": {
                "type": "number",
                "script": {"source": "doc['price'].value * 2", "lang": "painless"},
                "order": "desc",
            }
        }]
        assert result == expected

    def test_add_script_without_order(self):
        """order 없이 스크립트 정렬을 추가할 수 있는지 확인합니다."""
        builder = SortBuilder()
        script = {"source": "doc['score'].value", "lang": "painless"}
        builder.add_script(script)
        result = builder.build()
        expected = [{
            "_script": {
                "type": "number",
                "script": {"source": "doc['score'].value", "lang": "painless"},
            }
        }]
        assert result == expected

    def test_add_script_custom_type(self):
        """스크립트 정렬의 type을 커스터마이즈할 수 있는지 확인합니다."""
        builder = SortBuilder()
        script = {"source": "doc['name'].value", "lang": "painless"}
        builder.add_script(script, script_type="string")
        result = builder.build()
        assert result[0]["_script"]["type"] == "string"

    def test_add_script_with_lang(self):
        """add_script의 lang 파라미터로 스크립트에 lang을 추가할 수 있는지 확인합니다."""
        builder = SortBuilder()
        script = {"source": "doc['price'].value * params.factor"}
        builder.add_script(script, lang="painless")
        result = builder.build()
        assert result[0]["_script"]["script"]["lang"] == "painless"

    def test_add_script_default_type_is_number(self):
        """스크립트 정렬의 기본 type이 number인지 확인합니다."""
        builder = SortBuilder()
        builder.add_script({"source": "1"})
        result = builder.build()
        assert result[0]["_script"]["type"] == "number"

    def test_add_script_structure(self):
        """스크립트 정렬 결과의 구조가 올바른지 확인합니다."""
        builder = SortBuilder()
        script = {"source": "doc['price'].value", "lang": "painless"}
        builder.add_script(script, order=SortOrder.ASC)
        result = builder.build()
        script_body = result[0]["_script"]
        assert "type" in script_body
        assert "script" in script_body
        assert "order" in script_body


class TestSortBuilderMultiple:
    """SortBuilder 복수 정렬 테스트."""

    def test_multiple_sorts_order_preserved(self):
        """여러 정렬 조건을 추가하면 순서가 유지되는지 확인합니다."""
        builder = SortBuilder()
        builder.add("date", order=SortOrder.DESC)
        builder.add("_score")
        builder.add("title", order=SortOrder.ASC)
        result = builder.build()
        assert len(result) == 3
        assert "date" in result[0]
        assert "_score" in result[1]
        assert "title" in result[2]

    def test_multiple_sorts_with_mixed_types(self):
        """필드 정렬, _score 정렬, 스크립트 정렬을 혼합하여 사용할 수 있는지 확인합니다."""
        builder = SortBuilder()
        builder.add("date", order=SortOrder.DESC)
        builder.add_score()
        builder.add_script({"source": "doc['price'].value"}, order=SortOrder.ASC)
        result = builder.build()
        assert len(result) == 3
        assert "date" in result[0]
        assert "_score" in result[1]
        assert "_script" in result[2]


class TestSortBuilderSetAndMerge:
    """SortBuilder.set / merge 테스트."""

    def test_set(self):
        """set으로 기존 정렬을 완전히 교체할 수 있는지 확인합니다."""
        builder = SortBuilder()
        builder.add("old_field", order=SortOrder.ASC)
        builder.set([{"new_field": {"order": "desc"}}])
        result = builder.build()
        assert len(result) == 1
        assert "new_field" in result[0]

    def test_set_empty(self):
        """set으로 빈 배열을 설정하면 빌더가 비어지는지 확인합니다."""
        builder = SortBuilder()
        builder.add("field")
        builder.set([])
        assert builder.is_empty() is True
        assert builder.build() == []

    def test_set_replaces_all(self):
        """set이 기존의 모든 정렬 조건을 교체하는지 확인합니다."""
        builder = SortBuilder()
        builder.add("field1")
        builder.add("field2")
        builder.add("field3")
        builder.set([{"replacement": {"order": "asc"}}])
        result = builder.build()
        assert len(result) == 1
        assert "replacement" in result[0]

    def test_merge(self):
        """merge로 기존 정렬에 추가 정렬을 병합할 수 있는지 확인합니다."""
        builder = SortBuilder()
        builder.add("date", order=SortOrder.DESC)
        builder.merge([{"title": {"order": "asc"}}])
        result = builder.build()
        assert len(result) == 2
        assert "date" in result[0]
        assert "title" in result[1]

    def test_merge_preserves_existing(self):
        """merge가 기존 정렬 조건을 유지하면서 새 조건을 추가하는지 확인합니다."""
        builder = SortBuilder()
        builder.add("field1", order=SortOrder.ASC)
        builder.merge([{"field2": {"order": "desc"}}, {"field3": {}}])
        result = builder.build()
        assert len(result) == 3
        assert result[0] == {"field1": {"order": "asc"}}
        assert result[1] == {"field2": {"order": "desc"}}
        assert result[2] == {"field3": {}}

    def test_merge_empty_does_nothing(self):
        """빈 배열로 merge해도 기존 정렬이 유지되는지 확인합니다."""
        builder = SortBuilder()
        builder.add("date")
        builder.merge([])
        result = builder.build()
        assert len(result) == 1


class TestSortBuilderChaining:
    """SortBuilder 메서드 체이닝 테스트."""

    def test_add_returns_self(self):
        """add가 self를 반환하여 체이닝이 가능한지 확인합니다."""
        builder = SortBuilder()
        returned = builder.add("field")
        assert returned is builder

    def test_add_score_returns_self(self):
        """add_score가 self를 반환하여 체이닝이 가능한지 확인합니다."""
        builder = SortBuilder()
        returned = builder.add_score()
        assert returned is builder

    def test_add_script_returns_self(self):
        """add_script가 self를 반환하여 체이닝이 가능한지 확인합니다."""
        builder = SortBuilder()
        returned = builder.add_script({"source": "1"})
        assert returned is builder

    def test_set_returns_self(self):
        """set이 self를 반환하여 체이닝이 가능한지 확인합니다."""
        builder = SortBuilder()
        returned = builder.set([])
        assert returned is builder

    def test_merge_returns_self(self):
        """merge가 self를 반환하여 체이닝이 가능한지 확인합니다."""
        builder = SortBuilder()
        returned = builder.merge([])
        assert returned is builder

    def test_full_chaining(self):
        """모든 메서드를 체이닝으로 사용할 수 있는지 확인합니다."""
        result = (
            SortBuilder()
            .add("date", order=SortOrder.DESC)
            .add_score(order=SortOrder.ASC)
            .add("title")
            .build()
        )
        assert len(result) == 3
        assert "date" in result[0]
        assert "_score" in result[1]
        assert "title" in result[2]


class TestSortBuilderBuildImmutability:
    """SortBuilder.build()의 불변성 테스트."""

    def test_build_returns_copy(self):
        """build()가 내부 상태의 복사본을 반환하는지 확인합니다."""
        builder = SortBuilder()
        builder.add("date", order=SortOrder.DESC)
        result1 = builder.build()
        result2 = builder.build()
        assert result1 == result2
        assert result1 is not result2

    def test_modifying_build_result_does_not_affect_builder(self):
        """build() 결과를 수정해도 빌더 내부 상태에 영향이 없는지 확인합니다."""
        builder = SortBuilder()
        builder.add("date")
        result = builder.build()
        result.append({"extra": {}})
        assert len(builder.build()) == 1

    def test_set_creates_independent_copy(self):
        """set이 전달받은 배열의 독립적인 복사본을 사용하는지 확인합니다."""
        original = [{"date": {"order": "desc"}}]
        builder = SortBuilder()
        builder.set(original)
        original.append({"extra": {}})
        assert len(builder.build()) == 1
