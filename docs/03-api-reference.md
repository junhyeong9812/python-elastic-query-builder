# API 레퍼런스 (사용 예시)

## 기본 사용법

```python
from es_query_builder import QueryBuilder

# 간단한 검색
qb = QueryBuilder()
query = (
    qb.add_must(QueryBuilder.Match.build("title", "검색어", operator="and"))
      .add_filter(QueryBuilder.Range.build("date", gte="2024-01-01"))
      .set_size(10)
      .set_from(0)
      .build()
)
```

## 리프 쿼리 단독 사용

```python
from es_query_builder.query.leaf import TermQuery, MatchQuery, RangeQuery

# 각 쿼리를 독립적으로 사용 가능
term = TermQuery.build("status", "active")
match = MatchQuery.build("title", "검색어", boost=2.0, operator="and")
range_q = RangeQuery.build("price", gte=100, lte=500)
```

## Bool 쿼리 조합

```python
from es_query_builder import QueryBuilder

qb = QueryBuilder()

# 중첩 bool
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

## Aggregation 사용

```python
qb = QueryBuilder()

# 기본 aggregation
query = (
    qb.set_match_all()
      .set_size(0)
      .add_terms_agg("status_count", "status", size=10)
      .add_date_histogram_agg("monthly", "created_at", calendar_interval="1M")
      .build()
)

# 중첩 aggregation
sub_agg = qb.nested_agg()
sub_agg.add_terms("item_names", "items.name", size=5)

query = (
    qb.set_match_all()
      .set_size(0)
      .add_nested_agg("items_agg", "items", sub_agg.build())
      .build()
)
```

## 정렬

```python
from es_query_builder import QueryBuilder
from es_query_builder.core.enums import SortOrder, SortMissing

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

## _source 제어

```python
qb = QueryBuilder()

# includes만
query = qb.set_match_all().set_source_includes(["title", "date"]).build()

# excludes 추가
query = qb.set_match_all().add_source_excludes("content", "metadata").build()

# 비활성화
query = qb.set_match_all().set_source(False).build()
```

## Span 쿼리 (근접 검색)

```python
qb = QueryBuilder()
query = (
    qb.add_must(
        QueryBuilder.SpanNear.build(
            clauses=[
                QueryBuilder.SpanTerm.build("content", "인공"),
                QueryBuilder.SpanTerm.build("content", "지능"),
            ],
            slop=3,
            in_order=True
        )
    )
    .build()
)
```

## 복합 예시: 특허 검색

```python
qb = QueryBuilder()

# 검색 조건
qb.add_must(QueryBuilder.Match.build("productKor", "반도체", operator="and"))
qb.add_must(QueryBuilder.Match.build("abstract", "발광 다이오드", boost=2.0))

# 필터
qb.add_filter(QueryBuilder.Range.build("applicationDate", gte="20200101", lte="20241231"))
qb.add_filter(QueryBuilder.Term.build("statusCode", "registered"))

# 제외
qb.add_must_not(QueryBuilder.Term.build("applicantName", "테스트"))

# 정렬 + 페이징
qb.add_sort("applicationDate", SortOrder.DESC)
qb.set_size(20)
qb.set_from(0)
qb.set_track_total_hits(True)

# _source 제어
qb.set_source_includes(["applicationNumber", "productKor", "applicantName", "applicationDate"])

query = qb.build()
```
