from unittest                                                                                    import TestCase
from osbot_utils.testing.__                                                                      import __, __SKIP__
from mgraph_ai_service_semantic_text.schemas.Schema__Semantic_Text__Classification               import Schema__Semantic_Text__Classification
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria          import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.safe_float.Safe_Float__Text__Classification         import Safe_Float__Text__Classification
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__Random import Semantic_Text__Engine__Random


class test_Semantic_Text__Engine__Random(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.random_engine = Semantic_Text__Engine__Random()

    def test__init__(self):
        with self.random_engine as _:
            assert type(_) is Semantic_Text__Engine__Random

    def test_random_classification(self):
        with self.random_engine as _:
            assert type(_.random_classification()) is Safe_Float__Text__Classification
            for i in range(0,1000):
                assert 0 <= _.random_classification() <= 1

    def test_classify_text(self):
        with self.random_engine as _:
            result = _.classify_text(text='abc', classification_criteria=Enum__Text__Classification__Criteria.POSITIVE)
            assert type(result) is Schema__Semantic_Text__Classification
            assert result.obj() == __( text                 = 'abc'                   ,
                                       text__hash           = '900150983c'            ,        # the hash for 'abc' is always '900150983c'
                                       text__classification = __(positivity = __SKIP__),
                                       engine_mode          = 'random'                )