from unittest                                                                                             import TestCase
from osbot_utils.testing.__                                                                               import __
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                              import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                                     import Type_Safe__Dict
from osbot_utils.utils.Objects                                                                            import base_classes
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Response        import Schema__Text__Transformation__Response
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode        import Enum__Text__Transformation__Mode


class test_Schema__Text__Transformation__Response(TestCase):

    def test__init__(self):                                                         # Test auto-initialization of Schema__Text__Transformation__Response
        with Schema__Text__Transformation__Response() as _:
            assert type(_)                      is Schema__Text__Transformation__Response
            assert base_classes(_)              == [Type_Safe, object]
            assert type(_.transformed_mapping)  is Type_Safe__Dict
            assert type(_.total_hashes)         is Safe_UInt
            assert type(_.transformed_hashes)   is Safe_UInt
            assert _.success                    is False                            # Default bool value
            assert _.error_message              is None                             # Optional field

    def test_with_success_response(self):                                           # Test successful transformation response
        transformed_mapping = { Safe_Str__Hash("abc1234567") : "xxxxx" ,
                                Safe_Str__Hash("def1234567") : "World" }

        with Schema__Text__Transformation__Response(
            transformed_mapping = transformed_mapping                                                   ,
            transformation_mode = Enum__Text__Transformation__Mode.XXX_RANDOM                           ,
            success             = True                                                                  ,
            total_hashes        = Safe_UInt(2)                                                          ,
            transformed_hashes  = Safe_UInt(1)
        ) as _:
            assert _.success                    is True
            assert _.transformation_mode        == Enum__Text__Transformation__Mode.XXX_RANDOM
            assert _.total_hashes               == 2
            assert _.transformed_hashes         == 1
            assert _.error_message              is None
            assert len(_.transformed_mapping)   == 2

    def test_with_error_response(self):                                             # Test failed transformation response
        original_mapping = { Safe_Str__Hash("abc1234567") : "Hello" }

        with Schema__Text__Transformation__Response(
            transformed_mapping = original_mapping                                                      ,
            transformation_mode = Enum__Text__Transformation__Mode.HASHES_RANDOM                        ,
            success             = False                                                                 ,
            total_hashes        = Safe_UInt(1)                                                          ,
            transformed_hashes  = Safe_UInt(0)                                                          ,
            error_message       = Safe_Str__Text("Transformation failed: Unknown error")
        ) as _:
            assert _.success                    is False
            assert _.total_hashes               == 1
            assert _.transformed_hashes         == 0
            assert _.error_message              == "Transformation failed: Unknown error"

    def test_obj_comparison(self):                                                  # Test .obj() method for state verification
        transformed_mapping = { Safe_Str__Hash("abc1234567") : "aaaaa" }

        with Schema__Text__Transformation__Response(
            transformed_mapping = transformed_mapping                                                   ,
            transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE                        ,
            success             = True                                                                  ,
            total_hashes        = Safe_UInt(1)                                                          ,
            transformed_hashes  = Safe_UInt(1)
        ) as _:
            assert _.obj() == __(transformed_mapping = __(abc1234567 = 'aaaaa')                         ,
                                 transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE   ,
                                 success             = True                                             ,
                                 total_hashes        = 1                                                ,
                                 transformed_hashes  = 1                                                ,
                                 error_message       = None                                             )

    def test_json_round_trip(self):                                                 # Test JSON serialization round-trip
        transformed_mapping = { Safe_Str__Hash("abc1234567") : "Test output" }

        with Schema__Text__Transformation__Response(
            transformed_mapping = transformed_mapping                                                   ,
            transformation_mode = Enum__Text__Transformation__Mode.XXX_RANDOM                           ,
            success             = True                                                                  ,
            total_hashes        = Safe_UInt(5)                                                          ,
            transformed_hashes  = Safe_UInt(3)
        ) as _:
            json_data = _.json()
            restored  = Schema__Text__Transformation__Response(**json_data)

            assert restored.success                    == True
            assert restored.transformation_mode        == Enum__Text__Transformation__Mode.XXX_RANDOM
            assert restored.total_hashes               == 5
            assert restored.transformed_hashes         == 3
            assert "abc1234567"                        in restored.transformed_mapping
            assert restored.obj()                      == __(error_message       = None                        ,
                                                             transformed_mapping = __(abc1234567='Test output'),
                                                             transformation_mode = 'xxx-random'                ,
                                                             success             = True                        ,
                                                             total_hashes        = 5                           ,
                                                             transformed_hashes  = 3                           )
