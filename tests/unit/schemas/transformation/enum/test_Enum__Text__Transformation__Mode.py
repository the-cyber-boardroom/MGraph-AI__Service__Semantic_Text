from unittest                                                                                             import TestCase
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode        import Enum__Text__Transformation__Mode


class test_Enum__Text__Transformation__Mode(TestCase):

    def test__init__(self):                                                         # Test enum values and types
        assert Enum__Text__Transformation__Mode.XXX == 'xxx'
        assert Enum__Text__Transformation__Mode.HASHES == 'hashes'
        assert Enum__Text__Transformation__Mode.ABCDE_BY_SIZE == 'abcde-by-size'

        assert type(Enum__Text__Transformation__Mode.XXX) is Enum__Text__Transformation__Mode
        assert type(Enum__Text__Transformation__Mode.HASHES) is Enum__Text__Transformation__Mode
        assert type(Enum__Text__Transformation__Mode.ABCDE_BY_SIZE) is Enum__Text__Transformation__Mode

    def test_enum_members(self):                                                    # Test enum member count and names
        members = list(Enum__Text__Transformation__Mode)
        assert len(members) == 3

        member_names = [m.name for m in members]
        assert 'XXX'           in member_names
        assert 'HASHES'        in member_names
        assert 'ABCDE_BY_SIZE' in member_names

    def test_string_conversion(self):                                               # Test conversion from string
        assert Enum__Text__Transformation__Mode('xxx'          ) == Enum__Text__Transformation__Mode.XXX
        assert Enum__Text__Transformation__Mode('hashes'       ) == Enum__Text__Transformation__Mode.HASHES
        assert Enum__Text__Transformation__Mode('abcde-by-size') == Enum__Text__Transformation__Mode.ABCDE_BY_SIZE