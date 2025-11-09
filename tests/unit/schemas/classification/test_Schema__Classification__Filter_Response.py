from unittest                                                                                       import TestCase
from osbot_utils.testing.__                                                                     import __
from osbot_utils.type_safe.primitives.core.Safe_UInt                                            import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash              import Safe_Str__Hash
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Criteria import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.service.schemas.safe_float.Safe_Float__Text__Classification import Safe_Float__Text__Classification
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode import Enum__Classification__Output_Mode
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Filter_Response import Schema__Classification__Filter_Response


class test_Schema__Classification__Filter_Response(TestCase):

    def test__init__(self):                                                    # Test auto-initialization
        with Schema__Classification__Filter_Response() as _:
            assert _.filtered_hashes         == []
            assert _.filtered_with_text      is None
            assert _.filtered_with_ratings   is None
            assert _.classification_criteria is None
            assert _.output_mode             is None
            assert type(_.total_hashes)      is Safe_UInt
            assert type(_.filtered_count)    is Safe_UInt
            assert _.success                 is False
            assert type(_).__name__          == 'Schema__Classification__Filter_Response'

    def test__hashes_only_mode(self):                                          # Test HASHES_ONLY output mode
        filtered_hashes = [Safe_Str__Hash("abc1234567"), Safe_Str__Hash("def1234567")]

        with Schema__Classification__Filter_Response(filtered_hashes         = filtered_hashes                              ,
                                                     classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                     output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY ,
                                                     total_hashes            = Safe_UInt(10)                                 ,
                                                     filtered_count          = Safe_UInt(2)                                  ,
                                                     success                 = True                                          ) as _:
            assert _.success                 is True
            assert len(_.filtered_hashes)    == 2
            assert _.filtered_with_text      is None
            assert _.filtered_with_ratings   is None
            assert _.output_mode             == Enum__Classification__Output_Mode.HASHES_ONLY
            assert _.total_hashes            == 10
            assert _.filtered_count          == 2

    def test__hashes_with_text_mode(self):                                     # Test HASHES_WITH_TEXT output mode
        filtered_hashes    = [Safe_Str__Hash("abc1234567")]
        filtered_with_text = {Safe_Str__Hash("abc1234567"): "Hello World"}

        with Schema__Classification__Filter_Response(filtered_hashes         = filtered_hashes                              ,
                                                     filtered_with_text      = filtered_with_text                           ,
                                                     classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                     output_mode             = Enum__Classification__Output_Mode.HASHES_WITH_TEXT,
                                                     total_hashes            = Safe_UInt(5)                                  ,
                                                     filtered_count          = Safe_UInt(1)                                  ,
                                                     success                 = True                                          ) as _:
            assert _.success                 is True
            assert len(_.filtered_hashes)    == 1
            assert _.filtered_with_text      is not None
            assert _.filtered_with_text[Safe_Str__Hash("abc1234567")] == "Hello World"
            assert _.filtered_with_ratings   is None

    def test__full_ratings_mode(self):                                         # Test FULL_RATINGS output mode
        filtered_hashes      = [Safe_Str__Hash("abc1234567")]
        filtered_with_text   = {Safe_Str__Hash("abc1234567"): "Test"}
        filtered_with_ratings = {Safe_Str__Hash("abc1234567"): Safe_Float__Text__Classification(0.9)}

        with Schema__Classification__Filter_Response(filtered_hashes         = filtered_hashes                              ,
                                                     filtered_with_text      = filtered_with_text                           ,
                                                     filtered_with_ratings   = filtered_with_ratings                        ,
                                                     classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                     output_mode             = Enum__Classification__Output_Mode.FULL_RATINGS,
                                                     total_hashes            = Safe_UInt(3)                                  ,
                                                     filtered_count          = Safe_UInt(1)                                  ,
                                                     success                 = True                                          ) as _:
            assert _.success                 is True
            assert _.filtered_with_text      is not None
            assert _.filtered_with_ratings   is not None
            assert _.filtered_with_ratings[Safe_Str__Hash("abc1234567")] == 0.9

    def test__obj_comparison(self):                                            # Test .obj() method
        filtered_hashes = [Safe_Str__Hash("abc1234567")]

        with Schema__Classification__Filter_Response(filtered_hashes         = filtered_hashes                              ,
                                                     classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                     output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY ,
                                                     total_hashes            = Safe_UInt(5)                                  ,
                                                     filtered_count          = Safe_UInt(1)                                  ,
                                                     success                 = True                                          ) as _:
            assert _.obj() == __(filtered_hashes         = ['abc1234567']       ,
                                 filtered_with_text      = None                 ,
                                 filtered_with_ratings   = None                 ,
                                 classification_criteria = 'positivity'         ,
                                 output_mode             = 'hashes-only'        ,
                                 total_hashes            = 5                    ,
                                 filtered_count          = 1                    ,
                                 success                 = True                 )

    def test__empty_results(self):                                             # Test with no filtered results
        with Schema__Classification__Filter_Response(filtered_hashes         = []                                            ,
                                                     classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                     output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY ,
                                                     total_hashes            = Safe_UInt(10)                                 ,
                                                     filtered_count          = Safe_UInt(0)                                  ,
                                                     success                 = True                                          ) as _:
            assert _.success           is True
            assert _.filtered_hashes   == []
            assert _.filtered_count    == 0
            assert _.total_hashes      == 10
