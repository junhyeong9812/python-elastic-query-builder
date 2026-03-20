"""query/compound/bool_query.py에 대한 단위 테스트.

BoolQueryBuilder가 올바른 Elasticsearch bool 쿼리 딕셔너리를
생성하는지 검증합니다. 메서드 체이닝, 절 병합, 카운트 기능을 포함합니다.
"""

import pytest
from elastic_query_builder.query.compound.bool_query import BoolQueryBuilder
from elastic_query_builder.core.enums import BoolClause


class TestBoolQueryBuilderBasic:
    """BoolQueryBuilder 기본 동작 테스트."""

    def test_empty_bool(self):
        """빈 BoolQueryBuilder가 빈 bool 쿼리를 생성하는지 확인합니다."""
        result = BoolQueryBuilder().build()
        expected = {"bool": {}}
        assert result == expected

    def test_add_must(self):
        """add_must로 must 절에 조건을 추가할 수 있는지 확인합니다."""
        builder = BoolQueryBuilder()
        builder.add_must({"term": {"status": {"value": "active"}}})
        result = builder.build()
        expected = {
            "bool": {
                "must": [{"term": {"status": {"value": "active"}}}]
            }
        }
        assert result == expected

    def test_add_should(self):
        """add_should로 should 절에 조건을 추가할 수 있는지 확인합니다."""
        builder = BoolQueryBuilder()
        builder.add_should({"match": {"title": {"query": "검색어"}}})
        result = builder.build()
        expected = {
            "bool": {
                "should": [{"match": {"title": {"query": "검색어"}}}]
            }
        }
        assert result == expected

    def test_add_must_not(self):
        """add_must_not으로 must_not 절에 조건을 추가할 수 있는지 확인합니다."""
        builder = BoolQueryBuilder()
        builder.add_must_not({"term": {"status": {"value": "deleted"}}})
        result = builder.build()
        expected = {
            "bool": {
                "must_not": [{"term": {"status": {"value": "deleted"}}}]
            }
        }
        assert result == expected

    def test_add_filter(self):
        """add_filter로 filter 절에 조건을 추가할 수 있는지 확인합니다."""
        builder = BoolQueryBuilder()
        builder.add_filter({"range": {"age": {"gte": 18}}})
        result = builder.build()
        expected = {
            "bool": {
                "filter": [{"range": {"age": {"gte": 18}}}]
            }
        }
        assert result == expected


class TestBoolQueryBuilderMultiple:
    """BoolQueryBuilder 복수 조건 및 체이닝 테스트."""

    def test_multiple_must(self):
        """여러 must 조건을 추가하면 배열에 모두 포함되는지 확인합니다."""
        builder = BoolQueryBuilder()
        builder.add_must({"term": {"status": {"value": "active"}}})
        builder.add_must({"term": {"type": {"value": "post"}}})
        result = builder.build()
        expected = {
            "bool": {
                "must": [
                    {"term": {"status": {"value": "active"}}},
                    {"term": {"type": {"value": "post"}}},
                ]
            }
        }
        assert result == expected

    def test_method_chaining(self):
        """add_must가 self를 반환하여 메서드 체이닝이 가능한지 확인합니다."""
        builder = BoolQueryBuilder()
        returned = builder.add_must({"term": {"status": {"value": "active"}}})
        assert returned is builder

    def test_method_chaining_all_methods(self):
        """모든 add 메서드가 메서드 체이닝을 지원하는지 확인합니다."""
        builder = BoolQueryBuilder()
        result = (
            builder
            .add_must({"term": {"status": {"value": "active"}}})
            .add_should({"match": {"title": {"query": "검색"}}})
            .add_must_not({"term": {"deleted": {"value": True}}})
            .add_filter({"range": {"age": {"gte": 18}}})
        )
        assert result is builder
        built = builder.build()
        assert "must" in built["bool"]
        assert "should" in built["bool"]
        assert "must_not" in built["bool"]
        assert "filter" in built["bool"]


class TestBoolQueryBuilderOptions:
    """BoolQueryBuilder 옵션 테스트."""

    def test_add_minimum_should_match(self):
        """minimum_should_match를 설정할 수 있는지 확인합니다."""
        builder = BoolQueryBuilder()
        builder.add_should({"match": {"title": {"query": "foo"}}})
        builder.add_should({"match": {"body": {"query": "bar"}}})
        builder.add_minimum_should_match(1)
        result = builder.build()
        expected = {
            "bool": {
                "should": [
                    {"match": {"title": {"query": "foo"}}},
                    {"match": {"body": {"query": "bar"}}},
                ],
                "minimum_should_match": 1,
            }
        }
        assert result == expected

    def test_add_minimum_should_match_string(self):
        """minimum_should_match에 문자열 값을 설정할 수 있는지 확인합니다."""
        builder = BoolQueryBuilder()
        builder.add_should({"match": {"title": {"query": "foo"}}})
        builder.add_minimum_should_match("75%")
        result = builder.build()
        assert result["bool"]["minimum_should_match"] == "75%"

    def test_minimum_should_match_not_included_when_none(self):
        """minimum_should_match를 설정하지 않으면 결과에 포함되지 않는지 확인합니다."""
        builder = BoolQueryBuilder()
        builder.add_must({"term": {"status": {"value": "active"}}})
        result = builder.build()
        assert "minimum_should_match" not in result["bool"]

    def test_add_clauses(self):
        """add_clauses로 빈 절을 명시적으로 선언할 수 있는지 확인합니다."""
        builder = BoolQueryBuilder()
        builder.add_clauses(BoolClause.MUST, BoolClause.SHOULD)
        # add_clauses는 빈 배열을 명시적으로 초기화하는 역할
        # 내부적으로 _explicit_clauses 세트에 추가됨
        assert hasattr(builder, '_explicit_clauses')
        assert BoolClause.MUST in builder._explicit_clauses
        assert BoolClause.SHOULD in builder._explicit_clauses

    def test_add_clauses_returns_self(self):
        """add_clauses가 self를 반환하여 메서드 체이닝이 가능한지 확인합니다."""
        builder = BoolQueryBuilder()
        returned = builder.add_clauses(BoolClause.MUST)
        assert returned is builder


class TestBoolQueryBuilderMerge:
    """BoolQueryBuilder 병합 테스트."""

    def test_merge(self):
        """다른 BoolQueryBuilder의 모든 절을 병합할 수 있는지 확인합니다."""
        builder1 = BoolQueryBuilder()
        builder1.add_must({"term": {"status": {"value": "active"}}})
        builder1.add_should({"match": {"title": {"query": "foo"}}})

        builder2 = BoolQueryBuilder()
        builder2.add_must({"term": {"type": {"value": "post"}}})
        builder2.add_filter({"range": {"age": {"gte": 18}}})

        builder1.merge(builder2)
        result = builder1.build()

        assert len(result["bool"]["must"]) == 2
        assert len(result["bool"]["should"]) == 1
        assert len(result["bool"]["filter"]) == 1

    def test_merge_returns_self(self):
        """merge가 self를 반환하여 메서드 체이닝이 가능한지 확인합니다."""
        builder1 = BoolQueryBuilder()
        builder2 = BoolQueryBuilder()
        returned = builder1.merge(builder2)
        assert returned is builder1

    def test_merge_minimum_should_match(self):
        """merge 시 다른 빌더의 minimum_should_match가 전파되는지 확인합니다."""
        builder1 = BoolQueryBuilder()
        builder1.add_should({"match": {"title": {"query": "foo"}}})

        builder2 = BoolQueryBuilder()
        builder2.add_should({"match": {"body": {"query": "bar"}}})
        builder2.add_minimum_should_match(1)

        builder1.merge(builder2)
        result = builder1.build()
        assert result["bool"]["minimum_should_match"] == 1

    def test_merge_must(self):
        """merge_must로 다른 빌더의 must 절만 병합할 수 있는지 확인합니다."""
        builder1 = BoolQueryBuilder()
        builder1.add_must({"term": {"status": {"value": "active"}}})

        builder2 = BoolQueryBuilder()
        builder2.add_must({"term": {"type": {"value": "post"}}})
        builder2.add_should({"match": {"title": {"query": "foo"}}})

        builder1.merge_must(builder2)
        result = builder1.build()

        assert len(result["bool"]["must"]) == 2
        assert "should" not in result["bool"]

    def test_merge_should(self):
        """merge_should로 다른 빌더의 should 절만 병합할 수 있는지 확인합니다."""
        builder1 = BoolQueryBuilder()
        builder1.add_should({"match": {"title": {"query": "foo"}}})

        builder2 = BoolQueryBuilder()
        builder2.add_must({"term": {"status": {"value": "active"}}})
        builder2.add_should({"match": {"body": {"query": "bar"}}})

        builder1.merge_should(builder2)
        result = builder1.build()

        assert len(result["bool"]["should"]) == 2
        assert "must" not in result["bool"]


class TestBoolQueryBuilderCount:
    """BoolQueryBuilder 카운트 및 상태 확인 테스트."""

    def test_count_must(self):
        """count_must가 must 절의 조건 수를 올바르게 반환하는지 확인합니다."""
        builder = BoolQueryBuilder()
        assert builder.count_must() == 0
        builder.add_must({"term": {"status": {"value": "active"}}})
        assert builder.count_must() == 1
        builder.add_must({"term": {"type": {"value": "post"}}})
        assert builder.count_must() == 2

    def test_count_should(self):
        """count_should가 should 절의 조건 수를 올바르게 반환하는지 확인합니다."""
        builder = BoolQueryBuilder()
        assert builder.count_should() == 0
        builder.add_should({"match": {"title": {"query": "검색"}}})
        assert builder.count_should() == 1

    def test_count_must_not(self):
        """count_must_not이 must_not 절의 조건 수를 올바르게 반환하는지 확인합니다."""
        builder = BoolQueryBuilder()
        assert builder.count_must_not() == 0
        builder.add_must_not({"term": {"deleted": {"value": True}}})
        assert builder.count_must_not() == 1

    def test_count_filter(self):
        """count_filter가 filter 절의 조건 수를 올바르게 반환하는지 확인합니다."""
        builder = BoolQueryBuilder()
        assert builder.count_filter() == 0
        builder.add_filter({"range": {"age": {"gte": 18}}})
        assert builder.count_filter() == 1

    def test_is_empty(self):
        """새로 생성한 빌더는 비어 있고, 조건 추가 후에는 비어 있지 않은지 확인합니다."""
        builder = BoolQueryBuilder()
        assert builder.is_empty() is True

        builder.add_must({"term": {"status": {"value": "active"}}})
        assert builder.is_empty() is False

    def test_is_empty_with_should(self):
        """should 절에 조건을 추가하면 is_empty가 False를 반환하는지 확인합니다."""
        builder = BoolQueryBuilder()
        builder.add_should({"match": {"title": {"query": "foo"}}})
        assert builder.is_empty() is False

    def test_is_empty_with_must_not(self):
        """must_not 절에 조건을 추가하면 is_empty가 False를 반환하는지 확인합니다."""
        builder = BoolQueryBuilder()
        builder.add_must_not({"term": {"deleted": {"value": True}}})
        assert builder.is_empty() is False

    def test_is_empty_with_filter(self):
        """filter 절에 조건을 추가하면 is_empty가 False를 반환하는지 확인합니다."""
        builder = BoolQueryBuilder()
        builder.add_filter({"range": {"age": {"gte": 18}}})
        assert builder.is_empty() is False
