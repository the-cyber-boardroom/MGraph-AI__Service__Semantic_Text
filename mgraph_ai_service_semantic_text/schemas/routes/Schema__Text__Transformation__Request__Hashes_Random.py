from typing                                                                      import Dict
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                            import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash import Safe_Str__Hash


class Schema__Text__Transformation__Request__Hashes_Random(Type_Safe):           # Request for hashes-random transformation
    hash_mapping            : Dict[Safe_Str__Hash, str]                          # Hash → original text mapping
    randomness_percentage   : Safe_Float                       = 0.5             # Percentage of hashes to transform (0.0-1.0)