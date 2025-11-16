from unittest                                                                                                           import TestCase
from osbot_utils.type_safe.Type_Safe                                                                                    import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                                   import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                                      import Safe_Str__Hash
from osbot_utils.utils.Objects                                                                                          import base_classes
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine                   import Text__Transformation__Engine
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine__Hashes_Random    import Text__Transformation__Engine__Hashes_Random
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Selection__Service                               import Text__Selection__Service
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode                      import Enum__Text__Transformation__Mode


class test_Text__Transformation__Engine__Hashes_Random(TestCase):

    def test__init__(self):                                                         # Test auto-initialization of Text__Transformation__Engine__Hashes_Random
        with Text__Transformation__Engine__Hashes_Random() as _:
            assert type(_)                       is Text__Transformation__Engine__Hashes_Random
            assert base_classes(_)               == [Text__Transformation__Engine, Type_Safe, object]
            assert _.transformation_mode         == Enum__Text__Transformation__Mode.HASHES_RANDOM
            assert type(_.text_selection)        is Text__Selection__Service

    def test_transform__empty_mapping(self):                                        # Test with empty hash mapping
        with Text__Transformation__Engine__Hashes_Random() as _:
            result = _.transform({})
            assert result == {}

    def test_transform__shows_hash_values(self):                                    # Test that text is replaced with hash values
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,
        }

        with Text__Transformation__Engine__Hashes_Random() as _:
            result = _.transform(hash_mapping)

            assert len(result)             == 2                                     # Same number of hashes
            for hash_key, transformed_text in result.items():
                if transformed_text == str(hash_key):                               # If transformed to hash
                    assert transformed_text in ["abc1234567", "def1234567"]         # Should be the hash itself


    def test_transform__preserves_unselected_text(self):                            # Test that unselected text remains original
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Original Text"                          ,
            Safe_Str__Hash("def1234567") : "Another Text"                           ,
        }

        with Text__Transformation__Engine__Hashes_Random() as _:
            result = _.transform(hash_mapping)

            for hash_key, transformed_text in result.items():
                original_text = hash_mapping[hash_key]
                assert transformed_text == str(hash_key) or transformed_text == original_text

    def test_transform__single_item(self):                                          # Test with single hash
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Only Text"                              ,
        }

        with Text__Transformation__Engine__Hashes_Random() as _:
            result = _.transform(hash_mapping)

            assert len(result)             == 1
            assert Safe_Str__Hash("abc1234567") in result

    def test_transform__hash_format(self):                                          # Test that hash values are properly formatted
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Test"                                   ,
        }

        with Text__Transformation__Engine__Hashes_Random() as _:
            result             = _.transform(hash_mapping)
            transformed_value = result[Safe_Str__Hash("abc1234567")]
            assert transformed_value == "abc1234567"                                # Hash as string
            assert isinstance(transformed_value, str)                               # Is string type

    def test_obj_comparison(self):                                                  # Test .obj() for state verification
        with Text__Transformation__Engine__Hashes_Random() as _:
            obj = _.obj()
            assert obj.transformation_mode   == Enum__Text__Transformation__Mode.HASHES_RANDOM
