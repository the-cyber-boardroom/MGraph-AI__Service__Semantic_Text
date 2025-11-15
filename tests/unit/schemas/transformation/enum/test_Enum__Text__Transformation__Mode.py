from unittest                                                                                             import TestCase
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode        import Enum__Text__Transformation__Mode


class test_Enum__Text__Transformation__Mode(TestCase):

    def test__init__(self):                                                         # Test enum values and types
        assert Enum__Text__Transformation__Mode.XXX_RANDOM    == 'xxx-random'
        assert Enum__Text__Transformation__Mode.HASHES_RANDOM == 'hashes-random'
        assert Enum__Text__Transformation__Mode.ABCDE_BY_SIZE == 'abcde-by-size'

        assert type(Enum__Text__Transformation__Mode.XXX_RANDOM   ) is Enum__Text__Transformation__Mode
        assert type(Enum__Text__Transformation__Mode.HASHES_RANDOM) is Enum__Text__Transformation__Mode
        assert type(Enum__Text__Transformation__Mode.ABCDE_BY_SIZE) is Enum__Text__Transformation__Mode

    def test_enum_members(self):                                                    # Test enum member count and names
        members = list(Enum__Text__Transformation__Mode)
        assert len(members) == 3

        member_names = [m.name for m in members]
        assert 'XXX_RANDOM'    in member_names
        assert 'HASHES_RANDOM' in member_names
        assert 'ABCDE_BY_SIZE' in member_names

    def test_string_conversion(self):                                               # Test conversion from string
        assert Enum__Text__Transformation__Mode('xxx-random'   ) == Enum__Text__Transformation__Mode.XXX_RANDOM
        assert Enum__Text__Transformation__Mode('hashes-random') == Enum__Text__Transformation__Mode.HASHES_RANDOM
        assert Enum__Text__Transformation__Mode('abcde-by-size') == Enum__Text__Transformation__Mode.ABCDE_BY_SIZE