from unittest                                                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                                                import Type_Safe
from osbot_utils.utils.Objects                                                                                      import base_types
from mgraph_ai_service_semantic_text.schemas.topic.enums.Enum__Classification__Topic                                import Enum__Classification__Topic
from mgraph_ai_service_semantic_text.service.topic_classification.engines.Topic_Classification__Engine              import Topic_Classification__Engine
from mgraph_ai_service_semantic_text.service.topic_classification.engines.Topic_Classification__Engine__Hash_Based  import Topic_Classification__Engine__Hash_Based


class test_Topic_Classification__Engine__Hash_Based__reference_guide(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = Topic_Classification__Engine__Hash_Based()

    def test__init(self):
        with self.engine as _:
            assert type(_)        is Topic_Classification__Engine__Hash_Based
            assert base_types(_)  == [Topic_Classification__Engine, Type_Safe, object]

    def test__classify_topics__basic(self):
        text   = "Hello World"
        topics = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE,
                  Enum__Classification__Topic.BUSINESS_FINANCE     ]

        result = self.engine.classify_topics(text = text, topics = topics)

        assert type(result)                                    is dict
        assert len(result)                                     == 2
        assert Enum__Classification__Topic.TECHNOLOGY_SOFTWARE in result
        assert Enum__Classification__Topic.BUSINESS_FINANCE    in result

        assert float(result[Enum__Classification__Topic.TECHNOLOGY_SOFTWARE]) == 0.2915
        assert float(result[Enum__Classification__Topic.BUSINESS_FINANCE   ]) == 0.284

    def test_hash_based_confidence__deterministic(self):
        text  = "Sample text"
        topic = Enum__Classification__Topic.TECHNOLOGY_AI_ML

        confidence1 = self.engine.hash_based_confidence(text, topic)
        confidence2 = self.engine.hash_based_confidence(text, topic)
        confidence3 = self.engine.hash_based_confidence(text, topic)

        assert float(confidence1) == float(confidence2) == float(confidence3)

    def test_hash_based_confidence__range(self):
        test_texts = ["Hello World", "Test Text", "Sample text", "Another text", "Short",
                      "Very long text with many words and characters", ""]

        for text in test_texts:
            for topic in Enum__Classification__Topic:
                confidence       = self.engine.hash_based_confidence(text, topic)
                confidence_float = float(confidence)
                assert 0.0 <= confidence_float <= 1.0, f"Confidence {confidence_float} out of range for text '{text}' and topic {topic}"

    def test_hash_based_confidence__distribution(self):
        test_texts = [f"Text {i}" for i in range(100)]
        topic      = Enum__Classification__Topic.TECHNOLOGY_SOFTWARE

        confidences = [float(self.engine.hash_based_confidence(text, topic)) for text in test_texts]

        q1 = sum(1 for c in confidences if 0.00 <= c < 0.25)
        q2 = sum(1 for c in confidences if 0.25 <= c < 0.50)
        q3 = sum(1 for c in confidences if 0.50 <= c < 0.75)
        q4 = sum(1 for c in confidences if 0.75 <= c <= 1.00)

        assert q1 >= 15, f"Q1 too small: {q1}"
        assert q2 >= 15, f"Q2 too small: {q2}"
        assert q3 >= 15, f"Q3 too small: {q3}"
        assert q4 >= 15, f"Q4 too small: {q4}"

    def test__reference_guide__hello_world(self):
        text = "Hello World"

        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_SOFTWARE)) == 0.2915
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_HARDWARE)) == 0.066
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_AI_ML   )) == 0.3354
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_FINANCE   )) == 0.284
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_MARKETING )) == 0.3765
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.EDUCATION_ACADEMIC )) == 0.9113
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.HEALTH_MEDICAL     )) == 0.2608

    def test__reference_guide__test_text(self):
        text = "Test Text"

        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_SOFTWARE  )) == 0.3881
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_HARDWARE  )) == 0.6094
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_AI_ML     )) == 0.515
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_FINANCE     )) == 0.6692
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_MARKETING   )) == 0.9444
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_OPERATIONS  )) == 0.2369
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.HEALTH_MEDICAL       )) == 0.6505
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.HEALTH_WELLNESS      )) == 0.0071
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.HEALTH_MENTAL        )) == 0.0444
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.EDUCATION_ACADEMIC   )) == 0.6366
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.EDUCATION_TRAINING   )) == 0.1536
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.EDUCATION_ONLINE     )) == 0.3275
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.GENERAL_NEWS         )) == 0.6449
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.GENERAL_ENTERTAINMENT)) == 0.8782
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.GENERAL_LIFESTYLE    )) == 0.975

    def test__reference_guide__sample_text(self):
        text = "Sample text"

        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_SOFTWARE)) == 0.4057
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_FINANCE   )) == 0.8143
        assert float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.EDUCATION_ACADEMIC )) == 0.9458

    def test__reference_guide__different_text_different_scores(self):
        topic = Enum__Classification__Topic.HEALTH_WELLNESS

        score1 = float(self.engine.hash_based_confidence("Text A", topic))
        score2 = float(self.engine.hash_based_confidence("Text B", topic))
        score3 = float(self.engine.hash_based_confidence("Text C", topic))

        assert score1 != score2
        assert score2 != score3
        assert score1 != score3

    def test__reference_guide__same_text_different_topics(self):
        text = "Sample text for testing"

        scores = [float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_SOFTWARE   )) ,
                  float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.BUSINESS_OPERATIONS   )) ,
                  float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.HEALTH_MENTAL         )) ,
                  float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.EDUCATION_TRAINING    )) ,
                  float(self.engine.hash_based_confidence(text, Enum__Classification__Topic.GENERAL_ENTERTAINMENT ))]

        assert len(set(scores)) > 1

    def test__classify_topics__all_topics(self):
        text       = "Hello World"
        all_topics = list(Enum__Classification__Topic)

        result = self.engine.classify_topics(text = text, topics = all_topics)

        assert len(result) == 15

        for topic, confidence in result.items():
            assert 0.0 <= float(confidence) <= 1.0

        assert float(result[Enum__Classification__Topic.TECHNOLOGY_SOFTWARE]) == 0.2915
        assert float(result[Enum__Classification__Topic.TECHNOLOGY_HARDWARE]) == 0.066
        assert float(result[Enum__Classification__Topic.BUSINESS_FINANCE   ]) == 0.284

    def test__classify_topics__empty_text(self):
        text   = ""
        topics = [Enum__Classification__Topic.GENERAL_NEWS]

        result = self.engine.classify_topics(text = text, topics = topics)

        assert len(result) == 1
        assert Enum__Classification__Topic.GENERAL_NEWS in result
        assert 0.0 <= float(result[Enum__Classification__Topic.GENERAL_NEWS]) <= 1.0

    def test__classify_topics__long_text(self):
        text   = "This is a very long piece of text with many words " * 50
        topics = [Enum__Classification__Topic.GENERAL_LIFESTYLE]

        result = self.engine.classify_topics(text = text, topics = topics)

        assert len(result) == 1
        assert Enum__Classification__Topic.GENERAL_LIFESTYLE in result
        assert 0.0 <= float(result[Enum__Classification__Topic.GENERAL_LIFESTYLE]) <= 1.0

    def test__classify_topics__special_characters(self):
        text   = "Test!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        topics = [Enum__Classification__Topic.TECHNOLOGY_HARDWARE]

        result = self.engine.classify_topics(text = text, topics = topics)

        assert len(result) == 1
        assert Enum__Classification__Topic.TECHNOLOGY_HARDWARE in result
        assert 0.0 <= float(result[Enum__Classification__Topic.TECHNOLOGY_HARDWARE]) <= 1.0

    def test__classify_topics__unicode_text(self):
        text   = "Hello 世界 🌍 Привет مرحبا"
        topics = [Enum__Classification__Topic.EDUCATION_ONLINE]

        result = self.engine.classify_topics(text = text, topics = topics)

        assert len(result) == 1
        assert Enum__Classification__Topic.EDUCATION_ONLINE in result
        assert 0.0 <= float(result[Enum__Classification__Topic.EDUCATION_ONLINE]) <= 1.0

    def test__reference_values__python_programming(self):
        text = "Python programming is awesome"

        # Should score high for technology-software
        result = self.engine.hash_based_confidence(text, Enum__Classification__Topic.TECHNOLOGY_SOFTWARE)
        assert float(result) == 0.4688                                         # Expected high score

        # Should score lower for health topics
        result = self.engine.hash_based_confidence(text, Enum__Classification__Topic.HEALTH_MEDICAL)
        assert float(result) == 0.023                                          # Expected low score
