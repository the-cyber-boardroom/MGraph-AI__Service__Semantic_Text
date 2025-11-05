from typing                                                                                               import Dict
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode        import Enum__Text__Transformation__Mode


class Text__Transformation__Engine(Type_Safe):                                      # Base class for text transformation engines
    transformation_mode     : Enum__Text__Transformation__Mode                      # Transformation mode this engine handles
    randomness_percentage   : Safe_Float                    = Safe_Float(0.5)       # Percentage of hashes to transform (0.0-1.0)

    def transform(self,                                                             # Transform hash mapping according to engine logic
                       hash_mapping: Dict[Safe_Str__Hash, str]                      # Input hash → text mapping
                  ) -> Dict[Safe_Str__Hash, str]:                                   # Transformed hash → text mapping
        raise NotImplementedError(f"Subclass must implement transform() method")