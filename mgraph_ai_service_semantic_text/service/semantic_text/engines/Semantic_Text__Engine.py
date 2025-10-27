from osbot_utils.type_safe.Type_Safe                                                               import Type_Safe
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Criteria    import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Engine_Mode import Enum__Text__Classification__Engine_Mode


class Semantic_Text__Engine(Type_Safe):
    classification__criteria : Enum__Text__Classification__Criteria     = Enum__Text__Classification__Criteria.POSITIVITY        # todo: we start with this here, but we need a better way to indicate this
    engine_mode              : Enum__Text__Classification__Engine_Mode


    def classify_text(self):
        raise NotImplementedError()