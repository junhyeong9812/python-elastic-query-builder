# python-elastic-query-builder 아키텍처 설계 문서

## 1. 프로젝트 개요

Elasticsearch 쿼리를 Python 빌더 패턴으로 생성하는 라이브러리.
dict 기반 ES 쿼리를 타입 안전하고 체이닝 가능한 빌더 API로 구성한다.

### 핵심 가치
- **타입 안전성**: Python 타입 힌트를 통한 IDE 자동완성 및 오류 방지
- **빌더 패턴**: 메서드 체이닝으로 가독성 높은 쿼리 작성
- **도메인 분리**: Search Query / Bool Query / Aggregation / Sort를 독립 도메인으로 관리
- **무의존성**: 외부 라이브러리 의존 없이 순수 Python만으로 동작

## 2. 패키지 구조 (레이어드 아키텍처)

```
python-elastic-query-builder/
├── src/
│   └── elastic_query_builder/
│       ├── __init__.py              # 공개 API (QueryBuilder, 주요 클래스 export)
│       │
│       ├── core/                    # 핵심 도메인 레이어
│       │   ├── __init__.py
│       │   ├── enums.py             # SortOrder, SortMissing, BoolClause,
│       │   │                        # MultiMatchType, FunctionScoreMode, FunctionBoostMode
│       │   └── types.py             # 공통 타입 정의 (TypeAlias 등)
│       │
│       ├── query/                   # Search Query 도메인
│       │   ├── __init__.py          # 쿼리 클래스 export
│       │   ├── leaf/                # 리프 쿼리 (개별 조건)
│       │   │   ├── __init__.py
│       │   │   ├── term.py              # TermQuery, TermsQuery
│       │   │   ├── match.py             # MatchQuery, MatchPhraseQuery
│       │   │   ├── multi_match.py       # MultiMatchQuery
│       │   │   ├── match_phrase_prefix.py # MatchPhrasePrefixQuery
│       │   │   ├── match_bool_prefix.py # MatchBoolPrefixQuery
│       │   │   ├── range.py             # RangeQuery
│       │   │   ├── wildcard.py          # WildcardQuery
│       │   │   ├── exists.py            # ExistsQuery
│       │   │   ├── ids.py               # IdsQuery
│       │   │   ├── fuzzy.py             # FuzzyQuery
│       │   │   ├── prefix.py            # PrefixQuery
│       │   │   ├── regexp.py            # RegexpQuery
│       │   │   ├── terms_set.py         # TermsSetQuery
│       │   │   ├── query_string.py      # QueryStringQuery
│       │   │   ├── simple_query_string.py # SimpleQueryStringQuery
│       │   │   ├── combined_fields.py   # CombinedFieldsQuery
│       │   │   ├── intervals.py         # IntervalsQuery
│       │   │   └── special.py           # MatchAllQuery, MatchNoneQuery
│       │   ├── compound/            # 복합 쿼리
│       │   │   ├── __init__.py
│       │   │   ├── bool_query.py        # BoolQueryBuilder
│       │   │   ├── dis_max.py           # DisMaxQuery
│       │   │   ├── constant_score.py    # ConstantScoreQuery
│       │   │   ├── boosting.py          # BoostingQuery
│       │   │   └── function_score.py    # FunctionScoreQuery
│       │   ├── span/               # Span 쿼리
│       │   │   ├── __init__.py
│       │   │   ├── span_term.py         # SpanTermQuery
│       │   │   └── span_near.py         # SpanNearQuery
│       │   ├── specialized/        # 특수 쿼리
│       │   │   ├── __init__.py
│       │   │   ├── more_like_this.py    # MoreLikeThisQuery
│       │   │   ├── script_score.py      # ScriptScoreQuery
│       │   │   ├── pinned.py            # PinnedQuery
│       │   │   ├── rank_feature.py      # RankFeatureQuery
│       │   │   └── percolate.py         # PercolateQuery
│       │   ├── geo/                # 지리 쿼리
│       │   │   ├── __init__.py
│       │   │   ├── geo_distance.py      # GeoDistanceQuery
│       │   │   └── geo_bounding_box.py  # GeoBoundingBoxQuery
│       │   ├── nested.py           # NestedQuery
│       │   ├── has_child.py        # HasChildQuery
│       │   └── has_parent.py       # HasParentQuery
│       │
│       ├── aggregation/             # Aggregation 도메인
│       │   ├── __init__.py          # Aggregation 클래스 export
│       │   ├── bucket/              # 버킷 Aggregation
│       │   │   ├── __init__.py
│       │   │   ├── terms.py             # TermsAggregation
│       │   │   ├── date_histogram.py    # DateHistogramAggregation
│       │   │   ├── histogram.py         # HistogramAggregation
│       │   │   ├── range.py             # RangeAggregation
│       │   │   ├── filter.py            # FilterAggregation, FiltersAggregation
│       │   │   └── nested.py            # NestedAggregation
│       │   ├── metric/              # 메트릭 Aggregation
│       │   │   ├── __init__.py
│       │   │   ├── stats.py             # StatsAggregation
│       │   │   ├── cardinality.py       # CardinalityAggregation
│       │   │   ├── sum.py               # SumAggregation
│       │   │   ├── avg.py               # AvgAggregation
│       │   │   ├── min.py               # MinAggregation
│       │   │   ├── max.py               # MaxAggregation
│       │   │   └── top_hits.py          # TopHitsAggregation
│       │   └── aggregation_builder.py   # AggregationBuilder (조합기)
│       │
│       ├── sort/                    # Sort 도메인
│       │   ├── __init__.py
│       │   └── sort_builder.py      # SortBuilder (정렬 전담)
│       │
│       └── builder.py               # QueryBuilder (최상위 통합 빌더)
│
├── tests/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── test_enums.py
│   │   └── test_types.py
│   ├── query/
│   │   ├── __init__.py
│   │   ├── leaf/
│   │   │   ├── __init__.py
│   │   │   ├── test_term.py
│   │   │   ├── test_match.py
│   │   │   ├── test_multi_match.py
│   │   │   ├── test_match_phrase_prefix.py
│   │   │   ├── test_match_bool_prefix.py
│   │   │   ├── test_range.py
│   │   │   ├── test_wildcard.py
│   │   │   ├── test_exists.py
│   │   │   ├── test_ids.py
│   │   │   ├── test_fuzzy.py
│   │   │   ├── test_prefix.py
│   │   │   ├── test_regexp.py
│   │   │   ├── test_terms_set.py
│   │   │   ├── test_query_string.py
│   │   │   ├── test_simple_query_string.py
│   │   │   ├── test_combined_fields.py
│   │   │   ├── test_intervals.py
│   │   │   ├── test_special.py
│   │   │   └── test_leaf_init.py
│   │   ├── compound/
│   │   │   ├── __init__.py
│   │   │   ├── test_bool_query.py
│   │   │   ├── test_dis_max.py
│   │   │   ├── test_constant_score.py
│   │   │   ├── test_boosting.py
│   │   │   ├── test_function_score.py
│   │   │   └── test_compound_init.py
│   │   ├── span/
│   │   │   ├── __init__.py
│   │   │   ├── test_span_term.py
│   │   │   ├── test_span_near.py
│   │   │   └── test_span_init.py
│   │   ├── specialized/
│   │   │   ├── __init__.py
│   │   │   ├── test_more_like_this.py
│   │   │   ├── test_script_score.py
│   │   │   ├── test_pinned.py
│   │   │   ├── test_rank_feature.py
│   │   │   └── test_percolate.py
│   │   ├── geo/
│   │   │   ├── __init__.py
│   │   │   ├── test_geo_distance.py
│   │   │   └── test_geo_bounding_box.py
│   │   ├── test_nested.py
│   │   ├── test_has_child.py
│   │   ├── test_has_parent.py
│   │   └── test_query_init.py
│   ├── aggregation/
│   │   ├── __init__.py
│   │   ├── bucket/
│   │   │   ├── __init__.py
│   │   │   ├── test_terms.py
│   │   │   ├── test_date_histogram.py
│   │   │   ├── test_histogram.py
│   │   │   ├── test_range.py
│   │   │   ├── test_filter.py
│   │   │   ├── test_nested.py
│   │   │   └── test_bucket_init.py
│   │   ├── metric/
│   │   │   ├── __init__.py
│   │   │   ├── test_stats.py
│   │   │   ├── test_cardinality.py
│   │   │   ├── test_sum.py
│   │   │   ├── test_avg.py
│   │   │   ├── test_min.py
│   │   │   ├── test_max.py
│   │   │   ├── test_top_hits.py
│   │   │   └── test_metric_init.py
│   │   ├── test_aggregation_builder.py
│   │   └── test_aggregation_init.py
│   ├── sort/
│   │   ├── __init__.py
│   │   ├── test_sort_builder.py
│   │   └── test_sort_init.py
│   ├── integration/
│   │   └── __init__.py
│   ├── test_init.py
│   ├── test_query_builder.py              # QueryBuilder 통합 테스트
│   ├── test_query_builder_features.py     # QueryBuilder 확장 기능 테스트 (highlight, post_filter, suggest 등)
│   ├── test_query_builder_features2.py    # QueryBuilder 확장 기능 테스트 (collapse, search_after, rescore 등)
│   ├── test_query_builder_features3.py    # QueryBuilder 확장 기능 테스트 (script_fields, fields, stored_fields 등)
│   └── test_knn.py                        # KNN 검색 테스트
│
├── docs/
│   ├── 01-architecture.md           # 본 문서
│   ├── 02-class-design.md           # 클래스별 상세 설계
│   ├── 03-api-reference.md          # API 레퍼런스
│   └── 04-proposals.md              # 추가 기능 제안
│
├── pyproject.toml                   # 패키지 설정 (PEP 621)
├── README.md
├── LICENSE
└── .gitignore
```

## 3. 레이어 설계

### Layer 1: Core (핵심)
- `enums.py`: SortOrder, SortMissing, BoolClause, MultiMatchType, FunctionScoreMode, FunctionBoostMode 등 공통 Enum
- `types.py`: ESQuery (= Dict[str, Any]), ESAggregation 등 타입 별칭

### Layer 2: Query Domain (검색 쿼리)
ES의 Query DSL을 1:1로 매핑하는 레이어.
각 쿼리 타입이 독립적인 클래스로 존재하며, `build()` 정적 메서드로 dict를 생성.

**서브 도메인:**
- `leaf/` - 단일 필드에 대한 조건
  - 기본 매칭: term, terms, match, match_phrase, multi_match, match_phrase_prefix, match_bool_prefix
  - 범위/패턴: range, wildcard, fuzzy, prefix, regexp
  - 집합/존재: exists, ids, terms_set
  - 문자열 검색: query_string, simple_query_string, combined_fields, intervals
  - 특수: match_all, match_none
- `compound/` - 여러 쿼리를 조합 (bool, dis_max, constant_score, boosting, function_score)
- `span/` - 근접 검색 (span_near, span_term)
- `specialized/` - 특수 목적 쿼리 (more_like_this, script_score, pinned, rank_feature, percolate)
- `geo/` - 지리 기반 쿼리 (geo_distance, geo_bounding_box)
- 조인 쿼리: nested, has_child, has_parent

### Layer 3: Aggregation Domain (집계)
ES Aggregation을 매핑하는 레이어.

**서브 도메인:**
- `bucket/` - 문서를 그룹화 (terms, date_histogram, histogram, range, filter, filters, nested)
- `metric/` - 수치 계산 (sum, avg, min, max, stats, cardinality, top_hits)
- `AggregationBuilder` - 여러 aggregation을 조합하는 빌더

### Layer 4: Sort Domain (정렬)
Sort 로직을 QueryBuilder에서 분리하여 독립 도메인으로 관리.

### Layer 5: Builder (통합)
`QueryBuilder`가 모든 도메인을 통합하여 최종 ES 쿼리 dict를 생성.

**QueryBuilder 주요 기능:**
- **쿼리 설정**: set_query, set_match_all, set_match_none
- **Bool 쿼리**: create_bool, nested_bool, add_must, add_should, add_must_not, add_filter, add_clauses, add_minimum_should_match, finalize_bool, build_bool_only
- **페이징/크기**: set_size, set_from, set_timeout
- **소스 필터링**: set_source, set_source_includes, set_source_excludes, add_source_includes, add_source_excludes
- **트래킹**: set_track_total_hits, set_track_scores, set_min_score
- **하이라이트**: set_highlight, add_highlight_field
- **포스트 필터**: set_post_filter
- **제안**: set_suggest, add_suggest
- **접기**: set_collapse
- **페이지네이션**: set_search_after
- **리스코어링**: add_rescore, set_rescore
- **인덱스 부스트**: add_indices_boost
- **디버깅**: set_explain
- **스크립트 필드**: set_script_fields, add_script_field
- **필드 선택**: set_fields, set_stored_fields
- **KNN 검색**: set_knn
- **정렬**: add_sort, add_score_sort, add_script_sort, set_sort, merge_sort
- **집계**: create_agg, nested_agg, add_terms_agg, add_date_histogram_agg, add_cardinality_agg, add_stats_agg, add_nested_agg, set_aggs, merge_aggs

## 4. 의존성 방향

```
Builder (QueryBuilder)
  ├── Query Domain (BoolQueryBuilder, Leaf/Compound/Span/Specialized/Geo Queries)
  ├── Aggregation Domain (AggregationBuilder, Aggregations)
  ├── Sort Domain (SortBuilder)
  └── Core (Enums, Types)
```

- 하위 레이어는 상위 레이어를 참조하지 않는다.
- Core는 어떤 레이어도 참조하지 않는다.
- Query, Aggregation, Sort는 서로 참조하지 않고 Core만 참조한다.

## 5. 설계 원칙

1. **각 쿼리 클래스는 자신의 ES 쿼리만 생성한다** (단일 책임)
2. **build() 메서드는 항상 Dict[str, Any]를 반환한다** (일관된 인터페이스)
3. **빌더 메서드는 self를 반환하여 체이닝을 지원한다**
4. **None 값은 쿼리에 포함하지 않는다** (Optional 파라미터 처리)
5. **외부 의존성 없이 순수 Python으로 동작한다**
