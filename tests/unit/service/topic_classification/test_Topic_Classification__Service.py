from unittest                                                                                  import TestCase
from osbot_utils.testing.__                                                                import __
from osbot_utils.type_safe.Type_Safe                                                       import Type_Safe
from osbot_utils.utils.Objects                                                             import base_types
from mgraph_ai_service_semantic_text.service.schemas.topic.enums.Enum__Classification__Topic import Enum__Classification__Topic
from mgraph_ai_service_semantic_text.service.topic_classification.Topic_Classification__Service import Topic_Classification__Service
from mgraph_ai_service_semantic_text.service.topic_classification.engines.Topic_Classification__Engine__Hash_Based import Topic_Classification__Engine__Hash_Based


class test_Topic_Classification__Service(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service = Topic_Classification__Service().setup()

    def test__init(self):                                                      # Test initialization and setup
        with self.service as _:
            assert type(_)             is Topic_Classification__Service
            assert type(_.topic_engine) is Topic_Classification__Engine__Hash_Based
            assert base_types(_)       == [Type_Safe, object]

    def test__classify_topics__basic(self):                                   # Test basic topic classification
        text   = "Hello World"
        topics = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE,
                  Enum__Classification__Topic.BUSINESS_FINANCE]

        result = self.service.classify_topics(text=text, topics=topics)

        assert type(result) is dict
        assert len(result)  == 2
        assert Enum__Classification__Topic.TECHNOLOGY_SOFTWARE in result
        assert Enum__Classification__Topic.BUSINESS_FINANCE    in result

        # Deterministic scores from hash-based engine
        assert float(result[Enum__Classification__Topic.TECHNOLOGY_SOFTWARE]) == 0.7478
        assert float(result[Enum__Classification__Topic.BUSINESS_FINANCE   ]) == 0.6789

    def test__classify_topics__single_topic(self):                            # Test classification with single topic
        text   = "Test Text"
        topics = [Enum__Classification__Topic.EDUCATION_ACADEMIC]

        result = self.service.classify_topics(text=text, topics=topics)

        assert len(result) == 1
        assert Enum__Classification__Topic.EDUCATION_ACADEMIC in result
        assert float(result[Enum__Classification__Topic.EDUCATION_ACADEMIC]) == 0.5903

    def test__classify_topics__all_topics(self):                              # Test classification with all 15 topics
        text       = "Sample text"
        all_topics = list(Enum__Classification__Topic)

        result = self.service.classify_topics(text=text, topics=all_topics)

        assert len(result) == 15

        # Verify all topics present
        for topic in all_topics:
            assert topic in result
            confidence = float(result[topic])
            assert 0.0 <= confidence <= 1.0                                    # Valid range

    def test__classify_topics__deterministic(self):                           # Test that classification is deterministic
        text   = "Deterministic test"
        topics = [Enum__Classification__Topic.TECHNOLOGY_AI_ML]

        result1 = self.service.classify_topics(text=text, topics=topics)
        result2 = self.service.classify_topics(text=text, topics=topics)
        result3 = self.service.classify_topics(text=text, topics=topics)

        # All results should be identical
        assert float(result1[Enum__Classification__Topic.TECHNOLOGY_AI_ML]) == \
               float(result2[Enum__Classification__Topic.TECHNOLOGY_AI_ML]) == \
               float(result3[Enum__Classification__Topic.TECHNOLOGY_AI_ML])

    def test__classify_topics__different_texts(self):                         # Test that different texts produce different scores
        topic = [Enum__Classification__Topic.HEALTH_WELLNESS]

        result1 = self.service.classify_topics(text="Text A", topics=topic)
        result2 = self.service.classify_topics(text="Text B", topics=topic)

        score1 = float(result1[Enum__Classification__Topic.HEALTH_WELLNESS])
        score2 = float(result2[Enum__Classification__Topic.HEALTH_WELLNESS])

        assert score1 != score2                                                # Different texts should produce different scores

    def test__classify_topics__empty_text(self):                              # Test classification with empty text
        text   = ""
        topics = [Enum__Classification__Topic.GENERAL_NEWS]

        result = self.service.classify_topics(text=text, topics=topics)

        assert len(result) == 1
        assert Enum__Classification__Topic.GENERAL_NEWS in result
        # Empty text still produces a deterministic score
        assert 0.0 <= float(result[Enum__Classification__Topic.GENERAL_NEWS]) <= 1.0

    def test__classify_topics__long_text(self):                               # Test classification with long text
        text   = "This is a very long piece of text " * 20                    # 100+ words
        topics = [Enum__Classification__Topic.GENERAL_LIFESTYLE]

        result = self.service.classify_topics(text=text, topics=topics)

        assert len(result) == 1
        assert Enum__Classification__Topic.GENERAL_LIFESTYLE in result
        assert 0.0 <= float(result[Enum__Classification__Topic.GENERAL_LIFESTYLE]) <= 1.0

    def test__classify_topics__special_characters(self):                      # Test classification with special characters
        text   = "Test!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        topics = [Enum__Classification__Topic.TECHNOLOGY_HARDWARE]

        result = self.service.classify_topics(text=text, topics=topics)

        assert len(result) == 1
        assert Enum__Classification__Topic.TECHNOLOGY_HARDWARE in result
        # Should handle special characters without errors
        assert 0.0 <= float(result[Enum__Classification__Topic.TECHNOLOGY_HARDWARE]) <= 1.0

    def test__classify_topics__unicode_text(self):                            # Test classification with unicode text
        text   = "Hello 世界 🌍 Привет"
        topics = [Enum__Classification__Topic.EDUCATION_ONLINE]

        result = self.service.classify_topics(text=text, topics=topics)

        assert len(result) == 1
        assert Enum__Classification__Topic.EDUCATION_ONLINE in result
        # Should handle unicode without errors
        assert 0.0 <= float(result[Enum__Classification__Topic.EDUCATION_ONLINE]) <= 1.0

    def test__classify_topics__multiple_topics_different_scores(self):        # Test that multiple topics produce different scores for same text
        text   = "Sample text for testing"
        topics = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE,
                  Enum__Classification__Topic.BUSINESS_OPERATIONS,
                  Enum__Classification__Topic.HEALTH_MENTAL,
                  Enum__Classification__Topic.EDUCATION_TRAINING,
                  Enum__Classification__Topic.GENERAL_ENTERTAINMENT]

        result = self.service.classify_topics(text=text, topics=topics)

        assert len(result) == 5

        # Extract all scores
        scores = [float(result[topic]) for topic in topics]

        # All scores should be in valid range
        for score in scores:
            assert 0.0 <= score <= 1.0

        # Not all scores should be identical (extremely unlikely)
        assert len(set(scores)) > 1                                            # At least 2 different scores
