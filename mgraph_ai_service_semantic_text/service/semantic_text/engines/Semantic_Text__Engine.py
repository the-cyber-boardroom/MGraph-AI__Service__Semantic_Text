from osbot_utils.type_safe.Type_Safe                                                       import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text               import Safe_Str__Text
from mgraph_ai_service_semantic_text.schemas.Schema__Semantic_Text__Classification         import Schema__Semantic_Text__Classification
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria    import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Engine_Mode import Enum__Text__Classification__Engine_Mode


class Semantic_Text__Engine(Type_Safe):
    engine_mode              : Enum__Text__Classification__Engine_Mode

    def classify_text(self,
                      text                     : Safe_Str__Text,                            # todo: review the use of Safe_Ste__Text (I think it will be too restrictive, specially when we are using non-random data)
                      classification_criteria  : Enum__Text__Classification__Criteria
                 ) -> Schema__Semantic_Text__Classification:
        raise NotImplementedError()