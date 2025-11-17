from unittest                                                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                                  import Safe_Str__Hash
from osbot_utils.utils.Objects                                                                                      import base_classes
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine               import Text__Transformation__Engine
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine__XXX_Random   import Text__Transformation__Engine__XXX_Random
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode                  import Enum__Text__Transformation__Mode


class test_Text__Transformation__Engine__XXX_Random(TestCase):

    def test__init__(self):                                                         # Test auto-initialization of Text__Transformation__Engine__XXX_Random
        with Text__Transformation__Engine__XXX_Random() as _:
            assert type(_)                       is Text__Transformation__Engine__XXX_Random
            assert base_classes(_)               == [Text__Transformation__Engine, Type_Safe, object]
            assert _.transformation_mode         == Enum__Text__Transformation__Mode.XXX

    def test_transform__empty_mapping(self):                                        # Test with empty hash mapping
        with Text__Transformation__Engine__XXX_Random() as _:
            result = _.transform({})
            assert result == {}

    def test_transform__none_selected_hashes__transforms_none(self):                 # Test that None selected_hashes transforms all hashes
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,
        }

        with Text__Transformation__Engine__XXX_Random() as _:
            result = _.transform(hash_mapping, selected_hashes=None)

            assert len(result)             == 2                                     # Same number of hashes
            for hash_key, masked_text in result.items():
                assert 'x' not in masked_text                                       # All should not be masked
                assert masked_text == hash_mapping[hash_key]                        # All should be equal

    def test_transform__with_selected_hashes__transforms_only_selected(self):       # Test that only selected hashes are transformed
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,
        }

        selected_hashes = [ Safe_Str__Hash("abc1234567") ]                         # Only transform first hash

        with Text__Transformation__Engine__XXX_Random() as _:
            result = _.transform(hash_mapping, selected_hashes)

            assert len(result)             == 2                                     # Same number of hashes
            assert 'x' in result[Safe_Str__Hash("abc1234567")]                     # Selected hash is masked
            assert result[Safe_Str__Hash("def1234567")] == "World"                 # Unselected hash unchanged

    def test_transform__empty_selected_hashes__transforms_none(self):               # Test that empty selected_hashes transforms nothing
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,
        }

        selected_hashes = []                                                        # Empty list

        with Text__Transformation__Engine__XXX_Random() as _:
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

        with Text__Transformation__Engine__XXX_Random() as _:
            result = _.transform(hash_mapping, selected_hashes)

            assert 'x' in result[Safe_Str__Hash("aaa1234567")]                     # First transformed
            assert result[Safe_Str__Hash("bbb1234567")] == "Second"                # Second unchanged
            assert 'x' in result[Safe_Str__Hash("ccc1234567")]                     # Third transformed

    def test_mask_text__alphanumeric(self):                                         # Test masking alphanumeric characters
        with Text__Transformation__Engine__XXX_Random() as _:
            assert _._mask_text("Hello")   == "xxxxx"
            assert _._mask_text("World")   == "xxxxx"
            assert _._mask_text("ABC123")  == "xxxxxx"

    def test_mask_text__preserves_whitespace(self):                                 # Test that whitespace is preserved
        with Text__Transformation__Engine__XXX_Random() as _:
            assert _._mask_text("Hello World")      == "xxxxx xxxxx"
            assert _._mask_text("A B C")            == "x x x"
            assert _._mask_text("Multi  spaces")    == "xxxxx  xxxxxx"

    def test_mask_text__preserves_punctuation(self):                                # Test that punctuation is preserved
        with Text__Transformation__Engine__XXX_Random() as _:
            assert _._mask_text("Hello, World!")    == "xxxxx, xxxxx!"
            assert _._mask_text("Yes!")             == "xxx!"
            assert _._mask_text("What?")            == "xxxx?"
            assert _._mask_text("Hi: there")        == "xx: xxxxx"

    def test_mask_text__empty_string(self):                                         # Test with empty string
        with Text__Transformation__Engine__XXX_Random() as _:
            assert _._mask_text("")                 == ""

    def test_mask_text__special_characters(self):                                   # Test with various special characters
        with Text__Transformation__Engine__XXX_Random() as _:
            assert _._mask_text("$100")             == "$xxx"
            assert _._mask_text("user@example.com") == "xxxx@xxxxxxx.xxx"
            assert _._mask_text("(123) 456-7890")   == "(xxx) xxx-xxxx"

    def test_obj_comparison(self):                                                  # Test .obj() for state verification
        with Text__Transformation__Engine__XXX_Random() as _:
            obj = _.obj()
            assert obj.transformation_mode   == Enum__Text__Transformation__Mode.XXX
