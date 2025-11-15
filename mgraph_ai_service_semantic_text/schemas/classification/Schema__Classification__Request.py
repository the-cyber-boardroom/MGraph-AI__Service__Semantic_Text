from typing                                                                             import Dict
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash      import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria import Enum__Text__Classification__Criteria


class Schema__Classification__Request(Type_Safe):                              # Request to classify hash mapping by criteria
    hash_mapping             : Dict[Safe_Str__Hash, str]                       # Hash → original text mapping
    classification_criteria : Enum__Text__Classification__Criteria             # Criteria to classify by (e.g., positivity)
