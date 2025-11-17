import types
from unittest                                                                                             import TestCase
from osbot_utils.testing.__                                                                               import __
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                                     import Type_Safe__Dict
from osbot_utils.utils.Objects                                                                            import base_classes
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Request         import Schema__Text__Transformation__Request
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode        import Enum__Text__Transformation__Mode


class test_Schema__Text__Transformation__Request(TestCase):

    def test__init__(self):                                                         # Test auto-initialization of Schema__Text__Transformation__Request
        with Schema__Text__Transformation__Request() as _:
            assert type(_)                           is Schema__Text__Transformation__Request
            assert base_classes(_)                   == [Type_Safe, object]
            assert type(_.hash_mapping)              is Type_Safe__Dict
            assert type(_.transformation_mode)       is types.NoneType

    def test_with_values(self):                                                     # Test schema with specific values
        hash_mapping = { Safe_Str__Hash("abc1234567") : "Hello" ,
                         Safe_Str__Hash("def1234567") : "World" }

        with Schema__Text__Transformation__Request(hash_mapping          = hash_mapping                               ,
                                                   transformation_mode   = Enum__Text__Transformation__Mode.XXX) as _:
            assert _.obj() == __(logic_operator='and',
                                 hash_mapping=__(abc1234567='Hello', def1234567='World'),
                                 engine_mode=None,
                                 criterion_filters=[],
                                 transformation_mode='xxx')

    def test_json_round_trip(self):                                                 # Test JSON serialization round-trip
        hash_mapping = { Safe_Str__Hash("abc1234567") : "Test text" }

        with Schema__Text__Transformation__Request(hash_mapping          = hash_mapping                                    ,
                                                   transformation_mode   = Enum__Text__Transformation__Mode.HASHES) as _:
            json_data = _.json()
            restored  = Schema__Text__Transformation__Request(**json_data)

            assert restored.transformation_mode   == Enum__Text__Transformation__Mode.HASHES
            assert "abc1234567" in restored.hash_mapping
            assert restored.obj() == __(logic_operator      = 'and'                     ,
                                        hash_mapping        = __(abc1234567='Test text'),
                                        engine_mode         = None,
                                        criterion_filters   = [],
                                        transformation_mode = 'hashes')