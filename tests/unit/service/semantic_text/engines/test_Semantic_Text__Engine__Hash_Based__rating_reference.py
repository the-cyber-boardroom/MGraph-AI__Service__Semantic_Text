from unittest                                                                                        import TestCase
from osbot_utils.testing.__                                                                          import __
from osbot_utils.type_safe.Type_Safe                                                                 import Type_Safe
from osbot_utils.utils.Objects                                                                       import base_types
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Criteria      import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Engine_Mode   import Enum__Text__Classification__Engine_Mode
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine             import Semantic_Text__Engine
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__Hash_Based import Semantic_Text__Engine__Hash_Based


class test_Semantic_Text__Engine__Hash_Based__rating_reference(TestCase):
    """
    Test the deterministic hash-based classification engine.

    IMPORTANT: This test also serves as a RATING REFERENCE GUIDE for other tests.
    The mappings in test__rating_reference_guide() show the exact ratings that will be
    returned for specific text/hash combinations used throughout the test suite.
    """

    @classmethod
    def setUpClass(cls):
        cls.engine = Semantic_Text__Engine__Hash_Based()

    def test__init(self):                                                      # Test initialization and setup
        with self.engine as _:
            assert _.engine_mode                    == Enum__Text__Classification__Engine_Mode.TEXT_HASH
            assert _.semantic_text_hashes           is not None
            assert _.semantic_text_hashes.hash_size == 10
            assert _.obj()                          == __(engine_mode='text_hash', semantic_text_hashes=__(hash_size=10))
            assert base_types(_)                    == [ Semantic_Text__Engine, Type_Safe, object]

    def test__classify_text__basic(self):                                      # Test basic text classification
        result = self.engine.classify_text(text                     = "Hello World",
                                           classification_criteria= Enum__Text__Classification__Criteria.POSITIVITY)

        assert result.text                                      == "Hello World"
        assert result.text__hash                                == "b10a8db164"                    # Deterministic hash
        assert result.engine_mode                               == Enum__Text__Classification__Engine_Mode.TEXT_HASH
        assert len(result.text__classification)                 == 1
        assert Enum__Text__Classification__Criteria.POSITIVITY  in result.text__classification

        # Deterministic rating
        assert float(result.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]) == 0.7478

    def test__classify_text__different_criteria_same_text(self):               # Test that same text gives different ratings for different criteria
        text = "Test Text"

        result_positivity = self.engine.classify_text(text                     = text,
                                                      classification_criteria= Enum__Text__Classification__Criteria.POSITIVITY)
        result_negativity = self.engine.classify_text(text                     = text,
                                                      classification_criteria= Enum__Text__Classification__Criteria.NEGATIVITY)
        result_bias       = self.engine.classify_text(text                     = text,
                                                      classification_criteria= Enum__Text__Classification__Criteria.BIAS)
        result_urgency    = self.engine.classify_text(text                     = text,
                                                      classification_criteria= Enum__Text__Classification__Criteria.URGENCY)

        # Same text, same hash
        assert result_positivity.text__hash == result_negativity.text__hash == result_bias.text__hash == result_urgency.text__hash
        assert result_positivity.text__hash == "f1feeaa3d6"

        # Different ratings for different criteria
        pos_rating     = float(result_positivity.text__classification[Enum__Text__Classification__Criteria.POSITIVITY])
        neg_rating     = float(result_negativity.text__classification[Enum__Text__Classification__Criteria.NEGATIVITY])
        bias_rating    = float(result_bias      .text__classification[Enum__Text__Classification__Criteria.BIAS      ])
        urgency_rating = float(result_urgency   .text__classification[Enum__Text__Classification__Criteria.URGENCY   ])

        assert pos_rating     == 0.5080
        assert neg_rating     == 0.3946
        assert bias_rating    == 0.9818
        assert urgency_rating == 0.8035

        # Ratings are different
        assert pos_rating != neg_rating != bias_rating != urgency_rating

    def test__hash_based_classification__deterministic(self):                  # Test that hash_based_classification is deterministic
        text     = "Sample text"
        criteria = Enum__Text__Classification__Criteria.POSITIVITY

        # Call multiple times
        rating1 = self.engine.hash_based_classification(text, criteria)
        rating2 = self.engine.hash_based_classification(text, criteria)
        rating3 = self.engine.hash_based_classification(text, criteria)

        # All should be identical
        assert float(rating1) == float(rating2) == float(rating3)
        assert float(rating1) == 0.9569

    def test__hash_based_classification__range(self):                          # Test that ratings are within valid range
        test_texts = [
            "Hello World",
            "Test Text",
            "Sample text",
            "Another text",
            "Short",
            "Very long text with many words and characters",
            ""
        ]

        for text in test_texts:
            for criteria in Enum__Text__Classification__Criteria:
                rating = self.engine.hash_based_classification(text, criteria)
                rating_float = float(rating)

                # Must be in range [0.0, 1.0]
                assert 0.0 <= rating_float <= 1.0, f"Rating {rating_float} out of range for text '{text}' and criteria {criteria}"

    def test__hash_based_classification__distribution(self):                   # Test that ratings are well-distributed
        """
        Test that the hash-based classification produces well-distributed ratings
        across the 0.0-1.0 range (not clustered in one area)
        """
        test_texts = [f"Text {i}" for i in range(100)]
        criteria = Enum__Text__Classification__Criteria.POSITIVITY

        ratings = [float(self.engine.hash_based_classification(text, criteria)) for text in test_texts]

        # Check distribution across quartiles
        q1 = sum(1 for r in ratings if 0.00 <= r < 0.25)
        q2 = sum(1 for r in ratings if 0.25 <= r < 0.50)
        q3 = sum(1 for r in ratings if 0.50 <= r < 0.75)
        q4 = sum(1 for r in ratings if 0.75 <= r <= 1.00)

        # Each quartile should have at least 15% of values (allowing for statistical variance)
        assert q1 >= 15, f"Q1 too small: {q1}"
        assert q2 >= 15, f"Q2 too small: {q2}"
        assert q3 >= 15, f"Q3 too small: {q3}"
        assert q4 >= 15, f"Q4 too small: {q4}"

    # ========================================
    # RATING REFERENCE GUIDE
    # ========================================

    def test__rating_reference_guide__basic_hashes(self):                      # Reference guide for basic test hashes (Level 1 & 2)
        """
        RATING REFERENCE GUIDE - Basic Hashes

        These are the deterministic ratings used in Level 1 and Level 2 tests.
        Use this as a reference when writing or debugging tests.
        """

        # abc1234567 - "Hello World"
        result = self.engine.classify_text("Hello World", Enum__Text__Classification__Criteria.POSITIVITY)
        assert result.text__hash == "b10a8db164"
        assert float(result.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]) == 0.7478

        result = self.engine.classify_text("Hello World", Enum__Text__Classification__Criteria.NEGATIVITY)
        assert float(result.text__classification[Enum__Text__Classification__Criteria.NEGATIVITY]) == 0.1102

        result = self.engine.classify_text("Hello World", Enum__Text__Classification__Criteria.BIAS)
        assert float(result.text__classification[Enum__Text__Classification__Criteria.BIAS]) == 0.2316

        result = self.engine.classify_text("Hello World", Enum__Text__Classification__Criteria.URGENCY)
        assert float(result.text__classification[Enum__Text__Classification__Criteria.URGENCY]) == 0.3141

        # def1234567 - "Test Text"
        result = self.engine.classify_text("Test Text", Enum__Text__Classification__Criteria.POSITIVITY)
        assert result.text__hash == "f1feeaa3d6"
        assert float(result.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]) == 0.5080

        result = self.engine.classify_text("Test Text", Enum__Text__Classification__Criteria.NEGATIVITY)
        assert float(result.text__classification[Enum__Text__Classification__Criteria.NEGATIVITY]) == 0.3946

        result = self.engine.classify_text("Test Text", Enum__Text__Classification__Criteria.BIAS)
        assert float(result.text__classification[Enum__Text__Classification__Criteria.BIAS]) == 0.9818

        result = self.engine.classify_text("Test Text", Enum__Text__Classification__Criteria.URGENCY)
        assert float(result.text__classification[Enum__Text__Classification__Criteria.URGENCY]) == 0.8035

    def test__rating_reference_guide__level_2_filter_tests(self):              # Reference guide for Level 2 filter test hashes
        """
        RATING REFERENCE GUIDE - Level 2 Filter Tests

        Hash/text combinations used in multi-criteria filter tests.
        """

        # 1ba249ca59 - "Sample text" (used in test__classify__multi__rate__all_criteria)
        mappings = [
            ("1ba249ca59", "Sample text", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.9569,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.1469,
                Enum__Text__Classification__Criteria.BIAS:       0.2887,
                Enum__Text__Classification__Criteria.URGENCY:    0.7091
            }),

            # b5ead10d6e - "Positive text" (used in test__classify__multi__filter__and__basic)
            ("b5ead10d6e", "Positive text", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.4332,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.5403,
                Enum__Text__Classification__Criteria.BIAS:       0.4314,
                Enum__Text__Classification__Criteria.URGENCY:    0.1718
            }),

            # 9204d57da8 - "Another text"
            ("9204d57da8", "Another text", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.3018,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.7096,
                Enum__Text__Classification__Criteria.BIAS:       0.3574,
                Enum__Text__Classification__Criteria.URGENCY:    0.2635
            }),

            # 8bfa8e0684 - "Test content"
            ("8bfa8e0684", "Test content", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.6355,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.4913,
                Enum__Text__Classification__Criteria.BIAS:       0.3099,
                Enum__Text__Classification__Criteria.URGENCY:    0.9644
            }),

            # c5dd1b2697 - "Sample" (used in test__classify__multi__filter__and__full_ratings)
            ("c5dd1b2697", "Sample", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.0650,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.5169,
                Enum__Text__Classification__Criteria.BIAS:       0.5304,
                Enum__Text__Classification__Criteria.URGENCY:    0.2027
            }),
        ]

        for expected_hash, text, expected_ratings in mappings:
            for criteria, expected_rating in expected_ratings.items():
                result = self.engine.classify_text(text, criteria)
                assert result.text__hash == expected_hash
                assert float(result.text__classification[criteria]) == expected_rating

    def test__rating_reference_guide__or_logic_tests(self):                    # Reference guide for OR logic test hashes
        """
        RATING REFERENCE GUIDE - OR Logic Tests
        """

        mappings = [
            # c3d45f8fe6 - "High positive"
            ("c3d45f8fe6", "High positive", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.5667,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.6083,
                Enum__Text__Classification__Criteria.BIAS:       0.0494,
                Enum__Text__Classification__Criteria.URGENCY:    0.4699
            }),

            # 58537f27d7 - "High negative"
            ("58537f27d7", "High negative", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.5421,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.7642,
                Enum__Text__Classification__Criteria.BIAS:       0.8904,
                Enum__Text__Classification__Criteria.URGENCY:    0.9505
            }),

            # b0a2013306 - "Low both"
            ("b0a2013306", "Low both", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.1844,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.3436,
                Enum__Text__Classification__Criteria.BIAS:       0.9567,
                Enum__Text__Classification__Criteria.URGENCY:    0.2764
            }),

            # b840f6f2ae - "Text A"
            ("b840f6f2ae", "Text A", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.4814,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.5114,
                Enum__Text__Classification__Criteria.BIAS:       0.2776,
                Enum__Text__Classification__Criteria.URGENCY:    0.9335
            }),

            # eb5deeca9c - "Text B"
            ("eb5deeca9c", "Text B", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.8374,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.7441,
                Enum__Text__Classification__Criteria.BIAS:       0.1535,
                Enum__Text__Classification__Criteria.URGENCY:    0.0720
            }),

            # 9dffbf69ff - "Text"
            ("9dffbf69ff", "Text", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.9776,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.5651,
                Enum__Text__Classification__Criteria.BIAS:       0.9490,
                Enum__Text__Classification__Criteria.URGENCY:    0.4436
            }),
        ]

        for expected_hash, text, expected_ratings in mappings:
            for criteria, expected_rating in expected_ratings.items():
                result = self.engine.classify_text(text, criteria)
                assert result.text__hash == expected_hash
                assert float(result.text__classification[criteria]) == expected_rating

    def test__rating_reference_guide__filter_mode_tests(self):                 # Reference guide for filter mode test hashes
        """
        RATING REFERENCE GUIDE - Filter Mode Tests (BETWEEN, mixed modes)
        """

        # aaa0000012 - "Test text" (BETWEEN mode test)
        result = self.engine.classify_text("Test text", Enum__Text__Classification__Criteria.POSITIVITY)
        assert result.text__hash == "aaaf7028b8"
        assert float(result.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]) == 0.5506
        # NOTE: 0.5506 is NOT between 0.7 and 0.8, so test should adjust thresholds!

        result = self.engine.classify_text("Test text", Enum__Text__Classification__Criteria.NEGATIVITY)
        assert float(result.text__classification[Enum__Text__Classification__Criteria.NEGATIVITY]) == 0.2981

        # aaa0000013 - "Balanced text" (mixed ABOVE/BELOW modes test)
        result = self.engine.classify_text("Balanced text", Enum__Text__Classification__Criteria.POSITIVITY)
        assert result.text__hash == "c298542a7f"
        assert float(result.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]) == 0.7643
        # Check: 0.7643 > 0.6 ✓

        result = self.engine.classify_text("Balanced text", Enum__Text__Classification__Criteria.NEGATIVITY)
        assert float(result.text__classification[Enum__Text__Classification__Criteria.NEGATIVITY]) == 0.7631
        # Check: 0.7631 < 0.8 ✓
        # Both conditions pass!

        # aaa0000014 - "Test"
        result = self.engine.classify_text("Test", Enum__Text__Classification__Criteria.POSITIVITY)
        assert result.text__hash == "0cbc6611f5"
        assert float(result.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]) == 0.4636

    def test__rating_reference_guide__deterministic_multiple_hashes(self):     # Reference guide for deterministic multi-hash tests
        """
        RATING REFERENCE GUIDE - Deterministic Multiple Hash Test

        Used in test__classify__multi__filter__deterministic_results
        """

        mappings = [
            ("20c8b16b2a", "Text 0", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.7645,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.7672,
                Enum__Text__Classification__Criteria.BIAS:       0.4079,
                Enum__Text__Classification__Criteria.URGENCY:    0.0894
            }),

            ("161a6b3572", "Text 1", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.7402,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.0745,
                Enum__Text__Classification__Criteria.BIAS:       0.4710,
                Enum__Text__Classification__Criteria.URGENCY:    0.4165
            }),

            ("48e47cee20", "Text 2", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.4943,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.9681,
                Enum__Text__Classification__Criteria.BIAS:       0.0333,
                Enum__Text__Classification__Criteria.URGENCY:    0.9308
            }),

            ("0d96bbc2ec", "Text 3", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.3426,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.2576,
                Enum__Text__Classification__Criteria.BIAS:       0.8054,
                Enum__Text__Classification__Criteria.URGENCY:    0.1874
            }),

            ("c133c1f81c", "Text 4", {
                Enum__Text__Classification__Criteria.POSITIVITY: 0.6403,
                Enum__Text__Classification__Criteria.NEGATIVITY: 0.9734,
                Enum__Text__Classification__Criteria.BIAS:       0.9142,
                Enum__Text__Classification__Criteria.URGENCY:    0.1743
            }),
        ]

        for expected_hash, text, expected_ratings in mappings:
            for criteria, expected_rating in expected_ratings.items():
                result = self.engine.classify_text(text, criteria)
                assert result.text__hash == expected_hash
                assert float(result.text__classification[criteria]) == expected_rating

        # FILTER ANALYSIS for: positivity > 0.6 AND negativity > 0.6
        # a000000000: pos=0.7645 > 0.6 ✓, neg=0.7672 > 0.6 ✓ → MATCH
        # a000000001: pos=0.7402 > 0.6 ✓, neg=0.0745 > 0.6 ✗ → NO MATCH
        # a000000002: pos=0.4943 > 0.6 ✗, neg=0.9681 > 0.6 ✓ → NO MATCH
        # a000000003: pos=0.3426 > 0.6 ✗, neg=0.2576 > 0.6 ✗ → NO MATCH
        # a000000004: pos=0.6403 > 0.6 ✓, neg=0.9734 > 0.6 ✓ → MATCH
        # Expected matches: a000000000, a000000004 (count: 2)

    def test__rating_reference_guide__summary_table(self):                     # Summary table of all ratings for quick reference
        """
        QUICK REFERENCE SUMMARY

        This test generates a summary table showing ALL hash/text/rating combinations
        used throughout the test suite. Use this for quick lookups.
        """

        all_mappings = [("b10a8db164", "Hello World"  , 0.7478, 0.1102, 0.2316, 0.3141),
                        ("f1feeaa3d6", "Test Text"    , 0.5080, 0.3946, 0.9818, 0.8035),
                        ("1ba249ca59", "Sample text"  , 0.9569, 0.1469, 0.2887, 0.7091),
                        ("b5ead10d6e", "Positive text", 0.4332, 0.5403, 0.4314, 0.1718),
                        ("9204d57da8", "Another text" , 0.3018, 0.7096, 0.3574, 0.2635),
                        ("8bfa8e0684", "Test content" , 0.6355, 0.4913, 0.3099, 0.9644),
                        ("c5dd1b2697", "Sample"       , 0.0650, 0.5169, 0.5304, 0.2027),
                        ("c3d45f8fe6", "High positive", 0.5667, 0.6083, 0.0494, 0.4699),
                        ("58537f27d7", "High negative", 0.5421, 0.7642, 0.8904, 0.9505),
                        ("b0a2013306", "Low both"     , 0.1844, 0.3436, 0.9567, 0.2764),
                        ("b840f6f2ae", "Text A"       , 0.4814, 0.5114, 0.2776, 0.9335),
                        ("eb5deeca9c", "Text B"       , 0.8374, 0.7441, 0.1535, 0.0720),
                        ("9dffbf69ff", "Text"         , 0.9776, 0.5651, 0.9490, 0.4436),
                        ("aaaf7028b8", "Test text"    , 0.5506, 0.2981, 0.5889, 0.8154),
                        ("c298542a7f", "Balanced text", 0.7643, 0.7631, 0.6116, 0.6351),
                        ("0cbc6611f5", "Test"         , 0.4636, 0.2575, 0.8048, 0.7786),
                        ("20c8b16b2a", "Text 0"       , 0.7645, 0.7672, 0.4079, 0.0894),
                        ("161a6b3572", "Text 1"       , 0.7402, 0.0745, 0.4710, 0.4165),
                        ("48e47cee20", "Text 2"       , 0.4943, 0.9681, 0.0333, 0.9308),
                        ("0d96bbc2ec", "Text 3"       , 0.3426, 0.2576, 0.8054, 0.1874),
                        ("c133c1f81c", "Text 4"       , 0.6403, 0.9734, 0.9142, 0.1743)]



        # Verify all mappings
        for hash_id, text, pos, neg, bias, urg in all_mappings:
            result_pos  = self.engine.classify_text(text, Enum__Text__Classification__Criteria.POSITIVITY)
            result_neg  = self.engine.classify_text(text, Enum__Text__Classification__Criteria.NEGATIVITY)
            result_bias = self.engine.classify_text(text, Enum__Text__Classification__Criteria.BIAS      )
            result_urg  = self.engine.classify_text(text, Enum__Text__Classification__Criteria.URGENCY   )

            assert result_pos.text__hash == hash_id
            assert float(result_pos  .text__classification[Enum__Text__Classification__Criteria.POSITIVITY]) == pos
            assert float(result_neg  .text__classification[Enum__Text__Classification__Criteria.NEGATIVITY]) == neg
            assert float(result_bias .text__classification[Enum__Text__Classification__Criteria.BIAS      ]) == bias
            assert float(result_urg  .text__classification[Enum__Text__Classification__Criteria.URGENCY   ]) == urg