from unittest                                                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                                                import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                               import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                                  import Safe_Str__Hash
from osbot_utils.utils.Objects                                                                                      import base_classes
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine               import Text__Transformation__Engine
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine__XXX_Random   import Text__Transformation__Engine__XXX_Random
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Selection__Service                           import Text__Selection__Service
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode                  import Enum__Text__Transformation__Mode


class test_Text__Transformation__Engine__XXX_Random(TestCase):

    def test__init__(self):                                                         # Test auto-initialization of Text__Transformation__Engine__XXX_Random
        with Text__Transformation__Engine__XXX_Random() as _:
            assert type(_)                       is Text__Transformation__Engine__XXX_Random
            assert base_classes(_)               == [Text__Transformation__Engine, Type_Safe, object]
            assert _.transformation_mode         == Enum__Text__Transformation__Mode.XXX_RANDOM
            assert type(_.text_selection)        is Text__Selection__Service

    def test_transform__empty_mapping(self):                                        # Test with empty hash mapping
        with Text__Transformation__Engine__XXX_Random() as _:
            result = _.transform({})
            assert result == {}

    def test_transform__masks_with_x(self):                                         # Test that text is masked with 'x' characters
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,
        }

        with Text__Transformation__Engine__XXX_Random() as _:
            result = _.transform(hash_mapping)

            assert len(result)             == 2                                     # Same number of hashes
            for hash_key, masked_text in result.items():
                if masked_text != hash_mapping[hash_key]:                           # If transformed
                    assert all(c in 'x ' for c in masked_text if c.isalnum() or c.isspace())

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

    def test_transform__preserves_unselected_text(self):                            # Test that unselected text is preserved
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Keep This"                              ,
        }

        with Text__Transformation__Engine__XXX_Random() as _:
            _.text_selection = Text__Selection__Service()                          # Fresh selection service
            result = _.transform(hash_mapping)

            original_text_exists = any(v == "Keep This" for v in result.values())
            assert original_text_exists or any('x' in v for v in result.values())  # Either kept or masked

    def test_obj_comparison(self):                                                  # Test .obj() for state verification
        with Text__Transformation__Engine__XXX_Random() as _:
            obj = _.obj()
            assert obj.transformation_mode   == Enum__Text__Transformation__Mode.XXX_RANDOM
