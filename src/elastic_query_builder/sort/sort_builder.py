"""SortBuilder — 정렬 조건 빌더.

Elasticsearch의 정렬(Sort) 조건을 조합하여 최종 sort 배열을 생성합니다.
필드 정렬, _score 정렬, 스크립트 기반 정렬을 지원하며,
메서드 체이닝을 지원합니다.
"""

from typing import Any, Dict, List, Optional
from elastic_query_builder.core.enums import SortOrder, SortMissing


class SortBuilder:
    """정렬 조건을 조합하는 빌더.

    add()로 필드 정렬, add_score()로 _score 정렬,
    add_script()로 스크립트 정렬을 추가할 수 있습니다.
    set()으로 기존 정렬을 교체하거나, merge()로 정렬을 병합할 수 있습니다.
    모든 메서드는 self를 반환하여 메서드 체이닝을 지원합니다.
    """

    def __init__(self):
        self._sorts: List[Dict[str, Any]] = []

    def add(
        self, field: str,
        order: Optional[SortOrder] = None,
        missing: Optional[SortMissing] = None,
        mode: Optional[str] = None,
    ) -> 'SortBuilder':
        """필드 정렬을 추가합니다.

        Args:
            field: 정렬할 필드명.
            order: 정렬 방향 (선택). SortOrder.ASC 또는 SortOrder.DESC.
            missing: 누락 값 처리 방식 (선택). SortMissing.FIRST 또는 SortMissing.LAST.
            mode: 다중 값 필드의 정렬 모드 (선택). "min", "max", "avg", "sum" 중 하나.

        Returns:
            메서드 체이닝을 위한 self.
        """
        body: Dict[str, Any] = {}
        if order is not None:
            body["order"] = order.value
        if missing is not None:
            body["missing"] = missing.value
        if mode is not None:
            body["mode"] = mode
        self._sorts.append({field: body})
        return self

    def add_score(self, order: Optional[SortOrder] = None) -> 'SortBuilder':
        """_score 정렬을 추가합니다.

        Args:
            order: 정렬 방향 (선택). 기본적으로 _score는 내림차순이지만,
                   SortOrder.ASC를 지정하여 오름차순으로 변경할 수 있습니다.

        Returns:
            메서드 체이닝을 위한 self.
        """
        body: Dict[str, Any] = {}
        if order is not None:
            body["order"] = order.value
        self._sorts.append({"_score": body})
        return self

    def add_script(
        self, script: Dict[str, Any],
        order: Optional[SortOrder] = None,
        script_type: str = "number",
        lang: Optional[str] = None,
    ) -> 'SortBuilder':
        """스크립트 기반 정렬을 추가합니다.

        Args:
            script: 스크립트 본문 딕셔너리. 예: {"source": "doc['price'].value * 2"}.
            order: 정렬 방향 (선택).
            script_type: 스크립트 반환 타입 (기본값: "number"). "number" 또는 "string".
            lang: 스크립트 언어 (선택). 지정하면 script 딕셔너리에 lang 키가 추가됩니다.

        Returns:
            메서드 체이닝을 위한 self.
        """
        body: Dict[str, Any] = {"type": script_type, "script": script}
        if order is not None:
            body["order"] = order.value
        if lang is not None:
            body["script"]["lang"] = lang
        self._sorts.append({"_script": body})
        return self

    def set(self, sort_config: List[Dict[str, Any]]) -> 'SortBuilder':
        """기존 정렬 조건을 완전히 교체합니다.

        Args:
            sort_config: 새로운 정렬 배열.

        Returns:
            메서드 체이닝을 위한 self.
        """
        self._sorts = list(sort_config)
        return self

    def merge(self, sort_config: List[Dict[str, Any]]) -> 'SortBuilder':
        """기존 정렬 조건에 추가 정렬을 병합합니다.

        Args:
            sort_config: 병합할 정렬 배열.

        Returns:
            메서드 체이닝을 위한 self.
        """
        self._sorts.extend(sort_config)
        return self

    def is_empty(self) -> bool:
        """빌더에 추가된 정렬 조건이 없는지 확인합니다.

        Returns:
            정렬 조건이 없으면 True, 있으면 False.
        """
        return len(self._sorts) == 0

    def build(self) -> List[Dict[str, Any]]:
        """최종 정렬 배열을 생성합니다.

        Returns:
            정렬 조건 딕셔너리의 리스트.
        """
        return list(self._sorts)
