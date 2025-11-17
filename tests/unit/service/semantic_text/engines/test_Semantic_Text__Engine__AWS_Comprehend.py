from unittest                                                                                                    import TestCase
from osbot_utils.testing.__helpers                                                                               import obj
from osbot_utils.utils.Env                                                                                       import get_env, load_dotenv
from osbot_utils.testing.__                                                                                      import __
from osbot_utils.utils.Objects                                                                                   import base_classes
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__AWS_Comprehend         import Semantic_Text__Engine__AWS_Comprehend, ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__BASE_URL, ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_NAME, ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_VALUE
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine                         import Semantic_Text__Engine
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Engine_Mode                       import Enum__Text__Classification__Engine_Mode
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria                          import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.safe_float.Safe_Float__Text__Classification                         import Safe_Float__Text__Classification
from osbot_utils.type_safe.Type_Safe                                                                             import Type_Safe
import pytest


class test_Semantic_Text__Engine__AWS_Comprehend(TestCase):

    @classmethod
    def setUpClass(cls):                                                                    # Setup expensive resources once for all tests
        load_dotenv()
        cls.base_url     = get_env(ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__BASE_URL )    # Load env vars once
        cls.api_key_name = get_env(ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_NAME )
        cls.api_key      = get_env(ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_VALUE)

        cls.has_credentials = all([cls.base_url, cls.api_key_name, cls.api_key])           # Check if credentials available

        if cls.has_credentials:                                                             # Only create engine if credentials exist
            cls.engine = Semantic_Text__Engine__AWS_Comprehend()
        else:
            pytest.skip("AWS Comprehend not supported on this environment")

    def test__init__(self):                                                                 # Test AWS Comprehend engine initialization
        if not self.has_credentials:
            pytest.skip(f"Skipping: Missing AWS Comprehend credentials. Required env vars: "
                       f"{ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__BASE_URL}, "
                       f"{ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_NAME}, "
                       f"{ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_VALUE}")

        with self.engine as _:
            assert type(_)         is Semantic_Text__Engine__AWS_Comprehend                 # Verify type
            assert base_classes(_) == [Semantic_Text__Engine, Type_Safe, object]           # Verify inheritance chain

            assert _.engine_mode   == Enum__Text__Classification__Engine_Mode.AWS_COMPREHEND    # Verify engine mode set correctly
            assert _.base_url      == self.base_url                                         # Verify config loaded from env
            assert _.api_key_name  == self.api_key_name
            assert _.api_key       == self.api_key

            assert _.base_url     is not None                                               # Ensure credentials loaded
            assert _.api_key_name is not None
            assert _.api_key      is not None

    def test__init__missing_credentials(self):                                              # Test initialization fails gracefully without credentials
        import os
        original_base_url = os.environ.get(ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__BASE_URL)

        try:
            if ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__BASE_URL in os.environ:            # Remove env var temporarily
                del os.environ[ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__BASE_URL]

            with pytest.raises(ValueError) as exc_info:                                     # Should raise ValueError
                Semantic_Text__Engine__AWS_Comprehend()

            assert "Missing required environment variables" in str(exc_info.value)          # Verify error message
            assert ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__BASE_URL in str(exc_info.value)

        finally:
            if original_base_url:                                                           # Restore env var
                os.environ[ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__BASE_URL] = original_base_url

    def test_classify_text__positive_sentiment(self):                                       # Test classification of clearly positive text
        if not self.has_credentials:
            pytest.skip("Skipping: Missing AWS Comprehend credentials")

        positive_text = "This is absolutely wonderful! I love it so much. Best day ever!"

        scores = self.engine.classify_text(positive_text)                                   # Call AWS Comprehend API

        assert type(scores) is dict                                                         # Verify return type
        assert len(scores)  == 4                                                            # Should return all 4 criteria

        assert Enum__Text__Classification__Criteria.POSITIVE in scores                      # Verify all criteria present
        assert Enum__Text__Classification__Criteria.NEGATIVE in scores
        assert Enum__Text__Classification__Criteria.NEUTRAL  in scores
        assert Enum__Text__Classification__Criteria.MIXED    in scores

        for criterion, score in scores.items():                                             # Verify all scores are Safe_Float__Text__Classification
            assert type(score) is Safe_Float__Text__Classification
            assert 0.0 <= float(score) <= 1.0                                               # Verify score range

        total_score = sum(float(score) for score in scores.values())                       # Scores should sum to approximately 1.0
        assert 0.99 <= total_score <= 1.01                                                  # Allow small floating point variance

        assert float(scores[Enum__Text__Classification__Criteria.POSITIVE]) > 0.7          # Positive text should have high positive score

    def test_classify_text__negative_sentiment(self):                                       # Test classification of clearly negative text
        if not self.has_credentials:
            pytest.skip("Skipping: Missing AWS Comprehend credentials")

        negative_text = "This is terrible! I hate it. Worst experience ever. Very disappointing."

        scores = self.engine.classify_text(negative_text)

        assert type(scores) is dict
        assert len(scores)  == 4

        for criterion, score in scores.items():                                             # Verify types and ranges
            assert type(score) is Safe_Float__Text__Classification
            assert 0.0 <= float(score) <= 1.0

        total_score = sum(float(score) for score in scores.values())
        assert 0.99 <= total_score <= 1.01

        assert float(scores[Enum__Text__Classification__Criteria.NEGATIVE]) > 0.7          # Negative text should have high negative score

    def test_classify_text__neutral_sentiment(self):                                        # Test classification of neutral text
        if not self.has_credentials:
            pytest.skip("Skipping: Missing AWS Comprehend credentials")

        neutral_text = "The weather report shows 72 degrees. Traffic is moderate on Highway 101."

        scores = self.engine.classify_text(neutral_text)

        assert type(scores) is dict
        assert len(scores)  == 4

        for criterion, score in scores.items():
            assert type(score) is Safe_Float__Text__Classification
            assert 0.0 <= float(score) <= 1.0

        total_score = sum(float(score) for score in scores.values())
        assert 0.99 <= total_score <= 1.01

        assert float(scores[Enum__Text__Classification__Criteria.NEUTRAL]) > 0.5           # Neutral text should have higher neutral score

    def test_classify_text__mixed_sentiment(self):                                          # Test classification of text with mixed emotions
        if not self.has_credentials:
            pytest.skip("Skipping: Missing AWS Comprehend credentials")

        mixed_text = "The product quality is excellent, but the customer service was terrible. Love the features, hate the support."

        scores = self.engine.classify_text(mixed_text)
        assert obj(scores) == __(Enum__Text__Classification__Criteria_POSITIVE = Safe_Float__Text__Classification(0.0004150427121203393),
                                 Enum__Text__Classification__Criteria_NEGATIVE = Safe_Float__Text__Classification(0.0004507373087108135),
                                 Enum__Text__Classification__Criteria_NEUTRAL  = Safe_Float__Text__Classification(3.39194730258896e-06 ),
                                 Enum__Text__Classification__Criteria_MIXED    = Safe_Float__Text__Classification(0.99913090467453     ))


        assert type(scores) is dict
        assert len(scores)  == 4

        for criterion, score in scores.items():
            assert type(score) is Safe_Float__Text__Classification
            assert 0.0 <= float(score) <= 1.0

        total_score = sum(float(score) for score in scores.values())
        assert 0.99 <= total_score <= 1.01

        mixed_score = float(scores[Enum__Text__Classification__Criteria.MIXED])             # Mixed text should have significant both positive and negative

        assert mixed_score  > 0.9                                                           # Both should be notable


    def test_classify_text__empty_text(self):                                               # Test handling of edge case - empty text
        if not self.has_credentials:
            pytest.skip("Skipping: Missing AWS Comprehend credentials")

        empty_text = ""

        try:
            scores = self.engine.classify_text(empty_text)                                  # AWS may handle this or raise error

            if scores:                                                                      # If it returns scores
                assert type(scores) is dict
                assert len(scores)  == 4

                for criterion, score in scores.items():
                    assert type(score) is Safe_Float__Text__Classification

        except (ValueError, RuntimeError) as e:                                             # Or it may raise an error
            assert "empty" in str(e).lower() or "failed" in str(e).lower()                  # Error should mention the issue

    def test_classify_text__very_short_text(self):                                          # Test classification of very short text
        if not self.has_credentials:
            pytest.skip("Skipping: Missing AWS Comprehend credentials")

        short_text = "Great!"

        scores = self.engine.classify_text(short_text)

        assert type(scores) is dict
        assert len(scores)  == 4

        for criterion, score in scores.items():
            assert type(score) is Safe_Float__Text__Classification
            assert 0.0 <= float(score) <= 1.0

        total_score = sum(float(score) for score in scores.values())
        assert 0.99 <= total_score <= 1.01

    def test_classify_text__long_text(self):                                                # Test classification of longer text
        if not self.has_credentials:
            pytest.skip("Skipping: Missing AWS Comprehend credentials")

        long_text = """
        The product arrived on time and was well-packaged. The initial setup was straightforward, 
        and the documentation was clear and helpful. After using it for several weeks, I've found 
        the performance to be consistent and reliable. The build quality meets expectations, and 
        the price point seems reasonable for what you get. Customer support was responsive when 
        I had a question. Overall, this has been a positive experience and I would recommend it 
        to others looking for similar functionality.
        """

        scores = self.engine.classify_text(long_text)

        assert type(scores) is dict
        assert len(scores)  == 4

        for criterion, score in scores.items():
            assert type(score) is Safe_Float__Text__Classification
            assert 0.0 <= float(score) <= 1.0

        total_score = sum(float(score) for score in scores.values())
        assert 0.99 <= total_score <= 1.01

    def test_hash_based_confidence(self):                                                   # Test deterministic hash-based scoring
        if not self.has_credentials:
            pytest.skip("Skipping: Missing AWS Comprehend credentials")

        text1 = "Test text for classification"
        text2 = "Test text for classification"                                              # Same text
        text3 = "Different test text"                                                       # Different text

        scores1 = self.engine.classify_text(text1)                                          # Same text should produce same scores
        scores2 = self.engine.classify_text(text2)

        for criterion in Enum__Text__Classification__Criteria:
            assert float(scores1[criterion]) == float(scores2[criterion])                   # Exact same scores

        scores3 = self.engine.classify_text(text3)                                          # Different text should produce different scores

        differences = 0
        for criterion in Enum__Text__Classification__Criteria:
            if float(scores1[criterion]) != float(scores3[criterion]):
                differences += 1

        assert differences > 0                                                              # At least one score should differ

    def test__call_comprehend_api__invalid_credentials(self):                               # Test API call with invalid credentials
        if not self.has_credentials:
            pytest.skip("Skipping: Missing AWS Comprehend credentials")

        engine = Semantic_Text__Engine__AWS_Comprehend()                                    # Create engine with current credentials
        engine.api_key = "invalid_api_key_for_testing"                                      # Override with invalid key

        with pytest.raises(RuntimeError) as exc_info:                                       # Should raise RuntimeError
            engine._call_comprehend_api("Test text")

        assert "AWS Comprehend API request failed" in str(exc_info.value)                   # Verify error message

    def test__map_comprehend_response(self):                                                # Test mapping AWS Comprehend response to schema
        if not self.has_credentials:
            pytest.skip("Skipping: Missing AWS Comprehend credentials")

        mock_response = {                                                                   # Simulated AWS Comprehend response
            "score": {
                "positive": 0.75,
                "negative": 0.10,
                "neutral": 0.12,
                "mixed": 0.03
            }
        }

        scores = self.engine._map_comprehend_response(mock_response)

        assert type(scores) is dict
        assert len(scores)  == 4

        assert float(scores[Enum__Text__Classification__Criteria.POSITIVE]) == 0.75        # Verify each score mapped correctly
        assert float(scores[Enum__Text__Classification__Criteria.NEGATIVE]) == 0.10
        assert float(scores[Enum__Text__Classification__Criteria.NEUTRAL ]) == 0.12
        assert float(scores[Enum__Text__Classification__Criteria.MIXED   ]) == 0.03

    def test__map_comprehend_response__missing_scores(self):                                # Test mapping with missing score values
        if not self.has_credentials:
            pytest.skip("Skipping: Missing AWS Comprehend credentials")

        mock_response = {                                                                   # Response with missing scores
            "score": {
                "positive": 0.50,
                "negative": 0.30
            }
        }

        scores = self.engine._map_comprehend_response(mock_response)                        # Should default missing scores to 0.0

        assert float(scores[Enum__Text__Classification__Criteria.POSITIVE]) == 0.50
        assert float(scores[Enum__Text__Classification__Criteria.NEGATIVE]) == 0.30
        assert float(scores[Enum__Text__Classification__Criteria.NEUTRAL ]) == 0.00         # Default to 0.0
        assert float(scores[Enum__Text__Classification__Criteria.MIXED   ]) == 0.00         # Default to 0.0

    def test__map_comprehend_response__empty_response(self):                                # Test mapping with empty response
        if not self.has_credentials:
            pytest.skip("Skipping: Missing AWS Comprehend credentials")

        mock_response = {"score": {}}                                                       # Empty score object

        scores = self.engine._map_comprehend_response(mock_response)                        # Should default all to 0.0

        for criterion in Enum__Text__Classification__Criteria:
            assert float(scores[criterion]) == 0.00