from unittest                                                                                             import TestCase
from osbot_utils.testing.__                                                                               import __
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from osbot_utils.utils.Objects                                                                            import base_classes
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Grouping__Service                  import Text__Grouping__Service


class test_Text__Grouping__Service(TestCase):

    def test__init__(self):                                                         # Test auto-initialization of Text__Grouping__Service
        with Text__Grouping__Service() as _:
            assert type(_)             is Text__Grouping__Service
            assert base_classes(_)     == [Type_Safe, object]
            assert type(_.num_groups)  is Safe_UInt
            assert _.num_groups        == 5                                         # Default value

    def test_group_by_length__empty_mapping(self):                                  # Test with empty hash mapping
        with Text__Grouping__Service() as _:
            groups = _.group_by_length({})
            assert groups == {}

    def test_group_by_length__fewer_items_than_groups(self):                        # Test with fewer items than groups
        hash_mapping = { Safe_Str__Hash("abc1234567") : "Hi"                                     ,
                         Safe_Str__Hash("def1234567") : "Hello"                                  }

        with Text__Grouping__Service(num_groups=Safe_UInt(5)) as _:
            groups = _.group_by_length(hash_mapping)

            assert len(groups)         == 2                                         # Only 2 groups created
            assert len(groups[0])      == 1                                         # One item per group
            assert len(groups[1])      == 1

    def test_group_by_length__equal_distribution(self):                             # Test equal distribution across groups
        hash_mapping = { Safe_Str__Hash("a123456789") : "A"     ,                    # Length 1
                         Safe_Str__Hash("b123456789") : "BB"    ,                    # Length 2
                         Safe_Str__Hash("c123456789") : "CCC"   ,                    # Length 3
                         Safe_Str__Hash("d123456789") : "DDDD"  ,                    # Length 4
                         Safe_Str__Hash("e123456789") : "EEEEE" }                    # Length 5

        with Text__Grouping__Service(num_groups=Safe_UInt(5)) as _:
            groups = _.group_by_length(hash_mapping)

            assert len(groups)         == 5                                         # All 5 groups used
            assert len(groups[0])      == 1                                         # One item per group
            assert len(groups[1])      == 1
            assert len(groups[2])      == 1
            assert len(groups[3])      == 1
            assert len(groups[4])      == 1

    def test_group_by_length__sorted_by_length(self):                               # Test that items are sorted by length
        hash_mapping = { Safe_Str__Hash("a123456789") : "EEEEE" ,                   # Length 5
                         Safe_Str__Hash("b123456789") : "A"     ,                   # Length 1
                         Safe_Str__Hash("c123456789") : "CCC"   }                   # Length 3

        with Text__Grouping__Service(num_groups=Safe_UInt(3)) as _:
            groups = _.group_by_length(hash_mapping)

            assert len(groups)                 == 3
            assert Safe_Str__Hash("b123456789") in groups[0]                         # Shortest in group 0
            assert Safe_Str__Hash("c123456789") in groups[1]                         # Medium in group 1
            assert Safe_Str__Hash("a123456789") in groups[2]                         # Longest in group 2
            assert groups == {0: [Safe_Str__Hash('b123456789')],
                              1: [Safe_Str__Hash('c123456789')],
                              2: [Safe_Str__Hash('a123456789')]}

    def test_group_by_length__with_remainder(self):                                 # Test distribution with remainder
        hash_mapping = { Safe_Str__Hash(f"b{i:09d}") : "a" * (i + 1)
                        for i in range(7)                           }               # 7 items, 5 groups = 2 remainder


        with Text__Grouping__Service(num_groups=Safe_UInt(5)) as _:
            groups = _.group_by_length(hash_mapping)

            total_items = sum(len(hashes) for hashes in groups.values())
            assert total_items         == 7                                         # All items distributed
            assert len(groups[0])      == 2                                         # First groups get extra items
            assert len(groups[1])      == 2
            assert groups              == {0: [Safe_Str__Hash('b000000000'), Safe_Str__Hash('b000000001')],
                                           1: [Safe_Str__Hash('b000000002'), Safe_Str__Hash('b000000003')],
                                           2: [Safe_Str__Hash('b000000004')],
                                           3: [Safe_Str__Hash('b000000005')],
                                           4: [Safe_Str__Hash('b000000006')]}

    def test_get_group_stats(self):                                                 # Test statistics generation for groups
        hash_mapping = { Safe_Str__Hash("a123456789") : "Hi"    ,                   # Length 2
                         Safe_Str__Hash("b123456789") : "Hello" ,                   # Length 5
                         Safe_Str__Hash("c123456789") : "World" }                   # Length 5


        with Text__Grouping__Service(num_groups=Safe_UInt(2)) as _:
            groups = _.group_by_length(hash_mapping)
            stats  = _.get_group_stats(hash_mapping, groups)
            assert groups == { 0: [Safe_Str__Hash('a123456789'), Safe_Str__Hash('b123456789')],
                               1: [Safe_Str__Hash('c123456789')]}
            assert stats  == { 0: { 'avg_length': 3.5,
                                    'count'     : 2,
                                    'max_length': 5,
                                    'min_length': 2,
                                    'sample_texts': ['Hi', 'Hello']},
                               1: { 'avg_length': 5.0,
                                    'count'     : 1,
                                    'max_length': 5,
                                    'min_length': 5,
                                    'sample_texts': ['World']}}

            assert 0 in stats                                                       # Group 0 exists
            assert 1 in stats                                                       # Group 1 exists

            assert stats[0]['count']       == 2                                     # Shortest text alone
            assert stats[0]['min_length']  == 2
            assert stats[0]['max_length']  == 5

            assert stats[1]['count']       == 1                                     # Two longest texts
            assert stats[1]['min_length']  == 5
            assert stats[1]['max_length']  == 5

    def test_get_group_letter(self):                                                # Test group index to letter conversion
        with Text__Grouping__Service() as _:
            assert _.get_group_letter(0)  == 'a'
            assert _.get_group_letter(1)  == 'b'
            assert _.get_group_letter(2)  == 'c'
            assert _.get_group_letter(3)  == 'd'
            assert _.get_group_letter(4)  == 'e'
            assert _.get_group_letter(25) == 'z'

    def test_get_group_letter__beyond_26(self):                                     # Test letter generation beyond 26 groups
        with Text__Grouping__Service() as _:
            assert _.get_group_letter(26) == 'aa'
            assert _.get_group_letter(27) == 'ab'
            assert _.get_group_letter(52) == 'ba'

    def test_obj_comparison(self):                                                  # Test .obj() for state verification
        with Text__Grouping__Service(num_groups=Safe_UInt(3)) as _:
            assert _.obj() == __(num_groups = 3)
