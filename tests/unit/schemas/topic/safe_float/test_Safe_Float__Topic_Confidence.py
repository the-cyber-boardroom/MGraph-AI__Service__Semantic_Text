import re
from unittest                                                                                   import TestCase
import pytest
from mgraph_ai_service_semantic_text.schemas.topic.safe_float.Safe_Float__Topic_Confidence     import Safe_Float__Topic_Confidence


class test_Safe_Float__Topic_Confidence(TestCase):

    def test__init__valid_values(self):                                         # Test initialization with valid confidence values (0.0-1.0)
        conf_min = Safe_Float__Topic_Confidence(0.0)
        conf_mid = Safe_Float__Topic_Confidence(0.5)
        conf_max = Safe_Float__Topic_Confidence(1.0)

        assert float(conf_min) == 0.0
        assert float(conf_mid) == 0.5
        assert float(conf_max) == 1.0

    def test__init__min_max_values(self):                                       # Test min_value and max_value attributes
        conf = Safe_Float__Topic_Confidence(0.5)

        assert conf.min_value == 0.0
        assert conf.max_value == 1.0

    def test__init__boundary_values(self):                                      # Test exact boundary values
        min_conf = Safe_Float__Topic_Confidence(0.0)                            # No match
        max_conf = Safe_Float__Topic_Confidence(1.0)                            # Perfect match

        assert float(min_conf) == 0.0
        assert float(max_conf) == 1.0

    def test__init__invalid_below_range(self):                                  # Test values below 0.0 are rejected
        error_message = "Safe_Float__Topic_Confidence must be >= 0.0, got -0.1"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Float__Topic_Confidence(-0.1)

    def test__init__invalid_above_range(self):                                  # Test values above 1.0 are rejected
        error_message = "Safe_Float__Topic_Confidence must be <= 1.0, got 1.1"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Float__Topic_Confidence(1.1)

    def test__confidence_interpretations(self):                                 # Test typical confidence score interpretations
        no_match      = Safe_Float__Topic_Confidence(0.0)                       # No confidence (0.0)
        low_conf      = Safe_Float__Topic_Confidence(0.3)                       # Low confidence
        medium_conf   = Safe_Float__Topic_Confidence(0.6)                       # Medium confidence
        high_conf     = Safe_Float__Topic_Confidence(0.85)                      # High confidence
        perfect_match = Safe_Float__Topic_Confidence(1.0)                       # Perfect match (1.0)

        assert float(no_match) == 0.0
        assert float(low_conf) == 0.3
        assert float(medium_conf) == 0.6
        assert float(high_conf) == 0.85
        assert float(perfect_match) == 1.0

    def test__comparison_operations(self):                                      # Test comparison with confidence thresholds
        conf = Safe_Float__Topic_Confidence(0.7)

        assert conf > 0.5                                                       # Above medium confidence
        assert conf >= 0.7                                                      # At threshold
        assert conf < 0.9                                                       # Below high confidence
        assert conf <= 0.7                                                      # At threshold
        assert conf == 0.7                                                      # Exact match

    def test__comparison_with_another_confidence(self):                         # Test comparison between confidence values
        conf1 = Safe_Float__Topic_Confidence(0.6)
        conf2 = Safe_Float__Topic_Confidence(0.6)
        conf3 = Safe_Float__Topic_Confidence(0.8)

        assert conf1 == conf2
        assert conf1 != conf3
        assert conf1 < conf3
        assert conf3 > conf1

    def test__typical_topic_classification_use_case(self):                      # Test typical topic classification scenario
        # Hash-based topic classification returns confidence scores
        topic_scores = {
            'technology-software': Safe_Float__Topic_Confidence(0.85),          # High confidence
            'business-finance':    Safe_Float__Topic_Confidence(0.45),          # Medium confidence
            'health-medical':      Safe_Float__Topic_Confidence(0.12),          # Low confidence
            'general-news':        Safe_Float__Topic_Confidence(0.05)           # Very low confidence
        }

        # Filter by minimum confidence threshold
        min_confidence = 0.5
        high_confidence_topics = {
            topic: score
            for topic, score in topic_scores.items()
            if float(score) >= min_confidence
        }

        assert len(high_confidence_topics) == 1
        assert 'technology-software' in high_confidence_topics

    def test__precision_handling(self):                                         # Test handling of high-precision confidence values
        precise_conf = Safe_Float__Topic_Confidence(0.123456789)

        assert float(precise_conf) == 0.123456789

    def test__string_representation(self):                                      # Test string conversion
        conf = Safe_Float__Topic_Confidence(0.75)

        assert str(conf) == "0.75"

    def test__type_safety(self):                                                # Test that type is preserved
        conf = Safe_Float__Topic_Confidence(0.5)

        assert type(conf) is Safe_Float__Topic_Confidence
        assert isinstance(conf, Safe_Float__Topic_Confidence)

    def test__confidence_threshold_filtering(self):                             # Test filtering topics by confidence threshold
        confidences = [ Safe_Float__Topic_Confidence(0.9),
                        Safe_Float__Topic_Confidence(0.7),
                        Safe_Float__Topic_Confidence(0.5),
                        Safe_Float__Topic_Confidence(0.3),
                        Safe_Float__Topic_Confidence(0.1)]

        # Filter with different thresholds
        threshold_0_6 = [c for c in confidences if c >= 0.6]
        threshold_0_8 = [c for c in confidences if c >= 0.8]

        assert len(threshold_0_6) == 2                                          # 0.9, 0.7, (not 0.5)
        assert len(threshold_0_8) == 1                                          # Only 0.9