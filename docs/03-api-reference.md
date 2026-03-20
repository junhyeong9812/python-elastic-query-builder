# API 레퍼런스 (사용 예시)

## 기본 사용법

```python
from elastic_query_builder import QueryBuilder

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
from elastic_query_builder.query.leaf import TermQuery, MatchQuery, RangeQuery

# 각 쿼리를 독립적으로 사용 가능
term = TermQuery.build("status", "active")
match = MatchQuery.build("title", "검색어", boost=2.0, operator="and")
range_q = RangeQuery.build("price", gte=100, lte=500)
```

## Bool 쿼리 조합

```python
from elastic_query_builder import QueryBuilder

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

## Multi-Match 쿼리 (여러 필드 동시 검색)

```python
from elastic_query_builder import QueryBuilder, MultiMatchType

qb = QueryBuilder()

# 여러 필드에서 동시에 검색하고 best_fields 전략 사용
query = (
    qb.add_should(QueryBuilder.MultiMatch.build(
        ["korsum.unified", "engsum.unified", "engsumPronun.unified"],
        "에스페라",
        type="best_fields",
        tie_breaker=0.3,
        fuzziness="AUTO"
    ))
    .set_size(20)
    .build()
)
```

## Function Score (커스텀 스코어링)

```python
from elastic_query_builder import QueryBuilder

# 특정 조건에 가중치를 부여하여 스코어 조정
query = QueryBuilder.FunctionScore.build(
    query={"bool": {"should": [...]}},
    functions=[
        {"filter": {"term": {"status": {"value": "featured"}}}, "weight": 10},
        {"filter": {"match_phrase": {"korsum": {"query": "에스페라"}}}, "weight": 5},
    ],
    score_mode="sum",
    boost_mode="multiply",
    max_boost=42
)
```

## Fuzzy / Prefix / Regexp 쿼리

```python
from elastic_query_builder import QueryBuilder

# 오타 허용 검색
fuzzy = QueryBuilder.Fuzzy.build("trademark_name", "espera", fuzziness="AUTO", prefix_length=1)

# 접두어 검색
prefix = QueryBuilder.Prefix.build("trademark_name", "espe")

# 정규식 패턴 검색
regexp = QueryBuilder.Regexp.build("engsum", "espe[r|n]a")
```

## Highlight (검색어 하이라이팅)

```python
from elastic_query_builder import QueryBuilder

# set_highlight로 전체 설정을 한 번에 지정
qb = QueryBuilder()
query = (
    qb.add_must(QueryBuilder.Match.build("title", "검색어"))
      .set_highlight({
          "pre_tags": ["<em>"],
          "post_tags": ["</em>"],
          "fields": {
              "title": {"number_of_fragments": 3},
              "content": {}
          }
      })
      .build()
)

# 또는 add_highlight_field로 필드별로 추가
query = (
    QueryBuilder()
    .add_must(QueryBuilder.Match.build("title", "검색어"))
    .add_highlight_field("title", {"number_of_fragments": 3})
    .add_highlight_field("content")
    .build()
)
```

## Post Filter (집계에 영향 없는 필터링)

```python
from elastic_query_builder import QueryBuilder

# aggregation 결과에는 영향 없이 검색 결과만 필터링
query = (
    QueryBuilder()
    .set_match_all()
    .add_terms_agg("colors", "color")
    .set_post_filter({"term": {"color": {"value": "red"}}})
    .build()
)
```

## Suggest (검색어 제안)

```python
from elastic_query_builder import QueryBuilder

# 오타 교정 등 검색어 제안 기능
query = (
    QueryBuilder()
    .add_suggest("my-suggest", {
        "text": "에스페라",
        "term": {"field": "korsum"}
    })
    .build()
)
```

## Collapse + Search After (딥 페이지네이션)

```python
from elastic_query_builder import QueryBuilder
from elastic_query_builder.core.enums import SortOrder

# 특정 필드 기준 중복 제거 + 커서 기반 페이지네이션
query = (
    QueryBuilder()
    .add_must(QueryBuilder.Match.build("title", "검색어"))
    .set_collapse("applicant_id")
    .add_sort("date", SortOrder.DESC)
    .set_search_after([1630000000, "doc_id_123"])
    .set_size(20)
    .build()
)
```

## KNN (벡터 검색)

```python
from elastic_query_builder import QueryBuilder

# 벡터 유사도 기반 검색 (k-nearest neighbors)
query = (
    QueryBuilder()
    .set_knn(
        field="name_vector",
        query_vector=[0.1, 0.2, 0.3],
        k=10,
        num_candidates=100
    )
    .set_size(10)
    .build()
)
```

## Geo 쿼리 (지리 검색)

```python
from elastic_query_builder import QueryBuilder

# 특정 좌표에서 반경 내 검색
geo = QueryBuilder.GeoDistance.build(
    "location",
    {"lat": 37.5665, "lon": 126.978},
    "10km"
)

# 바운딩 박스 내 검색
bbox = QueryBuilder.GeoBoundingBox.build(
    "location",
    {"lat": 38, "lon": 126},
    {"lat": 37, "lon": 127}
)
```

## Rescore (재스코어링)

```python
from elastic_query_builder import QueryBuilder

# 상위 결과에 대해 더 정밀한 스코어링 적용
query = (
    QueryBuilder()
    .add_must(QueryBuilder.Match.build("title", "검색어"))
    .add_rescore({
        "window_size": 100,
        "query": {
            "rescore_query": {
                "match_phrase": {
                    "title": {"query": "검색어", "slop": 2}
                }
            },
            "query_weight": 0.7,
            "rescore_query_weight": 1.2
        }
    })
    .build()
)
```

## Script Fields + Explain (스크립트 필드 & 스코어 설명)

```python
from elastic_query_builder import QueryBuilder

# 스크립트로 계산된 필드 추가 + 스코어 계산 과정 확인
query = (
    QueryBuilder()
    .set_match_all()
    .add_script_field("doubled_price", {"source": "doc['price'].value * 2"})
    .set_explain(True)
    .set_size(10)
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
