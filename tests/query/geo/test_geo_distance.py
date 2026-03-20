"""GeoDistanceQuery에 대한 단위 테스트."""

import pytest
from elastic_query_builder.query.geo.geo_distance import GeoDistanceQuery


class TestGeoDistanceQuery:
    """GeoDistanceQuery 빌드 테스트."""

    def test_build_with_dict_point(self):
        """딕셔너리 형태의 좌표로 geo_distance 쿼리를 생성할 수 있는지 확인합니다."""
        result = GeoDistanceQuery.build(
            "location", {"lat": 40.73, "lon": -73.93}, "200km"
        )
        assert result == {
            "geo_distance": {
                "distance": "200km",
                "location": {"lat": 40.73, "lon": -73.93},
            }
        }

    def test_build_with_array_point(self):
        """배열 형태의 좌표로 geo_distance 쿼리를 생성할 수 있는지 확인합니다."""
        result = GeoDistanceQuery.build("location", [-73.93, 40.73], "100km")
        assert result == {
            "geo_distance": {
                "distance": "100km",
                "location": [-73.93, 40.73],
            }
        }

    def test_build_with_string_point(self):
        """문자열 형태의 좌표로 geo_distance 쿼리를 생성할 수 있는지 확인합니다."""
        result = GeoDistanceQuery.build("location", "40.73,-73.93", "50km")
        assert result == {
            "geo_distance": {
                "distance": "50km",
                "location": "40.73,-73.93",
            }
        }

    def test_build_with_distance_type(self):
        """distance_type 옵션을 지정할 수 있는지 확인합니다."""
        result = GeoDistanceQuery.build(
            "location", {"lat": 40.73, "lon": -73.93}, "200km",
            distance_type="plane"
        )
        assert result["geo_distance"]["distance_type"] == "plane"

    def test_build_with_all_options(self):
        """모든 옵션을 지정할 수 있는지 확인합니다."""
        result = GeoDistanceQuery.build(
            "location", {"lat": 40.73, "lon": -73.93}, "200km",
            distance_type="arc",
            validation_method="STRICT",
            boost=1.5,
        )
        body = result["geo_distance"]
        assert body["distance"] == "200km"
        assert body["location"] == {"lat": 40.73, "lon": -73.93}
        assert body["distance_type"] == "arc"
        assert body["validation_method"] == "STRICT"
        assert body["boost"] == 1.5
