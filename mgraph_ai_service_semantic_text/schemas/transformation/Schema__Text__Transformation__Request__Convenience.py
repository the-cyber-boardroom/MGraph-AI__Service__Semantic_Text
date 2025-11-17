from typing                                                                        import Dict
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text      import Safe_Str__Comprehend__Text
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash import Safe_Str__Hash

# todo: rename 'Convenience' to a better name
class Schema__Text__Transformation__Request__Convenience(Type_Safe):               # Simplified request schema for convenience routes with path params
    hash_mapping : Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]               # Hash → original text mapping (only required field)