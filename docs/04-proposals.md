# 추가 기능 제안서

기존 코드 분석을 통해 현재 구현에 없지만 ES 쿼리 빌더 라이브러리로서 필요한 기능들을 정리한다.

---

## P1: 높은 우선순위 (핵심 기능 보완)

### 1.1 쿼리 직렬화 / 디버깅 지원

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

### 1.2 쿼리 유효성 검증 (Validation)

**현재 문제**: 잘못된 필드 조합이나 빈 쿼리가 그대로 ES에 전달됨.

**제안**:
```python
qb = QueryBuilder()
qb.add_must(QueryBuilder.Range.build("date"))  # gte/lte/gt/lt 모두 없음

qb.validate()  # -> ValidationError: "RangeQuery requires at least one bound (gte, lte, gt, lt)"
```

검증 대상:
- RangeQuery에 bound가 하나도 없는 경우
- DateHistogram에 calendar_interval과 fixed_interval 둘 다 없는 경우
- BoolQuery가 비어 있는데 finalize하려는 경우
- size가 음수인 경우

### 1.3 QueryBuilder 복제 (copy/clone)

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

### 1.4 Function Score Query 지원

**현재 미지원**. ES에서 점수 커스터마이징에 필수적.

**제안**:
```python
class FunctionScoreQuery:
    @staticmethod
    def build(
        query: Dict,
        functions: List[Dict],
        score_mode: str = "multiply",
        boost_mode: str = "multiply",
        max_boost: Optional[float] = None,
        min_score: Optional[float] = None
    ) -> Dict:
        ...

# 사용 예
QueryBuilder.FunctionScore.build(
    query=QueryBuilder.MatchAll.build(),
    functions=[
        {"filter": {"term": {"featured": True}}, "weight": 10},
        {"field_value_factor": {"field": "popularity", "modifier": "log1p"}}
    ],
    score_mode="sum"
)
```

### 1.5 Multi-Match Query 지원

**현재 미지원**. 여러 필드에 동시 검색할 때 MatchQuery를 dis_max로 조합해야 함.

**제안**:
```python
class MultiMatchQuery:
    @staticmethod
    def build(
        query: str,
        fields: List[str],
        type: Optional[str] = None,       # best_fields, most_fields, cross_fields, phrase, phrase_prefix
        operator: Optional[str] = None,
        minimum_should_match: Optional[str] = None,
        tie_breaker: Optional[float] = None,
        analyzer: Optional[str] = None,
        boost: Optional[float] = None,
        fuzziness: Optional[str] = None
    ) -> Dict:
        ...
```

---

## P2: 중간 우선순위 (편의성 향상)

### 2.1 Highlight 지원

```python
class HighlightBuilder:
    def add_field(self, field: str, **options) -> 'HighlightBuilder': ...
    def set_pre_tags(self, *tags: str) -> 'HighlightBuilder': ...
    def set_post_tags(self, *tags: str) -> 'HighlightBuilder': ...
    def set_type(self, type: str) -> 'HighlightBuilder': ...  # unified, plain, fvh
    def build(self) -> Dict: ...

# QueryBuilder에 통합
qb.set_highlight(
    HighlightBuilder()
        .add_field("title", number_of_fragments=3)
        .add_field("content")
        .set_pre_tags("<em>")
        .set_post_tags("</em>")
)
```

### 2.2 Script Query / Script Field 지원

```python
class ScriptQuery:
    @staticmethod
    def build(source: str, lang: str = "painless", params: Optional[Dict] = None) -> Dict:
        ...

class ScriptField:
    @staticmethod
    def build(field_name: str, source: str, lang: str = "painless", params: Optional[Dict] = None) -> Dict:
        ...

# QueryBuilder에 통합
qb.add_script_field("calculated_price", "doc['price'].value * params.rate", params={"rate": 1.1})
```

### 2.3 Search After (커서 기반 페이징)

```python
qb.set_search_after([1609459200000, "doc_id_123"])
```

기존 `set_from`으로는 deep pagination이 비효율적. `search_after`로 커서 기반 페이징 지원.

### 2.4 Collapse (필드 그룹핑)

```python
qb.set_collapse("applicant_id")
# 또는
qb.set_collapse("applicant_id", inner_hits={"name": "latest", "size": 3, "sort": [{"date": "desc"}]})
```

### 2.5 Suggest (자동완성/오타교정)

```python
class SuggestBuilder:
    def add_term_suggest(self, name, field, text, **options) -> 'SuggestBuilder': ...
    def add_phrase_suggest(self, name, field, text, **options) -> 'SuggestBuilder': ...
    def add_completion_suggest(self, name, field, prefix, **options) -> 'SuggestBuilder': ...
    def build(self) -> Dict: ...
```

### 2.6 Pipeline Aggregation 지원

현재 bucket/metric agg만 지원. pipeline agg 추가:

```python
class BucketSortAggregation:
    @staticmethod
    def build(sort: List[Dict], size: Optional[int] = None, from_: Optional[int] = None) -> Dict: ...

class BucketSelectorAggregation:
    @staticmethod
    def build(buckets_path: Dict[str, str], script: str) -> Dict: ...

class DerivativeAggregation:
    @staticmethod
    def build(buckets_path: str) -> Dict: ...

class CumulativeSumAggregation:
    @staticmethod
    def build(buckets_path: str) -> Dict: ...
```

---

## P3: 낮은 우선순위 (확장성)

### 3.1 Geo 쿼리 지원

```python
class GeoBoundingBoxQuery:
    @staticmethod
    def build(field, top_left, bottom_right) -> Dict: ...

class GeoDistanceQuery:
    @staticmethod
    def build(field, lat, lon, distance) -> Dict: ...
```

### 3.2 Percolate Query 지원

```python
class PercolateQuery:
    @staticmethod
    def build(field, document) -> Dict: ...
```

### 3.3 Index Template / Mapping 빌더

쿼리 빌더와 별개로 인덱스 설정을 빌더 패턴으로 생성:

```python
class MappingBuilder:
    def add_keyword(self, name, **options) -> 'MappingBuilder': ...
    def add_text(self, name, analyzer=None, **options) -> 'MappingBuilder': ...
    def add_date(self, name, format=None) -> 'MappingBuilder': ...
    def add_nested(self, name, properties: 'MappingBuilder') -> 'MappingBuilder': ...
    def build(self) -> Dict: ...
```

### 3.4 Response Parser

ES 응답을 파싱하는 유틸리티:

```python
class ESResponse:
    def __init__(self, raw_response: Dict): ...

    @property
    def total(self) -> int: ...
    @property
    def hits(self) -> List[Dict]: ...
    @property
    def aggregations(self) -> Dict: ...

    def get_agg_buckets(self, name: str) -> List[Dict]: ...
    def get_agg_value(self, name: str) -> Any: ...
```

---

## 구현 로드맵

| 단계 | 내용 | 비고 |
|------|------|------|
| **Phase 1** | 기존 코드 이전 + 구조 분리 + 테스트 | 현재 기능 100% 호환 |
| **Phase 2** | P1 기능 추가 (validation, clone, function_score, multi_match) | 핵심 보완 |
| **Phase 3** | P2 기능 추가 (highlight, script, search_after, collapse, suggest, pipeline agg) | 편의성 |
| **Phase 4** | P3 기능 추가 (geo, percolate, mapping builder, response parser) | 확장 |
| **Phase 5** | PyPI 배포 + 문서화 + CI/CD | 라이브러리 공개 |
