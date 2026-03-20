"""FunctionScoreQuery 테스트."""

from elastic_query_builder.query.compound.function_score import FunctionScoreQuery


class TestFunctionScoreQuery:
    """FunctionScoreQuery.build 메서드 테스트."""

    def test_basic_query_only(self):
        """기본 쿼리만 전달하면 query만 포함된 function_score를 생성한다."""
        result = FunctionScoreQuery.build({"match_all": {}})
        assert result == {"function_score": {"query": {"match_all": {}}}}

    def test_with_weight_functions(self):
        """weight 함수를 포함한 function_score를 생성한다."""
        functions = [
            {"filter": {"term": {"status": "published"}}, "weight": 2}
        ]
        result = FunctionScoreQuery.build({"match_all": {}}, functions=functions)
        assert result == {
            "function_score": {
                "query": {"match_all": {}},
                "functions": [
                    {"filter": {"term": {"status": "published"}}, "weight": 2}
                ],
            }
        }

    def test_with_score_mode(self):
        """score_mode를 설정한 function_score를 생성한다."""
        result = FunctionScoreQuery.build({"match_all": {}}, score_mode="sum")
        assert result == {
            "function_score": {
                "query": {"match_all": {}},
                "score_mode": "sum",
            }
        }

    def test_with_boost_mode(self):
        """boost_mode를 설정한 function_score를 생성한다."""
        result = FunctionScoreQuery.build({"match_all": {}}, boost_mode="replace")
        assert result == {
            "function_score": {
                "query": {"match_all": {}},
                "boost_mode": "replace",
            }
        }

    def test_with_max_boost(self):
        """max_boost를 설정한 function_score를 생성한다."""
        result = FunctionScoreQuery.build({"match_all": {}}, max_boost=42.0)
        assert result == {
            "function_score": {
                "query": {"match_all": {}},
                "max_boost": 42.0,
            }
        }

    def test_with_min_score(self):
        """min_score를 설정한 function_score를 생성한다."""
        result = FunctionScoreQuery.build({"match_all": {}}, min_score=5.0)
        assert result == {
            "function_score": {
                "query": {"match_all": {}},
                "min_score": 5.0,
            }
        }

    def test_with_all_options(self):
        """모든 옵션을 설정한 function_score를 생성한다."""
        functions = [{"weight": 2}]
        result = FunctionScoreQuery.build(
            {"match_all": {}},
            functions=functions,
            score_mode="avg",
            boost_mode="multiply",
            max_boost=10.0,
            boost=1.5,
            min_score=3.0,
        )
        assert result == {
            "function_score": {
                "query": {"match_all": {}},
                "functions": [{"weight": 2}],
                "score_mode": "avg",
                "boost_mode": "multiply",
                "max_boost": 10.0,
                "boost": 1.5,
                "min_score": 3.0,
            }
        }

    def test_with_script_score_function(self):
        """script_score 함수를 포함한 function_score를 생성한다."""
        functions = [
            {
                "script_score": {
                    "script": {
                        "source": "_score * doc['popularity'].value"
                    }
                }
            }
        ]
        result = FunctionScoreQuery.build({"match_all": {}}, functions=functions)
        assert result == {
            "function_score": {
                "query": {"match_all": {}},
                "functions": [
                    {
                        "script_score": {
                            "script": {
                                "source": "_score * doc['popularity'].value"
                            }
                        }
                    }
                ],
            }
        }

    def test_with_filter_and_weight_functions(self):
        """filter+weight 조합의 여러 함수를 포함한 function_score를 생성한다."""
        functions = [
            {"filter": {"term": {"color": "red"}}, "weight": 3},
            {"filter": {"term": {"color": "blue"}}, "weight": 1.5},
        ]
        result = FunctionScoreQuery.build(
            {"match": {"title": "shoes"}},
            functions=functions,
            score_mode="sum",
        )
        assert result == {
            "function_score": {
                "query": {"match": {"title": "shoes"}},
                "functions": [
                    {"filter": {"term": {"color": "red"}}, "weight": 3},
                    {"filter": {"term": {"color": "blue"}}, "weight": 1.5},
                ],
                "score_mode": "sum",
            }
        }

    def test_with_decay_function(self):
        """decay 함수를 포함한 function_score를 생성한다."""
        functions = [
            {
                "gauss": {
                    "date": {
                        "origin": "2024-01-01",
                        "scale": "10d",
                        "offset": "5d",
                        "decay": 0.5,
                    }
                }
            }
        ]
        result = FunctionScoreQuery.build(
            {"match_all": {}},
            functions=functions,
            boost_mode="multiply",
        )
        assert result == {
            "function_score": {
                "query": {"match_all": {}},
                "functions": [
                    {
                        "gauss": {
                            "date": {
                                "origin": "2024-01-01",
                                "scale": "10d",
                                "offset": "5d",
                                "decay": 0.5,
                            }
                        }
                    }
                ],
                "boost_mode": "multiply",
            }
        }
