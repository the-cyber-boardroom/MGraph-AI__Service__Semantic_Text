from unittest                                                                                             import TestCase
from osbot_utils.testing.__                                                                               import __
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from osbot_utils.utils.Objects                                                                            import base_classes
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Selection__Service                 import Text__Selection__Service


class test_Text__Selection__Service(TestCase):

    def test__init__(self):                                                         # Test auto-initialization of Text__Selection__Service
        with Text__Selection__Service() as _:
            assert type(_)         is Text__Selection__Service
            assert base_classes(_) == [Type_Safe, object]

    def test_randomly_select_hashes__empty_mapping(self):                           # Test with empty hash mapping
        with Text__Selection__Service() as _:
            selected = _.randomly_select_hashes({}, Safe_Float(0.5))
            assert selected == []

    def test_randomly_select_hashes__50_percent(self):                              # Test 50% selection
        hash_mapping = {
            Safe_Str__Hash("a123456789") : "Text A"                                  ,
            Safe_Str__Hash("b123456789") : "Text B"                                  ,
            Safe_Str__Hash("c123456789") : "Text C"                                  ,
            Safe_Str__Hash("d123456789") : "Text D"                                  ,
        }

        with Text__Selection__Service() as _:
            selected = _.randomly_select_hashes(hash_mapping, Safe_Float(0.5))

            assert len(selected)   == 2                                             # 50% of 4 = 2
            assert all(h in hash_mapping for h in selected)                         # All selected are from original

    def test_randomly_select_hashes__100_percent(self):                             # Test 100% selection
        hash_mapping = {
            Safe_Str__Hash("a123456789") : "Text A"                                  ,
            Safe_Str__Hash("b123456789") : "Text B"                                  ,
            Safe_Str__Hash("c123456789") : "Text C"                                  ,
        }

        with Text__Selection__Service() as _:
            selected = _.randomly_select_hashes(hash_mapping, Safe_Float(1.0))

            assert len(selected)   == 3                                             # 100% of 3 = 3
            assert set(selected)   == set(hash_mapping.keys())                      # All hashes selected

    def test_randomly_select_hashes__0_percent(self):                               # Test 0% selection with minimum of 1
        hash_mapping = {
            Safe_Str__Hash("a123456789") : "Text A"                                  ,
            Safe_Str__Hash("b123456789") : "Text B"                                  ,
        }

        with Text__Selection__Service() as _:
            selected = _.randomly_select_hashes(hash_mapping, Safe_Float(0.0))

            assert len(selected)   == 1                                             # Minimum of 1 item selected

    def test_randomly_select_hashes__single_item(self):                             # Test with single item
        hash_mapping = {
            Safe_Str__Hash("a123456789") : "Only Text"                               ,
        }

        with Text__Selection__Service() as _:
            selected = _.randomly_select_hashes(hash_mapping, Safe_Float(0.5))

            assert len(selected)   == 1                                             # One item, must select it
            assert selected[0]     == Safe_Str__Hash("a123456789")

    def test_randomly_select_hashes__various_percentages(self):                     # Test various percentage values
        hash_mapping = {
            Safe_Str__Hash(f"a{i:09d}") : f"Text {i}"
            for i in range(10)                                                      # 10 items
        }

        with Text__Selection__Service() as _:
            selected_30 = _.randomly_select_hashes(hash_mapping, Safe_Float(0.3))
            selected_70 = _.randomly_select_hashes(hash_mapping, Safe_Float(0.7))

            assert len(selected_30) == 3                                            # 30% of 10 = 3
            assert len(selected_70) == 7                                            # 70% of 10 = 7

    def test_randomly_select_hashes__randomness(self):                              # Test that selection is actually random
        hash_mapping = {
            Safe_Str__Hash(f"a{i:09d}") : f"Text {i}"
            for i in range(20)                                                      # 20 items
        }

        with Text__Selection__Service() as _:
            results = []
            for i in range(10):                                                     # Run 10 times
                selected = _.randomly_select_hashes(hash_mapping, Safe_Float(0.5))
                results.append(tuple(sorted(selected)))

            unique_results = set(results)
            assert len(unique_results) > 1                                          # Should have different results

    def test_obj_comparison(self):                                                  # Test .obj() for state verification
        with Text__Selection__Service() as _:
            assert _.obj() == __()                                                  # No attributes to compare
