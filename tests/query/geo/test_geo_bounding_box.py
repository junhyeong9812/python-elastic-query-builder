"""GeoBoundingBoxQuery에 대한 단위 테스트."""

import pytest
from elastic_query_builder.query.geo.geo_bounding_box import GeoBoundingBoxQuery


class TestGeoBoundingBoxQuery:
    """GeoBoundingBoxQuery 빌드 테스트."""

    def test_build_basic(self):
        """기본 geo_bounding_box 쿼리를 생성할 수 있는지 확인합니다."""
        result = GeoBoundingBoxQuery.build(
            "location",
            top_left={"lat": 40.73, "lon": -74.1},
            bottom_right={"lat": 40.01, "lon": -71.12},
        )
        assert result == {
            "geo_bounding_box": {
                "location": {
                    "top_left": {"lat": 40.73, "lon": -74.1},
                    "bottom_right": {"lat": 40.01, "lon": -71.12},
                }
            }
        }

    def test_build_with_validation_method(self):
        """validation_method 옵션을 지정할 수 있는지 확인합니다."""
        result = GeoBoundingBoxQuery.build(
            "location",
            top_left={"lat": 40.73, "lon": -74.1},
            bottom_right={"lat": 40.01, "lon": -71.12},
            validation_method="COERCE",
        )
        assert result["geo_bounding_box"]["validation_method"] == "COERCE"

    def test_build_with_boost(self):
        """boost 옵션을 지정할 수 있는지 확인합니다."""
        result = GeoBoundingBoxQuery.build(
            "location",
            top_left={"lat": 40.73, "lon": -74.1},
            bottom_right={"lat": 40.01, "lon": -71.12},
            boost=2.0,
        )
        assert result["geo_bounding_box"]["boost"] == 2.0

    def test_build_no_optional(self):
        """선택 옵션 없이 빌드하면 해당 키가 없는지 확인합니다."""
        result = GeoBoundingBoxQuery.build(
            "location",
            top_left=[40.73, -74.1],
            bottom_right=[40.01, -71.12],
        )
        body = result["geo_bounding_box"]
        assert "validation_method" not in body
        assert "boost" not in body
        assert body["location"]["top_left"] == [40.73, -74.1]
