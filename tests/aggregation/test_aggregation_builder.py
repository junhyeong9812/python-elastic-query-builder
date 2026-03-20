"""aggregation/aggregation_builder.py에 대한 단위 테스트.

AggregationBuilder가 여러 집계를 올바르게 조합하고,
최종 Elasticsearch aggs 딕셔너리를 생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.aggregation.aggregation_builder import AggregationBuilder


class TestAggregationBuilderBasic:
    """AggregationBuilder 기본 동작 테스트."""

    def test_empty_builder(self):
        """빈 AggregationBuilder가 빈 딕셔너리를 생성하는지 확인합니다."""
        builder = AggregationBuilder()
        result = builder.build()
        assert result == {}

    def test_is_empty_when_new(self):
        """새로 생성된 AggregationBuilder가 비어 있는지 확인합니다."""
        builder = AggregationBuilder()
        assert builder.is_empty() is True

    def test_is_empty_after_add(self):
        """집계를 추가한 후 is_empty가 False를 반환하는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_aggregation("test", {"terms": {"field": "status"}})
        assert builder.is_empty() is False


class TestAggregationBuilderAddAggregation:
    """AggregationBuilder.add_aggregation 테스트."""

    def test_add_aggregation(self):
        """add_aggregation으로 집계를 추가하면 올바른 딕셔너리가 생성되는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_aggregation("status_count", {"terms": {"field": "status"}})
        result = builder.build()
        expected = {
            "status_count": {"terms": {"field": "status"}}
        }
        assert result == expected

    def test_add_aggregation_with_sub_aggs(self):
        """sub_aggs 파라미터를 사용하여 하위 집계를 추가할 수 있는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_aggregation(
            "by_status",
            {"terms": {"field": "status"}},
            sub_aggs={"avg_price": {"avg": {"field": "price"}}},
        )
        result = builder.build()
        expected = {
            "by_status": {
                "terms": {"field": "status"},
                "aggs": {"avg_price": {"avg": {"field": "price"}}},
            }
        }
        assert result == expected

    def test_add_aggregation_without_sub_aggs_has_no_aggs_key(self):
        """sub_aggs를 지정하지 않으면 결과에 aggs 키가 없는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_aggregation("test", {"terms": {"field": "status"}})
        result = builder.build()
        assert "aggs" not in result["test"]

    def test_add_aggregation_preserves_original_body(self):
        """add_aggregation이 원본 딕셔너리를 변경하지 않는지 확인합니다."""
        original = {"terms": {"field": "status"}}
        builder = AggregationBuilder()
        builder.add_aggregation("test", original, sub_aggs={"sub": {"avg": {"field": "x"}}})
        assert "aggs" not in original


class TestAggregationBuilderConvenienceMethods:
    """AggregationBuilder 편의 메서드 테스트."""

    def test_add_terms(self):
        """add_terms 편의 메서드가 올바른 terms 집계를 생성하는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_terms("by_status", "status", size=10)
        result = builder.build()
        expected = {
            "by_status": {"terms": {"field": "status", "size": 10}}
        }
        assert result == expected

    def test_add_terms_without_size(self):
        """size 없이 add_terms를 호출하면 size 키가 없는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_terms("by_status", "status")
        result = builder.build()
        expected = {
            "by_status": {"terms": {"field": "status"}}
        }
        assert result == expected

    def test_add_terms_with_order(self):
        """add_terms에 order 옵션을 지정할 수 있는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_terms("by_status", "status", order={"_count": "desc"})
        result = builder.build()
        expected = {
            "by_status": {"terms": {"field": "status", "order": {"_count": "desc"}}}
        }
        assert result == expected

    def test_add_date_histogram(self):
        """add_date_histogram 편의 메서드가 올바른 date_histogram 집계를 생성하는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_date_histogram("monthly", "date", calendar_interval="1M")
        result = builder.build()
        expected = {
            "monthly": {
                "date_histogram": {
                    "field": "date",
                    "calendar_interval": "1M",
                }
            }
        }
        assert result == expected

    def test_add_date_histogram_with_all_options(self):
        """add_date_histogram에 모든 옵션을 지정할 수 있는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_date_histogram(
            "daily",
            "created_at",
            calendar_interval="1d",
            format="yyyy-MM-dd",
            time_zone="Asia/Seoul",
            min_doc_count=0,
            extended_bounds={"min": "2024-01-01", "max": "2024-12-31"},
        )
        result = builder.build()
        expected = {
            "daily": {
                "date_histogram": {
                    "field": "created_at",
                    "calendar_interval": "1d",
                    "format": "yyyy-MM-dd",
                    "time_zone": "Asia/Seoul",
                    "min_doc_count": 0,
                    "extended_bounds": {"min": "2024-01-01", "max": "2024-12-31"},
                }
            }
        }
        assert result == expected

    def test_add_date_histogram_fixed_interval(self):
        """add_date_histogram에 fixed_interval을 사용할 수 있는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_date_histogram("hourly", "timestamp", fixed_interval="1h")
        result = builder.build()
        expected = {
            "hourly": {
                "date_histogram": {
                    "field": "timestamp",
                    "fixed_interval": "1h",
                }
            }
        }
        assert result == expected

    def test_add_cardinality(self):
        """add_cardinality 편의 메서드가 올바른 cardinality 집계를 생성하는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_cardinality("unique_users", "user_id", precision_threshold=100)
        result = builder.build()
        expected = {
            "unique_users": {
                "cardinality": {
                    "field": "user_id",
                    "precision_threshold": 100,
                }
            }
        }
        assert result == expected

    def test_add_cardinality_without_precision(self):
        """precision_threshold 없이 add_cardinality를 호출할 수 있는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_cardinality("unique_users", "user_id")
        result = builder.build()
        expected = {
            "unique_users": {"cardinality": {"field": "user_id"}}
        }
        assert result == expected

    def test_add_stats(self):
        """add_stats 편의 메서드가 올바른 stats 집계를 생성하는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_stats("price_stats", "price")
        result = builder.build()
        expected = {
            "price_stats": {"stats": {"field": "price"}}
        }
        assert result == expected

    def test_add_stats_with_missing(self):
        """add_stats에 missing 옵션을 지정할 수 있는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_stats("price_stats", "price", missing=0)
        result = builder.build()
        expected = {
            "price_stats": {"stats": {"field": "price", "missing": 0}}
        }
        assert result == expected

    def test_add_nested_aggregation(self):
        """add_nested_aggregation 편의 메서드가 올바른 nested 집계를 생성하는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_nested_aggregation(
            "items",
            "items",
            sub_aggs={"item_names": {"terms": {"field": "items.name"}}},
        )
        result = builder.build()
        expected = {
            "items": {
                "nested": {"path": "items"},
                "aggs": {"item_names": {"terms": {"field": "items.name"}}},
            }
        }
        assert result == expected

    def test_add_nested_aggregation_with_multiple_sub_aggs(self):
        """add_nested_aggregation에 여러 하위 집계를 지정할 수 있는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_nested_aggregation(
            "items",
            "items",
            sub_aggs={
                "item_names": {"terms": {"field": "items.name"}},
                "avg_qty": {"avg": {"field": "items.quantity"}},
            },
        )
        result = builder.build()
        assert "items" in result
        assert "aggs" in result["items"]
        assert "item_names" in result["items"]["aggs"]
        assert "avg_qty" in result["items"]["aggs"]


class TestAggregationBuilderMultiple:
    """AggregationBuilder 복수 집계 조합 테스트."""

    def test_multiple_aggregations(self):
        """여러 집계를 추가하면 모두 포함된 딕셔너리가 생성되는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_terms("by_status", "status", size=10)
        builder.add_cardinality("unique_users", "user_id")
        builder.add_stats("price_stats", "price")
        result = builder.build()

        assert "by_status" in result
        assert "unique_users" in result
        assert "price_stats" in result
        assert result["by_status"] == {"terms": {"field": "status", "size": 10}}
        assert result["unique_users"] == {"cardinality": {"field": "user_id"}}
        assert result["price_stats"] == {"stats": {"field": "price"}}

    def test_multiple_aggregations_count(self):
        """여러 집계를 추가한 후 결과에 정확한 개수의 키가 있는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_terms("agg1", "field1")
        builder.add_terms("agg2", "field2")
        builder.add_stats("agg3", "field3")
        result = builder.build()
        assert len(result) == 3

    def test_overwrite_same_name(self):
        """같은 이름으로 집계를 추가하면 나중 것이 덮어쓰는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_terms("my_agg", "field1")
        builder.add_stats("my_agg", "field2")
        result = builder.build()
        assert len(result) == 1
        assert "stats" in result["my_agg"]


class TestAggregationBuilderChaining:
    """AggregationBuilder 메서드 체이닝 테스트."""

    def test_add_aggregation_returns_self(self):
        """add_aggregation이 self를 반환하여 체이닝이 가능한지 확인합니다."""
        builder = AggregationBuilder()
        returned = builder.add_aggregation("test", {"terms": {"field": "x"}})
        assert returned is builder

    def test_add_terms_returns_self(self):
        """add_terms가 self를 반환하여 체이닝이 가능한지 확인합니다."""
        builder = AggregationBuilder()
        returned = builder.add_terms("test", "field")
        assert returned is builder

    def test_add_date_histogram_returns_self(self):
        """add_date_histogram이 self를 반환하여 체이닝이 가능한지 확인합니다."""
        builder = AggregationBuilder()
        returned = builder.add_date_histogram("test", "field")
        assert returned is builder

    def test_add_cardinality_returns_self(self):
        """add_cardinality가 self를 반환하여 체이닝이 가능한지 확인합니다."""
        builder = AggregationBuilder()
        returned = builder.add_cardinality("test", "field")
        assert returned is builder

    def test_add_stats_returns_self(self):
        """add_stats가 self를 반환하여 체이닝이 가능한지 확인합니다."""
        builder = AggregationBuilder()
        returned = builder.add_stats("test", "field")
        assert returned is builder

    def test_add_nested_aggregation_returns_self(self):
        """add_nested_aggregation이 self를 반환하여 체이닝이 가능한지 확인합니다."""
        builder = AggregationBuilder()
        returned = builder.add_nested_aggregation("test", "path", sub_aggs={})
        assert returned is builder

    def test_full_chaining(self):
        """모든 편의 메서드를 체이닝으로 사용할 수 있는지 확인합니다."""
        result = (
            AggregationBuilder()
            .add_terms("by_status", "status", size=10)
            .add_date_histogram("monthly", "date", calendar_interval="1M")
            .add_cardinality("unique_users", "user_id")
            .add_stats("price_stats", "price")
            .build()
        )
        assert len(result) == 4
        assert "by_status" in result
        assert "monthly" in result
        assert "unique_users" in result
        assert "price_stats" in result


class TestAggregationBuilderBuildImmutability:
    """AggregationBuilder.build()의 불변성 테스트."""

    def test_build_returns_copy(self):
        """build()가 내부 상태의 복사본을 반환하는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_terms("by_status", "status")
        result1 = builder.build()
        result2 = builder.build()
        assert result1 == result2
        assert result1 is not result2

    def test_modifying_build_result_does_not_affect_builder(self):
        """build() 결과를 수정해도 빌더 내부 상태에 영향이 없는지 확인합니다."""
        builder = AggregationBuilder()
        builder.add_terms("by_status", "status")
        result = builder.build()
        result["extra"] = {"terms": {"field": "extra"}}
        assert "extra" not in builder.build()
