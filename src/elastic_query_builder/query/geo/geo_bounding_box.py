from typing import Any, Dict, Optional


class GeoBoundingBoxQuery:
    @staticmethod
    def build(field: str, top_left: Any, bottom_right: Any,
              validation_method: Optional[str] = None,
              boost: Optional[float] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            field: {"top_left": top_left, "bottom_right": bottom_right}
        }
        if validation_method is not None:
            body["validation_method"] = validation_method
        if boost is not None:
            body["boost"] = boost
        return {"geo_bounding_box": body}
