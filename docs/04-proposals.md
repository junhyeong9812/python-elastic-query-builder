# 추가 기능 제안서

기존 코드 분석을 통해 현재 구현에 없지만 ES 쿼리 빌더 라이브러리로서 필요한 기능들을 정리한다.

> **최종 업데이트**: 2026-03-20 — v0.1.0 배포 완료 후 상태 반영

---

## P1: 높은 우선순위 (핵심 기능 보완)

### 1.1 쿼리 직렬화 / 디버깅 지원 — ⏳ 미구현

**현재 문제**: `build()` 결과를 JSON으로 보려면 직접 `json.dumps`해야 함.

**제안**:
```python
qb = QueryBuilder()
qb.add_must(...)

# JSON 문자열로 출력
print(qb.to_json(indent=2))

# pretty print
qb.pprint()
```

### 1.2 쿼리 유효성 검증 (Validation) — ⏳ 미구현

**현재 문제**: 잘못된 필드 조합이나 빈 쿼리가 그대로 ES에 전달됨.

**제안**:
```python
qb = QueryBuilder()
qb.add_must(QueryBuilder.Range.build("date"))  # gte/lte/gt/lt 모두 없음

qb.validate()  # -> ValidationError: "RangeQuery requires at least one bound (gte, lte, gt, lt)"
```

### 1.3 QueryBuilder 복제 (copy/clone) — ⏳ 미구현

**현재 문제**: QueryBuilder 인스턴스를 재사용하거나 분기할 수 없음.

**제안**:
```python
base = QueryBuilder()
base.add_filter(QueryBuilder.Term.build("status", "active"))
base.set_size(20)

# 분기
search_a = base.clone().add_must(QueryBuilder.Match.build("title", "A"))
search_b = base.clone().add_must(QueryBuilder.Match.build("title", "B"))
```

### 1.4 Function Score Query 지원 — ✅ 구현 완료

`FunctionScoreQuery` 클래스로 구현됨. `QueryBuilder.FunctionScore`로 접근 가능.

```python
QueryBuilder.FunctionScore.build(
    query=QueryBuilder.MatchAll.build(),
    functions=[
        {"filter": {"term": {"featured": True}}, "weight": 10},
        {"field_value_factor": {"field": "popularity", "modifier": "log1p"}}
    ],
    score_mode="sum"
)
```

### 1.5 Multi-Match Query 지원 — ✅ 구현 완료

`MultiMatchQuery` 클래스로 구현됨. 12개 옵셔널 파라미터 지원.

```python
QueryBuilder.MultiMatch.build(
    query="검색어",
    fields=["title^2", "content"],
    type=MultiMatchType.BEST_FIELDS,
    fuzziness="AUTO"
)
```

---

## P2: 중간 우선순위 (편의성 향상)

### 2.1 Highlight 지원 — ✅ 구현 완료

`QueryBuilder.set_highlight()`, `QueryBuilder.add_highlight_field()`로 지원.

```python
qb.set_highlight({"pre_tags": ["<em>"], "post_tags": ["</em>"], "fields": {"title": {}}})
qb.add_highlight_field("content", fragment_size=150)
```

### 2.2 Script Query / Script Field 지원 — ✅ 구현 완료

`QueryBuilder.set_script_fields()`, `QueryBuilder.add_script_field()`로 지원.

```python
qb.add_script_field("calculated_price", {
    "script": {"source": "doc['price'].value * params.rate", "params": {"rate": 1.1}}
})
```

### 2.3 Search After (커서 기반 페이징) — ✅ 구현 완료

```python
qb.set_search_after([1609459200000, "doc_id_123"])
```

### 2.4 Collapse (필드 그룹핑) — ✅ 구현 완료

```python
qb.set_collapse("applicant_id")
qb.set_collapse({"field": "applicant_id", "inner_hits": {"name": "latest", "size": 3}})
```

### 2.5 Suggest (자동완성/오타교정) — ✅ 구현 완료

`QueryBuilder.set_suggest()`, `QueryBuilder.add_suggest()`로 지원.

```python
qb.add_suggest("my-suggest", {"text": "검색", "term": {"field": "title"}})
```

### 2.6 Pipeline Aggregation 지원 — ⏳ 미구현

현재 bucket/metric agg만 지원. pipeline agg는 향후 추가 예정:

```python
class BucketSortAggregation: ...
class BucketSelectorAggregation: ...
class DerivativeAggregation: ...
class CumulativeSumAggregation: ...
```

---

## P3: 낮은 우선순위 (확장성)

### 3.1 Geo 쿼리 지원 — ✅ 구현 완료

`GeoDistanceQuery`, `GeoBoundingBoxQuery` 구현됨.

```python
QueryBuilder.GeoDistance.build("location", lat=37.5665, lon=126.9780, distance="10km")
QueryBuilder.GeoBoundingBox.build("location",
    top_left={"lat": 38.0, "lon": 126.0},
    bottom_right={"lat": 37.0, "lon": 127.0})
```

### 3.2 Percolate Query 지원 — ✅ 구현 완료

```python
QueryBuilder.Percolate.build("query", document={"title": "test", "content": "hello"})
```

### 3.3 Index Template / Mapping 빌더 — ⏳ 미구현

쿼리 빌더와 별개로 인덱스 설정을 빌더 패턴으로 생성하는 기능. 향후 검토.

### 3.4 Response Parser — ⏳ 미구현

ES 응답을 파싱하는 유틸리티. 향후 검토.

---

## 구현 현황 요약

| 상태 | 기능 |
|------|------|
| ✅ 완료 | FunctionScore, MultiMatch, Highlight, Script Fields, Search After, Collapse, Suggest, Geo 쿼리, Percolate, KNN, Rescore, Indices Boost, Explain, Fields, Stored Fields |
| ⏳ 미구현 | 직렬화/디버깅 (`to_json`), Validation, Clone, Pipeline Aggregation, Mapping Builder, Response Parser |

## 구현 로드맵

| 단계 | 내용 | 상태 |
|------|------|------|
| **Phase 1** | 기존 코드 이전 + 구조 분리 + 테스트 | ✅ 완료 |
| **Phase 2** | P1 기능 추가 (function_score, multi_match) | ✅ 완료 |
| **Phase 3** | P2 기능 추가 (highlight, script, search_after, collapse, suggest) | ✅ 완료 |
| **Phase 4** | P3 기능 추가 (geo, percolate) | ✅ 완료 |
| **Phase 5** | PyPI 배포 + 문서화 + CI/CD | ✅ 완료 (v0.1.0) |
| **Phase 6** | validation, clone, to_json, pipeline agg | 향후 예정 |
