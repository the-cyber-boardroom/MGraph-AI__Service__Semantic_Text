from typing                                                                          import Dict, List, Optional
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                             import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash import Safe_Str__Hash


class Schema__Topic_Filter__Response(Type_Safe):                               # Response with filtered hashes based on topic criteria
    filtered_hashes         : List[Safe_Str__Hash]                             # List of hash IDs that matched filters
    filtered_with_text      : Optional[Dict[Safe_Str__Hash, str]]      = None  # Hash → text mapping (if output_mode includes text)
    filtered_with_scores    : Optional[Dict[Safe_Str__Hash, Dict]]     = None  # Hash → {topic → confidence} (if output_mode includes scores)
    topics_used             : List                                             # List of Enum__Classification__Topic used in filtering
    logic_operator          : None                                             # Enum__Classification__Logic_Operator used - typed as None
    output_mode             : None                                             # Enum__Classification__Output_Mode used - typed as None
    total_hashes            : Safe_UInt                                        # Total number of hashes in input
    filtered_count          : Safe_UInt                                        # Number of hashes that passed filters
    success                 : bool                                             # Whether filtering succeeded
