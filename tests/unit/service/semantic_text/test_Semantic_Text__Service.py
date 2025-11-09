from unittest                                                                                        import TestCase
from osbot_utils.testing.__                                                                          import __, __SKIP__
from mgraph_ai_service_semantic_text.service.schemas.Schema__Semantic_Text__Classification           import Schema__Semantic_Text__Classification
from mgraph_ai_service_semantic_text.service.semantic_text.Semantic_Text__Service                    import Semantic_Text__Service
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__Hash_Based import Semantic_Text__Engine__Hash_Based


class test_Semantic_Text__Service(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.semantic_text_service = Semantic_Text__Service().setup()

    def test__init__(self):
        with self.semantic_text_service as _:
            assert type(_                      ) is Semantic_Text__Service
            assert type(_.semantic_text__engine) is Semantic_Text__Engine__Hash_Based


    def test_classify_text(self):                                               # Test with deterministic hash-based engine
        with self.semantic_text_service as _:
            result = _.classify_text('abc')
            assert type(result) is Schema__Semantic_Text__Classification
            assert result.obj() == __(text                 = 'abc'                                                       ,
                                      text__hash           = '900150983c'                                                ,   # the hash for 'abc' is always '900150983c'
                                      text__classification = __(Enum__Text__Classification__Criteria_POSITIVITY = 0.862) ,   # so is the text__classification (because we are using the Semantic_Text__Engine__Hash_Based)
                                      engine_mode          = 'text_hash'                                                 )

    def test_classify_text__deterministic(self):                                # Test that results are deterministic
        with self.semantic_text_service as _:
            result1 = _.classify_text('Hello World')
            result2 = _.classify_text('Hello World')
            result3 = _.classify_text('Hello World')

            # All should be identical
            assert result1.obj() == result2.obj()
            assert result2.obj() == result3.obj()

            # Known value for regression testing
            assert result1.obj() == __(text                 = 'Hello World'                                                ,
                                       text__hash           = 'b10a8db164'                                                 ,
                                       text__classification = __(Enum__Text__Classification__Criteria_POSITIVITY = 0.7478) ,
                                       engine_mode          = 'text_hash'                                                  )


    def test_classify_text__different_texts(self):                              # Test that different texts get different ratings
        with self.semantic_text_service as _:
            result1 = _.classify_text('Positive')
            result2 = _.classify_text('Negative')

            rating1 = result1.text__classification[result1.text__classification.keys().__iter__().__next__()]
            rating2 = result2.text__classification[result2.text__classification.keys().__iter__().__next__()]

            assert rating1 != rating2

            assert rating1 == 0.3449
            assert rating2 == 0.1429
