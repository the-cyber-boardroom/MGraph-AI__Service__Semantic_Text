from unittest                                                                                                         import TestCase
from osbot_utils.testing.__                                                                                           import __
from osbot_utils.type_safe.Type_Safe                                                                                  import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                                  import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                                    import Safe_Str__Hash
from osbot_utils.utils.Objects                                                                                        import base_classes
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine                 import Text__Transformation__Engine
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine__ABCDE_By_Size  import Text__Transformation__Engine__ABCDE_By_Size
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Grouping__Service                              import Text__Grouping__Service
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode                    import Enum__Text__Transformation__Mode


class test_Text__Transformation__Engine__ABCDE_By_Size(TestCase):

    def test__init__(self):                                                         # Test auto-initialization of Text__Transformation__Engine__ABCDE_By_Size
        with Text__Transformation__Engine__ABCDE_By_Size() as _:
            assert type(_)                       is Text__Transformation__Engine__ABCDE_By_Size
            assert base_classes(_)               == [Text__Transformation__Engine, Type_Safe, object]
            assert _.transformation_mode         == Enum__Text__Transformation__Mode.ABCDE_BY_SIZE
            assert _.randomness_percentage       == 0.5
            assert type(_.text_grouping)         is Text__Grouping__Service
            assert _.num_groups                  == 5                               # Default 5 groups

    def test_setup(self):                                                           # Test setup configures text_grouping with num_groups
        with Text__Transformation__Engine__ABCDE_By_Size(num_groups=Safe_UInt(3)) as _:
            _.setup()
            assert _.text_grouping.num_groups == 3

    def test_transform__empty_mapping(self):                                        # Test with empty hash mapping
        with Text__Transformation__Engine__ABCDE_By_Size() as _:
            _.setup()
            result = _.transform({})
            assert result == {}

    def test_transform__groups_by_length(self):                                     # Test that text is grouped by length and replaced with letters
        hash_mapping = { Safe_Str__Hash("a123456789") : "A"     ,                   # Length 1 → group 0 → 'a'
                         Safe_Str__Hash("b123456789") : "BB"    ,                   # Length 2 → group 1 → 'b'
                         Safe_Str__Hash("c123456789") : "CCC"   ,                   # Length 3 → group 2 → 'c'
                         Safe_Str__Hash("d123456789") : "DDDD"  ,                   # Length 4 → group 3 → 'd'
                         Safe_Str__Hash("e123456789") : "EEEEE" }                   # Length 5 → group 4 → 'e'


        with Text__Transformation__Engine__ABCDE_By_Size() as _:
            _.setup()
            result = _.transform(hash_mapping)
            assert type(result) is dict
            assert result       == { Safe_Str__Hash('a123456789'): 'a',
                                     Safe_Str__Hash('b123456789'): 'bb',
                                     Safe_Str__Hash('c123456789'): 'ccc',
                                     Safe_Str__Hash('d123456789'): 'dddd',
                                     Safe_Str__Hash('e123456789'): 'eeeee'}

            assert result[Safe_Str__Hash("a123456789")] == "a"                      # Shortest → 'a'
            assert result[Safe_Str__Hash("b123456789")] == "bb"                     # Next → 'b'
            assert result[Safe_Str__Hash("c123456789")] == "ccc"                    # Next → 'c'
            assert result[Safe_Str__Hash("d123456789")] == "dddd"                   # Next → 'd'
            assert result[Safe_Str__Hash("e123456789")] == "eeeee"                  # Longest → 'e'

    def test_replace_with_letter__alphanumeric(self):                               # Test replacing alphanumeric characters with letter
        with Text__Transformation__Engine__ABCDE_By_Size() as _:
            assert _._replace_with_letter("Hello", "a" ) == "aaaaa"
            assert _._replace_with_letter("World", "b" ) == "bbbbb"
            assert _._replace_with_letter("ABC123", "c") == "cccccc"

    def test_replace_with_letter__preserves_whitespace(self):                       # Test that whitespace is preserved
        with Text__Transformation__Engine__ABCDE_By_Size() as _:
            assert _._replace_with_letter("Hello World", "a") == "aaaaa aaaaa"
            assert _._replace_with_letter("A B C", "b") == "b b b"
            assert _._replace_with_letter("Multi  spaces", "c") == "ccccc  cccccc"

    def test_replace_with_letter__preserves_punctuation(self):                      # Test that punctuation is preserved
        with Text__Transformation__Engine__ABCDE_By_Size() as _:
            assert _._replace_with_letter("Hello, World!", "a") == "aaaaa, aaaaa!"
            assert _._replace_with_letter("Yes!"         , "b") == "bbb!"
            assert _._replace_with_letter("What?"        , "c") == "cccc?"

    def test_replace_with_letter__empty_string(self):                               # Test with empty string
        with Text__Transformation__Engine__ABCDE_By_Size() as _:
            assert _._replace_with_letter("", "a") == ""

    def test_transform__3_groups(self):                                             # Test with 3 groups instead of 5
        hash_mapping = {
            Safe_Str__Hash("a123456789") : "Hi"                                      ,   # Length 2
            Safe_Str__Hash("b123456789") : "Hello"                                   ,   # Length 5
            Safe_Str__Hash("c123456789") : "World"                                   ,   # Length 5
        }

        with Text__Transformation__Engine__ABCDE_By_Size(num_groups=Safe_UInt(3)) as _:
            _.setup()
            result = _.transform(hash_mapping)

            assert 'a' in result[Safe_Str__Hash("a123456789")]                      # Shortest gets 'a'
            assert 'b' in result[Safe_Str__Hash("b123456789")] or 'c' in result[Safe_Str__Hash("b123456789")]

    def test_transform__mixed_lengths(self):                                        # Test with mixed text lengths
        hash_mapping = {
            Safe_Str__Hash("a123456789") : "x"                                       ,
            Safe_Str__Hash("b123456789") : "yy"                                      ,
            Safe_Str__Hash("c123456789") : "zzz"                                     ,
            Safe_Str__Hash("d123456789") : "wwww"                                    ,
            Safe_Str__Hash("e123456789") : "vvvvv"                                   ,
            Safe_Str__Hash("f123456789") : "uuuuuu"                                  ,
            Safe_Str__Hash("0123456789") : "ttttttt"                                 ,
            Safe_Str__Hash("1123456789") : "ssssssss"                                ,
            Safe_Str__Hash("2123456789") : "rrrrrrrrr"                               ,
            Safe_Str__Hash("3123456789") : "qqqqqqqqqq"                              ,
        }

        with Text__Transformation__Engine__ABCDE_By_Size() as _:
            _.setup()
            result = _.transform(hash_mapping)

            assert len(result)             == 10                                    # All hashes transformed
            unique_letters = set()
            for text in result.values():
                if text:
                    unique_letters.add(text[0])

            assert len(unique_letters)     <= 5                                     # At most 5 different letters

    def test_transform__preserves_special_chars(self):                              # Test that special characters are preserved
        hash_mapping = {
            Safe_Str__Hash("a123456789") : "Hello, World!"                           ,
        }

        with Text__Transformation__Engine__ABCDE_By_Size() as _:
            _.setup()
            result = _.transform(hash_mapping)

            transformed = result[Safe_Str__Hash("a123456789")]
            assert ", " in transformed                                              # Comma and space preserved
            assert "!" in transformed                                               # Exclamation preserved

    def test_transform__single_item(self):                                          # Test with single hash
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Only Text"                              ,
        }

        with Text__Transformation__Engine__ABCDE_By_Size() as _:
            _.setup()
            result = _.transform(hash_mapping)

            assert len(result)             == 1
            assert Safe_Str__Hash("abc1234567") in result
            assert 'a' in result[Safe_Str__Hash("abc1234567")]                     # Should be first group

    def test_obj_comparison(self):                                                  # Test .obj() for state verification
        with Text__Transformation__Engine__ABCDE_By_Size(num_groups=Safe_UInt(7)) as _:
            obj = _.obj()
            assert obj.transformation_mode   == Enum__Text__Transformation__Mode.ABCDE_BY_SIZE
            assert obj.num_groups            == 7
