from typing import Any, Dict, List, Optional, Union


class GeoDistanceQuery:
    @staticmethod
    def build(field: str, point: Any, distance: str,
              distance_type: Optional[str] = None,
              validation_method: Optional[str] = None,
              boost: Optional[float] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"distance": distance, field: point}
        if distance_type is not None:
            body["distance_type"] = distance_type
        if validation_method is not None:
            body["validation_method"] = validation_method
        if boost is not None:
            body["boost"] = boost
        return {"geo_distance": body}
