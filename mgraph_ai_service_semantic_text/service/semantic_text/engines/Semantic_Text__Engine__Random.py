from osbot_utils.utils.Misc                                                                         import random_number
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                      import type_safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                        import Safe_Str__Text
from mgraph_ai_service_semantic_text.service.schemas.Schema__Semantic_Text__Classification          import Schema__Semantic_Text__Classification
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Engine_Mode  import Enum__Text__Classification__Engine_Mode
from mgraph_ai_service_semantic_text.service.schemas.safe_float.Safe_Float__Text__Classification    import Safe_Float__Text__Classification
from mgraph_ai_service_semantic_text.service.semantic_text.Semantic_Text__Hashes                    import Semantic_Text__Hashes
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine            import Semantic_Text__Engine


# todo: Semantic_Text__Engine__Text_Hash (uses classification from text_hash)

class Semantic_Text__Engine__Random(Semantic_Text__Engine):

    engine_mode              : Enum__Text__Classification__Engine_Mode  = Enum__Text__Classification__Engine_Mode.RANDOM
    semantic_text_hashes     : Semantic_Text__Hashes

    @type_safe
    def classify_text(self,text: Safe_Str__Text) -> Schema__Semantic_Text__Classification:
        classification_value = self.random_classification()
        text_hash            = self.semantic_text_hashes.hash__for_text(text)               # todo: double check if we always need to calculate this (specially since in some case we will already know the hash)
        kwargs = dict(text                 = text                                                 ,
                      text__hash           = text_hash                                            ,
                      text__classification = { self.classification__criteria:classification_value},
                      engine_mode          = self.engine_mode                                     )
        return Schema__Semantic_Text__Classification(**kwargs)

    def random_classification(self) -> Safe_Float__Text__Classification:
        value = random_number(0,100) / 100
        return Safe_Float__Text__Classification(value)
