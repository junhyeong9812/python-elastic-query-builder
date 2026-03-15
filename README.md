# elastic-query-builder

**A lightweight, zero-dependency Python library for building Elasticsearch queries using the builder pattern.**

[![PyPI version](https://badge.fury.io/py/elastic-query-builder.svg)](https://pypi.org/project/elastic-query-builder/)
[![Python](https://img.shields.io/pypi/pyversions/elastic-query-builder.svg)](https://pypi.org/project/elastic-query-builder/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/junhyeong9812/python-elastic-query-builder/actions/workflows/tests.yml/badge.svg)](https://github.com/junhyeong9812/python-elastic-query-builder/actions/workflows/tests.yml)

Build Elasticsearch queries in Python with **type safety**, **method chaining**, and **zero external dependencies**. The library generates plain `dict` output that works seamlessly with any Elasticsearch client.

---

## Features

- **Zero dependencies** -- pure Python only, no external packages required
- **Builder pattern** with a fluent, chainable API
- **Full type hints** for IDE autocomplete and static analysis
- **Comprehensive query support**:
  - Leaf queries: Bool, Term, Terms, Match, MatchPhrase, Range, Wildcard, Exists, IDs, MatchAll, MatchNone
  - Compound queries: DisMax, Nested
  - Span queries: SpanTerm, SpanNear
- **Aggregations**:
  - Bucket: Terms, DateHistogram, Histogram, Range, Filter, Filters, Nested
  - Metric: Sum, Avg, Min, Max, Stats, Cardinality, TopHits
- **Sort builder** with field sorting, score sorting, and script sorting
- **Source filtering** with includes/excludes control
- **Generates plain `dict`** -- use with `elasticsearch-py`, `opensearch-py`, or any HTTP client

---

## Installation

```bash
pip install elastic-query-builder
```

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

## Usage Examples

### Basic Search

```python
from elastic_query_builder import QueryBuilder

qb = QueryBuilder()
query = (
    qb.add_must(QueryBuilder.Match.build("title", "검색어", operator="and"))
      .add_filter(QueryBuilder.Range.build("date", gte="2024-01-01"))
      .set_size(10)
      .build()
)
```

### Leaf Queries (Standalone)

Each query type can be used independently to generate its corresponding ES query dict:

```python
from elastic_query_builder.query.leaf import TermQuery, MatchQuery, RangeQuery

# Term query
term = TermQuery.build("status", "active")
# {"term": {"status": {"value": "active"}}}

# Match query with options
match = MatchQuery.build("title", "search terms", boost=2.0, operator="and")
# {"match": {"title": {"query": "search terms", "boost": 2.0, "operator": "and"}}}

# Range query
range_q = RangeQuery.build("price", gte=100, lte=500)
# {"range": {"price": {"gte": 100, "lte": 500}}}
```

### Bool Query with Nested Bool

```python
from elastic_query_builder import QueryBuilder

qb = QueryBuilder()

# Create an inner bool query
inner_bool = qb.nested_bool()
inner_bool.add_should(QueryBuilder.Match.build("title", "keyword"))
inner_bool.add_should(QueryBuilder.Match.build("content", "keyword"))
inner_bool.add_minimum_should_match(1)

# Nest it inside the outer bool query
query = (
    qb.add_must(inner_bool.build())
      .add_filter(QueryBuilder.Term.build("status", "published"))
      .set_size(20)
      .build()
)
```

### Aggregations

**Basic aggregations:**

```python
qb = QueryBuilder()
query = (
    qb.set_match_all()
      .set_size(0)
      .add_terms_agg("status_count", "status", size=10)
      .add_date_histogram_agg("monthly", "created_at", calendar_interval="1M")
      .build()
)
```

**Nested aggregations:**

```python
qb = QueryBuilder()

sub_agg = qb.nested_agg()
sub_agg.add_terms("item_names", "items.name", size=5)

query = (
    qb.set_match_all()
      .set_size(0)
      .add_nested_agg("items_agg", "items", sub_agg.build())
      .build()
)
```

### Sorting

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

### Source Filtering

```python
qb = QueryBuilder()

# Include specific fields only
query = qb.set_match_all().set_source_includes(["title", "date"]).build()

# Add excludes
query = qb.set_match_all().add_source_excludes("content", "metadata").build()

# Disable _source entirely
query = qb.set_match_all().set_source(False).build()
```

### Span Queries (Proximity Search)

```python
qb = QueryBuilder()
query = (
    qb.add_must(
        QueryBuilder.SpanNear.build(
            clauses=[
                QueryBuilder.SpanTerm.build("content", "artificial"),
                QueryBuilder.SpanTerm.build("content", "intelligence"),
            ],
            slop=3,
            in_order=True
        )
    )
    .build()
)
```

### Real-World Example: Patent Search

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

## API Reference

For full API documentation, see the [`docs/`](docs/) folder:

- [Architecture](docs/01-architecture.md) -- layered architecture and design principles
- [Class Design](docs/02-class-design.md) -- detailed class specifications
- [API Reference](docs/03-api-reference.md) -- usage examples for every feature
- [Proposals](docs/04-proposals.md) -- future feature proposals

---

## Architecture

The library follows a **layered architecture** with clear domain separation:

```
elastic_query_builder/
├── core/                  # Enums (SortOrder, SortMissing, BoolClause) and type aliases
├── query/                 # Search Query domain
│   ├── leaf/              #   Term, Match, Range, Wildcard, Exists, IDs, MatchAll, MatchNone
│   ├── compound/          #   BoolQueryBuilder, DisMaxQuery
│   ├── span/              #   SpanTermQuery, SpanNearQuery
│   └── nested.py          #   NestedQuery
├── aggregation/           # Aggregation domain
│   ├── bucket/            #   Terms, DateHistogram, Histogram, Range, Filter, Filters, Nested
│   ├── metric/            #   Sum, Avg, Min, Max, Stats, Cardinality, TopHits
│   └── aggregation_builder.py
├── sort/                  # Sort domain (SortBuilder)
└── builder.py             # QueryBuilder -- top-level integration builder
```

**Design principles:**

1. Each query class is responsible for generating only its own ES query (single responsibility)
2. `build()` always returns `Dict[str, Any]` (consistent interface)
3. Builder methods return `self` to support method chaining
4. `None` values are excluded from generated queries (clean output)
5. No external dependencies -- pure Python only

---

## Contributing

Contributions are welcome! Here is how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`pytest`)
5. Commit your changes (`git commit -m "Add my feature"`)
6. Push to your branch (`git push origin feature/my-feature`)
7. Open a Pull Request

Please make sure to:
- Follow the existing code style
- Add type hints to all public methods
- Include tests for new functionality
- Update documentation as needed

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
