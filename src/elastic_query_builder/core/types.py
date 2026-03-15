from typing import Any, Dict, List, Union

"""Elasticsearch 쿼리 빌더에서 사용하는 타입 별칭 정의."""
ESQuery = Dict[str, Any]
ESAggregation = Dict[str, Any]
ESSort = Union[Dict[str, Any], List[Dict[str, Any]]]