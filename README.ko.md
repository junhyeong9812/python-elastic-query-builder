# elastic-query-builder

**읽을 수 있는 Elasticsearch 쿼리를 만드세요.**

[![PyPI version](https://badge.fury.io/py/elastic-query-builder.svg)](https://pypi.org/project/elastic-query-builder/)
[![Python version](https://img.shields.io/pypi/pyversions/elastic-query-builder.svg)](https://pypi.org/project/elastic-query-builder/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Java의 `QueryBuilders` 패턴을 Python에 그대로 가져온 경량 라이브러리입니다. 메서드 체이닝, 명시적인 bool clause 제어, 그리고 plain `dict` 출력 — 마법도 없고, 숨겨진 추상화도 없습니다.

---

## 왜 만들었나

### raw dict의 고통

Python에서 ES 쿼리를 짜면 보통 이렇게 시작합니다:

```python
query = {"query": {"bool": {"must": [], "filter": []}}}

if keyword:
    query["query"]["bool"]["must"].append(
        {"match": {"title": {"query": keyword, "operator": "and"}}}
    )

if date_from or date_to:
    range_q = {"range": {"date": {}}}
    if date_from:
        range_q["range"]["date"]["gte"] = date_from
    if date_to:
        range_q["range"]["date"]["lte"] = date_to
    query["query"]["bool"]["filter"].append(range_q)

if status:
    query["query"]["bool"]["filter"].append(
        {"term": {"status": status}}
    )

if exclude_test:
    query["query"]["bool"].setdefault("must_not", []).append(
        {"term": {"applicant": "테스트"}}
    )

query["size"] = 20
query["sort"] = [{"date": {"order": "desc"}}]
```

동적 조건이 10~20개쯤 되면 이건 읽을 수가 없어요. 대괄호 중첩, `setdefault` 호출, 수동 list append — 리뷰하기 어렵고, 실수하기 쉽습니다.

### elasticsearch-dsl의 접근

공식 `elasticsearch-dsl`은 이걸 자체 추상화로 감쌉니다. 간단한 경우엔 깔끔해요:

```python
s = Search().query("match", title="python").filter("term", status="active")
```

하지만 nested bool에 여러 clause가 섞이면 깊은 생성자 중첩을 강제합니다:

```python
s = Search()
s = s.query(
    Q('bool',
        must=[
            Q('match', title={'query': '반도체', 'operator': 'and'}),
            Q('bool',
                should=[
                    Q('match', content='LED'),
                    Q('match_phrase', abstract='발광 다이오드'),
                ],
                minimum_should_match=1
            ),
        ],
        filter=[
            Q('range', application_date={'gte': '20200101', 'lte': '20241231'}),
            Q('term', status_code='registered'),
        ],
        must_not=[Q('term', applicant_name='테스트')]
    )
)
```

`Q()` 래퍼가 노이즈가 됩니다. 중첩을 머릿속으로 펼쳐야 뭐가 `must`에 있고 뭐가 `filter`에 있는지 알 수 있어요. 추상화가 ES 구조를 명확하게 만드는 게 아니라 오히려 가리고 있습니다.

### 이 라이브러리의 접근

ES의 Query DSL 구조를 그대로 — JSON 중첩 대신 Python 메서드 체이닝으로 표현한다고 생각하면 됩니다:

```python
qb = QueryBuilder()

inner = qb.nested_bool()
inner.add_should(QueryBuilder.Match.build("content", "LED"))
inner.add_should(QueryBuilder.MatchPhrase.build("abstract", "발광 다이오드"))
inner.add_minimum_should_match(1)

query = (
    qb.add_must(QueryBuilder.Match.build("title", "반도체", operator="and"))
      .add_must(inner.build())
      .add_filter(QueryBuilder.Range.build("application_date", gte="20200101", lte="20241231"))
      .add_filter(QueryBuilder.Term.build("status_code", "registered"))
      .add_must_not(QueryBuilder.Term.build("applicant_name", "테스트"))
      .build()
)
```

각 줄이 정확히 무엇을 하는지 보입니다. `add_must`는 `must`로, `add_filter`는 `filter`로. 이미 알고 있는 ES Query DSL 구조가 코드에 그대로 드러납니다.

그리고 동적 조건 조합도 깔끔합니다:

```python
qb = QueryBuilder()

if keyword:
    qb.add_must(QueryBuilder.Match.build("title", keyword, operator="and"))

if date_from or date_to:
    qb.add_filter(QueryBuilder.Range.build("date", gte=date_from, lte=date_to))

if status:
    qb.add_filter(QueryBuilder.Term.build("status", status))

if exclude_test:
    qb.add_must_not(QueryBuilder.Term.build("applicant", "테스트"))

query = qb.build()
```

대괄호 지옥도 없고, `setdefault`도 없고, 수동 list 관리도 없습니다. 조건을 추가하고 build하면 끝.

**코드 리뷰할 때 이게 중요합니다.** 본인이 짠 쿼리든, 동료가 짠 거든, LLM이 생성한 거든 — 누군가는 의도대로 동작하는지 검증해야 합니다. 읽기 쉬운 구조는 그 검증을 빠르게 만들어줍니다.

---

## 설치

```bash
pip install elastic-query-builder
```

외부 의존성 없음. `elasticsearch-py`, `opensearch-py`, 또는 어떤 HTTP 클라이언트와도 사용 가능 — `build()`는 plain `dict`를 반환합니다.

---

## 빠른 시작

```python
from elastic_query_builder import QueryBuilder

qb = QueryBuilder()
query = (
    qb.add_must(QueryBuilder.Match.build("title", "elasticsearch"))
      .add_filter(QueryBuilder.Range.build("date", gte="2024-01-01"))
      .set_size(10)
      .build()
)

# 아무 ES 클라이언트에 바로 전달
# es.search(index="my-index", body=query)
```

---

## 실전 예시: 특허 검색

```python
from elastic_query_builder import QueryBuilder
from elastic_query_builder.core.enums import SortOrder

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

# 소스 필터링
qb.set_source_includes(["applicationNumber", "productKor", "applicantName", "applicationDate"])

query = qb.build()
```

---

## 지원 범위

**쿼리** — Bool, Term, Terms, Match, MatchPhrase, Range, Wildcard, Exists, IDs, MatchAll, MatchNone, DisMax, Nested, SpanTerm, SpanNear

**집계** — Terms, DateHistogram, Histogram, Range, Filter, Filters, Nested (버킷) / Sum, Avg, Min, Max, Stats, Cardinality, TopHits (메트릭)

**정렬** — 필드 정렬, 스코어 정렬, 스크립트 정렬, missing 값 처리

**소스 필터링** — includes/excludes 제어, 완전 비활성화

**출력** — plain `dict`. 벤더 종속 없음.

전체 API 문서와 예제는 [`docs/`](docs/) 폴더를 참고하세요.

---

## 설계 원칙

1. **명시적이 암시적보다 낫다** — 메서드 이름이 ES bool clause에 직접 대응 (`add_must`, `add_filter`, `add_should`, `add_must_not`)
2. **`build()`는 `Dict[str, Any]`를 반환** — 예측 가능하고, 검사 가능하고, 직렬화 가능
3. **`return self`로 메서드 체이닝** — 가독성을 해치지 않는 fluent API
4. **외부 의존성 제로** — 순수 Python, 전이 의존성 리스크 없음
5. **각 쿼리 클래스가 자기 출력을 책임** — 단일 책임, 확장 용이

---

## 기여하기

기여를 환영합니다. Fork → 브랜치 → 테스트 작성 → PR. 아키텍처 상세는 [`docs/`](docs/)를 참고하세요.

## 라이선스

MIT — [LICENSE](LICENSE) 참고.
