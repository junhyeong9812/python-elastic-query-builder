"""builder.py에 대한 단위 테스트.

QueryBuilder가 모든 도메인(Query, Sort, Aggregation)을 통합하여
올바른 Elasticsearch 검색 요청 딕셔너리를 생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.builder import QueryBuilder
from elastic_query_builder.core.enums import SortOrder, SortMissing
from elastic_query_builder.query.compound.bool_query import BoolQueryBuilder
from elastic_query_builder.aggregation.aggregation_builder import AggregationBuilder


class TestQueryBuilderEmpty:
    """QueryBuilder 빈 상태 테스트."""

    def test_empty_build(self):
        """빈 QueryBuilder가 빈 딕셔너리를 생성하는지 확인합니다."""
        result = QueryBuilder().build()
        assert result == {}

    def test_is_empty_when_new(self):
        """새로 생성된 QueryBuilder가 비어 있는지 확인합니다."""
        builder = QueryBuilder()
        assert builder.is_empty() is True

    def test_has_conditions_when_new(self):
        """새로 생성된 QueryBuilder에 조건이 없는지 확인합니다."""
        builder = QueryBuilder()
        assert builder.has_conditions() is False


class TestQueryBuilderPagination:
    """QueryBuilder 페이지네이션 & 설정 테스트."""

    def test_set_size(self):
        """set_size로 size를 설정할 수 있는지 확인합니다."""
        result = QueryBuilder().set_size(10).build()
        assert result["size"] == 10

    def test_set_size_zero(self):
        """set_size(0)으로 집계 전용 쿼리를 만들 수 있는지 확인합니다."""
        result = QueryBuilder().set_size(0).build()
        assert result["size"] == 0

    def test_set_from(self):
        """set_from으로 from을 설정할 수 있는지 확인합니다."""
        result = QueryBuilder().set_from(20).build()
        assert result["from"] == 20

    def test_set_from_zero(self):
        """set_from(0)을 설정할 수 있는지 확인합니다."""
        result = QueryBuilder().set_from(0).build()
        assert result["from"] == 0

    def test_set_timeout(self):
        """set_timeout으로 timeout을 설정할 수 있는지 확인합니다."""
        result = QueryBuilder().set_timeout("30s").build()
        assert result["timeout"] == "30s"

    def test_size_and_from_together(self):
        """size와 from을 함께 설정할 수 있는지 확인합니다."""
        result = QueryBuilder().set_size(10).set_from(20).build()
        assert result["size"] == 10
        assert result["from"] == 20


class TestQueryBuilderSource:
    """QueryBuilder _source 설정 테스트."""

    def test_set_source_false(self):
        """set_source(False)로 _source를 비활성화할 수 있는지 확인합니다."""
        result = QueryBuilder().set_source(False).build()
        assert result["_source"] is False

    def test_set_source_true(self):
        """set_source(True)로 _source를 활성화할 수 있는지 확인합니다."""
        result = QueryBuilder().set_source(True).build()
        assert result["_source"] is True

    def test_set_source_includes(self):
        """set_source_includes로 포함할 필드를 지정할 수 있는지 확인합니다."""
        result = QueryBuilder().set_source_includes(["title", "date"]).build()
        assert result["_source"] == {"includes": ["title", "date"]}

    def test_set_source_excludes(self):
        """set_source_excludes로 제외할 필드를 지정할 수 있는지 확인합니다."""
        result = QueryBuilder().set_source_excludes(["content"]).build()
        assert result["_source"] == {"excludes": ["content"]}

    def test_set_source_includes_and_excludes(self):
        """includes와 excludes를 동시에 설정할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .set_source_includes(["title", "date"])
            .set_source_excludes(["content"])
            .build()
        )
        assert result["_source"] == {
            "includes": ["title", "date"],
            "excludes": ["content"],
        }

    def test_add_source_includes(self):
        """add_source_includes로 포함 필드를 누적 추가할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_source_includes("field1", "field2")
            .add_source_includes("field3")
            .build()
        )
        assert result["_source"] == {"includes": ["field1", "field2", "field3"]}

    def test_add_source_excludes(self):
        """add_source_excludes로 제외 필드를 누적 추가할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_source_excludes("field1")
            .add_source_excludes("field2")
            .build()
        )
        assert result["_source"] == {"excludes": ["field1", "field2"]}

    def test_set_source_overrides_includes_excludes(self):
        """set_source가 기존 includes/excludes를 무시하는지 확인합니다."""
        result = (
            QueryBuilder()
            .set_source_includes(["title"])
            .set_source(False)
            .build()
        )
        assert result["_source"] is False

    def test_no_source_in_build_when_not_set(self):
        """_source를 설정하지 않으면 build 결과에 포함되지 않는지 확인합니다."""
        result = QueryBuilder().build()
        assert "_source" not in result


class TestQueryBuilderTrackAndScore:
    """QueryBuilder track_total_hits, track_scores, min_score 테스트."""

    def test_set_track_total_hits_true(self):
        """set_track_total_hits(True)를 설정할 수 있는지 확인합니다."""
        result = QueryBuilder().set_track_total_hits(True).build()
        assert result["track_total_hits"] is True

    def test_set_track_total_hits_int(self):
        """set_track_total_hits에 정수 값을 설정할 수 있는지 확인합니다."""
        result = QueryBuilder().set_track_total_hits(10000).build()
        assert result["track_total_hits"] == 10000

    def test_set_track_scores(self):
        """set_track_scores(True)를 설정할 수 있는지 확인합니다."""
        result = QueryBuilder().set_track_scores(True).build()
        assert result["track_scores"] is True

    def test_set_min_score(self):
        """set_min_score로 최소 점수를 설정할 수 있는지 확인합니다."""
        result = QueryBuilder().set_min_score(0.5).build()
        assert result["min_score"] == 0.5

    def test_no_track_in_build_when_not_set(self):
        """track 설정을 하지 않으면 build 결과에 포함되지 않는지 확인합니다."""
        result = QueryBuilder().build()
        assert "track_total_hits" not in result
        assert "track_scores" not in result
        assert "min_score" not in result


class TestQueryBuilderSetQuery:
    """QueryBuilder 쿼리 설정 테스트."""

    def test_set_match_all(self):
        """set_match_all()로 match_all 쿼리를 설정할 수 있는지 확인합니다."""
        result = QueryBuilder().set_match_all().build()
        assert result["query"] == {"match_all": {}}

    def test_set_match_all_with_boost(self):
        """set_match_all에 boost를 지정할 수 있는지 확인합니다."""
        result = QueryBuilder().set_match_all(boost=1.5).build()
        assert result["query"] == {"match_all": {"boost": 1.5}}

    def test_set_match_none(self):
        """set_match_none()으로 match_none 쿼리를 설정할 수 있는지 확인합니다."""
        result = QueryBuilder().set_match_none().build()
        assert result["query"] == {"match_none": {}}

    def test_set_query(self):
        """set_query로 커스텀 쿼리를 직접 설정할 수 있는지 확인합니다."""
        custom_query = {"custom": {"key": "value"}}
        result = QueryBuilder().set_query(custom_query).build()
        assert result["query"] == custom_query

    def test_set_query_overrides_previous(self):
        """set_query가 이전에 설정된 쿼리를 덮어쓰는지 확인합니다."""
        result = (
            QueryBuilder()
            .set_match_all()
            .set_query({"term": {"status": {"value": "active"}}})
            .build()
        )
        assert result["query"] == {"term": {"status": {"value": "active"}}}


class TestQueryBuilderBoolQuery:
    """QueryBuilder Bool 쿼리 관리 테스트."""

    def test_create_bool_and_add_must(self):
        """create_bool 후 add_must로 must 절을 추가할 수 있는지 확인합니다."""
        term = {"term": {"status": {"value": "active"}}}
        result = QueryBuilder().create_bool().add_must(term).build()
        assert result["query"] == {
            "bool": {
                "must": [term]
            }
        }

    def test_add_must_directly(self):
        """create_bool 없이 add_must를 호출하면 자동으로 bool이 생성되는지 확인합니다."""
        term = {"term": {"status": {"value": "active"}}}
        result = QueryBuilder().add_must(term).build()
        assert result["query"] == {
            "bool": {
                "must": [term]
            }
        }

    def test_add_should(self):
        """add_should로 should 절을 추가할 수 있는지 확인합니다."""
        match = {"match": {"title": {"query": "검색어"}}}
        result = QueryBuilder().add_should(match).build()
        assert result["query"] == {
            "bool": {
                "should": [match]
            }
        }

    def test_add_must_not(self):
        """add_must_not으로 must_not 절을 추가할 수 있는지 확인합니다."""
        term = {"term": {"status": {"value": "deleted"}}}
        result = QueryBuilder().add_must_not(term).build()
        assert result["query"] == {
            "bool": {
                "must_not": [term]
            }
        }

    def test_add_filter(self):
        """add_filter로 filter 절을 추가할 수 있는지 확인합니다."""
        range_q = {"range": {"date": {"gte": "2024-01-01"}}}
        result = QueryBuilder().add_filter(range_q).build()
        assert result["query"] == {
            "bool": {
                "filter": [range_q]
            }
        }

    def test_add_minimum_should_match(self):
        """add_minimum_should_match로 minimum_should_match를 설정할 수 있는지 확인합니다."""
        match1 = {"match": {"title": {"query": "A"}}}
        match2 = {"match": {"content": {"query": "B"}}}
        result = (
            QueryBuilder()
            .add_should(match1)
            .add_should(match2)
            .add_minimum_should_match(1)
            .build()
        )
        assert result["query"]["bool"]["minimum_should_match"] == 1

    def test_multiple_bool_clauses(self):
        """여러 종류의 bool 절을 조합할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_must({"match": {"title": {"query": "검색어"}}})
            .add_filter({"range": {"date": {"gte": "2024-01-01"}}})
            .add_must_not({"term": {"status": {"value": "deleted"}}})
            .build()
        )
        bool_query = result["query"]["bool"]
        assert "must" in bool_query
        assert "filter" in bool_query
        assert "must_not" in bool_query

    def test_nested_bool(self):
        """nested_bool()이 새 BoolQueryBuilder를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        nested = builder.nested_bool()
        assert isinstance(nested, BoolQueryBuilder)

    def test_nested_bool_independent(self):
        """nested_bool()이 독립적인 BoolQueryBuilder를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        nested1 = builder.nested_bool()
        nested2 = builder.nested_bool()
        nested1.add_must({"term": {"a": {"value": "1"}}})
        assert nested2.is_empty() is True

    def test_nested_bool_usage(self):
        """nested_bool()로 생성한 중첩 bool 쿼리를 사용할 수 있는지 확인합니다."""
        builder = QueryBuilder()
        inner = builder.nested_bool()
        inner.add_should({"match": {"title": {"query": "A"}}})
        inner.add_should({"match": {"content": {"query": "A"}}})
        inner.add_minimum_should_match(1)

        result = builder.add_must(inner.build()).build()
        bool_query = result["query"]["bool"]
        assert "must" in bool_query
        assert len(bool_query["must"]) == 1
        inner_bool = bool_query["must"][0]["bool"]
        assert "should" in inner_bool
        assert len(inner_bool["should"]) == 2

    def test_finalize_bool(self):
        """finalize_bool로 bool 쿼리를 확정할 수 있는지 확인합니다."""
        builder = QueryBuilder()
        builder.create_bool()
        builder.add_must({"term": {"status": {"value": "active"}}})
        builder.finalize_bool()
        result = builder.build()
        assert "query" in result
        assert "bool" in result["query"]

    def test_build_bool_only(self):
        """build_bool_only로 bool 쿼리만 추출할 수 있는지 확인합니다."""
        builder = QueryBuilder()
        builder.add_must({"term": {"status": {"value": "active"}}})
        result = builder.build_bool_only()
        assert "bool" in result
        assert "must" in result["bool"]

    def test_build_bool_only_when_empty(self):
        """bool 빌더가 없을 때 build_bool_only가 빈 bool을 반환하는지 확인합니다."""
        builder = QueryBuilder()
        result = builder.build_bool_only()
        assert result == {"bool": {}}

    def test_has_conditions_true(self):
        """bool에 조건을 추가하면 has_conditions가 True를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        builder.add_must({"term": {"status": {"value": "active"}}})
        assert builder.has_conditions() is True

    def test_is_empty_false_with_query(self):
        """쿼리가 설정되면 is_empty가 False를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        builder.set_match_all()
        assert builder.is_empty() is False

    def test_is_empty_false_with_bool(self):
        """bool에 조건이 있으면 is_empty가 False를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        builder.add_must({"term": {"x": {"value": "y"}}})
        assert builder.is_empty() is False

    def test_set_query_takes_priority_over_bool(self):
        """set_query가 bool 빌더보다 우선하는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_must({"term": {"status": {"value": "active"}}})
            .set_query({"match_all": {}})
            .build()
        )
        assert result["query"] == {"match_all": {}}


class TestQueryBuilderStaticReferences:
    """QueryBuilder 정적 쿼리 클래스 참조 테스트."""

    def test_term_reference(self):
        """QueryBuilder.Term이 TermQuery를 참조하는지 확인합니다."""
        from elastic_query_builder.query.leaf.term import TermQuery
        assert QueryBuilder.Term is TermQuery

    def test_terms_reference(self):
        """QueryBuilder.Terms가 TermsQuery를 참조하는지 확인합니다."""
        from elastic_query_builder.query.leaf.term import TermsQuery
        assert QueryBuilder.Terms is TermsQuery

    def test_match_reference(self):
        """QueryBuilder.Match가 MatchQuery를 참조하는지 확인합니다."""
        from elastic_query_builder.query.leaf.match import MatchQuery
        assert QueryBuilder.Match is MatchQuery

    def test_match_phrase_reference(self):
        """QueryBuilder.MatchPhrase가 MatchPhraseQuery를 참조하는지 확인합니다."""
        from elastic_query_builder.query.leaf.match import MatchPhraseQuery
        assert QueryBuilder.MatchPhrase is MatchPhraseQuery

    def test_range_reference(self):
        """QueryBuilder.Range가 RangeQuery를 참조하는지 확인합니다."""
        from elastic_query_builder.query.leaf.range import RangeQuery
        assert QueryBuilder.Range is RangeQuery

    def test_wildcard_reference(self):
        """QueryBuilder.Wildcard가 WildcardQuery를 참조하는지 확인합니다."""
        from elastic_query_builder.query.leaf.wildcard import WildcardQuery
        assert QueryBuilder.Wildcard is WildcardQuery

    def test_exists_reference(self):
        """QueryBuilder.Exists가 ExistsQuery를 참조하는지 확인합니다."""
        from elastic_query_builder.query.leaf.exists import ExistsQuery
        assert QueryBuilder.Exists is ExistsQuery

    def test_ids_reference(self):
        """QueryBuilder.Ids가 IdsQuery를 참조하는지 확인합니다."""
        from elastic_query_builder.query.leaf.ids import IdsQuery
        assert QueryBuilder.Ids is IdsQuery

    def test_match_all_reference(self):
        """QueryBuilder.MatchAll이 MatchAllQuery를 참조하는지 확인합니다."""
        from elastic_query_builder.query.leaf.special import MatchAllQuery
        assert QueryBuilder.MatchAll is MatchAllQuery

    def test_match_none_reference(self):
        """QueryBuilder.MatchNone이 MatchNoneQuery를 참조하는지 확인합니다."""
        from elastic_query_builder.query.leaf.special import MatchNoneQuery
        assert QueryBuilder.MatchNone is MatchNoneQuery

    def test_bool_reference(self):
        """QueryBuilder.Bool이 BoolQueryBuilder를 참조하는지 확인합니다."""
        assert QueryBuilder.Bool is BoolQueryBuilder

    def test_dis_max_reference(self):
        """QueryBuilder.DisMax가 DisMaxQuery를 참조하는지 확인합니다."""
        from elastic_query_builder.query.compound.dis_max import DisMaxQuery
        assert QueryBuilder.DisMax is DisMaxQuery

    def test_span_term_reference(self):
        """QueryBuilder.SpanTerm이 SpanTermQuery를 참조하는지 확인합니다."""
        from elastic_query_builder.query.span.span_term import SpanTermQuery
        assert QueryBuilder.SpanTerm is SpanTermQuery

    def test_span_near_reference(self):
        """QueryBuilder.SpanNear가 SpanNearQuery를 참조하는지 확인합니다."""
        from elastic_query_builder.query.span.span_near import SpanNearQuery
        assert QueryBuilder.SpanNear is SpanNearQuery

    def test_nested_reference(self):
        """QueryBuilder.Nested가 NestedQuery를 참조하는지 확인합니다."""
        from elastic_query_builder.query.nested import NestedQuery
        assert QueryBuilder.Nested is NestedQuery

    def test_static_references_are_usable(self):
        """정적 참조를 통해 실제 쿼리를 생성할 수 있는지 확인합니다."""
        term = QueryBuilder.Term.build("status", "active")
        assert "term" in term
        match = QueryBuilder.Match.build("title", "test")
        assert "match" in match
        range_q = QueryBuilder.Range.build("price", gte=100)
        assert "range" in range_q


class TestQueryBuilderSort:
    """QueryBuilder 정렬 관리 테스트."""

    def test_add_sort(self):
        """add_sort로 정렬 조건을 추가할 수 있는지 확인합니다."""
        result = QueryBuilder().add_sort("date", SortOrder.DESC).build()
        assert "sort" in result
        assert result["sort"] == [{"date": {"order": "desc"}}]

    def test_add_sort_basic(self):
        """옵션 없이 add_sort를 호출할 수 있는지 확인합니다."""
        result = QueryBuilder().add_sort("date").build()
        assert result["sort"] == [{"date": {}}]

    def test_add_sort_with_missing(self):
        """add_sort에 missing 옵션을 지정할 수 있는지 확인합니다."""
        result = QueryBuilder().add_sort("name", missing=SortMissing.LAST).build()
        assert result["sort"] == [{"name": {"missing": "_last"}}]

    def test_add_sort_with_mode(self):
        """add_sort에 mode 옵션을 지정할 수 있는지 확인합니다."""
        result = QueryBuilder().add_sort("price", mode="avg").build()
        assert result["sort"] == [{"price": {"mode": "avg"}}]

    def test_add_score_sort(self):
        """add_score_sort로 _score 정렬을 추가할 수 있는지 확인합니다."""
        result = QueryBuilder().add_score_sort().build()
        assert "sort" in result
        assert result["sort"] == [{"_score": {}}]

    def test_add_score_sort_with_order(self):
        """add_score_sort에 order를 지정할 수 있는지 확인합니다."""
        result = QueryBuilder().add_score_sort(order=SortOrder.ASC).build()
        assert result["sort"] == [{"_score": {"order": "asc"}}]

    def test_add_script_sort(self):
        """add_script_sort로 스크립트 정렬을 추가할 수 있는지 확인합니다."""
        script = {"source": "doc['price'].value * 2", "lang": "painless"}
        result = QueryBuilder().add_script_sort(script, order=SortOrder.DESC).build()
        assert "sort" in result
        assert result["sort"] == [{
            "_script": {
                "type": "number",
                "script": {"source": "doc['price'].value * 2", "lang": "painless"},
                "order": "desc",
            }
        }]

    def test_multiple_sorts(self):
        """여러 정렬 조건을 추가하면 순서가 유지되는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_sort("date", SortOrder.DESC)
            .add_score_sort()
            .add_sort("title", SortOrder.ASC)
            .build()
        )
        assert len(result["sort"]) == 3
        assert "date" in result["sort"][0]
        assert "_score" in result["sort"][1]
        assert "title" in result["sort"][2]

    def test_set_sort(self):
        """set_sort로 기존 정렬을 교체할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_sort("old_field")
            .set_sort([{"new_field": {"order": "desc"}}])
            .build()
        )
        assert len(result["sort"]) == 1
        assert "new_field" in result["sort"][0]

    def test_merge_sort(self):
        """merge_sort로 기존 정렬에 추가 정렬을 병합할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_sort("date", SortOrder.DESC)
            .merge_sort([{"title": {"order": "asc"}}])
            .build()
        )
        assert len(result["sort"]) == 2
        assert "date" in result["sort"][0]
        assert "title" in result["sort"][1]

    def test_no_sort_in_build_when_empty(self):
        """정렬을 설정하지 않으면 build 결과에 sort가 없는지 확인합니다."""
        result = QueryBuilder().build()
        assert "sort" not in result


class TestQueryBuilderAggregation:
    """QueryBuilder 집계 관리 테스트."""

    def test_add_terms_agg(self):
        """add_terms_agg로 terms 집계를 추가할 수 있는지 확인합니다."""
        result = QueryBuilder().add_terms_agg("by_status", "status", size=10).build()
        assert "aggs" in result
        assert result["aggs"] == {
            "by_status": {"terms": {"field": "status", "size": 10}}
        }

    def test_add_terms_agg_without_size(self):
        """size 없이 add_terms_agg를 호출할 수 있는지 확인합니다."""
        result = QueryBuilder().add_terms_agg("by_status", "status").build()
        assert result["aggs"] == {
            "by_status": {"terms": {"field": "status"}}
        }

    def test_add_date_histogram_agg(self):
        """add_date_histogram_agg로 date_histogram 집계를 추가할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_date_histogram_agg("monthly", "date", calendar_interval="1M")
            .build()
        )
        assert "aggs" in result
        assert result["aggs"] == {
            "monthly": {
                "date_histogram": {
                    "field": "date",
                    "calendar_interval": "1M",
                }
            }
        }

    def test_add_cardinality_agg(self):
        """add_cardinality_agg로 cardinality 집계를 추가할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_cardinality_agg("unique_users", "user_id", precision_threshold=100)
            .build()
        )
        assert "aggs" in result
        assert result["aggs"] == {
            "unique_users": {
                "cardinality": {"field": "user_id", "precision_threshold": 100}
            }
        }

    def test_add_stats_agg(self):
        """add_stats_agg로 stats 집계를 추가할 수 있는지 확인합니다."""
        result = QueryBuilder().add_stats_agg("price_stats", "price").build()
        assert "aggs" in result
        assert result["aggs"] == {
            "price_stats": {"stats": {"field": "price"}}
        }

    def test_add_nested_agg(self):
        """add_nested_agg로 nested 집계를 추가할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_nested_agg(
                "items", "items",
                sub_aggs={"item_names": {"terms": {"field": "items.name"}}},
            )
            .build()
        )
        assert "aggs" in result
        assert result["aggs"] == {
            "items": {
                "nested": {"path": "items"},
                "aggs": {"item_names": {"terms": {"field": "items.name"}}},
            }
        }

    def test_multiple_aggs(self):
        """여러 집계를 추가할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_terms_agg("by_status", "status")
            .add_cardinality_agg("unique_users", "user_id")
            .build()
        )
        assert len(result["aggs"]) == 2
        assert "by_status" in result["aggs"]
        assert "unique_users" in result["aggs"]

    def test_nested_agg(self):
        """nested_agg()가 새 AggregationBuilder를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        agg_builder = builder.nested_agg()
        assert isinstance(agg_builder, AggregationBuilder)

    def test_nested_agg_independent(self):
        """nested_agg()가 독립적인 AggregationBuilder를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        agg1 = builder.nested_agg()
        agg2 = builder.nested_agg()
        agg1.add_terms("test", "field")
        assert agg2.is_empty() is True

    def test_create_agg(self):
        """create_agg()로 내부 AggregationBuilder를 초기화할 수 있는지 확인합니다."""
        builder = QueryBuilder()
        returned = builder.create_agg()
        assert returned is builder

    def test_set_aggs(self):
        """set_aggs로 기존 집계를 교체할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_terms_agg("old_agg", "old_field")
            .set_aggs({"new_agg": {"terms": {"field": "new_field"}}})
            .build()
        )
        assert len(result["aggs"]) == 1
        assert "new_agg" in result["aggs"]
        assert "old_agg" not in result["aggs"]

    def test_merge_aggs(self):
        """merge_aggs로 기존 집계에 새 집계를 병합할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_terms_agg("agg1", "field1")
            .merge_aggs({"agg2": {"stats": {"field": "field2"}}})
            .build()
        )
        assert len(result["aggs"]) == 2
        assert "agg1" in result["aggs"]
        assert "agg2" in result["aggs"]

    def test_no_aggs_in_build_when_empty(self):
        """집계를 설정하지 않으면 build 결과에 aggs가 없는지 확인합니다."""
        result = QueryBuilder().build()
        assert "aggs" not in result


class TestQueryBuilderMethodChaining:
    """QueryBuilder 메서드 체이닝 테스트."""

    def test_set_size_returns_self(self):
        """set_size가 self를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        assert builder.set_size(10) is builder

    def test_set_from_returns_self(self):
        """set_from이 self를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        assert builder.set_from(0) is builder

    def test_set_timeout_returns_self(self):
        """set_timeout이 self를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        assert builder.set_timeout("30s") is builder

    def test_set_source_returns_self(self):
        """set_source가 self를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        assert builder.set_source(False) is builder

    def test_set_query_returns_self(self):
        """set_query가 self를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        assert builder.set_query({}) is builder

    def test_set_match_all_returns_self(self):
        """set_match_all이 self를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        assert builder.set_match_all() is builder

    def test_add_must_returns_self(self):
        """add_must가 self를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        assert builder.add_must({"term": {"x": {"value": "y"}}}) is builder

    def test_add_sort_returns_self(self):
        """add_sort가 self를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        assert builder.add_sort("field") is builder

    def test_add_terms_agg_returns_self(self):
        """add_terms_agg가 self를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        assert builder.add_terms_agg("name", "field") is builder

    def test_finalize_bool_returns_self(self):
        """finalize_bool이 self를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        assert builder.finalize_bool() is builder

    def test_create_bool_returns_self(self):
        """create_bool이 self를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        assert builder.create_bool() is builder


class TestQueryBuilderFullIntegration:
    """QueryBuilder 전체 통합 테스트."""

    def test_patent_search_query(self):
        """특허 검색 쿼리를 완전하게 구성할 수 있는지 확인합니다."""
        qb = QueryBuilder()

        keyword_bool = qb.nested_bool()
        keyword_bool.add_should(
            QueryBuilder.Match.build("title", "인공지능", operator="and")
        )
        keyword_bool.add_should(
            QueryBuilder.Match.build("abstract", "인공지능")
        )
        keyword_bool.add_minimum_should_match(1)

        result = (
            qb
            .add_must(keyword_bool.build())
            .add_filter(QueryBuilder.Term.build("status", "granted"))
            .add_filter(QueryBuilder.Range.build("filing_date", gte="2020-01-01"))
            .add_must_not(QueryBuilder.Exists.build("deleted_at"))
            .set_size(20)
            .set_from(0)
            .set_timeout("30s")
            .set_source_includes(["title", "abstract", "filing_date", "applicant", "ipc_code"])
            .set_source_excludes(["full_text"])
            .set_track_total_hits(True)
            .set_min_score(0.5)
            .add_sort("filing_date", SortOrder.DESC)
            .add_score_sort()
            .add_date_histogram_agg(
                "yearly_filings", "filing_date",
                calendar_interval="1y", format="yyyy"
            )
            .add_terms_agg("top_ipc", "ipc_code", size=10)
            .add_cardinality_agg("unique_applicants", "applicant.keyword")
            .build()
        )

        assert "query" in result
        bool_query = result["query"]["bool"]
        assert "must" in bool_query
        assert "filter" in bool_query
        assert "must_not" in bool_query

        inner_bool = bool_query["must"][0]["bool"]
        assert len(inner_bool["should"]) == 2
        assert inner_bool["minimum_should_match"] == 1

        assert len(bool_query["filter"]) == 2
        assert len(bool_query["must_not"]) == 1
        assert "exists" in bool_query["must_not"][0]

        assert result["size"] == 20
        assert result["from"] == 0
        assert result["timeout"] == "30s"

        assert "includes" in result["_source"]
        assert "excludes" in result["_source"]
        assert "title" in result["_source"]["includes"]
        assert "full_text" in result["_source"]["excludes"]

        assert result["track_total_hits"] is True
        assert result["min_score"] == 0.5

        assert len(result["sort"]) == 2
        assert "filing_date" in result["sort"][0]
        assert result["sort"][0]["filing_date"]["order"] == "desc"
        assert "_score" in result["sort"][1]

        assert len(result["aggs"]) == 3
        assert "yearly_filings" in result["aggs"]
        assert "top_ipc" in result["aggs"]
        assert "unique_applicants" in result["aggs"]

        yearly = result["aggs"]["yearly_filings"]
        assert yearly["date_histogram"]["calendar_interval"] == "1y"
        assert yearly["date_histogram"]["format"] == "yyyy"

        top_ipc = result["aggs"]["top_ipc"]
        assert top_ipc["terms"]["field"] == "ipc_code"
        assert top_ipc["terms"]["size"] == 10

        unique = result["aggs"]["unique_applicants"]
        assert unique["cardinality"]["field"] == "applicant.keyword"

    def test_aggregation_only_query(self):
        """집계 전용 쿼리(size=0)를 구성할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .set_match_all()
            .set_size(0)
            .add_terms_agg("status_distribution", "status", size=5)
            .add_stats_agg("price_statistics", "price")
            .add_date_histogram_agg(
                "monthly_trend", "created_at", calendar_interval="1M"
            )
            .build()
        )

        assert result["query"] == {"match_all": {}}
        assert result["size"] == 0
        assert len(result["aggs"]) == 3
        assert "status_distribution" in result["aggs"]
        assert "price_statistics" in result["aggs"]
        assert "monthly_trend" in result["aggs"]

    def test_simple_search_query(self):
        """간단한 키워드 검색 쿼리를 구성할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_must(QueryBuilder.Match.build("title", "검색어", operator="and"))
            .add_filter(QueryBuilder.Range.build("date", gte="2024-01-01"))
            .set_size(10)
            .set_from(0)
            .build()
        )

        assert result["size"] == 10
        assert result["from"] == 0
        assert "query" in result
        bool_q = result["query"]["bool"]
        assert len(bool_q["must"]) == 1
        assert len(bool_q["filter"]) == 1

    def test_script_sort_with_nested_agg_query(self):
        """스크립트 정렬과 nested 집계를 포함한 쿼리를 구성할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .add_filter(QueryBuilder.Term.build("category", "electronics"))
            .set_size(50)
            .add_script_sort(
                {"source": "doc['price'].value * doc['discount'].value", "lang": "painless"},
                order=SortOrder.ASC,
            )
            .add_nested_agg(
                "product_reviews", "reviews",
                sub_aggs={
                    "avg_rating": {"avg": {"field": "reviews.rating"}},
                    "top_reviewers": {"terms": {"field": "reviews.author", "size": 5}},
                },
            )
            .build()
        )

        assert result["size"] == 50
        assert "sort" in result
        assert "_script" in result["sort"][0]
        assert "aggs" in result
        assert "product_reviews" in result["aggs"]
        nested_agg = result["aggs"]["product_reviews"]
        assert nested_agg["nested"]["path"] == "reviews"
        assert "avg_rating" in nested_agg["aggs"]
        assert "top_reviewers" in nested_agg["aggs"]

    def test_build_does_not_include_unset_fields(self):
        """설정하지 않은 필드는 build 결과에 포함되지 않는지 확인합니다."""
        result = QueryBuilder().set_size(10).build()
        assert "size" in result
        assert "query" not in result
        assert "from" not in result
        assert "timeout" not in result
        assert "_source" not in result
        assert "sort" not in result
        assert "aggs" not in result
        assert "track_total_hits" not in result
        assert "track_scores" not in result
        assert "min_score" not in result
