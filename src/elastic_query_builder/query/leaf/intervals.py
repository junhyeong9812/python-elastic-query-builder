"""intervals 쿼리 빌더.

Elasticsearch의 intervals 쿼리를 생성합니다.
텍스트 필드에서 용어의 순서와 근접성을 기반으로 문서를 검색합니다.
"""

from typing import Any, Dict


class IntervalsQuery:
    """intervals 쿼리를 생성하는 정적 빌더."""

    @staticmethod
    def build(field: str, rule: Dict[str, Any]) -> Dict[str, Any]:
        """intervals 쿼리를 생성합니다.

        rule은 match, prefix, wildcard, fuzzy, all_of, any_of 중 하나여야 합니다.

        사용 예시::

            IntervalsQuery.build("my_text", {
                "all_of": {
                    "ordered": True,
                    "intervals": [
                        {"match": {"query": "hot"}},
                        {"match": {"query": "dog"}}
                    ]
                }
            })

        Args:
            field: 검색할 필드명.
            rule: intervals 규칙 딕셔너리.

        Returns:
            intervals 쿼리 딕셔너리.
        """
        return {"intervals": {field: rule}}
