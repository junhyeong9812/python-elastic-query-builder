# 코드 이전 및 구현 계획

## 기존 코드 → 라이브러리 매핑

| 원본 파일 | 원본 클래스 | 이전 위치 |
|-----------|------------|-----------|
| `enums/enums.py` | `SortOrder` | `core/enums.py` |
| `enums/enums.py` | `SortMissing` | `core/enums.py` |
| `enums/enums.py` | `BoolClause` | `core/enums.py` |
| `search/search_builder.py` | `TermQuery` | `query/leaf/term.py` |
| `search/search_builder.py` | `TermsQuery` | `query/leaf/term.py` |
| `search/search_builder.py` | `MatchQuery` | `query/leaf/match.py` |
| `search/search_builder.py` | `MatchPhraseQuery` | `query/leaf/match.py` |
| `search/search_builder.py` | `RangeQuery` | `query/leaf/range.py` |
| `search/search_builder.py` | `WildcardQuery` | `query/leaf/wildcard.py` |
| `search/search_builder.py` | `ExistsQuery` | `query/leaf/exists.py` |
| `search/search_builder.py` | `IdsQuery` | `query/leaf/ids.py` |
| `search/search_builder.py` | `MatchAllQuery` | `query/leaf/special.py` |
| `search/search_builder.py` | `MatchNoneQuery` | `query/leaf/special.py` |
| `search/search_builder.py` | `DisMaxQuery` | `query/compound/dis_max.py` |
| `search/search_builder.py` | `BoolQueryBuilder` | `query/compound/bool_query.py` |
| `search/search_builder.py` | `SpanTermQuery` | `query/span/span_term.py` |
| `search/search_builder.py` | `SpanNearQuery` | `query/span/span_near.py` |
| `search/search_builder.py` | `NestedQuery` | `query/nested.py` |
| `aggregation/aggregation_builder.py` | `TermsAggregation` | `aggregation/bucket/terms.py` |
| `aggregation/aggregation_builder.py` | `DateHistogramAggregation` | `aggregation/bucket/date_histogram.py` |
| `aggregation/aggregation_builder.py` | `HistogramAggregation` | `aggregation/bucket/histogram.py` |
| `aggregation/aggregation_builder.py` | `RangeAggregation` | `aggregation/bucket/range.py` |
| `aggregation/aggregation_builder.py` | `FilterAggregation` | `aggregation/bucket/filter.py` |
| `aggregation/aggregation_builder.py` | `FiltersAggregation` | `aggregation/bucket/filter.py` |
| `aggregation/aggregation_builder.py` | `NestedAggregation` | `aggregation/bucket/nested.py` |
| `aggregation/aggregation_builder.py` | `CardinalityAggregation` | `aggregation/metric/cardinality.py` |
| `aggregation/aggregation_builder.py` | `SumAggregation` | `aggregation/metric/sum.py` |
| `aggregation/aggregation_builder.py` | `AvgAggregation` | `aggregation/metric/avg.py` |
| `aggregation/aggregation_builder.py` | `MinAggregation` | `aggregation/metric/min.py` |
| `aggregation/aggregation_builder.py` | `MaxAggregation` | `aggregation/metric/max.py` |
| `aggregation/aggregation_builder.py` | `StatsAggregation` | `aggregation/metric/stats.py` |
| `aggregation/aggregation_builder.py` | `TopHitsAggregation` | `aggregation/metric/top_hits.py` |
| `aggregation/aggregation_builder.py` | `AggregationBuilder` | `aggregation/aggregation_builder.py` |
| `query_builder.py` | `QueryBuilder` (sort 부분) | `sort/sort_builder.py` (신규 분리) |
| `query_builder.py` | `QueryBuilder` | `builder.py` |

## 이전 시 변경 사항

1. **import 경로 변경**: 프로젝트 내부 절대 경로 → 패키지 상대 경로
2. **marshmallow 의존성 제거**: `aggregation_builder.py`의 `from marshmallow import missing` (미사용 import 제거)
3. **Sort 로직 분리**: QueryBuilder의 정렬 관련 메서드 → SortBuilder로 이전
4. **중복 메서드 제거**: `set_track_scores`가 2번 정의되어 있음 (line 105, 158) → 1개로 통합
5. **`__init__.py` 구성**: 각 도메인의 공개 API를 최상위에서 import 가능하도록 구성

## 작업 순서

### Step 1: 프로젝트 기반 구성
- [ ] pyproject.toml 작성
- [ ] 디렉토리 구조 생성
- [ ] .gitignore 작성

### Step 2: Core 도메인 이전
- [ ] core/enums.py
- [ ] core/types.py
- [ ] tests/core/test_enums.py

### Step 3: Query Leaf 이전
- [ ] query/leaf/*.py (각 쿼리 클래스)
- [ ] tests/query/leaf/*.py

### Step 4: Query Compound 이전
- [ ] query/compound/bool_query.py
- [ ] query/compound/dis_max.py
- [ ] tests/query/compound/*.py

### Step 5: Query Span + Nested 이전
- [ ] query/span/*.py
- [ ] query/nested.py
- [ ] tests

### Step 6: Aggregation 이전
- [ ] aggregation/bucket/*.py
- [ ] aggregation/metric/*.py
- [ ] aggregation/aggregation_builder.py
- [ ] tests

### Step 7: Sort 도메인 생성
- [ ] sort/sort_builder.py (QueryBuilder에서 분리)
- [ ] tests/sort/test_sort_builder.py

### Step 8: QueryBuilder 통합
- [ ] builder.py (최상위 빌더)
- [ ] tests/test_query_builder.py (통합 테스트)

### Step 9: 패키지 마무리
- [ ] __init__.py 공개 API 정리
- [ ] README.md 작성
- [ ] 전체 테스트 통과 확인
