"""Span 쿼리 패키지.

Elasticsearch의 Span 쿼리 빌더들을 제공합니다.
Span 쿼리는 토큰의 위치 정보를 활용하여 정밀한 근접 검색을 수행합니다.
"""

from elastic_query_builder.query.span.span_term import SpanTermQuery
from elastic_query_builder.query.span.span_near import SpanNearQuery

__all__ = ["SpanTermQuery", "SpanNearQuery"]
