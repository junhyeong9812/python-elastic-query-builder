"""KNN 검색에 대한 단위 테스트.

QueryBuilder의 set_knn 메서드와 build 출력을 검증합니다.
"""

import pytest
from elastic_query_builder.builder import QueryBuilder


class TestKnn:
    """KNN 검색 테스트."""

    def test_basic_knn(self):
        """기본 KNN 검색을 설정할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .set_knn("embedding", [0.1, 0.2, 0.3], k=10, num_candidates=100)
            .build()
        )
        assert result["knn"] == {
            "field": "embedding",
            "query_vector": [0.1, 0.2, 0.3],
            "k": 10,
            "num_candidates": 100,
        }

    def test_knn_with_filter(self):
        """KNN 검색에 filter를 지정할 수 있는지 확인합니다."""
        filter_q = {"term": {"status": {"value": "published"}}}
        result = (
            QueryBuilder()
            .set_knn("embedding", [0.1, 0.2], k=5, num_candidates=50, filter=filter_q)
            .build()
        )
        assert result["knn"]["filter"] == filter_q

    def test_knn_with_similarity(self):
        """KNN 검색에 similarity를 지정할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .set_knn("embedding", [0.1], k=10, num_candidates=100, similarity=0.8)
            .build()
        )
        assert result["knn"]["similarity"] == 0.8

    def test_knn_with_boost(self):
        """KNN 검색에 boost를 지정할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .set_knn("embedding", [0.1], k=10, num_candidates=100, boost=1.5)
            .build()
        )
        assert result["knn"]["boost"] == 1.5

    def test_knn_in_build_output(self):
        """KNN과 다른 쿼리를 함께 사용할 수 있는지 확인합니다."""
        result = (
            QueryBuilder()
            .set_match_all()
            .set_knn("embedding", [0.1, 0.2], k=10, num_candidates=100)
            .set_size(20)
            .build()
        )
        assert "query" in result
        assert "knn" in result
        assert result["size"] == 20
        assert result["knn"]["field"] == "embedding"

    def test_no_knn_when_not_set(self):
        """KNN을 설정하지 않으면 build 결과에 knn이 없는지 확인합니다."""
        result = QueryBuilder().set_size(10).build()
        assert "knn" not in result

    def test_set_knn_returns_self(self):
        """set_knn이 self를 반환하는지 확인합니다."""
        builder = QueryBuilder()
        assert builder.set_knn("embedding", [0.1], k=10, num_candidates=100) is builder
