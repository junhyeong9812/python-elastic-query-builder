# elastic-query-builder

**Build Elasticsearch queries you can actually read.**

[![PyPI version](https://badge.fury.io/py/elastic-query-builder.svg)](https://pypi.org/project/elastic-query-builder/)
[![Python](https://img.shields.io/pypi/pyversions/elastic-query-builder.svg)](https://pypi.org/project/elastic-query-builder/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/junhyeong9812/python-elastic-query-builder/actions/workflows/tests.yml/badge.svg)](https://github.com/junhyeong9812/python-elastic-query-builder/actions/workflows/tests.yml)

A lightweight, zero-dependency Python library that brings Java's `QueryBuilders` pattern to Python. Method chaining, explicit bool clause control, and plain `dict` output — no magic, no hidden abstractions.

---

## Why This Exists

The official `elasticsearch-dsl` library wraps Elasticsearch queries in its own abstraction layer. That works fine for simple queries:

```python
# elasticsearch-dsl — clean enough for simple cases
s = Search().query("match", title="python").filter("term", status="active")
```

But real-world queries aren't simple. When you need nested bool queries with mixed `must`, `should`, `filter`, and `minimum_should_match`, `dsl` forces you into deeply nested constructor calls:

```python
# elasticsearch-dsl — a realistic query
s = Search()
s = s.query(
    Q('bool',
        must=[
            Q('match', title={'query': 'semiconductor', 'operator': 'and'}),
            Q('bool',
                should=[
                    Q('match', content='LED'),
                    Q('match_phrase', abstract='light emitting diode'),
                ],
                minimum_should_match=1
            ),
        ],
        filter=[
            Q('range', application_date={'gte': '20200101', 'lte': '20241231'}),
            Q('term', status_code='registered'),
        ],
        must_not=[Q('term', applicant_name='test')]
    )
)
```

At this point, `Q()` wrappers are just noise. You have to mentally parse the nesting to figure out what's in `must` vs `filter` vs `should`. It's no better than writing raw `dict` — arguably worse, because the abstraction hides the actual Elasticsearch structure behind it.

**This library takes the opposite approach.** Instead of abstracting away the ES query DSL, it mirrors it directly with explicit, chainable methods:

```python
# elastic-query-builder — same query
qb = QueryBuilder()

inner = qb.nested_bool()
inner.add_should(QueryBuilder.Match.build("content", "LED"))
inner.add_should(QueryBuilder.MatchPhrase.build("abstract", "light emitting diode"))
inner.add_minimum_should_match(1)

query = (
    qb.add_must(QueryBuilder.Match.build("title", "semiconductor", operator="and"))
      .add_must(inner.build())
      .add_filter(QueryBuilder.Range.build("application_date", gte="20200101", lte="20241231"))
      .add_filter(QueryBuilder.Term.build("status_code", "registered"))
      .add_must_not(QueryBuilder.Term.build("applicant_name", "test"))
      .build()
)
```

Every line tells you exactly what it does. `add_must` goes to `must`. `add_filter` goes to `filter`. No guessing, no digging through source code to understand where your clause ends up.

**This matters for code review.** Whether you wrote the query, a teammate wrote it, or an LLM generated it — someone has to verify it does what it's supposed to. Readable structure makes that verification fast.

---

## Installation

```bash
pip install elastic-query-builder
```

Zero dependencies. Works with `elasticsearch-py`, `opensearch-py`, or any HTTP client — `build()` returns a plain `dict`.

---

## Quick Start

```python
from elastic_query_builder import QueryBuilder

qb = QueryBuilder()
query = (
    qb.add_must(QueryBuilder.Match.build("title", "elasticsearch"))
      .add_filter(QueryBuilder.Range.build("date", gte="2024-01-01"))
      .set_size(10)
      .build()
)

# Use with any ES client
# es.search(index="my-index", body=query)
```

---

## Real-World Example: Patent Search

```python
from elastic_query_builder import QueryBuilder
from elastic_query_builder.core.enums import SortOrder

qb = QueryBuilder()

# Search conditions
qb.add_must(QueryBuilder.Match.build("productKor", "반도체", operator="and"))
qb.add_must(QueryBuilder.Match.build("abstract", "발광 다이오드", boost=2.0))

# Filters
qb.add_filter(QueryBuilder.Range.build("applicationDate", gte="20200101", lte="20241231"))
qb.add_filter(QueryBuilder.Term.build("statusCode", "registered"))

# Exclusions
qb.add_must_not(QueryBuilder.Term.build("applicantName", "테스트"))

# Sort + Pagination
qb.add_sort("applicationDate", SortOrder.DESC)
qb.set_size(20)
qb.set_from(0)
qb.set_track_total_hits(True)

# Source filtering
qb.set_source_includes(["applicationNumber", "productKor", "applicantName", "applicationDate"])

query = qb.build()
```

---

## What It Supports

**Queries** — Bool, Term, Terms, Match, MatchPhrase, Range, Wildcard, Exists, IDs, MatchAll, MatchNone, DisMax, Nested, SpanTerm, SpanNear

**Aggregations** — Terms, DateHistogram, Histogram, Range, Filter, Filters, Nested (bucket) / Sum, Avg, Min, Max, Stats, Cardinality, TopHits (metric)

**Sort** — Field sorting, score sorting, script sorting, missing value handling

**Source filtering** — Includes/excludes control, full disable

**Output** — Plain `dict`. No vendor lock-in.

For full API documentation with examples, see the [`docs/`](docs/) folder.

---

## Design Principles

1. **Explicit over implicit** — method names map directly to ES bool clauses (`add_must`, `add_filter`, `add_should`, `add_must_not`)
2. **`build()` returns `Dict[str, Any]`** — predictable, inspectable, serializable
3. **Method chaining via `return self`** — fluent API without sacrificing readability
4. **Zero dependencies** — pure Python, no transitive dependency risks
5. **Each query class owns its own output** — single responsibility, easy to extend

---

## Contributing

Contributions are welcome. Fork, branch, write tests, open a PR. See [`docs/`](docs/) for architecture details.

## License

MIT — see [LICENSE](LICENSE).
