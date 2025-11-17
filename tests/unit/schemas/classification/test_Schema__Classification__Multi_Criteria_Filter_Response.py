from unittest                                                                                                       import TestCase
from osbot_utils.testing.__                                                                                         import __
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                                import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                                  import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria                             import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.safe_float.Safe_Float__Text__Classification                            import Safe_Float__Text__Classification
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Filter_Response  import Schema__Classification__Multi_Criteria_Filter_Response
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode                 import Enum__Classification__Output_Mode
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Logic_Operator              import Enum__Classification__Logic_Operator


class test_Schema__Classification__Multi_Criteria_Filter_Response(TestCase):

    def test__init__(self):                                                    # Test auto-initialization
        with Schema__Classification__Multi_Criteria_Filter_Response() as _:
            assert _.filtered_hashes       == []
            assert _.filtered_with_text    == {}
            assert _.filtered_with_ratings == {}
            assert _.criteria_used         == []
            assert _.logic_operator        is None
            assert _.output_mode           is None
            assert _.total_hashes          == 0
            assert _.filtered_count        == 0
            assert _.success               is False
            assert type(_).__name__        == 'Schema__Classification__Multi_Criteria_Filter_Response'

    def test__with_hashes_only_mode(self):                                     # Test HASHES_ONLY output mode
        filtered_hashes = [Safe_Str__Hash("b10a8db164")]

        with Schema__Classification__Multi_Criteria_Filter_Response(
            filtered_hashes       = filtered_hashes,
            filtered_with_text    = None,
            filtered_with_ratings = None,
            criteria_used         = [Enum__Text__Classification__Criteria.POSITIVE],
            logic_operator        = Enum__Classification__Logic_Operator.AND,
            output_mode           = Enum__Classification__Output_Mode.HASHES_ONLY,
            total_hashes          = Safe_UInt(1),
            filtered_count        = Safe_UInt(1),
            success               = True
        ) as _:
            assert len(_.filtered_hashes) == 1
            assert _.filtered_with_text == {}
            assert _.filtered_with_ratings == {}
            assert _.output_mode == Enum__Classification__Output_Mode.HASHES_ONLY
            assert _.logic_operator == Enum__Classification__Logic_Operator.AND
            assert _.filtered_count == 1
            assert _.success is True

    def test__with_hashes_with_text_mode(self):                                # Test HASHES_WITH_TEXT output mode
        filtered_hashes = [Safe_Str__Hash("b10a8db164")]
        filtered_with_text = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        with Schema__Classification__Multi_Criteria_Filter_Response(
            filtered_hashes       = filtered_hashes,
            filtered_with_text    = filtered_with_text,
            filtered_with_ratings = None,
            criteria_used         = [Enum__Text__Classification__Criteria.POSITIVE],
            logic_operator        = Enum__Classification__Logic_Operator.AND,
            output_mode           = Enum__Classification__Output_Mode.HASHES_WITH_TEXT,
            total_hashes          = Safe_UInt(1),
            filtered_count        = Safe_UInt(1),
            success               = True
        ) as _:
            assert len(_.filtered_hashes)                             == 1
            assert _.filtered_with_text                               is not None
            assert len(_.filtered_with_text)                          == 1
            assert _.filtered_with_text[Safe_Str__Hash("b10a8db164")] == "Hello World"
            assert _.filtered_with_ratings                            == {}
            assert _.output_mode                                      == Enum__Classification__Output_Mode.HASHES_WITH_TEXT

    def test__with_full_ratings_mode(self):                                    # Test FULL_RATINGS output mode
        filtered_hashes = [Safe_Str__Hash("b10a8db164")]
        filtered_with_text = {Safe_Str__Hash("b10a8db164"): "Hello World"}
        filtered_with_ratings = {
            Safe_Str__Hash("b10a8db164"): {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.7478),
                Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.1102)
            }
        }

        with Schema__Classification__Multi_Criteria_Filter_Response(
            filtered_hashes       = filtered_hashes,
            filtered_with_text    = filtered_with_text,
            filtered_with_ratings = filtered_with_ratings,
            criteria_used         = [Enum__Text__Classification__Criteria.POSITIVE,
                                     Enum__Text__Classification__Criteria.NEGATIVE],
            logic_operator        = Enum__Classification__Logic_Operator.AND,
            output_mode           = Enum__Classification__Output_Mode.FULL_RATINGS,
            total_hashes          = Safe_UInt(1),
            filtered_count        = Safe_UInt(1),
            success               = True
        ) as _:
            assert len(_.filtered_hashes) == 1
            assert _.filtered_with_text is not None
            assert _.filtered_with_ratings is not None
            assert _.output_mode == Enum__Classification__Output_Mode.FULL_RATINGS

            ratings = _.filtered_with_ratings[Safe_Str__Hash("b10a8db164")]
            assert float(ratings[Enum__Text__Classification__Criteria.POSITIVE]) == 0.7478
            assert float(ratings[Enum__Text__Classification__Criteria.NEGATIVE]) == 0.1102

    def test__with_or_logic(self):                                             # Test OR logic operator
        filtered_hashes = [Safe_Str__Hash("b10a8db164"), Safe_Str__Hash("f1feeaa3d6")]

        with Schema__Classification__Multi_Criteria_Filter_Response(
            filtered_hashes       = filtered_hashes,
            filtered_with_text    = None,
            filtered_with_ratings = None,
            criteria_used         = [Enum__Text__Classification__Criteria.POSITIVE,
                                     Enum__Text__Classification__Criteria.MIXED],
            logic_operator        = Enum__Classification__Logic_Operator.OR,
            output_mode           = Enum__Classification__Output_Mode.HASHES_ONLY,
            total_hashes          = Safe_UInt(3),
            filtered_count        = Safe_UInt(2),
            success               = True
        ) as _:
            assert _.logic_operator == Enum__Classification__Logic_Operator.OR
            assert len(_.filtered_hashes) == 2
            assert _.filtered_count == 2
            assert _.total_hashes == 3

    def test__multiple_criteria(self):                                         # Test with multiple criteria
        filtered_hashes = [Safe_Str__Hash("b10a8db164")]

        with Schema__Classification__Multi_Criteria_Filter_Response(
            filtered_hashes       = filtered_hashes,
            filtered_with_text    = None,
            filtered_with_ratings = None,
            criteria_used         = [Enum__Text__Classification__Criteria.POSITIVE,
                                     Enum__Text__Classification__Criteria.NEGATIVE,
                                     Enum__Text__Classification__Criteria.NEUTRAL],
            logic_operator        = Enum__Classification__Logic_Operator.AND,
            output_mode           = Enum__Classification__Output_Mode.HASHES_ONLY,
            total_hashes          = Safe_UInt(1),
            filtered_count        = Safe_UInt(1),
            success               = True
        ) as _:
            assert len(_.criteria_used) == 3
            assert Enum__Text__Classification__Criteria.POSITIVE in _.criteria_used
            assert Enum__Text__Classification__Criteria.NEGATIVE in _.criteria_used
            assert Enum__Text__Classification__Criteria.NEUTRAL in _.criteria_used

    def test__no_matches(self):                                                # Test with no filtered results
        with Schema__Classification__Multi_Criteria_Filter_Response(
            filtered_hashes       = [],
            filtered_with_text    = None,
            filtered_with_ratings = None,
            criteria_used         = [Enum__Text__Classification__Criteria.POSITIVE],
            logic_operator        = Enum__Classification__Logic_Operator.AND,
            output_mode           = Enum__Classification__Output_Mode.HASHES_ONLY,
            total_hashes          = Safe_UInt(5),
            filtered_count        = Safe_UInt(0),
            success               = True
        ) as _:
            assert len(_.filtered_hashes) == 0
            assert _.filtered_count == 0
            assert _.total_hashes == 5
            assert _.success is True

    def test__multiple_filtered_hashes(self):                                  # Test with multiple filtered hashes
        filtered_hashes = [
            Safe_Str__Hash("b10a8db164"),
            Safe_Str__Hash("f1feeaa3d6"),
            Safe_Str__Hash("1ba249ca59")
        ]

        filtered_with_text = {
            Safe_Str__Hash("b10a8db164"): "Hello World",
            Safe_Str__Hash("f1feeaa3d6"): "Test Text",
            Safe_Str__Hash("1ba249ca59"): "Sample text"
        }

        with Schema__Classification__Multi_Criteria_Filter_Response(
            filtered_hashes       = filtered_hashes,
            filtered_with_text    = filtered_with_text,
            filtered_with_ratings = None,
            criteria_used         = [Enum__Text__Classification__Criteria.POSITIVE],
            logic_operator        = Enum__Classification__Logic_Operator.AND,
            output_mode           = Enum__Classification__Output_Mode.HASHES_WITH_TEXT,
            total_hashes          = Safe_UInt(10),
            filtered_count        = Safe_UInt(3),
            success               = True
        ) as _:
            assert len(_.filtered_hashes) == 3
            assert len(_.filtered_with_text) == 3
            assert _.filtered_count == 3
            assert _.total_hashes == 10

    def test__obj(self):                                                       # Test .obj() serialization
        filtered_hashes = [Safe_Str__Hash("b10a8db164")]

        response = Schema__Classification__Multi_Criteria_Filter_Response(
            filtered_hashes       = filtered_hashes,
            filtered_with_text    = None,
            filtered_with_ratings = None,
            criteria_used         = [Enum__Text__Classification__Criteria.POSITIVE],
            logic_operator        = Enum__Classification__Logic_Operator.AND,
            output_mode           = Enum__Classification__Output_Mode.HASHES_ONLY,
            total_hashes          = Safe_UInt(1),
            filtered_count        = Safe_UInt(1),
            success               = True
        )

        assert response.obj() == __(filtered_hashes       = ['b10a8db164']   ,
                                    filtered_with_text    = __()             ,
                                    filtered_with_ratings = __()             ,
                                    criteria_used         = ['positive']     ,
                                    logic_operator        = 'and'            ,
                                    output_mode           = 'hashes-only'    ,
                                    total_hashes          = 1                ,
                                    filtered_count        = 1                ,
                                    success               = True             )

    def test__json(self):                                                      # Test .json() serialization
        filtered_hashes    = [Safe_Str__Hash("b10a8db164")]
        filtered_with_text = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        response = Schema__Classification__Multi_Criteria_Filter_Response(
            filtered_hashes       = filtered_hashes,
            filtered_with_text    = filtered_with_text,
            filtered_with_ratings = None,
            criteria_used         = [Enum__Text__Classification__Criteria.POSITIVE,
                                     Enum__Text__Classification__Criteria.NEGATIVE],
            logic_operator        = Enum__Classification__Logic_Operator.OR,
            output_mode           = Enum__Classification__Output_Mode.HASHES_WITH_TEXT,
            total_hashes          = Safe_UInt(2),
            filtered_count        = Safe_UInt(1),
            success               = True
        )

        json_data = response.json()

        assert json_data['success'       ]       is True
        assert json_data['filtered_count']       == 1
        assert json_data['total_hashes'  ]       == 2
        assert json_data['logic_operator']       == 'or'
        assert json_data['output_mode'   ]       == 'hashes-with-text'
        assert len(json_data['filtered_hashes']) == 1
        assert json_data['filtered_with_text' ]  == {'b10a8db164': 'Hello World'}
        assert json_data                         == {'criteria_used': ['positive', 'negative'],
                                                     'filtered_count': 1,
                                                     'filtered_hashes': ['b10a8db164'],
                                                     'filtered_with_ratings': {},
                                                     'filtered_with_text': {'b10a8db164': 'Hello World'},
                                                     'logic_operator': 'or',
                                                     'output_mode': 'hashes-with-text',
                                                     'success': True,
                                                     'total_hashes': 2}


    def test__success_false(self):                                             # Test with success=False
        response = Schema__Classification__Multi_Criteria_Filter_Response(
            filtered_hashes       = [],
            filtered_with_text    = None,
            filtered_with_ratings = None,
            criteria_used         = [],
            logic_operator        = Enum__Classification__Logic_Operator.AND,
            output_mode           = Enum__Classification__Output_Mode.HASHES_ONLY,
            total_hashes          = Safe_UInt(0),
            filtered_count        = Safe_UInt(0),
            success               = False
        )

        assert response.success is False
        assert response.filtered_count == 0
        assert len(response.filtered_hashes) == 0

    def test__with_all_four_criteria(self):                                    # Test with all 4 classification criteria
        filtered_hashes = [Safe_Str__Hash("1ba249ca59")]
        filtered_with_ratings = {
            Safe_Str__Hash("1ba249ca59"): {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.9569),
                Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.1469),
                Enum__Text__Classification__Criteria.NEUTRAL:       Safe_Float__Text__Classification(0.2887),
                Enum__Text__Classification__Criteria.MIXED:    Safe_Float__Text__Classification(0.7091)
            }
        }

        response = Schema__Classification__Multi_Criteria_Filter_Response(
            filtered_hashes       = filtered_hashes,
            filtered_with_text    = {Safe_Str__Hash("1ba249ca59"): "Sample text"},
            filtered_with_ratings = filtered_with_ratings,
            criteria_used         = [Enum__Text__Classification__Criteria.POSITIVE,
                                     Enum__Text__Classification__Criteria.NEGATIVE,
                                     Enum__Text__Classification__Criteria.NEUTRAL,
                                     Enum__Text__Classification__Criteria.MIXED],
            logic_operator        = Enum__Classification__Logic_Operator.AND,
            output_mode           = Enum__Classification__Output_Mode.FULL_RATINGS,
            total_hashes          = Safe_UInt(1),
            filtered_count        = Safe_UInt(1),
            success               = True
        )

        assert len(response.criteria_used) == 4
        ratings = response.filtered_with_ratings[Safe_Str__Hash("1ba249ca59")]
        assert len(ratings) == 4