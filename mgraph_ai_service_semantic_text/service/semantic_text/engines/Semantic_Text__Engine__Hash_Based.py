from hashlib                                                                                        import md5
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                      import type_safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                        import Safe_Str__Text
from mgraph_ai_service_semantic_text.service.schemas.Schema__Semantic_Text__Classification          import Schema__Semantic_Text__Classification
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Criteria     import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Engine_Mode  import Enum__Text__Classification__Engine_Mode
from mgraph_ai_service_semantic_text.service.schemas.safe_float.Safe_Float__Text__Classification    import Safe_Float__Text__Classification
from mgraph_ai_service_semantic_text.service.semantic_text.Semantic_Text__Hashes                    import Semantic_Text__Hashes
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine            import Semantic_Text__Engine


class Semantic_Text__Engine__Hash_Based(Semantic_Text__Engine):                # Deterministic hash-based classification engine

    engine_mode              : Enum__Text__Classification__Engine_Mode  = Enum__Text__Classification__Engine_Mode.TEXT_HASH
    semantic_text_hashes     : Semantic_Text__Hashes

    @type_safe
    def classify_text(self,
                      text                    : Safe_Str__Text,                                         # todo: review the use of Safe_Ste__Text (I think it will be too restrictive, specially when we are using non-random data)
                      classification_criteria : Enum__Text__Classification__Criteria
                 ) -> Schema__Semantic_Text__Classification:

        classification_value = self.hash_based_classification(text                    = text,
                                                              classification_criteria = classification_criteria)
        text_hash            = self.semantic_text_hashes.hash__for_text(text)
        kwargs = dict(text                 = text,
                      text__hash           = text_hash,
                      text__classification = {classification_criteria:classification_value},
                      engine_mode          = self.engine_mode)
        return Schema__Semantic_Text__Classification(**kwargs)


    @type_safe
    def hash_based_classification(self,
                                  text                    : Safe_Str__Text                      ,
                                  classification_criteria : Enum__Text__Classification__Criteria
                             ) -> Safe_Float__Text__Classification:

        combined  = f"{text}_{classification_criteria.value}"                                         # Combine text + criteria for unique rating per criterion
        full_hash = md5(combined.encode()).hexdigest()                                                      # Get MD5 hash (32 hex characters)
        hash_int  = int(full_hash[:16], 16)                                                                 # Convert first 16 hex chars (64 bits) to integer
        rating    = (hash_int % 10000) / 10000.0                                                            # Normalize to 0.0-1.0 range using modulo for even distribution
        return Safe_Float__Text__Classification(rating)
