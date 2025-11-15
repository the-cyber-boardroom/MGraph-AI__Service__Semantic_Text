from unittest                                                                                           import TestCase
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Logic_Operator  import Enum__Classification__Logic_Operator


class test_Enum__Classification__Logic_Operator(TestCase):

    def test__init__(self):                                                    # Test enum values and types
        assert Enum__Classification__Logic_Operator.AND == 'and'
        assert Enum__Classification__Logic_Operator.OR  == 'or'

        assert type(Enum__Classification__Logic_Operator.AND) is Enum__Classification__Logic_Operator
        assert type(Enum__Classification__Logic_Operator.OR ) is Enum__Classification__Logic_Operator

    def test_enum_members(self):                                               # Test enum member count and names
        members = list(Enum__Classification__Logic_Operator)
        assert len(members) == 2

        member_names = [m.name for m in members]
        assert 'AND' in member_names
        assert 'OR'  in member_names

    def test_string_conversion(self):                                          # Test conversion from string
        assert Enum__Classification__Logic_Operator('and') == Enum__Classification__Logic_Operator.AND
        assert Enum__Classification__Logic_Operator('or' ) == Enum__Classification__Logic_Operator.OR