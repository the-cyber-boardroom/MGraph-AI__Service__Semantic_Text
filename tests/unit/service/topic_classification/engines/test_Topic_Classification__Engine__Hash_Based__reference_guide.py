from unittest                                                                                               import TestCase
from osbot_utils.testing.__                                                                                 import __
from osbot_utils.type_safe.Type_Safe                                                                        import Type_Safe
from osbot_utils.utils.Objects                                                                              import base_types
from mgraph_ai_service_semantic_text.service.schemas.topic.enums.Enum__Classification__Topic                import Enum__Classification__Topic
from mgraph_ai_service_semantic_text.service.topic_classification.engines.Topic_Classification__Engine     import Topic_Classification__Engine
from mgraph_ai_service_semantic_text.service.topic_classification.engines.Topic_Classification__Engine__Hash_Based import Topic_Classification__Engine__Hash_Based


class test_Topic_Classification__Engine__Hash_Based__reference_guide(TestCase):
    """
    TOPIC CLASSIFICATION - DETERMINISTIC REFERENCE GUIDE

    IMPORTANT: This test serves as a REFERENCE GUIDE for other tests.
    The mappings show the exact topic confidence scores that will be returned
    for specific text/hash combinations used throughout the test suite.

    Key Principle: Same text + same topic = ALWAYS same confidence score
    """

    @classmethod
    def setUpClass(cls):
        cls.engine = Topic_Classification__Engine__Hash_Based()

    def test__init(self):                                                      # Test initialization and setup
        with self.engine as _:
            assert type(_)        is Topic_Classification__Engine__Hash_Based
            assert base_types(_)  == [Type_Safe, object]

    def test__classify_topics__basic(self):                                   # Test basic topic classification
        text   = "Hello World"
        topics = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE,
                  Enum__Classification__Topic.BUSINESS_FINANCE]

        result = self.engine.classify_topics(text=text, topics=topics)

        assert type(result) is dict
        assert len(result)  == 2
        assert Enum__Classification__Topic.TECHNOLOGY_SOFTWARE in result
        assert Enum__Classification__Topic.BUSINESS_FINANCE    in result

        # Deterministic scores
        assert float(result[Enum__Classification__Topic.TECHNOLOGY_SOFTWARE]) == 0.7478
        assert float(result[Enum__Classification__Topic.BUSINESS_FINANCE   ]) == 0.6789

    def test__hash_based_confidence__deterministic(self):                     # Test that _hash_based_confidence is deterministic
        text  = "Sample text"
        topic = Enum__Classification__Topic.TECHNOLOGY_AI_ML

        # Call multiple times
        confidence1 = self.engine._hash_based_confidence(text, topic)
        confidence2 = self.engine._hash_based_confidence(text, topic)
        confidence3 = self.engine._hash_based_confidence(text, topic)

        # All should be identical
        assert float(confidence1) == float(confidence2) == float(confidence3)

    def test__hash_based_confidence__range(self):                             # Test that confidence scores are within valid range (0.0-1.0)
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
            for topic in Enum__Classification__Topic:
                confidence = self.engine._hash_based_confidence(text, topic)
                confidence_float = float(confidence)

                # Must be in range [0.0, 1.0]
                assert 0.0 <= confidence_float <= 1.0, f"Confidence {confidence_float} out of range for text '{text}' and topic {topic}"

    def test__hash_based_confidence__distribution(self):                      # Test that confidence scores are well-distributed
        test_texts = [f"Text {i}" for i in range(100)]
        topic      = Enum__Classification__Topic.TECHNOLOGY_SOFTWARE

        confidences = [float(self.engine._hash_based_confidence(text, topic)) for text in test_texts]

        # Check distribution across quartiles
        q1 = sum(1 for c in confidences if 0.00 <= c < 0.25)
        q2 = sum(1 for c in confidences if 0.25 <= c < 0.50)
        q3 = sum(1 for c in confidences if 0.50 <= c < 0.75)
        q4 = sum(1 for c in confidences if 0.75 <= c <= 1.00)

        # Each quartile should have at least 15% of values (allowing for statistical variance)
        assert q1 >= 15, f"Q1 too small: {q1}"
        assert q2 >= 15, f"Q2 too small: {q2}"
        assert q3 >= 15, f"Q3 too small: {q3}"
        assert q4 >= 15, f"Q4 too small: {q4}"

    # ========================================
    # TOPIC CONFIDENCE REFERENCE GUIDE
    # ========================================

    def test__reference_guide__hello_world(self):                             # Reference values for "Hello World" (hash: b10a8db164)
        """
        REFERENCE: "Hello World" topic confidence scores

        These are the CANONICAL values for "Hello World" text.
        Hash: b10a8db164 (10 chars)

        All other tests should reference these values.
        """
        text = "Hello World"

        # Technology topics
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_SOFTWARE)) == 0.7478
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_HARDWARE)) == 0.8234
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_AI_ML   )) == 0.4521

        # Business topics
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_FINANCE   )) == 0.6789
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_MARKETING )) == 0.3456
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_OPERATIONS)) == 0.5623

        # Health topics
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.HEALTH_MEDICAL     )) == 0.0861
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.HEALTH_WELLNESS    )) == 0.3122
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.HEALTH_MENTAL      )) == 0.9734

        # Education topics
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.EDUCATION_ACADEMIC )) == 0.1512
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.EDUCATION_TRAINING )) == 0.4289
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.EDUCATION_ONLINE   )) == 0.8901

        # General topics
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.GENERAL_NEWS        )) == 0.2678
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.GENERAL_ENTERTAINMENT)) == 0.7845
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.GENERAL_LIFESTYLE  )) == 0.6012

    def test__reference_guide__test_text(self):                               # Reference values for "Test Text" (hash: f1feeaa3d6)
        """
        REFERENCE: "Test Text" topic confidence scores

        Hash: f1feeaa3d6 (10 chars)
        """
        text = "Test Text"

        # Technology topics
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_SOFTWARE)) == 0.508
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_HARDWARE)) == 0.3401
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_AI_ML   )) == 0.9123

        # Business topics
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_FINANCE   )) == 0.2507
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_MARKETING )) == 0.7834
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_OPERATIONS)) == 0.1256

        # Health topics
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.HEALTH_MEDICAL     )) == 0.4789
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.HEALTH_WELLNESS    )) == 0.6623
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.HEALTH_MENTAL      )) == 0.8345

        # Education topics
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.EDUCATION_ACADEMIC )) == 0.5903
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.EDUCATION_TRAINING )) == 0.2178
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.EDUCATION_ONLINE   )) == 0.9512

        # General topics
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.GENERAL_NEWS        )) == 0.3689
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.GENERAL_ENTERTAINMENT)) == 0.7201
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.GENERAL_LIFESTYLE  )) == 0.4456

    def test__reference_guide__sample_text(self):                             # Reference values for "Sample text"
        """
        REFERENCE: "Sample text" topic confidence scores

        Used in various tests for validation
        """
        text = "Sample text"

        # Selected topics for quick reference
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_SOFTWARE)) == 0.9569
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_FINANCE   )) == 0.2887
        assert float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.EDUCATION_ACADEMIC )) == 0.7091

    def test__reference_guide__different_text_different_scores(self):         # Verify different texts produce different scores for same topic
        topic = Enum__Classification__Topic.HEALTH_WELLNESS

        score1 = float(self.engine._hash_based_confidence("Text A", topic))
        score2 = float(self.engine._hash_based_confidence("Text B", topic))
        score3 = float(self.engine._hash_based_confidence("Text C", topic))

        # All should be different (extremely unlikely to collide)
        assert score1 != score2
        assert score2 != score3
        assert score1 != score3

    def test__reference_guide__same_text_different_topics(self):              # Verify same text produces different scores for different topics
        text = "Sample text for testing"

        # Get scores for 5 different topics
        scores = [
            float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_SOFTWARE)),
            float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_OPERATIONS)),
            float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.HEALTH_MENTAL)),
            float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.EDUCATION_TRAINING)),
            float(self.engine._hash_based_confidence(text, Enum__Classification__Topic.GENERAL_ENTERTAINMENT))
        ]

        # Not all scores should be identical
        assert len(set(scores)) > 1                                            # At least 2 different scores

    def test__classify_topics__all_topics(self):                              # Test classification with all 15 topics
        text       = "Hello World"
        all_topics = list(Enum__Classification__Topic)

        result = self.engine.classify_topics(text=text, topics=all_topics)

        # Should return confidence for all 15 topics
        assert len(result) == 15

        # All values should be between 0.0 and 1.0
        for topic, confidence in result.items():
            assert 0.0 <= float(confidence) <= 1.0

        # Verify specific known values match reference
        assert float(result[Enum__Classification__Topic.TECHNOLOGY_SOFTWARE]) == 0.7478
        assert float(result[Enum__Classification__Topic.TECHNOLOGY_HARDWARE]) == 0.8234
        assert float(result[Enum__Classification__Topic.BUSINESS_FINANCE   ]) == 0.6789

    def test__classify_topics__empty_text(self):                              # Test classification with empty text
        text   = ""
        topics = [Enum__Classification__Topic.GENERAL_NEWS]

        result = self.engine.classify_topics(text=text, topics=topics)

        assert len(result) == 1
        assert Enum__Classification__Topic.GENERAL_NEWS in result
        # Empty text still produces a deterministic score
        assert 0.0 <= float(result[Enum__Classification__Topic.GENERAL_NEWS]) <= 1.0

    def test__classify_topics__long_text(self):                               # Test classification with long text
        text   = "This is a very long piece of text with many words " * 50    # 400+ words
        topics = [Enum__Classification__Topic.GENERAL_LIFESTYLE]

        result = self.engine.classify_topics(text=text, topics=topics)

        assert len(result) == 1
        assert Enum__Classification__Topic.GENERAL_LIFESTYLE in result
        assert 0.0 <= float(result[Enum__Classification__Topic.GENERAL_LIFESTYLE]) <= 1.0

    def test__classify_topics__special_characters(self):                      # Test classification with special characters
        text   = "Test!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        topics = [Enum__Classification__Topic.TECHNOLOGY_HARDWARE]

        result = self.engine.classify_topics(text=text, topics=topics)

        assert len(result) == 1
        assert Enum__Classification__Topic.TECHNOLOGY_HARDWARE in result
        # Should handle special characters without errors
        assert 0.0 <= float(result[Enum__Classification__Topic.TECHNOLOGY_HARDWARE]) <= 1.0

    def test__classify_topics__unicode_text(self):                            # Test classification with unicode text
        text   = "Hello 世界 🌍 Привет مرحبا"
        topics = [Enum__Classification__Topic.EDUCATION_ONLINE]

        result = self.engine.classify_topics(text=text, topics=topics)

        assert len(result) == 1
        assert Enum__Classification__Topic.EDUCATION_ONLINE in result
        # Should handle unicode without errors
        assert 0.0 <= float(result[Enum__Classification__Topic.EDUCATION_ONLINE]) <= 1.0
