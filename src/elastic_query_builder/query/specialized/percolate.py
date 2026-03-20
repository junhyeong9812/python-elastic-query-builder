from typing import Any, Dict, List, Optional


class PercolateQuery:
    @staticmethod
    def build(field: str, document: Optional[Dict[str, Any]] = None,
              index: Optional[str] = None, id: Optional[str] = None,
              documents: Optional[List[Dict[str, Any]]] = None,
              boost: Optional[float] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"field": field}
        if document is not None:
            body["document"] = document
        if documents is not None:
            body["documents"] = documents
        if index is not None:
            body["index"] = index
        if id is not None:
            body["id"] = id
        if boost is not None:
            body["boost"] = boost
        return {"percolate": body}
