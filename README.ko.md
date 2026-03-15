# elastic-query-builder

[![PyPI version](https://badge.fury.io/py/elastic-query-builder.svg)](https://pypi.org/project/elastic-query-builder/)
[![Python version](https://img.shields.io/pypi/pyversions/elastic-query-builder.svg)](https://pypi.org/project/elastic-query-builder/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/junhyeong9812/python-elastic-query-builder/actions/workflows/tests.yml/badge.svg)](https://github.com/junhyeong9812/python-elastic-query-builder/actions)

**Elasticsearch 쿼리를 Python 빌더 패턴으로 간결하고 안전하게 작성하세요.**

복잡한 dict 중첩 없이, 메서드 체이닝과 타입 힌트를 활용하여 가독성 높은 ES 쿼리를 생성하는 라이브러리입니다.

---

## 특징

- **외부 의존성 없음** - 순수 Python만으로 동작합니다. 별도의 패키지 설치가 필요 없습니다.
- **빌더 패턴 + 메서드 체이닝** - 직관적인 API로 복잡한 쿼리도 깔끔하게 작성할 수 있습니다.
- **타입 힌트 완전 지원** - IDE 자동완성과 정적 분석의 이점을 누릴 수 있습니다.
- **dict 출력** - `build()` 결과는 순수 Python dict이므로, `elasticsearch-py`, `opensearch-py` 등 어떤 ES 클라이언트와도 호환됩니다.
- **도메인 분리** - Query, Aggregation, Sort를 독립 도메인으로 관리하여 관심사를 명확히 분리합니다.

---

## 설치

```bash
pip install elastic-query-builder
```

---

## 빠른 시작

```python
from elastic_query_builder import QueryBuilder

qb = QueryBuilder()
query = (
    qb.add_must(QueryBuilder.Match.build("title", "검색어", operator="and"))
      .add_filter(QueryBuilder.Range.build("date", gte="2024-01-01"))
      .set_size(10)
      .set_from(0)
      .build()
)

# 결과는 순수 dict — 바로 ES 클라이언트에 전달 가능
# es.search(index="my_index", body=query)
```

---

## 사용 예시

### 기본 검색

`QueryBuilder`를 사용하여 검색 조건, 페이징, 정렬을 한 번에 구성할 수 있습니다.

```python
from elastic_query_builder import QueryBuilder

qb = QueryBuilder()
query = (
    qb.add_must(QueryBuilder.Match.build("title", "검색어", operator="and"))
      .add_filter(QueryBuilder.Range.build("date", gte="2024-01-01"))
      .set_size(10)
      .set_from(0)
      .build()
)
```

### 리프 쿼리 (독립 사용)

각 쿼리 클래스는 `QueryBuilder` 없이도 독립적으로 사용할 수 있습니다. `build()` 정적 메서드를 호출하면 ES 쿼리 dict가 바로 생성됩니다.

```python
from elastic_query_builder.query.leaf import TermQuery, MatchQuery, RangeQuery

# Term 쿼리: 정확한 값 일치
term = TermQuery.build("status", "active")
# {"term": {"status": {"value": "active"}}}

# Match 쿼리: 전문 검색 (Full-text)
match = MatchQuery.build("title", "검색어", boost=2.0, operator="and")
# {"match": {"title": {"query": "검색어", "boost": 2.0, "operator": "and"}}}

# Range 쿼리: 범위 조건
range_q = RangeQuery.build("price", gte=100, lte=500)
# {"range": {"price": {"gte": 100, "lte": 500}}}
```

### Bool 쿼리 (중첩)

`nested_bool()`을 사용하면 중첩된 bool 쿼리를 손쉽게 구성할 수 있습니다. 내부 bool 쿼리를 먼저 구성한 뒤, 외부 bool 쿼리에 조건으로 추가하는 방식입니다.

```python
from elastic_query_builder import QueryBuilder

qb = QueryBuilder()

# 중첩 bool 쿼리 생성
inner_bool = qb.nested_bool()
inner_bool.add_should(QueryBuilder.Match.build("title", "키워드A"))
inner_bool.add_should(QueryBuilder.Match.build("content", "키워드A"))
inner_bool.add_minimum_should_match(1)

query = (
    qb.add_must(inner_bool.build())
      .add_filter(QueryBuilder.Term.build("status", "published"))
      .set_size(20)
      .build()
)
```

### Aggregation

집계(Aggregation)는 편의 메서드를 통해 간단하게 추가할 수 있습니다. 중첩 집계도 `nested_agg()`로 구성합니다.

```python
qb = QueryBuilder()

# 기본 집계
query = (
    qb.set_match_all()
      .set_size(0)
      .add_terms_agg("status_count", "status", size=10)
      .add_date_histogram_agg("monthly", "created_at", calendar_interval="1M")
      .build()
)

# 중첩 집계 (Nested Aggregation)
sub_agg = qb.nested_agg()
sub_agg.add_terms("item_names", "items.name", size=5)

query = (
    qb.set_match_all()
      .set_size(0)
      .add_nested_agg("items_agg", "items", sub_agg.build())
      .build()
)
```

### 정렬

정렬 조건을 여러 개 추가할 수 있으며, `_score` 기반 정렬도 지원합니다.

```python
from elastic_query_builder import QueryBuilder
from elastic_query_builder.core.enums import SortOrder, SortMissing

qb = QueryBuilder()
query = (
    qb.set_match_all()
      .add_sort("date", SortOrder.DESC)
      .add_sort("name", SortOrder.ASC, missing=SortMissing.LAST)
      .add_score_sort()
      .set_size(50)
      .build()
)
```

### _source 제어

응답에 포함할 필드를 세밀하게 제어할 수 있습니다. `includes`/`excludes`를 조합하거나, `_source`를 완전히 비활성화할 수 있습니다.

```python
qb = QueryBuilder()

# includes만 설정 — 지정한 필드만 반환
query = qb.set_match_all().set_source_includes(["title", "date"]).build()

# excludes 추가 — 특정 필드 제외
query = qb.set_match_all().add_source_excludes("content", "metadata").build()

# _source 비활성화 — 문서 내용 없이 _id만 반환
query = qb.set_match_all().set_source(False).build()
```

### 실전 예시 (특허 검색)

실무에서 사용할 수 있는 복합 쿼리 예시입니다. 검색 조건, 필터, 제외 조건, 정렬, 페이징, `_source` 제어를 모두 조합합니다.

```python
from elastic_query_builder import QueryBuilder
from elastic_query_builder.core.enums import SortOrder

qb = QueryBuilder()

# 검색 조건 (must)
qb.add_must(QueryBuilder.Match.build("productKor", "반도체", operator="and"))
qb.add_must(QueryBuilder.Match.build("abstract", "발광 다이오드", boost=2.0))

# 필터 (filter) — 점수에 영향 없이 조건 적용
qb.add_filter(QueryBuilder.Range.build("applicationDate", gte="20200101", lte="20241231"))
qb.add_filter(QueryBuilder.Term.build("statusCode", "registered"))

# 제외 조건 (must_not)
qb.add_must_not(QueryBuilder.Term.build("applicantName", "테스트"))

# 정렬 + 페이징
qb.add_sort("applicationDate", SortOrder.DESC)
qb.set_size(20)
qb.set_from(0)
qb.set_track_total_hits(True)

# _source 제어 — 필요한 필드만 반환
qb.set_source_includes(["applicationNumber", "productKor", "applicantName", "applicationDate"])

query = qb.build()
```

---

## 지원하는 쿼리 타입

### Leaf Queries

단일 필드에 대한 조건을 표현하는 쿼리입니다.

| 클래스 | ES 쿼리 | 설명 |
|--------|---------|------|
| `TermQuery` | `term` | 정확한 값 일치 검색 |
| `TermsQuery` | `terms` | 여러 값 중 하나와 일치 검색 |
| `MatchQuery` | `match` | 전문 검색 (Full-text search) |
| `MatchPhraseQuery` | `match_phrase` | 구문 일치 검색 |
| `RangeQuery` | `range` | 범위 조건 (gte, lte, gt, lt) |
| `WildcardQuery` | `wildcard` | 와일드카드 패턴 검색 |
| `ExistsQuery` | `exists` | 필드 존재 여부 확인 |
| `IdsQuery` | `ids` | 문서 ID 기반 검색 |
| `MatchAllQuery` | `match_all` | 모든 문서 매칭 |
| `MatchNoneQuery` | `match_none` | 어떤 문서도 매칭하지 않음 |

### Compound Queries

여러 쿼리를 논리적으로 조합하는 복합 쿼리입니다.

| 클래스 | ES 쿼리 | 설명 |
|--------|---------|------|
| `BoolQueryBuilder` | `bool` | must / should / must_not / filter 절 조합 |
| `DisMaxQuery` | `dis_max` | 여러 쿼리 중 최고 점수 선택 |
| `NestedQuery` | `nested` | 중첩 객체 내부 검색 |

### Span Queries

토큰 간의 위치(근접도)를 기반으로 검색하는 쿼리입니다.

| 클래스 | ES 쿼리 | 설명 |
|--------|---------|------|
| `SpanTermQuery` | `span_term` | 단일 토큰 span 검색 |
| `SpanNearQuery` | `span_near` | 여러 토큰의 근접 검색 (slop, in_order 지원) |

### Aggregations - Bucket

문서를 그룹(버킷)으로 나누는 집계입니다.

| 클래스 | ES 집계 | 설명 |
|--------|---------|------|
| `TermsAggregation` | `terms` | 필드 값별 그룹화 |
| `DateHistogramAggregation` | `date_histogram` | 날짜 간격별 그룹화 |
| `HistogramAggregation` | `histogram` | 수치 간격별 그룹화 |
| `RangeAggregation` | `range` | 사용자 정의 범위별 그룹화 |
| `FilterAggregation` | `filter` | 단일 필터 기반 그룹화 |
| `FiltersAggregation` | `filters` | 복수 필터 기반 그룹화 |
| `NestedAggregation` | `nested` | 중첩 객체 내부 집계 |

### Aggregations - Metric

수치 계산을 수행하는 집계입니다.

| 클래스 | ES 집계 | 설명 |
|--------|---------|------|
| `SumAggregation` | `sum` | 합계 계산 |
| `AvgAggregation` | `avg` | 평균 계산 |
| `MinAggregation` | `min` | 최솟값 계산 |
| `MaxAggregation` | `max` | 최댓값 계산 |
| `StatsAggregation` | `stats` | 통계 요약 (count, min, max, avg, sum) |
| `CardinalityAggregation` | `cardinality` | 고유 값 개수 (유사 distinct count) |
| `TopHitsAggregation` | `top_hits` | 버킷 내 상위 문서 반환 |

---

## 아키텍처

이 프로젝트는 **레이어드 아키텍처**를 채택하여 각 도메인의 관심사를 명확히 분리합니다. 하위 레이어는 상위 레이어를 참조하지 않으며, 각 도메인(Query, Aggregation, Sort)은 서로 독립적입니다.

### 레이어 구조

```
Layer 5: QueryBuilder (통합 빌더)
  ├── Layer 2: Query Domain (검색 쿼리)
  ├── Layer 3: Aggregation Domain (집계)
  ├── Layer 4: Sort Domain (정렬)
  └── Layer 1: Core (Enum, 타입 정의)
```

### 패키지 트리

```
elastic_query_builder/
├── __init__.py                  # 공개 API (QueryBuilder export)
├── builder.py                   # QueryBuilder (최상위 통합 빌더)
│
├── core/                        # 핵심 레이어
│   ├── enums.py                 # SortOrder, SortMissing, BoolClause
│   └── types.py                 # ESQuery, ESAggregation 등 타입 별칭
│
├── query/                       # 검색 쿼리 도메인
│   ├── leaf/                    # 리프 쿼리
│   │   ├── term.py              # TermQuery, TermsQuery
│   │   ├── match.py             # MatchQuery, MatchPhraseQuery
│   │   ├── range.py             # RangeQuery
│   │   ├── wildcard.py          # WildcardQuery
│   │   ├── exists.py            # ExistsQuery
│   │   ├── ids.py               # IdsQuery
│   │   └── special.py           # MatchAllQuery, MatchNoneQuery
│   ├── compound/                # 복합 쿼리
│   │   ├── bool_query.py        # BoolQueryBuilder
│   │   └── dis_max.py           # DisMaxQuery
│   ├── span/                    # Span 쿼리
│   │   ├── span_term.py         # SpanTermQuery
│   │   └── span_near.py         # SpanNearQuery
│   └── nested.py                # NestedQuery
│
├── aggregation/                 # 집계 도메인
│   ├── bucket/                  # 버킷 집계
│   │   ├── terms.py             # TermsAggregation
│   │   ├── date_histogram.py    # DateHistogramAggregation
│   │   ├── histogram.py         # HistogramAggregation
│   │   ├── range.py             # RangeAggregation
│   │   ├── filter.py            # FilterAggregation, FiltersAggregation
│   │   └── nested.py            # NestedAggregation
│   ├── metric/                  # 메트릭 집계
│   │   ├── stats.py             # StatsAggregation
│   │   ├── cardinality.py       # CardinalityAggregation
│   │   ├── sum.py               # SumAggregation
│   │   ├── avg.py               # AvgAggregation
│   │   ├── min.py               # MinAggregation
│   │   ├── max.py               # MaxAggregation
│   │   └── top_hits.py          # TopHitsAggregation
│   └── aggregation_builder.py   # AggregationBuilder
│
└── sort/                        # 정렬 도메인
    └── sort_builder.py          # SortBuilder
```

### 설계 원칙

1. **단일 책임** - 각 쿼리 클래스는 자신의 ES 쿼리만 생성합니다.
2. **일관된 인터페이스** - `build()` 메서드는 항상 `Dict[str, Any]`를 반환합니다.
3. **메서드 체이닝** - 빌더 메서드는 `self`를 반환하여 체이닝을 지원합니다.
4. **None 값 제거** - `None`인 Optional 파라미터는 쿼리에 포함되지 않습니다.
5. **무의존성** - 외부 라이브러리 없이 순수 Python만으로 동작합니다.

---

## API 레퍼런스

상세한 API 문서는 [`docs/`](./docs/) 폴더를 참고하세요.

| 문서 | 내용 |
|------|------|
| [01-architecture.md](./docs/01-architecture.md) | 아키텍처 설계 및 레이어 구조 |
| [02-class-design.md](./docs/02-class-design.md) | 클래스별 상세 설계 및 메서드 목록 |
| [03-api-reference.md](./docs/03-api-reference.md) | API 사용 예시 모음 |
| [04-proposals.md](./docs/04-proposals.md) | 추가 기능 제안 |
| [05-migration-plan.md](./docs/05-migration-plan.md) | 마이그레이션 계획 |

---

## 기여하기

이 프로젝트에 기여해 주셔서 감사합니다! 다음 절차를 따라 주세요.

1. **저장소 포크** - GitHub에서 이 저장소를 포크합니다.

2. **브랜치 생성** - 기능 또는 수정 사항에 맞는 브랜치를 생성합니다.
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **변경 사항 구현** - 코드를 수정하고 테스트를 추가합니다.

4. **테스트 실행** - 모든 테스트가 통과하는지 확인합니다.
   ```bash
   pytest
   ```

5. **커밋 & 푸시**
   ```bash
   git commit -m "Add: 기능 설명"
   git push origin feature/your-feature-name
   ```

6. **Pull Request 생성** - GitHub에서 PR을 생성합니다.

### 기여 시 유의사항

- 기존 코드 스타일과 패턴을 따라 주세요.
- 새로운 쿼리 타입 추가 시, 반드시 단위 테스트를 함께 작성해 주세요.
- 타입 힌트를 빠뜨리지 않도록 해 주세요.
- 외부 의존성을 추가하지 마세요.

---

## 라이선스

이 프로젝트는 [MIT License](./LICENSE)에 따라 배포됩니다.
