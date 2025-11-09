from unittest                                                                                       import TestCase
from osbot_utils.testing.__                                                                     import __
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash              import Safe_Str__Hash
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Criteria import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Request     import Schema__Classification__Request


class test_Schema__Classification__Request(TestCase):

    def test__init__(self):                                                    # Test auto-initialization
        with Schema__Classification__Request() as _:
            assert _.hash_mapping            == {}
            assert _.classification_criteria is None
            assert type(_).__name__          == 'Schema__Classification__Request'

    def test__with_data(self):                                                 # Test with actual data
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"}

        with Schema__Classification__Request(hash_mapping            = hash_mapping                                    ,
                                             classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY) as _:
            assert len(_.hash_mapping)            == 1
            assert _.hash_mapping[Safe_Str__Hash("abc1234567")] == "Hello World"
            assert _.classification_criteria      == Enum__Text__Classification__Criteria.POSITIVITY

    def test__obj(self):                                                       # Test .obj() serialization
        hash_mapping = {Safe_Str__Hash("abc1234567"): "test"}
        request      = Schema__Classification__Request(hash_mapping            = hash_mapping                                    ,
                                                       classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY)

        assert request.obj() == __(hash_mapping            = __(abc1234567='test')                ,
                                   classification_criteria = 'positivity'                         )

    def test__json_round_trip(self):                                           # Test JSON serialization round-trip
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test text"}

        with Schema__Classification__Request(hash_mapping            = hash_mapping                                    ,
                                            classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY) as _:
            json_data = _.json()
            restored  = Schema__Classification__Request(**json_data)

            assert restored.classification_criteria == Enum__Text__Classification__Criteria.POSITIVITY
            assert "abc1234567"                    in restored.hash_mapping
            assert restored.hash_mapping[Safe_Str__Hash("abc1234567")] == "Test text"
