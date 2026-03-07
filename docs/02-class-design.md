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

### 2.3 range.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `RangeQuery` | `build(field, gte?, lte?, gt?, lt?)` | 범위 조건 |

출력: `{"range": {field: {"gte": ..., "lte": ...}}}`

### 2.4 wildcard.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `WildcardQuery` | `build(field, value, boost?, case_insensitive?)` | 와일드카드 패턴 |

### 2.5 exists.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `ExistsQuery` | `build(field)` | 필드명 |

### 2.6 ids.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `IdsQuery` | `build(values)` | ID 리스트 |

### 2.7 special.py

| 클래스 | 메서드 | 입력 |
|--------|--------|------|
| `MatchAllQuery` | `build(boost?)` | - |
| `MatchNoneQuery` | `build()` | - |

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

## 6. Aggregation 도메인 - Bucket

### 6.1 terms.py - TermsAggregation

```python
build(field, size?, order?, min_doc_count?, missing?, include?, exclude?)
```
출력: `{"terms": {"field": ..., "size": ...}}`

### 6.2 date_histogram.py - DateHistogramAggregation

```python
build(field, calendar_interval?, fixed_interval?, format?, time_zone?, min_doc_count?, extended_bounds?)
```

### 6.3 histogram.py - HistogramAggregation

```python
build(field, interval, min_doc_count?, extended_bounds?)
```

### 6.4 range.py - RangeAggregation

```python
build(field, ranges, keyed?)
```

### 6.5 filter.py - FilterAggregation / FiltersAggregation

```python
# FilterAggregation
build(filter_query)

# FiltersAggregation
build(filters, other_bucket?, other_bucket_key?)
```

### 6.6 nested.py - NestedAggregation

```python
build(path, sub_aggs?)
```

---

## 7. Aggregation 도메인 - Metric

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

## 8. AggregationBuilder

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

## 9. SortBuilder (신규 분리)

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

## 10. QueryBuilder (통합 빌더)

최상위 빌더. 모든 도메인을 통합하여 최종 ES 쿼리를 생성.

```
QueryBuilder
├── [Query 생성 - 정적 참조]
│   ├── Term = TermQuery
│   ├── Terms = TermsQuery
│   ├── Match = MatchQuery
│   ├── ... (모든 리프 쿼리)
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
