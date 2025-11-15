from unittest                                                                                            import TestCase
from osbot_utils.testing.__                                                                              import __
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                     import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                       import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.routes.Schema__Text__Transformation__Request__ABCDE_By_Size import Schema__Text__Transformation__Request__ABCDE_By_Size


class test__Schema__Text__Transformation__Request__ABCDE_By_Size(TestCase):

    def test__init__(self):                                                     # Verify Type_Safe inheritance and auto-initialization
        with Schema__Text__Transformation__Request__ABCDE_By_Size() as _:
            assert _.hash_mapping == {}
            assert _.randomness_percentage == 0.5
            assert _.num_groups == 5
            assert type(_).__name__ == 'Schema__Text__Transformation__Request__ABCDE_By_Size'

    def test__with_data(self):                                                  # Test with actual data including num_groups
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Another test"}

        with Schema__Text__Transformation__Request__ABCDE_By_Size(hash_mapping          = hash_mapping,
                                                                  randomness_percentage = 0.8,
                                                                  num_groups            = Safe_UInt(7)) as _:
            assert len(_.hash_mapping) == 1
            assert _.hash_mapping[Safe_Str__Hash("abc1234567")] == "Another test"
            assert _.randomness_percentage == 0.8
            assert _.num_groups == 7

    def test__default_num_groups(self):                                         # Test default num_groups value
        request = Schema__Text__Transformation__Request__ABCDE_By_Size()
        assert request.num_groups == 5

    def test__obj(self):                                                        # Test .obj() serialization
        hash_mapping = {Safe_Str__Hash("abc1234567"): "test"}
        request      = Schema__Text__Transformation__Request__ABCDE_By_Size(hash_mapping=hash_mapping)
        assert request.obj() == __(randomness_percentage = 0.5  ,
                                   num_groups            = 5    ,
                                   hash_mapping          = __(abc1234567='test'))

