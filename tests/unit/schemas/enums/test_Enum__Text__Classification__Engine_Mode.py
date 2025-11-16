from unittest                                                                                   import TestCase
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Engine_Mode     import Enum__Text__Classification__Engine_Mode


class test_Enum__Text__Classification__Engine_Mode(TestCase):

    def test__enum_values(self):                                                # Test all enum values exist and have correct string values
        assert Enum__Text__Classification__Engine_Mode.AWS_COMPREHEND.value == 'aws_comprehend'
        assert Enum__Text__Classification__Engine_Mode.TEXT_HASH.value      == 'text_hash'
        assert Enum__Text__Classification__Engine_Mode.RANDOM.value         == 'random'
        assert Enum__Text__Classification__Engine_Mode.LLM_SINGLE.value     == 'llm_single'
        assert Enum__Text__Classification__Engine_Mode.LLM_MULTIPLE.value   == 'llm_multiple'

    def test__enum_members(self):                                               # Test all expected members exist
        expected_members = {'AWS_COMPREHEND', 'TEXT_HASH', 'RANDOM', 'LLM_SINGLE', 'LLM_MULTIPLE'}
        actual_members   = {member.name for member in Enum__Text__Classification__Engine_Mode}

        assert actual_members == expected_members

    def test__enum_count(self):                                                 # Test total number of enum members
        assert len(Enum__Text__Classification__Engine_Mode) == 5

    def test__string_conversion(self):                                          # Test that enum can be compared with strings
        assert Enum__Text__Classification__Engine_Mode.AWS_COMPREHEND == 'aws_comprehend'
        assert Enum__Text__Classification__Engine_Mode.TEXT_HASH      == 'text_hash'
        assert Enum__Text__Classification__Engine_Mode.RANDOM         == 'random'

    def test__enum_from_string(self):                                           # Test creating enum from string value
        assert Enum__Text__Classification__Engine_Mode('aws_comprehend') == Enum__Text__Classification__Engine_Mode.AWS_COMPREHEND
        assert Enum__Text__Classification__Engine_Mode('text_hash')      == Enum__Text__Classification__Engine_Mode.TEXT_HASH
        assert Enum__Text__Classification__Engine_Mode('random')         == Enum__Text__Classification__Engine_Mode.RANDOM

    def test__enum_iteration(self):                                             # Test iterating over enum members
        modes = list(Enum__Text__Classification__Engine_Mode)

        assert len(modes) == 5
        assert Enum__Text__Classification__Engine_Mode.AWS_COMPREHEND   in modes
        assert Enum__Text__Classification__Engine_Mode.TEXT_HASH        in modes
        assert Enum__Text__Classification__Engine_Mode.RANDOM           in modes
        assert Enum__Text__Classification__Engine_Mode.LLM_SINGLE       in modes
        assert Enum__Text__Classification__Engine_Mode.LLM_MULTIPLE     in modes

    def test__enum_uniqueness(self):                                            # Test all enum values are unique
        values = [mode.value for mode in Enum__Text__Classification__Engine_Mode]
        assert len(values) == len(set(values))                                  # No duplicates