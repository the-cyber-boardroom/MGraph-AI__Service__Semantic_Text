from typing                                                                                      import Dict
from osbot_utils.type_safe.Type_Safe                                                             import Type_Safe
from osbot_utils.type_safe.primitives.safe_str.cryptography.hashes.Safe_Str__Hash                import Safe_Str__Hash
from osbot_utils.type_safe.primitives.safe_str.text.Safe_Str__Text                               import Safe_Str__Text
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Criteria  import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Engine_Mode import Enum__Text__Classification__Engine_Mode
from mgraph_ai_service_semantic_text.service.schemas.safe_float.Safe_Float__Text__Classification import Safe_Float__Text__Classification


class Schema__Semantic_Text__Classification(Type_Safe):
    text                : Safe_Str__Text
    text__hash          : Safe_Str__Hash                            = None
    text__classification: Dict[Enum__Text__Classification__Criteria,
                               Safe_Float__Text__Classification    ]
    engine_mode         : Enum__Text__Classification__Engine_Mode

