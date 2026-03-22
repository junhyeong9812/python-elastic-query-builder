"""QueryBuilder — 최상위 통합 빌더.

모든 도메인(Query, Aggregation, Sort)을 통합하여 완성된
Elasticsearch 검색 요청 딕셔너리를 생성합니다.
라이브러리의 핵심 진입점입니다.
"""

import copy
from typing import Any, Dict, List, Optional, Union
from elastic_query_builder.core.enums import SortOrder, SortMissing
from elastic_query_builder.query.leaf.term import TermQuery, TermsQuery
from elastic_query_builder.query.leaf.match import MatchQuery, MatchPhraseQuery
from elastic_query_builder.query.leaf.multi_match import MultiMatchQuery
from elastic_query_builder.query.leaf.match_phrase_prefix import MatchPhrasePrefixQuery
from elastic_query_builder.query.leaf.match_bool_prefix import MatchBoolPrefixQuery
from elastic_query_builder.query.leaf.range import RangeQuery
from elastic_query_builder.query.leaf.wildcard import WildcardQuery
from elastic_query_builder.query.leaf.fuzzy import FuzzyQuery
from elastic_query_builder.query.leaf.prefix import PrefixQuery
from elastic_query_builder.query.leaf.regexp import RegexpQuery
from elastic_query_builder.query.leaf.exists import ExistsQuery
from elastic_query_builder.query.leaf.ids import IdsQuery
from elastic_query_builder.query.leaf.special import MatchAllQuery, MatchNoneQuery
from elastic_query_builder.query.leaf.terms_set import TermsSetQuery
from elastic_query_builder.query.leaf.query_string import QueryStringQuery
from elastic_query_builder.query.leaf.simple_query_string import SimpleQueryStringQuery
from elastic_query_builder.query.leaf.combined_fields import CombinedFieldsQuery
from elastic_query_builder.query.leaf.intervals import IntervalsQuery
from elastic_query_builder.query.compound.bool_query import BoolQueryBuilder
from elastic_query_builder.query.compound.dis_max import DisMaxQuery
from elastic_query_builder.query.compound.constant_score import ConstantScoreQuery
from elastic_query_builder.query.compound.boosting import BoostingQuery
from elastic_query_builder.query.compound.function_score import FunctionScoreQuery
from elastic_query_builder.query.span.span_term import SpanTermQuery
from elastic_query_builder.query.span.span_near import SpanNearQuery
from elastic_query_builder.query.nested import NestedQuery
from elastic_query_builder.query.has_child import HasChildQuery
from elastic_query_builder.query.has_parent import HasParentQuery
from elastic_query_builder.query.geo.geo_distance import GeoDistanceQuery
from elastic_query_builder.query.geo.geo_bounding_box import GeoBoundingBoxQuery
from elastic_query_builder.query.specialized.percolate import PercolateQuery
from elastic_query_builder.query.specialized.more_like_this import MoreLikeThisQuery
from elastic_query_builder.query.specialized.script_score import ScriptScoreQuery
from elastic_query_builder.query.specialized.pinned import PinnedQuery
from elastic_query_builder.query.specialized.rank_feature import RankFeatureQuery
from elastic_query_builder.aggregation.aggregation_builder import AggregationBuilder
from elastic_query_builder.sort.sort_builder import SortBuilder


class QueryBuilder:
    """최상위 통합 빌더.

    Elasticsearch 검색 요청에 필요한 모든 구성 요소를
    메서드 체이닝 방식으로 조립합니다.

    사용 예시::

        from elastic_query_builder import QueryBuilder, SortOrder

        result = (
            QueryBuilder()
            .add_must(QueryBuilder.Match.build("title", "검색어"))
            .add_filter(QueryBuilder.Range.build("date", gte="2024-01-01"))
            .set_size(10)
            .add_sort("date", SortOrder.DESC)
            .build()
        )
    """

    # ── 정적 쿼리 클래스 참조 ──
    Term = TermQuery
    Terms = TermsQuery
    Match = MatchQuery
    MatchPhrase = MatchPhraseQuery
    MultiMatch = MultiMatchQuery
    MatchPhrasePrefix = MatchPhrasePrefixQuery
    MatchBoolPrefix = MatchBoolPrefixQuery
    Range = RangeQuery
    Wildcard = WildcardQuery
    Fuzzy = FuzzyQuery
    Prefix = PrefixQuery
    Regexp = RegexpQuery
    Exists = ExistsQuery
    Ids = IdsQuery
    MatchAll = MatchAllQuery
    MatchNone = MatchNoneQuery
    Bool = BoolQueryBuilder
    DisMax = DisMaxQuery
    ConstantScore = ConstantScoreQuery
    Boosting = BoostingQuery
    SpanTerm = SpanTermQuery
    SpanNear = SpanNearQuery
    Nested = NestedQuery
    HasChild = HasChildQuery
    HasParent = HasParentQuery
    TermsSet = TermsSetQuery
    QueryString = QueryStringQuery
    SimpleQueryString = SimpleQueryStringQuery
    CombinedFields = CombinedFieldsQuery
    FunctionScore = FunctionScoreQuery
    Intervals = IntervalsQuery
    GeoDistance = GeoDistanceQuery
    GeoBoundingBox = GeoBoundingBoxQuery
    Percolate = PercolateQuery
    MoreLikeThis = MoreLikeThisQuery
    ScriptScore = ScriptScoreQuery
    Pinned = PinnedQuery
    RankFeature = RankFeatureQuery

    def __init__(self):
        self._query: Optional[Dict[str, Any]] = None
        self._bool_builder: Optional[BoolQueryBuilder] = None
        self._agg_builder: Optional[AggregationBuilder] = None
        self._sort_builder: SortBuilder = SortBuilder()
        self._size: Optional[int] = None
        self._from: Optional[int] = None
        self._timeout: Optional[str] = None
        self._source: Optional[Union[bool, Dict[str, List[str]]]] = None
        self._source_includes: Optional[List[str]] = None
        self._source_excludes: Optional[List[str]] = None
        self._track_total_hits: Optional[Union[bool, int]] = None
        self._track_scores: Optional[bool] = None
        self._min_score: Optional[float] = None
        self._highlight: Optional[Dict[str, Any]] = None
        self._post_filter: Optional[Dict[str, Any]] = None
        self._suggest: Optional[Dict[str, Any]] = None
        self._knn: Optional[Dict[str, Any]] = None
        self._collapse: Optional[Dict[str, Any]] = None
        self._search_after: Optional[List[Any]] = None
        self._rescore: Optional[List[Dict[str, Any]]] = None
        self._indices_boost: Optional[List[Dict[str, float]]] = None
        self._explain: Optional[bool] = None
        self._script_fields: Optional[Dict[str, Any]] = None
        self._fields: Optional[List[Any]] = None
        self._stored_fields: Optional[List[str]] = None

    # ── Bool Query 관리 ──

    def create_bool(self) -> 'QueryBuilder':
        """내부 BoolQueryBuilder를 명시적으로 초기화합니다."""
        self._bool_builder = BoolQueryBuilder()
        return self

    def nested_bool(self) -> BoolQueryBuilder:
        """독립적인 BoolQueryBuilder 인스턴스를 생성하여 반환합니다."""
        return BoolQueryBuilder()

    def _ensure_bool(self) -> None:
        """내부 BoolQueryBuilder가 없으면 자동으로 생성합니다."""
        if self._bool_builder is None:
            self._bool_builder = BoolQueryBuilder()

    def add_must(self, condition: Dict[str, Any]) -> 'QueryBuilder':
        """must 절에 조건을 추가합니다."""
        self._ensure_bool()
        self._bool_builder.add_must(condition)
        return self

    def add_should(self, condition: Dict[str, Any]) -> 'QueryBuilder':
        """should 절에 조건을 추가합니다."""
        self._ensure_bool()
        self._bool_builder.add_should(condition)
        return self

    def add_must_not(self, condition: Dict[str, Any]) -> 'QueryBuilder':
        """must_not 절에 조건을 추가합니다."""
        self._ensure_bool()
        self._bool_builder.add_must_not(condition)
        return self

    def add_filter(self, condition: Dict[str, Any]) -> 'QueryBuilder':
        """filter 절에 조건을 추가합니다."""
        self._ensure_bool()
        self._bool_builder.add_filter(condition)
        return self

    def add_clauses(self, *clauses) -> 'QueryBuilder':
        """빈 절 배열을 명시적으로 선언합니다."""
        self._ensure_bool()
        self._bool_builder.add_clauses(*clauses)
        return self

    def add_minimum_should_match(self, value: Any) -> 'QueryBuilder':
        """minimum_should_match 값을 설정합니다."""
        self._ensure_bool()
        self._bool_builder.add_minimum_should_match(value)
        return self

    def finalize_bool(self) -> 'QueryBuilder':
        """Bool 쿼리를 확정하여 _query에 저장합니다."""
        if self._bool_builder is not None:
            self._query = self._bool_builder.build()
        return self

    def build_bool_only(self) -> Dict[str, Any]:
        """Bool 쿼리 딕셔너리만 반환합니다."""
        if self._bool_builder is not None:
            return self._bool_builder.build()
        return {"bool": {}}

    def has_conditions(self) -> bool:
        """Bool 빌더에 조건이 있는지 확인합니다."""
        return self._bool_builder is not None and not self._bool_builder.is_empty()

    def is_empty(self) -> bool:
        """QueryBuilder에 쿼리가 설정되어 있는지 확인합니다."""
        return self._query is None and (
            self._bool_builder is None or self._bool_builder.is_empty()
        )

    # ── 쿼리 설정 ──

    def set_query(self, query: Dict[str, Any]) -> 'QueryBuilder':
        """커스텀 쿼리를 직접 설정합니다."""
        self._query = query
        return self

    def set_match_all(self, boost: Optional[float] = None) -> 'QueryBuilder':
        """match_all 쿼리를 설정합니다."""
        self._query = MatchAllQuery.build(boost=boost)
        return self

    def set_match_none(self) -> 'QueryBuilder':
        """match_none 쿼리를 설정합니다."""
        self._query = MatchNoneQuery.build()
        return self

    # ── 페이지네이션 & 설정 ──

    def set_size(self, size: int) -> 'QueryBuilder':
        """검색 결과 수를 설정합니다."""
        self._size = size
        return self

    def set_from(self, from_: int) -> 'QueryBuilder':
        """검색 시작 오프셋을 설정합니다."""
        self._from = from_
        return self

    def set_timeout(self, timeout: str) -> 'QueryBuilder':
        """검색 타임아웃을 설정합니다."""
        self._timeout = timeout
        return self

    def set_source(self, value: Union[bool, Dict[str, Any]]) -> 'QueryBuilder':
        """_source 설정을 지정합니다."""
        self._source = value
        self._source_includes = None
        self._source_excludes = None
        return self

    def set_source_includes(self, fields: List[str]) -> 'QueryBuilder':
        """_source에 포함할 필드를 설정합니다 (기존 목록 교체)."""
        self._source_includes = list(fields)
        return self

    def set_source_excludes(self, fields: List[str]) -> 'QueryBuilder':
        """_source에서 제외할 필드를 설정합니다 (기존 목록 교체)."""
        self._source_excludes = list(fields)
        return self

    def add_source_includes(self, *fields: str) -> 'QueryBuilder':
        """_source에 포함할 필드를 누적 추가합니다."""
        if self._source_includes is None:
            self._source_includes = []
        self._source_includes.extend(fields)
        return self

    def add_source_excludes(self, *fields: str) -> 'QueryBuilder':
        """_source에서 제외할 필드를 누적 추가합니다."""
        if self._source_excludes is None:
            self._source_excludes = []
        self._source_excludes.extend(fields)
        return self

    def set_track_total_hits(self, value: Union[bool, int]) -> 'QueryBuilder':
        """track_total_hits를 설정합니다."""
        self._track_total_hits = value
        return self

    def set_track_scores(self, value: bool) -> 'QueryBuilder':
        """track_scores를 설정합니다."""
        self._track_scores = value
        return self

    def set_min_score(self, min_score: float) -> 'QueryBuilder':
        """최소 점수를 설정합니다."""
        self._min_score = min_score
        return self

    # ── Highlight 관리 ──

    def set_highlight(self, highlight: Dict[str, Any]) -> 'QueryBuilder':
        """하이라이트 설정을 지정합니다."""
        self._highlight = copy.deepcopy(highlight)
        return self

    def add_highlight_field(self, field: str, options: Optional[Dict[str, Any]] = None) -> 'QueryBuilder':
        """하이라이트 필드를 추가합니다."""
        if self._highlight is None:
            self._highlight = {"fields": {}}
        if "fields" not in self._highlight:
            self._highlight["fields"] = {}
        self._highlight["fields"][field] = options if options is not None else {}
        return self

    # ── Post Filter ──

    def set_post_filter(self, filter_query: Dict[str, Any]) -> 'QueryBuilder':
        """post_filter를 설정합니다."""
        self._post_filter = copy.deepcopy(filter_query)
        return self

    # ── Suggest ──

    def set_suggest(self, suggest: Dict[str, Any]) -> 'QueryBuilder':
        """suggest 설정을 지정합니다."""
        self._suggest = copy.deepcopy(suggest)
        return self

    def add_suggest(self, name: str, suggest_body: Dict[str, Any]) -> 'QueryBuilder':
        """suggest를 추가합니다."""
        if self._suggest is None:
            self._suggest = {}
        self._suggest[name] = copy.deepcopy(suggest_body)
        return self

    # ── KNN ──

    def set_knn(self, field: str, query_vector: Any, k: int, num_candidates: int,
                filter: Optional[Dict[str, Any]] = None,
                similarity: Optional[float] = None,
                boost: Optional[float] = None) -> 'QueryBuilder':
        """KNN 검색을 설정합니다."""
        self._knn = {"field": field, "query_vector": query_vector, "k": k, "num_candidates": num_candidates}
        if filter is not None:
            self._knn["filter"] = copy.deepcopy(filter)
        if similarity is not None:
            self._knn["similarity"] = similarity
        if boost is not None:
            self._knn["boost"] = boost
        return self

    # ── Collapse ──

    def set_collapse(self, field: str, inner_hits: Optional[Dict[str, Any]] = None,
                     max_concurrent_group_searches: Optional[int] = None) -> 'QueryBuilder':
        """필드 기준 결과 축소(중복 제거)를 설정합니다."""
        self._collapse = {"field": field}
        if inner_hits is not None:
            self._collapse["inner_hits"] = copy.deepcopy(inner_hits)
        if max_concurrent_group_searches is not None:
            self._collapse["max_concurrent_group_searches"] = max_concurrent_group_searches
        return self

    # ── Search After ──

    def set_search_after(self, values: List[Any]) -> 'QueryBuilder':
        """커서 기반 딥 페이지네이션을 위한 search_after를 설정합니다."""
        self._search_after = values
        return self

    # ── Rescore ──

    def add_rescore(self, rescore: Dict[str, Any]) -> 'QueryBuilder':
        """재스코어링 설정을 추가합니다."""
        if self._rescore is None:
            self._rescore = []
        self._rescore.append(copy.deepcopy(rescore))
        return self

    def set_rescore(self, rescore: List[Dict[str, Any]]) -> 'QueryBuilder':
        """재스코어링 설정을 교체합니다."""
        self._rescore = list(rescore)
        return self

    # ── Indices Boost ──

    def add_indices_boost(self, index: str, boost: float) -> 'QueryBuilder':
        """인덱스별 부스트를 추가합니다."""
        if self._indices_boost is None:
            self._indices_boost = []
        self._indices_boost.append({index: boost})
        return self

    # ── Explain ──

    def set_explain(self, explain: bool) -> 'QueryBuilder':
        """스코어링 설명을 활성화/비활성화합니다."""
        self._explain = explain
        return self

    # ── Script Fields ──

    def set_script_fields(self, script_fields: Dict[str, Any]) -> 'QueryBuilder':
        """스크립트 계산 필드를 설정합니다."""
        self._script_fields = copy.deepcopy(script_fields)
        return self

    def add_script_field(self, name: str, script: Dict[str, Any]) -> 'QueryBuilder':
        """스크립트 계산 필드를 추가합니다."""
        if self._script_fields is None:
            self._script_fields = {}
        self._script_fields[name] = {"script": script}
        return self

    # ── Fields ──

    def set_fields(self, fields: List[Any]) -> 'QueryBuilder':
        """반환할 필드 목록을 설정합니다."""
        self._fields = fields
        return self

    # ── Stored Fields ──

    def set_stored_fields(self, fields: List[str]) -> 'QueryBuilder':
        """반환할 stored_fields를 설정합니다."""
        self._stored_fields = fields
        return self

    # ── Sort 관리 ──

    def add_sort(
        self, field: str, order: Optional[SortOrder] = None,
        missing: Optional[SortMissing] = None, mode: Optional[str] = None,
    ) -> 'QueryBuilder':
        """필드 정렬을 추가합니다."""
        self._sort_builder.add(field, order=order, missing=missing, mode=mode)
        return self

    def add_score_sort(self, order: Optional[SortOrder] = None) -> 'QueryBuilder':
        """_score 정렬을 추가합니다."""
        self._sort_builder.add_score(order=order)
        return self

    def add_script_sort(
        self, script: Dict[str, Any], order: Optional[SortOrder] = None,
        script_type: str = "number", lang: Optional[str] = None,
    ) -> 'QueryBuilder':
        """스크립트 기반 정렬을 추가합니다."""
        self._sort_builder.add_script(
            script, order=order, script_type=script_type, lang=lang,
        )
        return self

    def set_sort(self, sort_config: List[Dict[str, Any]]) -> 'QueryBuilder':
        """기존 정렬을 교체합니다."""
        self._sort_builder.set(sort_config)
        return self

    def merge_sort(self, sort_config: List[Dict[str, Any]]) -> 'QueryBuilder':
        """기존 정렬에 추가 정렬을 병합합니다."""
        self._sort_builder.merge(sort_config)
        return self

    # ── Aggregation 관리 ──

    def create_agg(self) -> 'QueryBuilder':
        """내부 AggregationBuilder를 명시적으로 초기화합니다."""
        self._agg_builder = AggregationBuilder()
        return self

    def nested_agg(self) -> AggregationBuilder:
        """독립적인 AggregationBuilder 인스턴스를 생성하여 반환합니다."""
        return AggregationBuilder()

    def _ensure_agg(self) -> None:
        """내부 AggregationBuilder가 없으면 자동으로 생성합니다."""
        if self._agg_builder is None:
            self._agg_builder = AggregationBuilder()

    def add_terms_agg(
        self, name: str, field: str, size: Optional[int] = None, **kwargs,
    ) -> 'QueryBuilder':
        """Terms 집계를 추가합니다."""
        self._ensure_agg()
        self._agg_builder.add_terms(name, field, size=size, **kwargs)
        return self

    def add_date_histogram_agg(
        self, name: str, field: str, **kwargs,
    ) -> 'QueryBuilder':
        """DateHistogram 집계를 추가합니다."""
        self._ensure_agg()
        self._agg_builder.add_date_histogram(name, field, **kwargs)
        return self

    def add_cardinality_agg(
        self, name: str, field: str, precision_threshold: Optional[int] = None,
    ) -> 'QueryBuilder':
        """Cardinality 집계를 추가합니다."""
        self._ensure_agg()
        self._agg_builder.add_cardinality(
            name, field, precision_threshold=precision_threshold,
        )
        return self

    def add_stats_agg(
        self, name: str, field: str, missing: Optional[Any] = None,
    ) -> 'QueryBuilder':
        """Stats 집계를 추가합니다."""
        self._ensure_agg()
        self._agg_builder.add_stats(name, field, missing=missing)
        return self

    def add_nested_agg(
        self, name: str, path: str, sub_aggs: Dict[str, Any],
    ) -> 'QueryBuilder':
        """Nested 집계를 추가합니다."""
        self._ensure_agg()
        self._agg_builder.add_nested_aggregation(name, path, sub_aggs)
        return self

    def set_aggs(self, aggs: Dict[str, Any]) -> 'QueryBuilder':
        """기존 집계를 교체합니다."""
        self._agg_builder = AggregationBuilder()
        for name, agg_body in aggs.items():
            self._agg_builder.add_aggregation(name, agg_body)
        return self

    def merge_aggs(self, aggs: Dict[str, Any]) -> 'QueryBuilder':
        """기존 집계에 새 집계를 병합합니다."""
        self._ensure_agg()
        for name, agg_body in aggs.items():
            self._agg_builder.add_aggregation(name, agg_body)
        return self

    # ── Build ──

    def build(self) -> Dict[str, Any]:
        """최종 Elasticsearch 검색 요청 딕셔너리를 생성합니다."""
        result: Dict[str, Any] = {}

        # Query
        if self._query is not None:
            result["query"] = self._query
        elif self._bool_builder is not None and not self._bool_builder.is_empty():
            result["query"] = self._bool_builder.build()

        # Size / From
        if self._size is not None:
            result["size"] = self._size
        if self._from is not None:
            result["from"] = self._from

        # Timeout
        if self._timeout is not None:
            result["timeout"] = self._timeout

        # Source
        if self._source is not None:
            result["_source"] = self._source
        elif self._source_includes is not None or self._source_excludes is not None:
            source_body: Dict[str, List[str]] = {}
            if self._source_includes is not None:
                source_body["includes"] = self._source_includes
            if self._source_excludes is not None:
                source_body["excludes"] = self._source_excludes
            result["_source"] = source_body

        # Track total hits
        if self._track_total_hits is not None:
            result["track_total_hits"] = self._track_total_hits

        # Track scores
        if self._track_scores is not None:
            result["track_scores"] = self._track_scores

        # Min score
        if self._min_score is not None:
            result["min_score"] = self._min_score

        # Sort
        if not self._sort_builder.is_empty():
            result["sort"] = self._sort_builder.build()

        # Highlight
        if self._highlight is not None:
            result["highlight"] = self._highlight

        # Post filter
        if self._post_filter is not None:
            result["post_filter"] = self._post_filter

        # Suggest
        if self._suggest is not None:
            result["suggest"] = self._suggest

        # KNN
        if self._knn is not None:
            result["knn"] = self._knn

        # Collapse
        if self._collapse is not None:
            result["collapse"] = self._collapse

        # Search after
        if self._search_after is not None:
            result["search_after"] = self._search_after

        # Rescore
        if self._rescore is not None:
            result["rescore"] = self._rescore

        # Indices boost
        if self._indices_boost is not None:
            result["indices_boost"] = self._indices_boost

        # Explain
        if self._explain is not None:
            result["explain"] = self._explain

        # Script fields
        if self._script_fields is not None:
            result["script_fields"] = self._script_fields

        # Fields
        if self._fields is not None:
            result["fields"] = self._fields

        # Stored fields
        if self._stored_fields is not None:
            result["stored_fields"] = self._stored_fields

        # Aggregations
        if self._agg_builder is not None and not self._agg_builder.is_empty():
            result["aggs"] = self._agg_builder.build()

        return copy.deepcopy(result)
