from unittest                                                                                              import TestCase
from osbot_utils.testing.__                                                                                import __
from mgraph_ai_service_semantic_text.schemas.routes.Schema__Text__Transformation__Request__XXX_Random      import Schema__Text__Transformation__Request__XXX_Random
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                         import Safe_Str__Hash

class test__Schema__Text__Transformation__Request__XXX_Random(TestCase):

    def test__init__(self):                                                     # Verify Type_Safe inheritance and auto-initialization
        with Schema__Text__Transformation__Request__XXX_Random() as _:
            assert _.hash_mapping == {}
            assert type(_).__name__ == 'Schema__Text__Transformation__Request__XXX_Random'

    def test__with_data(self):                                                  # Test with actual data
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"}

        with Schema__Text__Transformation__Request__XXX_Random(hash_mapping          = hash_mapping) as _:
            assert len(_.hash_mapping)                          == 1
            assert _.hash_mapping[Safe_Str__Hash("abc1234567")] == "Hello World"
            assert _.obj()                                      == __(hash_mapping          = __(abc1234567='Hello World'))

    def test__obj(self):                                                        # Test .obj() serialization
        hash_mapping = {Safe_Str__Hash("abc1234567"): "test"}
        request = Schema__Text__Transformation__Request__XXX_Random(hash_mapping=hash_mapping)

        assert request.obj() == __(hash_mapping          = __(abc1234567='test'))