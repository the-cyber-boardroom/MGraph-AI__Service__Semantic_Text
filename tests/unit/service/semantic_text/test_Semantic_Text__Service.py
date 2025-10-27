from unittest                                                                                    import TestCase
from osbot_utils.testing.__                                                                      import __, __SKIP__
from mgraph_ai_service_semantic_text.service.schemas.Schema__Semantic_Text__Classification       import Schema__Semantic_Text__Classification
from mgraph_ai_service_semantic_text.service.semantic_text.Semantic_Text__Service                import Semantic_Text__Service
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__Random import Semantic_Text__Engine__Random

class test_Semantic_Text__Service(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.semantic_text_service = Semantic_Text__Service().setup()

    def test__init__(self):
        with self.semantic_text_service as _:
            assert type(_                      ) is Semantic_Text__Service
            assert type(_.semantic_text__engine) is Semantic_Text__Engine__Random

    def test_classify_text(self):
        with self.semantic_text_service as _:
            result = _.classify_text('abc')
            assert type(result) is Schema__Semantic_Text__Classification
            assert result.obj() ==  __(text                 = 'abc'                    ,
                                       text__hash           = '900150983c'             ,        # the hash for 'abc' is always '900150983c'
                                       text__classification = __(positivity = __SKIP__),
                                       engine_mode          = 'random'                 )

