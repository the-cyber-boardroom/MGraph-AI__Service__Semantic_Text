from typing                                                                                         import Dict, List
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash              import Safe_Str__Hash
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Criteria import Enum__Text__Classification__Criteria


class Schema__Classification__Multi_Criteria_Request(Type_Safe):               # Request to classify hashes by multiple criteria
    hash_mapping               : Dict[Safe_Str__Hash, str]                     # Hash → original text mapping
    classification_criteria    : List[Enum__Text__Classification__Criteria]    # List of criteria to classify by (e.g., [positivity, negativity, toxicity])
