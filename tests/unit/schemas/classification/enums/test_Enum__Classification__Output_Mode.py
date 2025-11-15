from unittest                                                                                       import TestCase
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode import Enum__Classification__Output_Mode


class test_Enum__Classification__Output_Mode(TestCase):

    def test__init__(self):                                                    # Test enum values and types
        assert Enum__Classification__Output_Mode.HASHES_ONLY      == 'hashes-only'
        assert Enum__Classification__Output_Mode.HASHES_WITH_TEXT == 'hashes-with-text'
        assert Enum__Classification__Output_Mode.FULL_RATINGS     == 'full-ratings'
        assert Enum__Classification__Output_Mode.SEPARATED        == 'separated'
        assert Enum__Classification__Output_Mode.COMBINED         == 'combined'

        assert type(Enum__Classification__Output_Mode.HASHES_ONLY     ) is Enum__Classification__Output_Mode
        assert type(Enum__Classification__Output_Mode.HASHES_WITH_TEXT) is Enum__Classification__Output_Mode
        assert type(Enum__Classification__Output_Mode.FULL_RATINGS    ) is Enum__Classification__Output_Mode
        assert type(Enum__Classification__Output_Mode.SEPARATED       ) is Enum__Classification__Output_Mode
        assert type(Enum__Classification__Output_Mode.COMBINED        ) is Enum__Classification__Output_Mode

    def test_enum_members(self):                                               # Test enum member count and names
        members = list(Enum__Classification__Output_Mode)
        assert len(members) == 5

        member_names = [m.name for m in members]
        assert 'HASHES_ONLY'      in member_names
        assert 'HASHES_WITH_TEXT' in member_names
        assert 'FULL_RATINGS'     in member_names
        assert 'SEPARATED'        in member_names
        assert 'COMBINED'         in member_names

    def test_string_conversion(self):                                          # Test conversion from string
        assert Enum__Classification__Output_Mode('hashes-only'     ) == Enum__Classification__Output_Mode.HASHES_ONLY
        assert Enum__Classification__Output_Mode('hashes-with-text') == Enum__Classification__Output_Mode.HASHES_WITH_TEXT
        assert Enum__Classification__Output_Mode('full-ratings'    ) == Enum__Classification__Output_Mode.FULL_RATINGS
        assert Enum__Classification__Output_Mode('separated'       ) == Enum__Classification__Output_Mode.SEPARATED
        assert Enum__Classification__Output_Mode('combined'        ) == Enum__Classification__Output_Mode.COMBINED
