# 클래스별 상세 설계

## 1. Core 도메인

### 1.1 enums.py

```python
class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class SortMissing(str, Enum):
    FIRST = "_first"
    LAST = "_last"

class BoolClause(str, Enum):
    MUST = "must"
    SHOULD = "should"
    MUST_NOT = "must_not"
    FILTER = "filter"

class MultiMatchType(str, Enum):
    BEST_FIELDS = "best_fields"
    MOST_FIELDS = "most_fields"
    CROSS_FIELDS = "cross_fields"
    PHRASE = "phrase"
    PHRASE_PREFIX = "phrase_prefix"
    BOOL_PREFIX = "bool_prefix"

class FunctionScoreMode(str, Enum):
    MULTIPLY = "multiply"
    SUM = "sum"
    AVG = "avg"
    FIRST = "first"
    MAX = "max"
    MIN = "min"

class FunctionBoostMode(str, Enum):
    MULTIPLY = "multiply"
    REPLACE = "replace"
    SUM = "sum"
    AVG = "avg"
    MAX = "max"
    MIN = "min"
```

### 1.2 types.py

```python
from typing import Any, Dict, List, Union

ESQuery = Dict[str, Any]
ESAggregation = Dict[str, Any]
ESSort = Union[Dict[str, Any], List[Dict[str, Any]]]
```

---

## 2. Query 도메인 - Leaf Queries

모든 리프 쿼리는 동일한 패턴을 따른다:
- 클래스 자체가 쿼리 타입을 표현
- `build()` 정적 메서드로 ES 쿼리 dict 생성
- 필수 파라미터 + Optional 파라미터 구조

### 2.1 term.py

| 클래스 | 메서드 | 입력 | 출력 |
|--------|--------|------|------|
| `TermQuery` | `build(field, value, boost?)` | 필드명, 값 | `{"term": {field: {"value": v}}}` |
| `TermsQuery` | `build(field, values, boost?)` | 필드명, 값 리스트 | `{"terms": {field: [...]}}` |

### 2.2 match.py

| 클래스 | 메서드 | 주요 옵션 |
|--------|--------|-----------|
| `MatchQuery` | `build(field, value, ...)` | boost, fuzziness, operator, analyzer, minimum_should_match 등 |
| `MatchPhraseQuery` | `build(field, query, boost?, slop?)` | boost, slop |

### 2.3 multi_match.py

| 클래스 | 메서드 | 주요 옵션 |
|--------|--------|-----------|
| `MultiMatchQuery` | `build(fields, query, type?, tie_breaker?, boost?, fuzziness?, operator?, minimum_should_match?, analyzer?, max_expansions?, prefix_length?, zero_terms_query?)` | 다중 필드 매칭, MultiMatchType 지원 |

### 2.4 match_phrase_prefix.py

| 클래스 | 메서드 | 주요 옵션 |
|--------|--------|-----------|
| `MatchPhrasePrefixQuery` | `build(field, query, max_expansions?, boost?, slop?, analyzer?)` | 구문 접두사 매칭 |

### 2.5 match_bool_prefix.py

| 클래스 | 메서드 | 주요 옵션 |
|--------|--------|-----------|
| `MatchBoolPrefixQuery` | `build(field, query, boost?, fuzziness?, operator?, minimum_should_match?, analyzer?)` | Bool 접두사 매칭 |

### 2.6 range.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `RangeQuery` | `build(field, gte?, lte?, gt?, lt?)` | 범위 조건 |

출력: `{"range": {field: {"gte": ..., "lte": ...}}}`

### 2.7 wildcard.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `WildcardQuery` | `build(field, value, boost?, case_insensitive?)` | 와일드카드 패턴 |

### 2.8 exists.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `ExistsQuery` | `build(field)` | 필드명 |

### 2.9 ids.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `IdsQuery` | `build(values)` | ID 리스트 |

### 2.10 special.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `MatchAllQuery` | `build(boost?)` | - |
| `MatchNoneQuery` | `build()` | - |

### 2.11 fuzzy.py

| 클래스 | 메서드 | 주요 옵션 |
|--------|--------|-----------|
| `FuzzyQuery` | `build(field, value, fuzziness?, prefix_length?, max_expansions?, transpositions?, boost?)` | 유사 검색 |

### 2.12 prefix.py

| 클래스 | 메서드 | 주요 옵션 |
|--------|--------|-----------|
| `PrefixQuery` | `build(field, value, boost?, case_insensitive?)` | 접두사 검색 |

### 2.13 regexp.py

| 클래스 | 메서드 | 주요 옵션 |
|--------|--------|-----------|
| `RegexpQuery` | `build(field, value, flags?, max_determinized_states?, boost?, case_insensitive?)` | 정규식 검색 |

### 2.14 terms_set.py

| 클래스 | 메서드 | 주요 옵션 |
|--------|--------|-----------|
| `TermsSetQuery` | `build(field, terms, minimum_should_match_field?, minimum_should_match_script?, boost?)` | 최소 매칭 조건 기반 terms 검색 |

### 2.15 query_string.py

| 클래스 | 메서드 | 주요 옵션 |
|--------|--------|-----------|
| `QueryStringQuery` | `build(query, fields?, default_field?, default_operator?, analyzer?, allow_leading_wildcard?, fuzziness?, boost?, minimum_should_match?)` | Lucene 쿼리 문법 지원 |

### 2.16 simple_query_string.py

| 클래스 | 메서드 | 주요 옵션 |
|--------|--------|-----------|
| `SimpleQueryStringQuery` | `build(query, fields?, default_operator?, analyzer?, flags?, minimum_should_match?, boost?)` | 간소화된 쿼리 문법 |

### 2.17 combined_fields.py

| 클래스 | 메서드 | 주요 옵션 |
|--------|--------|-----------|
| `CombinedFieldsQuery` | `build(query, fields, operator?, minimum_should_match?, boost?)` | 다중 필드 결합 검색 |

### 2.18 intervals.py

| 클래스 | 메서드 | 주요 옵션 |
|--------|--------|-----------|
| `IntervalsQuery` | `build(field, rule)` | 구간 기반 검색 규칙 |

---

## 3. Query 도메인 - Compound Queries

### 3.1 bool_query.py - BoolQueryBuilder

상태를 가지는 빌더 클래스. 메서드 체이닝을 지원.

```
BoolQueryBuilder
├── add_must(condition) -> self
├── add_should(condition) -> self
├── add_must_not(condition) -> self
├── add_filter(condition) -> self
├── add_clauses(*clauses: BoolClause) -> self     # 빈 절 초기화
├── add_minimum_should_match(value) -> self
├── merge(bool_query) -> self                      # 다른 bool의 모든 절 병합
├── merge_must(bool_query) -> self                 # must 절만 병합
├── merge_should(bool_query) -> self               # should 절만 병합
├── count_must() -> int
├── count_should() -> int
├── count_must_not() -> int
├── count_filter() -> int
├── is_empty() -> bool
└── build() -> Dict
```

출력: `{"bool": {"must": [...], "should": [...], ...}}`

### 3.2 dis_max.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `DisMaxQuery` | `build(queries, tie_breaker?, boost?)` | 쿼리 리스트 |

### 3.3 constant_score.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `ConstantScoreQuery` | `build(filter, boost?)` | 필터 쿼리 |

출력: `{"constant_score": {"filter": ..., "boost": ...}}`

### 3.4 boosting.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `BoostingQuery` | `build(positive, negative, negative_boost)` | positive 쿼리, negative 쿼리, negative_boost 값 |

출력: `{"boosting": {"positive": ..., "negative": ..., "negative_boost": ...}}`

### 3.5 function_score.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `FunctionScoreQuery` | `build(query, functions?, score_mode?, boost_mode?, max_boost?, boost?, min_score?)` | 쿼리, 스코어 함수 리스트 |

출력: `{"function_score": {"query": ..., "functions": [...], "score_mode": ..., "boost_mode": ...}}`

---

## 4. Query 도메인 - Span Queries

### 4.1 span_term.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `SpanTermQuery` | `build(field, value)` | 필드명, 검색어 |

### 4.2 span_near.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `SpanNearQuery` | `build(clauses, slop, in_order?, boost?)` | span 쿼리 리스트 |

---

## 5. Query 도메인 - Nested

### 5.1 nested.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `NestedQuery` | `build(path, query, score_mode?, ignore_unmapped?)` | 경로, 내부 쿼리 |

---

## 6. Query 도메인 - Joining Queries

### 6.1 has_child.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `HasChildQuery` | `build(type, query, score_mode?, min_children?, max_children?, ignore_unmapped?)` | 자식 타입, 쿼리 |

출력: `{"has_child": {"type": ..., "query": ..., "score_mode": ...}}`

### 6.2 has_parent.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `HasParentQuery` | `build(parent_type, query, score?, ignore_unmapped?)` | 부모 타입, 쿼리 |

출력: `{"has_parent": {"parent_type": ..., "query": ..., "score": ...}}`

---

## 7. Query 도메인 - Specialized Queries

### 7.1 more_like_this.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `MoreLikeThisQuery` | `build(fields, like, min_term_freq?, min_doc_freq?, max_query_terms?, minimum_should_match?, boost?)` | 필드 리스트, 유사 문서/텍스트 |

### 7.2 script_score.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `ScriptScoreQuery` | `build(query, script, boost?, min_score?)` | 쿼리, 스크립트 |

### 7.3 pinned.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `PinnedQuery` | `build(ids, organic, boost?)` | 고정 문서 ID 리스트, 유기 쿼리 |

### 7.4 rank_feature.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `RankFeatureQuery` | `build(field, boost?, saturation?, log?, sigmoid?, linear?)` | 필드명, 스코어 함수 옵션 |

### 7.5 percolate.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `PercolateQuery` | `build(field, document?, index?, id?, documents?, boost?)` | 필드명, 퍼콜레이트 대상 문서 |

---

## 8. Query 도메인 - Geo Queries

### 8.1 geo_distance.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `GeoDistanceQuery` | `build(field, point, distance, distance_type?, validation_method?, boost?)` | 필드명, 기준점, 거리 |

출력: `{"geo_distance": {"distance": ..., field: ...}}`

### 8.2 geo_bounding_box.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `GeoBoundingBoxQuery` | `build(field, top_left, bottom_right, validation_method?, boost?)` | 필드명, 좌상단, 우하단 좌표 |

출력: `{"geo_bounding_box": {field: {"top_left": ..., "bottom_right": ...}}}`

---

## 9. Aggregation 도메인 - Bucket

### 9.1 terms.py - TermsAggregation

```python
build(field, size?, order?, min_doc_count?, missing?, include?, exclude?)
```
출력: `{"terms": {"field": ..., "size": ...}}`

### 9.2 date_histogram.py - DateHistogramAggregation

```python
build(field, calendar_interval?, fixed_interval?, format?, time_zone?, min_doc_count?, extended_bounds?)
```

### 9.3 histogram.py - HistogramAggregation

```python
build(field, interval, min_doc_count?, extended_bounds?)
```

### 9.4 range.py - RangeAggregation

```python
build(field, ranges, keyed?)
```

### 9.5 filter.py - FilterAggregation / FiltersAggregation

```python
# FilterAggregation
build(filter_query)

# FiltersAggregation
build(filters, other_bucket?, other_bucket_key?)
```

### 9.6 nested.py - NestedAggregation

```python
build(path, sub_aggs?)
```

---

## 10. Aggregation 도메인 - Metric

모든 메트릭 agg는 동일 패턴: `build(field, missing?)`

| 클래스 | ES 타입 |
|--------|---------|
| `SumAggregation` | sum |
| `AvgAggregation` | avg |
| `MinAggregation` | min |
| `MaxAggregation` | max |
| `StatsAggregation` | stats |
| `CardinalityAggregation` | cardinality (+ precision_threshold) |
| `TopHitsAggregation` | top_hits (size, sort, _source) |

---

## 11. AggregationBuilder

여러 aggregation을 조합하는 빌더.

```
AggregationBuilder
├── add_aggregation(name, agg_type, sub_aggs?) -> self
├── add_terms(name, field, size?, order?, **kwargs) -> self
├── add_date_histogram(name, field, ...) -> self
├── add_cardinality(name, field, precision_threshold?) -> self
├── add_stats(name, field, missing?) -> self
├── add_nested_aggregation(name, path, sub_aggs) -> self
├── is_empty() -> bool
└── build() -> Dict
```

---

## 12. SortBuilder (신규 분리)

기존 QueryBuilder에 포함되어 있던 정렬 로직을 독립 클래스로 분리.

```
SortBuilder
├── add(field, order?, missing?, mode?) -> self
├── add_score(order?) -> self
├── add_script(script, order?, script_type?, lang?) -> self
├── set(sort_config) -> self          # 덮어쓰기
├── merge(sort_config) -> self        # 병합
├── is_empty() -> bool
└── build() -> List[Dict]
```

---

## 13. QueryBuilder (통합 빌더)

최상위 빌더. 모든 도메인을 통합하여 최종 ES 쿼리를 생성.

```
QueryBuilder
├── [Query 생성 - 정적 참조]
│   ├── Term = TermQuery
│   ├── Terms = TermsQuery
│   ├── Match = MatchQuery
│   ├── MatchPhrase = MatchPhraseQuery
│   ├── MultiMatch = MultiMatchQuery
│   ├── MatchPhrasePrefixQuery = MatchPhrasePrefixQuery
│   ├── MatchBoolPrefix = MatchBoolPrefixQuery
│   ├── Range = RangeQuery
│   ├── Wildcard = WildcardQuery
│   ├── Exists = ExistsQuery
│   ├── Ids = IdsQuery
│   ├── MatchAll = MatchAllQuery
│   ├── MatchNone = MatchNoneQuery
│   ├── Fuzzy = FuzzyQuery
│   ├── Prefix = PrefixQuery
│   ├── Regexp = RegexpQuery
│   ├── TermsSet = TermsSetQuery
│   ├── QueryString = QueryStringQuery
│   ├── SimpleQueryString = SimpleQueryStringQuery
│   ├── CombinedFields = CombinedFieldsQuery
│   ├── Intervals = IntervalsQuery
│   ├── DisMax = DisMaxQuery
│   ├── ConstantScore = ConstantScoreQuery
│   ├── Boosting = BoostingQuery
│   ├── FunctionScore = FunctionScoreQuery
│   ├── Nested = NestedQuery
│   ├── HasChild = HasChildQuery
│   ├── HasParent = HasParentQuery
│   ├── SpanTerm = SpanTermQuery
│   ├── SpanNear = SpanNearQuery
│   ├── MoreLikeThis = MoreLikeThisQuery
│   ├── ScriptScore = ScriptScoreQuery
│   ├── Pinned = PinnedQuery
│   ├── RankFeature = RankFeatureQuery
│   ├── Percolate = PercolateQuery
│   ├── GeoDistance = GeoDistanceQuery
│   └── GeoBoundingBox = GeoBoundingBoxQuery
│
├── [Bool 쿼리 관리]
│   ├── create_bool() -> self
│   ├── nested_bool() -> BoolQueryBuilder
│   ├── add_must/should/must_not/filter(condition) -> self
│   ├── add_clauses(*clauses) -> self
│   ├── add_minimum_should_match(value) -> self
│   ├── finalize_bool() -> self
│   ├── build_bool_only() -> Dict
│   ├── has_conditions() -> bool
│   └── is_empty() -> bool
│
├── [Aggregation 관리]
│   ├── create_agg() -> self
│   ├── nested_agg() -> AggregationBuilder
│   ├── add_*_agg(...) -> self (각 agg 타입별 편의 메서드)
│   ├── set_aggs(aggs) -> self
│   └── merge_aggs(aggs) -> self
│
├── [Sort 관리]
│   ├── add_sort(field, order?, missing?, mode?) -> self
│   ├── add_score_sort(order?) -> self
│   ├── add_script_sort(script, ...) -> self
│   ├── set_sort(sort_config) -> self
│   └── merge_sort(sort_config) -> self
│
├── [Highlight 관리]
│   ├── set_highlight(highlight) -> self
│   └── add_highlight_field(field, **options) -> self
│
├── [Post Filter]
│   └── set_post_filter(query) -> self
│
├── [Suggest]
│   ├── set_suggest(suggest) -> self
│   └── add_suggest(name, suggest) -> self
│
├── [Collapse]
│   └── set_collapse(collapse) -> self
│
├── [Search After]
│   └── set_search_after(values) -> self
│
├── [Rescore]
│   ├── add_rescore(rescore) -> self
│   └── set_rescore(rescore) -> self
│
├── [Indices Boost]
│   └── add_indices_boost(index, boost) -> self
│
├── [Explain]
│   └── set_explain(value) -> self
│
├── [Script Fields]
│   ├── set_script_fields(script_fields) -> self
│   └── add_script_field(name, script) -> self
│
├── [Fields]
│   └── set_fields(fields) -> self
│
├── [Stored Fields]
│   └── set_stored_fields(fields) -> self
│
├── [KNN]
│   └── set_knn(knn) -> self
│
├── [쿼리 설정]
│   ├── set_query(query) -> self
│   ├── set_match_none() -> self
│   ├── set_match_all(boost?) -> self
│   ├── set_size(size) -> self
│   ├── set_from(from_) -> self
│   ├── set_timeout(timeout) -> self
│   ├── set_source(value) -> self
│   ├── add_source_includes(*fields) -> self
│   ├── add_source_excludes(*fields) -> self
│   ├── set_source_includes(fields) -> self
│   ├── set_source_excludes(fields) -> self
│   ├── set_track_total_hits(value) -> self
│   ├── set_track_scores(value) -> self
│   └── set_min_score(min_score) -> self
│
└── build() -> Dict                   # 최종 ES 쿼리 dict 반환
```
