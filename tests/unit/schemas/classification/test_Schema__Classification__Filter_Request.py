from unittest                                                                                       import TestCase
from osbot_utils.testing.__                                                                     import __
from osbot_utils.type_safe.primitives.core.Safe_Float                                           import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash              import Safe_Str__Hash
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Criteria import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode import Enum__Classification__Output_Mode
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode import Enum__Classification__Filter_Mode
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Filter_Request import Schema__Classification__Filter_Request


class test_Schema__Classification__Filter_Request(TestCase):

    def test__init__(self):                                                    # Test auto-initialization
        with Schema__Classification__Filter_Request() as _:
            assert _.hash_mapping            == {}
            assert _.classification_criteria is None
            assert _.filter_mode             is None
            assert _.threshold               == 0.0
            assert _.threshold_max           is None
            assert _.output_mode             == Enum__Classification__Output_Mode.FULL_RATINGS
            assert type(_).__name__          == 'Schema__Classification__Filter_Request'

    def test__with_basic_filter(self):                                         # Test with basic ABOVE filter
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"}

        with Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                    classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                    filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                    threshold               = Safe_Float(0.5)                                ,
                                                    output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY ) as _:
            assert len(_.hash_mapping)            == 1
            assert _.classification_criteria      == Enum__Text__Classification__Criteria.POSITIVITY
            assert _.filter_mode                  == Enum__Classification__Filter_Mode.ABOVE
            assert _.threshold                    == 0.5
            assert _.threshold_max                is None
            assert _.output_mode                  == Enum__Classification__Output_Mode.HASHES_ONLY

    def test__with_between_filter(self):                                       # Test with BETWEEN filter using threshold_max
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        with Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                    classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                    filter_mode             = Enum__Classification__Filter_Mode.BETWEEN      ,
                                                    threshold               = Safe_Float(0.3)                                ,
                                                    threshold_max           = Safe_Float(0.7)                                ) as _:
            assert _.filter_mode   == Enum__Classification__Filter_Mode.BETWEEN
            assert _.threshold     == 0.3
            assert _.threshold_max == 0.7

    def test__obj(self):                                                       # Test .obj() serialization
        hash_mapping = {Safe_Str__Hash("abc1234567"): "test"}
        request      = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                              classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                              filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                              threshold               = Safe_Float(0.5)                                )

        assert request.obj() == __(hash_mapping            = __(abc1234567='test')                ,
                                   classification_criteria = 'positivity'                         ,
                                   filter_mode             = 'above'                              ,
                                   threshold               = 0.5                                  ,
                                   threshold_max           = None                                 ,
                                   output_mode             = 'full-ratings'                       )

    def test__all_output_modes(self):                                          # Test all output mode options
        hash_mapping = {Safe_Str__Hash("abc1234567"): "test"}

        for output_mode in Enum__Classification__Output_Mode:
            request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                             classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                             filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                             threshold               = Safe_Float(0.5)                                ,
                                                             output_mode             = output_mode                                    )
            assert request.output_mode == output_mode
