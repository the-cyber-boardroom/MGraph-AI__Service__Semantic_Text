from typing                                                                                               import Dict
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text                             import Safe_Str__Comprehend__Text
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode        import Enum__Text__Transformation__Mode

class Schema__Text__Transformation__Request(Type_Safe):                             # Text transformation request from Mitmproxy
    hash_mapping            : Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]      # Hash → original text mapping from HTML Service
    transformation_mode     : Enum__Text__Transformation__Mode                      # Transformation mode to apply
    randomness_percentage   : Safe_Float                       = 0.5                # Percentage of hashes to transform (0.0-1.0)