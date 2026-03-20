"""elastic_query_builder — Python Elasticsearch Query Builder.

Elasticsearch 검색 요청을 타입 안전하고 메서드 체이닝 방식으로
구성할 수 있는 라이브러리입니다.

기본 사용 예시::

    from elastic_query_builder import QueryBuilder, SortOrder

    result = (
        QueryBuilder()
        .add_must(QueryBuilder.Match.build("title", "검색어"))
        .add_filter(QueryBuilder.Range.build("date", gte="2024-01-01"))
        .set_size(10)
        .add_sort("date", SortOrder.DESC)
        .build()
    )
"""

from elastic_query_builder.builder import QueryBuilder
from elastic_query_builder.core.enums import SortOrder, SortMissing, BoolClause
from elastic_query_builder.query.compound.bool_query import BoolQueryBuilder
from elastic_query_builder.aggregation.aggregation_builder import AggregationBuilder
from elastic_query_builder.sort.sort_builder import SortBuilder

__all__ = [
    "QueryBuilder",
    "SortOrder", "SortMissing", "BoolClause",
    "BoolQueryBuilder", "AggregationBuilder", "SortBuilder",
]
