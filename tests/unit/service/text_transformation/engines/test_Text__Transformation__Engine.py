from unittest                                                                                             import TestCase
from osbot_utils.testing.__                                                                               import __
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from osbot_utils.utils.Objects                                                                            import base_classes
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine     import Text__Transformation__Engine
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode        import Enum__Text__Transformation__Mode


class test_Text__Transformation__Engine(TestCase):

    def test__init__(self):                                                         # Test auto-initialization of Text__Transformation__Engine
        with Text__Transformation__Engine() as _:
            assert type(_)                       is Text__Transformation__Engine
            assert base_classes(_)               == [Type_Safe, object]

    def test_with_mode(self):                                                       # Test engine with specific transformation mode
        with Text__Transformation__Engine(
            transformation_mode   = Enum__Text__Transformation__Mode.XXX_RANDOM     ,
        ) as _:
            assert _.transformation_mode   == Enum__Text__Transformation__Mode.XXX_RANDOM

    def test_transform_not_implemented(self):                                       # Test that transform raises NotImplementedError
        hash_mapping = { Safe_Str__Hash("abc1234567") : "Hello" }

        with Text__Transformation__Engine() as _:
            try:
                _.transform(hash_mapping)
                assert False, "Should have raised NotImplementedError"
            except NotImplementedError as e:
                assert "Subclass must implement transform() method" in str(e)

    def test_obj_comparison(self):                                                  # Test .obj() for state verification
        with Text__Transformation__Engine(transformation_mode   = Enum__Text__Transformation__Mode.HASHES_RANDOM) as _:
            assert _.obj() == __(transformation_mode   = Enum__Text__Transformation__Mode.HASHES_RANDOM  )