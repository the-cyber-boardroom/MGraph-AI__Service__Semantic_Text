from unittest                                                                                                           import TestCase
from osbot_utils.type_safe.Type_Safe                                                                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                                      import Safe_Str__Hash
from osbot_utils.utils.Objects                                                                                          import base_classes
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine                   import Text__Transformation__Engine
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine__Hashes_Random    import Text__Transformation__Engine__Hashes_Random
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode                      import Enum__Text__Transformation__Mode


class test_Text__Transformation__Engine__Hashes_Random(TestCase):

    def test__init__(self):                                                         # Test auto-initialization of Text__Transformation__Engine__Hashes_Random
        with Text__Transformation__Engine__Hashes_Random() as _:
            assert type(_)                       is Text__Transformation__Engine__Hashes_Random
            assert base_classes(_)               == [Text__Transformation__Engine, Type_Safe, object]
            assert _.transformation_mode         == Enum__Text__Transformation__Mode.HASHES_RANDOM

    def test_transform__empty_mapping(self):                                        # Test with empty hash mapping
        with Text__Transformation__Engine__Hashes_Random() as _:
            result = _.transform({})
            assert result == {}

    def test_transform__none_selected_hashes__transforms_none(self):                 # Test that None selected_hashes transforms no hashes
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,
        }

        with Text__Transformation__Engine__Hashes_Random() as _:
            result = _.transform(hash_mapping, selected_hashes=None)

            assert len(result)             == 2                                     # Same number of hashes
            assert result[Safe_Str__Hash("abc1234567")] == "Hello"            # All show hash values
            assert result[Safe_Str__Hash("def1234567")] == "World"

    def test_transform__with_selected_hashes__transforms_only_selected(self):       # Test that only selected hashes are transformed
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,
        }

        selected_hashes = [ Safe_Str__Hash("abc1234567") ]                         # Only transform first hash

        with Text__Transformation__Engine__Hashes_Random() as _:
            result = _.transform(hash_mapping, selected_hashes)

            assert len(result)             == 2                                     # Same number of hashes
            assert result[Safe_Str__Hash("abc1234567")] == "abc1234567"            # Selected hash shows hash value
            assert result[Safe_Str__Hash("def1234567")] == "World"                 # Unselected hash unchanged

    def test_transform__empty_selected_hashes__transforms_none(self):               # Test that empty selected_hashes transforms nothing
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,
        }

        selected_hashes = []                                                        # Empty list

        with Text__Transformation__Engine__Hashes_Random() as _:
            result = _.transform(hash_mapping, selected_hashes)

            assert len(result)             == 2                                     # Same number of hashes
            assert result[Safe_Str__Hash("abc1234567")] == "Hello"                 # Both unchanged
            assert result[Safe_Str__Hash("def1234567")] == "World"

    def test_transform__partial_selection(self):                                    # Test transforming some hashes
        hash_mapping = {
            Safe_Str__Hash("aaa1234567") : "First"                                  ,
            Safe_Str__Hash("bbb1234567") : "Second"                                 ,
            Safe_Str__Hash("ccc1234567") : "Third"                                  ,
        }

        selected_hashes = [
            Safe_Str__Hash("aaa1234567")                                            ,
            Safe_Str__Hash("ccc1234567")                                            ,
        ]

        with Text__Transformation__Engine__Hashes_Random() as _:
            result = _.transform(hash_mapping, selected_hashes)

            assert result[Safe_Str__Hash("aaa1234567")] == "aaa1234567"            # First shows hash
            assert result[Safe_Str__Hash("bbb1234567")] == "Second"                # Second unchanged
            assert result[Safe_Str__Hash("ccc1234567")] == "ccc1234567"            # Third shows hash

    def test_transform__single_item(self):                                          # Test with single hash
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Only Text"                              ,
        }

        with Text__Transformation__Engine__Hashes_Random() as _:
            result = _.transform(hash_mapping, selected_hashes=['abc1234567'])

            assert len(result)             == 1
            assert Safe_Str__Hash("abc1234567") in result
            assert result[Safe_Str__Hash("abc1234567")] == "abc1234567"

    def test_transform__hash_format(self):                                          # Test that hash values are properly formatted
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Test"                                   ,
        }

        with Text__Transformation__Engine__Hashes_Random() as _:
            result             = _.transform(hash_mapping, selected_hashes=['abc1234567'])
            transformed_value = result[Safe_Str__Hash("abc1234567")]
            assert transformed_value == "abc1234567"                                # Hash as string
            assert isinstance(transformed_value, str)                               # Is string type

    def test_obj_comparison(self):                                                  # Test .obj() for state verification
        with Text__Transformation__Engine__Hashes_Random() as _:
            obj = _.obj()
            assert obj.transformation_mode   == Enum__Text__Transformation__Mode.HASHES_RANDOM
