"""query/specialized/script_score.py에 대한 단위 테스트.

ScriptScoreQuery가 올바른 Elasticsearch script_score 쿼리 딕셔너리를
생성하는지 검증합니다.
"""

import pytest
from elastic_query_builder.query.specialized.script_score import ScriptScoreQuery


class TestScriptScoreQuery:
    """ScriptScoreQuery 테스트."""

    def test_basic(self):
        """기본 script_score 쿼리가 올바른 구조를 생성하는지 확인합니다."""
        result = ScriptScoreQuery.build(
            query={"match_all": {}},
            script={"source": "_score * doc['popularity'].value"},
        )
        expected = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {"source": "_score * doc['popularity'].value"},
            }
        }
        assert result == expected

    def test_with_boost(self):
        """boost 옵션이 올바르게 설정되는지 확인합니다."""
        result = ScriptScoreQuery.build(
            query={"match": {"title": "검색"}},
            script={"source": "_score * 2"},
            boost=1.5,
        )
        assert result["script_score"]["boost"] == 1.5

    def test_with_min_score(self):
        """min_score 옵션이 올바르게 설정되는지 확인합니다."""
        result = ScriptScoreQuery.build(
            query={"match_all": {}},
            script={"source": "_score"},
            min_score=10.0,
        )
        assert result["script_score"]["min_score"] == 10.0

    def test_with_all_options(self):
        """모든 옵션이 올바르게 설정되는지 확인합니다."""
        result = ScriptScoreQuery.build(
            query={"bool": {"must": [{"match": {"title": "test"}}]}},
            script={"source": "Math.log(2 + doc['likes'].value)", "lang": "painless"},
            boost=2.0,
            min_score=5.0,
        )
        body = result["script_score"]
        assert body["query"] == {"bool": {"must": [{"match": {"title": "test"}}]}}
        assert body["script"]["lang"] == "painless"
        assert body["boost"] == 2.0
        assert body["min_score"] == 5.0

    def test_optional_params_not_included_when_none(self):
        """None인 선택적 파라미터가 결과에 포함되지 않는지 확인합니다."""
        result = ScriptScoreQuery.build(
            query={"match_all": {}},
            script={"source": "_score"},
        )
        body = result["script_score"]
        assert "boost" not in body
        assert "min_score" not in body
