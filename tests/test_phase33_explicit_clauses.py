"""Phase 33 테스트 — _explicit_clauses 데드 코드 정리 검증.

__init__에서 _explicit_clauses가 초기화되는지,
add_clauses 후 빈 절이 build 결과에 포함되는지 확인합니다.
"""

import pytest
from elastic_query_builder.query.compound.bool_query import BoolQueryBuilder
from elastic_query_builder.core.enums import BoolClause


class TestExplicitClausesInit:
    """__init__ 시점에 _explicit_clauses 속성 존재 검증."""

    def test_explicit_clauses_exists_after_init(self):
        builder = BoolQueryBuilder()
        assert hasattr(builder, '_explicit_clauses')
        assert isinstance(builder._explicit_clauses, set)
        assert len(builder._explicit_clauses) == 0


class TestExplicitClausesBuild:
    """add_clauses 후 빈 절이 build 결과에 포함되는지 검증."""

    def test_empty_must_included_when_explicit(self):
        builder = BoolQueryBuilder()
        builder.add_clauses(BoolClause.MUST)
        result = builder.build()
        assert "must" in result["bool"]
        assert result["bool"]["must"] == []

    def test_empty_should_included_when_explicit(self):
        builder = BoolQueryBuilder()
        builder.add_clauses(BoolClause.SHOULD)
        result = builder.build()
        assert "should" in result["bool"]
        assert result["bool"]["should"] == []

    def test_empty_must_not_included_when_explicit(self):
        builder = BoolQueryBuilder()
        builder.add_clauses(BoolClause.MUST_NOT)
        result = builder.build()
        assert "must_not" in result["bool"]
        assert result["bool"]["must_not"] == []

    def test_empty_filter_included_when_explicit(self):
        builder = BoolQueryBuilder()
        builder.add_clauses(BoolClause.FILTER)
        result = builder.build()
        assert "filter" in result["bool"]
        assert result["bool"]["filter"] == []

    def test_multiple_explicit_clauses(self):
        builder = BoolQueryBuilder()
        builder.add_clauses(BoolClause.MUST, BoolClause.FILTER)
        result = builder.build()
        assert "must" in result["bool"]
        assert "filter" in result["bool"]
        assert "should" not in result["bool"]

    def test_explicit_with_actual_data(self):
        builder = BoolQueryBuilder()
        builder.add_clauses(BoolClause.MUST, BoolClause.SHOULD)
        builder.add_must({"term": {"status": {"value": "active"}}})
        result = builder.build()
        assert len(result["bool"]["must"]) == 1
        assert result["bool"]["should"] == []

    def test_no_explicit_clauses_empty_build(self):
        """명시적 선언 없이 빈 절은 build 결과에 포함되지 않음."""
        builder = BoolQueryBuilder()
        result = builder.build()
        assert "must" not in result["bool"]
        assert "should" not in result["bool"]
        assert "must_not" not in result["bool"]
        assert "filter" not in result["bool"]
