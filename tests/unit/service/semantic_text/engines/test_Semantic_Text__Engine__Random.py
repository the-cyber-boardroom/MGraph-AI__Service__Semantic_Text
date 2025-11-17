from unittest                                                                                    import TestCase
from osbot_utils.testing.__                                                                      import __
from osbot_utils.type_safe.Type_Safe                                                             import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                            import Type_Safe__Dict
from osbot_utils.utils.Objects                                                                   import base_types
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria          import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Engine_Mode       import Enum__Text__Classification__Engine_Mode
from mgraph_ai_service_semantic_text.schemas.safe_float.Safe_Float__Text__Classification         import Safe_Float__Text__Classification
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine         import Semantic_Text__Engine
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__Random import Semantic_Text__Engine__Random


class test_Semantic_Text__Engine__Random(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.random_engine = Semantic_Text__Engine__Random()

    def test__init__(self):
        with self.random_engine as _:
            assert type(_)       is Semantic_Text__Engine__Random
            assert _.engine_mode == Enum__Text__Classification__Engine_Mode.RANDOM
            assert _.obj()       == __(engine_mode = 'random')
            assert base_types(_) == [Semantic_Text__Engine, Type_Safe, object]

    def test__generate_scores__basic(self):                                    # Test that generate_scores returns 4 criteria
        scores = self.random_engine.generate_scores()

        assert type(scores) is Type_Safe__Dict
        assert len(scores) == 4
        assert Enum__Text__Classification__Criteria.POSITIVE in scores
        assert Enum__Text__Classification__Criteria.NEGATIVE in scores
        assert Enum__Text__Classification__Criteria.NEUTRAL in scores
        assert Enum__Text__Classification__Criteria.MIXED in scores

    def test__generate_scores__valid_range(self):                              # Test that all scores are in valid range (0.0-1.0)
        for _ in range(100):
            scores = self.random_engine.generate_scores()

            for criterion, score in scores.items():
                assert type(score) is Safe_Float__Text__Classification
                assert 0.0 <= float(score) <= 1.0

    def test__generate_scores__sum_to_one(self):                               # Test that scores sum to 1.0 (normalized)
        for _ in range(100):
            scores = self.random_engine.generate_scores()
            total = sum(scores.values())
            assert abs(total - 1.0) < 0.0001                                    # Should sum to ~1.0

    def test__generate_scores__different_each_time(self):                      # Test that scores are different each time (random)
        scores1 = self.random_engine.generate_scores()
        scores2 = self.random_engine.generate_scores()
        scores3 = self.random_engine.generate_scores()

        # At least one score should be different between any two generations
        assert scores1 != scores2 or scores1 != scores3 or scores2 != scores3

    def test__classify_text__basic(self):                                      # Test basic text classification
        result = self.random_engine.classify_text(text='abc')

        assert type(result) is Type_Safe__Dict
        assert len(result) == 4                                                 # Always returns all 4 criteria
        assert Enum__Text__Classification__Criteria.POSITIVE in result
        assert Enum__Text__Classification__Criteria.NEGATIVE in result
        assert Enum__Text__Classification__Criteria.NEUTRAL in result
        assert Enum__Text__Classification__Criteria.MIXED   in result

    def test__classify_text__valid_scores(self):                               # Test that classification returns valid scores
        result = self.random_engine.classify_text(text='Hello World')

        for criterion, score in result.items():
            assert type(score) is Safe_Float__Text__Classification
            assert 0.0 <= float(score) <= 1.0

        total = sum(result.values())
        assert abs(total - 1.0) < 0.0001                                        # Scores should sum to ~1.0

    def test__classify_text__random_each_call(self):                           # Test that same text gets different random scores
        result1 = self.random_engine.classify_text(text='Same text')
        result2 = self.random_engine.classify_text(text='Same text')
        result3 = self.random_engine.classify_text(text='Same text')

        # At least one result should differ (random nature)
        # We can't guarantee ALL are different due to randomness, but at least some should be
        all_same = (result1.obj() == result2.obj() == result3.obj())
        assert not all_same, "Random engine should produce different scores for same text"

    def test__classify_text__multiple_texts(self):                             # Test classification of multiple different texts
        texts = ['Text 1', 'Text 2', 'Text 3', 'Different', 'Another']

        for text in texts:
            result = self.random_engine.classify_text(text=text)

            assert len(result) == 4
            total = sum(result.values())
            assert abs(total - 1.0) < 0.0001

    def test__classify_text__distribution(self):                               # Test that scores are well distributed over many samples
        results = []
        for i in range(100):
            result = self.random_engine.classify_text(text=f'Sample {i}')
            results.append(result[Enum__Text__Classification__Criteria.POSITIVE])

        # Check we have variety
        unique_values = len(set(float(r) for r in results))
        assert unique_values > 50, f"Only {unique_values} unique scores out of 100"

        # Check coverage of range
        min_score = min(float(r) for r in results)
        max_score = max(float(r) for r in results)
        assert min_score < max_score

    def test__classify_text__empty_string(self):                               # Test with empty string
        result = self.random_engine.classify_text(text='')

        assert len(result) == 4
        total = sum(result.values())
        assert abs(total - 1.0) < 0.0001

    def test__classify_text__special_characters(self):                         # Test with special characters
        result = self.random_engine.classify_text(text='!@#$%^&*()')

        assert len(result) == 4
        total = sum(result.values())
        assert abs(total - 1.0) < 0.0001

    def test__classify_text__unicode(self):                                    # Test with unicode characters
        result = self.random_engine.classify_text(text='Hello 世界')

        assert len(result) == 4
        total = sum(result.values())
        assert abs(total - 1.0) < 0.0001