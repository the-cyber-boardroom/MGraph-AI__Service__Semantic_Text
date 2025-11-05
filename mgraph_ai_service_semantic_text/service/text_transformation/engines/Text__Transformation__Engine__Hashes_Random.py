from typing                                                                                               import Dict
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                            import type_safe
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine     import Text__Transformation__Engine
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Selection__Service                 import Text__Selection__Service
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode        import Enum__Text__Transformation__Mode


class Text__Transformation__Engine__Hashes_Random(Text__Transformation__Engine):                            # Randomly replace text with hash values
    transformation_mode : Enum__Text__Transformation__Mode = Enum__Text__Transformation__Mode.HASHES_RANDOM
    text_selection      : Text__Selection__Service                                                          # Service for random selection

    @type_safe
    def transform(self,                                                             # Randomly show ~50% of text as hash values
                  hash_mapping: Dict[Safe_Str__Hash, str]                           # Input hash → text mapping
             ) -> Dict[Safe_Str__Hash, str]:                                        # Transformed hash → text mapping
        if not hash_mapping:
            return hash_mapping

        selected_hashes  = self.text_selection.randomly_select_hashes(hash_mapping, self.randomness_percentage)
        modified_mapping = {}

        for hash_key, original_text in hash_mapping.items():
            if hash_key in selected_hashes:
                modified_mapping[hash_key] = str(hash_key)                          # Replace text with hash value itself
            else:
                modified_mapping[hash_key] = original_text                          # Keep original text

        return modified_mapping