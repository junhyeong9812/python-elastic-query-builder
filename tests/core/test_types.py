from elastic_query_builder.core.types import ESQuery, ESAggregation, ESSort

"""core/types.py에 대한 단위 테스트.

타입 별칭이 올바르게 정의되었는지 확인합니다.
"""
class TestTypeAliases:
    """타입 별칭 정의 테스트."""

    def test_es_query_type_exists(self):
        """ESQuery 타입 별칭이 존재하는지 확인합니다."""
        assert ESQuery is not None

    def test_es_aggregation_type_exists(self):
        """ESAggregation 타입 별칭이 존재하는지 확인합니다."""
        assert ESAggregation is not None

    def test_es_sort_type_exists(self):
        """ESSort 타입 별칭이 존재하는지 확인합니다."""
        assert ESSort is not None

    def test_es_query_accepts_dict(self):
        """ESQuery 타입이 딕셔너리를 허용하는지 확인합니다."""
        query: ESQuery = {"match": {"title": "test"}}
        assert isinstance(query, dict)

    def test_es_aggregation_accepts_dict(self):
        """ESAggregation 타입이 딕셔너리를 허용하는지 확인합니다."""
        agg: ESAggregation = {"terms": {"field": "status"}}
        assert isinstance(agg, dict)

    def test_es_sort_accepts_dict(self):
        """ESSort 타입이 딕셔너리를 허용하는지 확인합니다."""
        sort: ESSort = {"price": {"order": "asc"}}
        assert isinstance(sort, dict)

    def test_es_sort_accepts_list(self):
        """ESSort 타입이 리스트도 허용하는지 확인합니다."""
        sort: ESSort = [{"price": {"order": "asc"}}]
        assert isinstance(sort, list)