from unittest                                                                                        import TestCase
from osbot_utils.testing.__                                                                          import __
from osbot_utils.type_safe.Type_Safe                                                                 import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                                import Type_Safe__Dict
from osbot_utils.utils.Objects                                                                       import base_types
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria              import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Engine_Mode           import Enum__Text__Classification__Engine_Mode
from mgraph_ai_service_semantic_text.schemas.safe_float.Safe_Float__Text__Classification             import Safe_Float__Text__Classification
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine             import Semantic_Text__Engine
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__Hash_Based import Semantic_Text__Engine__Hash_Based


class test_Semantic_Text__Engine__Hash_Based(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.hash_engine = Semantic_Text__Engine__Hash_Based()

    def test__init__(self):
        with self.hash_engine as _:
            assert type(_)       is Semantic_Text__Engine__Hash_Based
            assert _.engine_mode == Enum__Text__Classification__Engine_Mode.TEXT_HASH
            assert _.obj()       == __(engine_mode = 'text_hash')
            assert base_types(_) == [Semantic_Text__Engine, Type_Safe, object]

    def test__hash_score_for_criterion__deterministic(self):                   # Test that hash_score_for_criterion is deterministic
        text     = 'Hello World'
        criterion = Enum__Text__Classification__Criteria.POSITIVE

        rating1 = self.hash_engine.hash_score_for_criterion(text, criterion)
        rating2 = self.hash_engine.hash_score_for_criterion(text, criterion)
        rating3 = self.hash_engine.hash_score_for_criterion(text, criterion)

        assert float(rating1) == float(rating2) == float(rating3)
        assert float(rating1) == 0.6974                                         # Raw unnormalized value
        assert rating1        == 0.6974

    def test__classify_text__basic(self):                                      # Test basic text classification returns all 4 criteria
        result = self.hash_engine.classify_text(text='Hello World')

        assert type(result) is Type_Safe__Dict
        assert len(result) == 4                                                 # Always returns all 4 criteria
        assert Enum__Text__Classification__Criteria.POSITIVE in result
        assert Enum__Text__Classification__Criteria.NEGATIVE in result
        assert Enum__Text__Classification__Criteria.NEUTRAL in result
        assert Enum__Text__Classification__Criteria.MIXED in result

        # Check normalized values (sum to 1.0)
        assert result.obj() == __(positive = 0.61575136853258      ,
                                  negative = 0.06092177291188416   ,
                                  neutral  = 0.2944552357407734    ,
                                  mixed    = 0.028871622814762493  )

        total = sum(result.values())
        assert abs(total - 1.0) < 0.0001                                        # Sum should be ~1.0

    def test__classify_text__deterministic(self):                              # Test that same text always produces same ratings
        result1 = self.hash_engine.classify_text(text='Hello World')
        result2 = self.hash_engine.classify_text(text='Hello World')
        result3 = self.hash_engine.classify_text(text='Hello World')

        assert result1[Enum__Text__Classification__Criteria.POSITIVE] == result2[Enum__Text__Classification__Criteria.POSITIVE]
        assert result2[Enum__Text__Classification__Criteria.POSITIVE] == result3[Enum__Text__Classification__Criteria.POSITIVE]
        assert result1.obj() == result2.obj() == result3.obj()

    def test__classify_text__known_values(self):                               # Test specific known hash values for regression testing
        result_abc   = self.hash_engine.classify_text(text='abc')
        result_xyz   = self.hash_engine.classify_text(text='xyz')
        result_hello = self.hash_engine.classify_text(text='Hello World')

        # These values are deterministic based on MD5 hash (normalized)
        assert result_abc.obj()   == __(positive=0.27980546549328394,
                                        negative=0.3474293654469662,
                                        neutral=0.2902732746641964,
                                        mixed=0.0824918943955535)

        assert result_xyz.obj()   == __(positive=0.21508352758352758,
                                        negative=0.05676961926961927,
                                        neutral=0.42045454545454547,
                                        mixed=0.3076923076923077)

        assert result_hello.obj() == __(positive = 0.61575136853258      ,
                                        negative = 0.06092177291188416   ,
                                        neutral  = 0.2944552357407734    ,
                                        mixed    = 0.028871622814762493  )

    def test__classify_text__different_text_different_ratings(self):           # Test that different text produces different ratings
        result1 = self.hash_engine.classify_text(text='Positive')
        result2 = self.hash_engine.classify_text(text='Negative')
        result3 = self.hash_engine.classify_text(text='Neutral')

        rating1 = result1[Enum__Text__Classification__Criteria.POSITIVE]
        rating2 = result2[Enum__Text__Classification__Criteria.POSITIVE]
        rating3 = result3[Enum__Text__Classification__Criteria.POSITIVE]

        # All should be different
        assert rating1 != rating2
        assert rating2 != rating3
        assert rating1 != rating3

        assert type(rating1) is Safe_Float__Text__Classification
        assert rating1 == 0.27130292347683654
        assert rating2 == 0.5445267284834153
        assert rating3 == 0.5256974248927039

    def test__classify_text__different_criteria_same_text(self):               # Test that same text produces different ratings for each criterion
        text = 'The same text'
        result = self.hash_engine.classify_text(text=text)

        rating_positive = result[Enum__Text__Classification__Criteria.POSITIVE]
        rating_negative = result[Enum__Text__Classification__Criteria.NEGATIVE]
        rating_neutral  = result[Enum__Text__Classification__Criteria.NEUTRAL]
        rating_mixed    = result[Enum__Text__Classification__Criteria.MIXED]

        # Same text, different criteria should produce different ratings
        assert rating_positive != rating_negative
        assert rating_negative != rating_neutral
        assert rating_neutral  != rating_mixed
        assert rating_positive == 0.18653727028701217
        assert rating_negative == 0.30629774932892834
        assert rating_neutral  == 0.19529217427214537
        assert rating_mixed    == 0.3118728061119141

    def test__classify_text__ratings_in_range(self):                           # Test that all ratings are within valid range (0.0-1.0)
        test_texts = ['Hello', 'World', 'Test', 'Classification', 'Random text',
                     'Short', 'A very long piece of text that should still produce a valid rating',
                     '123', 'Special !@#$%', '']

        for text in test_texts:
            result = self.hash_engine.classify_text(text=text)

            for criterion in Enum__Text__Classification__Criteria:
                rating = result[criterion]
                assert 0.0 <= float(rating) <= 1.0, f"Rating {rating} for text '{text}' criterion {criterion} is out of range"

    def test__classify_text__empty_string(self):                               # Test with empty string
        result = self.hash_engine.classify_text(text='')

        assert type(result) is Type_Safe__Dict
        assert len(result) == 4

        for criterion in Enum__Text__Classification__Criteria:
            rating = result[criterion]
            assert 0.0 <= float(rating) <= 1.0

    def test__classify_text__special_characters(self):                         # Test with special characters
        result1 = self.hash_engine.classify_text(text='Hello!')
        result2 = self.hash_engine.classify_text(text='Hello!')

        # Should be deterministic even with special chars
        assert result1 == result2
        assert result1.obj() == result2.obj()

    def test__classify_text__unicode(self):                                    # Test with unicode characters
        result1 = self.hash_engine.classify_text(text='Hello 世界')
        result2 = self.hash_engine.classify_text(text='Hello 世界')

        # Should be deterministic with unicode
        assert result1 == result2
        assert result1[Enum__Text__Classification__Criteria.POSITIVE] == 0.24120288190456302

    def test__classify_text__whitespace_sensitive(self):                       # Test that whitespace differences matter
        result1 = self.hash_engine.classify_text(text='Hello World')
        result2 = self.hash_engine.classify_text(text='HelloWorld'  )
        result3 = self.hash_engine.classify_text(text='Hello  World')

        rating1 = result1[Enum__Text__Classification__Criteria.POSITIVE]
        rating2 = result2[Enum__Text__Classification__Criteria.POSITIVE]
        rating3 = result3[Enum__Text__Classification__Criteria.POSITIVE]

        # All should be different (whitespace matters)
        assert rating1 != rating2
        assert rating2 != rating3
        assert rating1 != rating3
        assert rating1 == 0.61575136853258
        assert rating2 == 0.060433662516101334
        assert rating3 == 0.4939106901217862

    def test__classify_text__case_sensitive(self):                             # Test that case differences matter
        result1 = self.hash_engine.classify_text(text='hello')
        result2 = self.hash_engine.classify_text(text='Hello')
        result3 = self.hash_engine.classify_text(text='HELLO')

        rating1 = result1[Enum__Text__Classification__Criteria.POSITIVE]
        rating2 = result2[Enum__Text__Classification__Criteria.POSITIVE]
        rating3 = result3[Enum__Text__Classification__Criteria.POSITIVE]

        # All should be different (case matters)
        assert rating1 != rating2
        assert rating2 != rating3
        assert rating1 != rating3
        assert rating1 == 0.03312968961417032
        assert rating2 == 0.29310656775827754
        assert rating3 == 0.4463864413308296

    def test__hash_score_for_criterion__distribution(self):                    # Test that raw scores are reasonably distributed
        ratings = []
        criterion = Enum__Text__Classification__Criteria.POSITIVE

        for i in range(100):
            rating = self.hash_engine.hash_score_for_criterion(text=f'Text sample {i}', criterion=criterion)
            ratings.append(float(rating))

        # Check we have variety (not all the same)
        unique_ratings = len(set(ratings))
        assert unique_ratings > 50, f"Only {unique_ratings} unique ratings out of 100"

        # Check we cover the range reasonably
        min_rating = min(ratings)
        max_rating = max(ratings)
        assert min_rating < 0.3, f"Min rating {min_rating} should be lower"
        assert max_rating > 0.7, f"Max rating {max_rating} should be higher"

    def test__normalize_scores__basic(self):                                   # Test score normalization
        raw_scores = {
            Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.5),
            Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.3),
            Enum__Text__Classification__Criteria.NEUTRAL:  Safe_Float__Text__Classification(0.2),
            Enum__Text__Classification__Criteria.MIXED:    Safe_Float__Text__Classification(0.1)
        }

        normalized = self.hash_engine._normalize_scores(raw_scores)

        # Check sum is 1.0
        total = sum(normalized.values())
        assert abs(total - 1.0) < 0.0001

        # Check proportions maintained
        assert normalized[Enum__Text__Classification__Criteria.POSITIVE] > normalized[Enum__Text__Classification__Criteria.NEGATIVE]
        assert normalized[Enum__Text__Classification__Criteria.NEGATIVE] > normalized[Enum__Text__Classification__Criteria.NEUTRAL]
        assert normalized[Enum__Text__Classification__Criteria.NEUTRAL]  > normalized[Enum__Text__Classification__Criteria.MIXED]

    def test__normalize_scores__all_zeros(self):                               # Test normalization with all zeros (edge case)
        raw_scores = {
            Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.0),
            Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.0),
            Enum__Text__Classification__Criteria.NEUTRAL:  Safe_Float__Text__Classification(0.0),
            Enum__Text__Classification__Criteria.MIXED:    Safe_Float__Text__Classification(0.0)
        }

        normalized = self.hash_engine._normalize_scores(raw_scores)

        # Should distribute equally when all zeros
        total = sum(normalized.values())
        assert abs(total - 1.0) < 0.0001
        assert all(abs(float(v) - 0.25) < 0.0001 for v in normalized.values())