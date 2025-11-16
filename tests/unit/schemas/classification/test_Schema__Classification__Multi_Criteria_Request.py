from unittest                                                                                               import TestCase
from osbot_utils.testing.__                                                                                 import __
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                          import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria             import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Request  import Schema__Classification__Multi_Criteria_Request


class test_Schema__Classification__Multi_Criteria_Request(TestCase):

    def test__init__(self):                                                    # Test auto-initialization
        with Schema__Classification__Multi_Criteria_Request() as _:
            assert _.hash_mapping            == {}
            assert _.classification_criteria == []
            assert type(_).__name__          == 'Schema__Classification__Multi_Criteria_Request'

    def test__with_single_criterion(self):                                     # Test with single criterion
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"}

        with Schema__Classification__Multi_Criteria_Request(
            hash_mapping            = hash_mapping                                                          ,
            classification_criteria = [Enum__Text__Classification__Criteria.POSITIVE]
        ) as _:
            assert len(_.hash_mapping)            == 1
            assert len(_.classification_criteria) == 1
            assert _.hash_mapping[Safe_Str__Hash("abc1234567")] == "Hello World"
            assert _.classification_criteria[0]   == Enum__Text__Classification__Criteria.POSITIVE

    def test__with_multiple_criteria(self):                                    # Test with multiple criteria
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        with Schema__Classification__Multi_Criteria_Request(
            hash_mapping            = hash_mapping                                                          ,
            classification_criteria = [Enum__Text__Classification__Criteria.POSITIVE,
                                       Enum__Text__Classification__Criteria.NEGATIVE,
                                       Enum__Text__Classification__Criteria.NEUTRAL]
        ) as _:
            assert len(_.classification_criteria) == 3
            assert Enum__Text__Classification__Criteria.POSITIVE in _.classification_criteria
            assert Enum__Text__Classification__Criteria.NEGATIVE in _.classification_criteria
            assert Enum__Text__Classification__Criteria.NEUTRAL       in _.classification_criteria

    def test__obj(self):                                                       # Test .obj() serialization
        hash_mapping = {Safe_Str__Hash("abc1234567"): "test"}
        request      = Schema__Classification__Multi_Criteria_Request(
            hash_mapping            = hash_mapping                                                          ,
            classification_criteria = [Enum__Text__Classification__Criteria.POSITIVE,
                                       Enum__Text__Classification__Criteria.NEGATIVE]
        )

        assert request.obj() == __(hash_mapping            = __(abc1234567='test')              ,
                                   classification_criteria = ['positivity', 'negativity']       )

    def test__json_round_trip(self):                                           # Test JSON serialization round-trip
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test text"}

        with Schema__Classification__Multi_Criteria_Request(
            hash_mapping            = hash_mapping                                                          ,
            classification_criteria = [Enum__Text__Classification__Criteria.POSITIVE,
                                       Enum__Text__Classification__Criteria.MIXED]
        ) as _:
            json_data = _.json()
            restored  = Schema__Classification__Multi_Criteria_Request(**json_data)

            assert len(restored.classification_criteria) == 2
            assert Enum__Text__Classification__Criteria.POSITIVE in restored.classification_criteria
            assert Enum__Text__Classification__Criteria.MIXED    in restored.classification_criteria
            assert "abc1234567"                                    in restored.hash_mapping

    def test__all_criteria(self):                                              # Test with all available criteria
        hash_mapping = {Safe_Str__Hash("abc1234567"): "test"}

        request = Schema__Classification__Multi_Criteria_Request(
            hash_mapping            = hash_mapping                                                          ,
            classification_criteria = [Enum__Text__Classification__Criteria.POSITIVE,
                                       Enum__Text__Classification__Criteria.NEGATIVE,
                                       Enum__Text__Classification__Criteria.NEUTRAL,
                                       Enum__Text__Classification__Criteria.MIXED]
        )

        assert len(request.classification_criteria) == 4