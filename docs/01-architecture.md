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
│   └── es_query_builder/
│       ├── __init__.py              # 공개 API (QueryBuilder, 주요 클래스 export)
│       │
│       ├── core/                    # 핵심 도메인 레이어
│       │   ├── __init__.py
│       │   ├── enums.py             # SortOrder, SortMissing, BoolClause
│       │   └── types.py             # 공통 타입 정의 (TypeAlias 등)
│       │
│       ├── query/                   # Search Query 도메인
│       │   ├── __init__.py          # 쿼리 클래스 export
│       │   ├── leaf/                # 리프 쿼리 (개별 조건)
│       │   │   ├── __init__.py
│       │   │   ├── term.py          # TermQuery, TermsQuery
│       │   │   ├── match.py         # MatchQuery, MatchPhraseQuery
│       │   │   ├── range.py         # RangeQuery
│       │   │   ├── wildcard.py      # WildcardQuery
│       │   │   ├── exists.py        # ExistsQuery
│       │   │   ├── ids.py           # IdsQuery
│       │   │   └── special.py       # MatchAllQuery, MatchNoneQuery
│       │   ├── compound/            # 복합 쿼리
│       │   │   ├── __init__.py
│       │   │   ├── bool_query.py    # BoolQueryBuilder
│       │   │   └── dis_max.py       # DisMaxQuery
│       │   └── span/               # Span 쿼리
│       │       ├── __init__.py
│       │       ├── span_term.py     # SpanTermQuery
│       │       └── span_near.py     # SpanNearQuery
│       │   └── nested.py           # NestedQuery (compound와 leaf 사이)
│       │
│       ├── aggregation/             # Aggregation 도메인
│       │   ├── __init__.py          # Aggregation 클래스 export
│       │   ├── bucket/              # 버킷 Aggregation
│       │   │   ├── __init__.py
│       │   │   ├── terms.py         # TermsAggregation
│       │   │   ├── date_histogram.py # DateHistogramAggregation
│       │   │   ├── histogram.py     # HistogramAggregation
│       │   │   ├── range.py         # RangeAggregation
│       │   │   ├── filter.py        # FilterAggregation, FiltersAggregation
│       │   │   └── nested.py        # NestedAggregation
│       │   ├── metric/              # 메트릭 Aggregation
│       │   │   ├── __init__.py
│       │   │   ├── stats.py         # StatsAggregation
│       │   │   ├── cardinality.py   # CardinalityAggregation
│       │   │   ├── sum.py           # SumAggregation
│       │   │   ├── avg.py           # AvgAggregation
│       │   │   ├── min.py           # MinAggregation
│       │   │   ├── max.py           # MaxAggregation
│       │   │   └── top_hits.py      # TopHitsAggregation
│       │   └── aggregation_builder.py # AggregationBuilder (조합기)
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
│   │   └── test_enums.py
│   ├── query/
│   │   ├── leaf/
│   │   │   ├── test_term.py
│   │   │   ├── test_match.py
│   │   │   ├── test_range.py
│   │   │   ├── test_wildcard.py
│   │   │   ├── test_exists.py
│   │   │   ├── test_ids.py
│   │   │   └── test_special.py
│   │   ├── compound/
│   │   │   ├── test_bool_query.py
│   │   │   └── test_dis_max.py
│   │   ├── span/
│   │   │   ├── test_span_term.py
│   │   │   └── test_span_near.py
│   │   └── test_nested.py
│   ├── aggregation/
│   │   ├── bucket/
│   │   │   ├── test_terms.py
│   │   │   ├── test_date_histogram.py
│   │   │   ├── test_histogram.py
│   │   │   ├── test_range.py
│   │   │   ├── test_filter.py
│   │   │   └── test_nested.py
│   │   ├── metric/
│   │   │   ├── test_stats.py
│   │   │   ├── test_cardinality.py
│   │   │   ├── test_sum.py
│   │   │   ├── test_avg.py
│   │   │   ├── test_min.py
│   │   │   ├── test_max.py
│   │   │   └── test_top_hits.py
│   │   └── test_aggregation_builder.py
│   ├── sort/
│   │   └── test_sort_builder.py
│   └── test_query_builder.py        # 통합 테스트
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
- `enums.py`: SortOrder, SortMissing, BoolClause 등 공통 Enum
- `types.py`: ESQuery (= Dict[str, Any]), ESAggregation 등 타입 별칭

### Layer 2: Query Domain (검색 쿼리)
ES의 Query DSL을 1:1로 매핑하는 레이어.
각 쿼리 타입이 독립적인 클래스로 존재하며, `build()` 정적 메서드로 dict를 생성.

**서브 도메인:**
- `leaf/` - 단일 필드에 대한 조건 (term, match, range 등)
- `compound/` - 여러 쿼리를 조합 (bool, dis_max)
- `span/` - 근접 검색 (span_near, span_term)

### Layer 3: Aggregation Domain (집계)
ES Aggregation을 매핑하는 레이어.

**서브 도메인:**
- `bucket/` - 문서를 그룹화 (terms, date_histogram, range, filter, nested)
- `metric/` - 수치 계산 (sum, avg, min, max, stats, cardinality, top_hits)
- `AggregationBuilder` - 여러 aggregation을 조합하는 빌더

### Layer 4: Sort Domain (정렬)
Sort 로직을 QueryBuilder에서 분리하여 독립 도메인으로 관리.

### Layer 5: Builder (통합)
`QueryBuilder`가 모든 도메인을 통합하여 최종 ES 쿼리 dict를 생성.

## 4. 의존성 방향

```
Builder (QueryBuilder)
  ├── Query Domain (BoolQueryBuilder, Leaf Queries)
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
