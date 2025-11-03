from typing                                                                                                   import Dict
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode        import Enum__Text__Transformation__Mode


# todo: create Safe_Str__* schema for hash_mapping str
class Schema__Text__Transformation__Request(Type_Safe):                             # Text transformation request from Mitmproxy
    hash_mapping            : Dict[Safe_Str__Hash, str]                             # Hash → original text mapping from HTML Service
    transformation_mode     : Enum__Text__Transformation__Mode                      # Transformation mode to apply
    randomness_percentage   : Safe_Float                       = 0.5                # Percentage of hashes to transform (0.0-1.0)