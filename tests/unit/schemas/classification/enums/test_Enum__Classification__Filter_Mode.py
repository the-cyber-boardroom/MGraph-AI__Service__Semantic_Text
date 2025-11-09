from unittest                                                                                       import TestCase
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode import Enum__Classification__Filter_Mode


class test_Enum__Classification__Filter_Mode(TestCase):

    def test__init__(self):                                                    # Test enum values and types
        assert Enum__Classification__Filter_Mode.ABOVE   == 'above'
        assert Enum__Classification__Filter_Mode.BELOW   == 'below'
        assert Enum__Classification__Filter_Mode.BETWEEN == 'between'
        assert Enum__Classification__Filter_Mode.EQUALS  == 'equals'

        assert type(Enum__Classification__Filter_Mode.ABOVE  ) is Enum__Classification__Filter_Mode
        assert type(Enum__Classification__Filter_Mode.BELOW  ) is Enum__Classification__Filter_Mode
        assert type(Enum__Classification__Filter_Mode.BETWEEN) is Enum__Classification__Filter_Mode
        assert type(Enum__Classification__Filter_Mode.EQUALS ) is Enum__Classification__Filter_Mode

    def test_enum_members(self):                                               # Test enum member count and names
        members = list(Enum__Classification__Filter_Mode)
        assert len(members) == 4

        member_names = [m.name for m in members]
        assert 'ABOVE'   in member_names
        assert 'BELOW'   in member_names
        assert 'BETWEEN' in member_names
        assert 'EQUALS'  in member_names

    def test_string_conversion(self):                                          # Test conversion from string
        assert Enum__Classification__Filter_Mode('above'  ) == Enum__Classification__Filter_Mode.ABOVE
        assert Enum__Classification__Filter_Mode('below'  ) == Enum__Classification__Filter_Mode.BELOW
        assert Enum__Classification__Filter_Mode('between') == Enum__Classification__Filter_Mode.BETWEEN
        assert Enum__Classification__Filter_Mode('equals' ) == Enum__Classification__Filter_Mode.EQUALS
