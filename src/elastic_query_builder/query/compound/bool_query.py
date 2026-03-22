"""Bool 쿼리 빌더.

Elasticsearch의 bool 쿼리를 메서드 체이닝 방식으로 조립하는
상태 기반(stateful) 빌더를 제공합니다.
"""

import copy
from typing import Any, Dict, List, Optional
from elastic_query_builder.core.enums import BoolClause


class BoolQueryBuilder:
    """Bool 쿼리를 조립하는 빌더.

    Elasticsearch bool 쿼리에 대응합니다.
    must, should, must_not, filter 절을 메서드 체이닝 방식으로 추가하고,
    build()를 호출하여 최종 쿼리 딕셔너리를 생성합니다.
    """

    def __init__(self):
        """BoolQueryBuilder를 초기화합니다."""
        self._must: List[Dict[str, Any]] = []
        self._should: List[Dict[str, Any]] = []
        self._must_not: List[Dict[str, Any]] = []
        self._filter: List[Dict[str, Any]] = []
        self._minimum_should_match: Optional[Any] = None

    def add_must(self, condition: Dict[str, Any]) -> 'BoolQueryBuilder':
        """must 절에 조건을 추가합니다.

        Args:
            condition: 추가할 쿼리 조건 딕셔너리.

        Returns:
            메서드 체이닝을 위한 self.
        """
        self._must.append(copy.deepcopy(condition))
        return self

    def add_should(self, condition: Dict[str, Any]) -> 'BoolQueryBuilder':
        """should 절에 조건을 추가합니다.

        Args:
            condition: 추가할 쿼리 조건 딕셔너리.

        Returns:
            메서드 체이닝을 위한 self.
        """
        self._should.append(copy.deepcopy(condition))
        return self

    def add_must_not(self, condition: Dict[str, Any]) -> 'BoolQueryBuilder':
        """must_not 절에 조건을 추가합니다.

        Args:
            condition: 추가할 쿼리 조건 딕셔너리.

        Returns:
            메서드 체이닝을 위한 self.
        """
        self._must_not.append(copy.deepcopy(condition))
        return self

    def add_filter(self, condition: Dict[str, Any]) -> 'BoolQueryBuilder':
        """filter 절에 조건을 추가합니다.

        Args:
            condition: 추가할 쿼리 조건 딕셔너리.

        Returns:
            메서드 체이닝을 위한 self.
        """
        self._filter.append(copy.deepcopy(condition))
        return self

    def add_clauses(self, *clauses: BoolClause) -> 'BoolQueryBuilder':
        """빈 절 배열을 명시적으로 선언합니다.

        build 출력에 포함시키기 위해 절을 명시적으로 등록할 때 사용합니다.

        Args:
            *clauses: 초기화할 BoolClause 열거형 값들.

        Returns:
            메서드 체이닝을 위한 self.
        """
        if not hasattr(self, '_explicit_clauses'):
            self._explicit_clauses = set()
        for clause in clauses:
            self._explicit_clauses.add(clause)
        return self

    def add_minimum_should_match(self, value: Any) -> 'BoolQueryBuilder':
        """minimum_should_match 값을 설정합니다.

        Args:
            value: minimum_should_match 값. 정수 또는 문자열(예: "75%").

        Returns:
            메서드 체이닝을 위한 self.
        """
        self._minimum_should_match = value
        return self

    def merge(self, other: 'BoolQueryBuilder') -> 'BoolQueryBuilder':
        """다른 BoolQueryBuilder의 모든 절을 병합합니다.

        Args:
            other: 병합할 다른 BoolQueryBuilder 인스턴스.

        Returns:
            메서드 체이닝을 위한 self.
        """
        self._must.extend(copy.deepcopy(other._must))
        self._should.extend(copy.deepcopy(other._should))
        self._must_not.extend(copy.deepcopy(other._must_not))
        self._filter.extend(copy.deepcopy(other._filter))
        if other._minimum_should_match is not None:
            self._minimum_should_match = other._minimum_should_match
        return self

    def merge_must(self, other: 'BoolQueryBuilder') -> 'BoolQueryBuilder':
        """다른 BoolQueryBuilder의 must 절만 병합합니다.

        Args:
            other: 병합할 다른 BoolQueryBuilder 인스턴스.

        Returns:
            메서드 체이닝을 위한 self.
        """
        self._must.extend(copy.deepcopy(other._must))
        return self

    def merge_should(self, other: 'BoolQueryBuilder') -> 'BoolQueryBuilder':
        """다른 BoolQueryBuilder의 should 절만 병합합니다.

        Args:
            other: 병합할 다른 BoolQueryBuilder 인스턴스.

        Returns:
            메서드 체이닝을 위한 self.
        """
        self._should.extend(copy.deepcopy(other._should))
        return self

    def count_must(self) -> int:
        """must 절의 조건 수를 반환합니다."""
        return len(self._must)

    def count_should(self) -> int:
        """should 절의 조건 수를 반환합니다."""
        return len(self._should)

    def count_must_not(self) -> int:
        """must_not 절의 조건 수를 반환합니다."""
        return len(self._must_not)

    def count_filter(self) -> int:
        """filter 절의 조건 수를 반환합니다."""
        return len(self._filter)

    def is_empty(self) -> bool:
        """빌더에 조건이 하나도 없는지 확인합니다.

        Returns:
            모든 절이 비어 있으면 True, 아니면 False.
        """
        return (
            len(self._must) == 0
            and len(self._should) == 0
            and len(self._must_not) == 0
            and len(self._filter) == 0
        )

    def build(self) -> Dict[str, Any]:
        """최종 Elasticsearch bool 쿼리 딕셔너리를 생성합니다.

        Returns:
            Elasticsearch bool 쿼리 딕셔너리.
        """
        bool_body: Dict[str, Any] = {}
        if self._must:
            bool_body["must"] = self._must
        if self._should:
            bool_body["should"] = self._should
        if self._must_not:
            bool_body["must_not"] = self._must_not
        if self._filter:
            bool_body["filter"] = self._filter
        if self._minimum_should_match is not None:
            bool_body["minimum_should_match"] = self._minimum_should_match
        return {"bool": bool_body}
