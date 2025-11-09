from typing                                                                                             import Dict, List
from osbot_utils.type_safe.Type_Safe                                                                    import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                   import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                    import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                      import Safe_Str__Hash
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                          import type_safe
from mgraph_ai_service_semantic_text.service.semantic_text.Semantic_Text__Service                       import Semantic_Text__Service
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Criteria         import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.service.schemas.safe_float.Safe_Float__Text__Classification        import Safe_Float__Text__Classification
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Request             import Schema__Classification__Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Response            import Schema__Classification__Response
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Filter_Request      import Schema__Classification__Filter_Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Filter_Response     import Schema__Classification__Filter_Response
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode     import Enum__Classification__Output_Mode
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode     import Enum__Classification__Filter_Mode


class Classification__Filter__Service(Type_Safe):                              # Service for filtering hashes based on classification criteria
    semantic_text_service : Semantic_Text__Service = None                      # Service that provides text classifications

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.semantic_text_service = Semantic_Text__Service().setup()          # todo: at the moment this will use Semantic_Text__Engine__Random, when ready we will need to support multiple modes


    @type_safe
    def classify_all(self                                     ,                # Classify all hashes in mapping
                     request: Schema__Classification__Request                  # Classification request
                ) -> Schema__Classification__Response:                         # Classification response with all ratings
        hash_ratings = {}

        for hash_key, text_value in request.hash_mapping.items():
            classification = self.semantic_text_service.classify_text(text_value)
            rating         = classification.text__classification.get(request.classification_criteria)

            if rating is not None:
                hash_ratings[hash_key] = rating

        return Schema__Classification__Response(hash_ratings            = hash_ratings                        ,
                                                classification_criteria = request.classification_criteria      ,
                                                total_hashes            = Safe_UInt(len(request.hash_mapping)) ,
                                                success                 = True                                 )

    @type_safe
    def filter_by_criteria(self                                           ,    # Filter hashes based on criteria threshold
                           request: Schema__Classification__Filter_Request     # Filter request
                      ) -> Schema__Classification__Filter_Response:            # Filtered results
        # First, get all classifications
        classify_request = Schema__Classification__Request(hash_mapping            = request.hash_mapping           ,
                                                           classification_criteria = request.classification_criteria)

        classify_response = self.classify_all(classify_request)

        if not classify_response.success:
            return Schema__Classification__Filter_Response(filtered_hashes         = []                                              ,
                                                           classification_criteria = request.classification_criteria                 ,
                                                           output_mode             = request.output_mode                              ,
                                                           total_hashes            = Safe_UInt(len(request.hash_mapping))             ,
                                                           filtered_count          = Safe_UInt(0)                                     ,
                                                           success                 = False                                            )

        # Apply filter based on filter_mode
        filtered_hashes = self.apply_filter(classify_response.hash_ratings  ,
                                            request.filter_mode              ,
                                            request.threshold                ,
                                            request.threshold_max            )

        # Build response based on output_mode
        return self._build_filter_response(filtered_hashes                ,
                                           request.hash_mapping           ,
                                           classify_response.hash_ratings ,
                                           request.classification_criteria,
                                           request.output_mode            ,
                                           classify_response.total_hashes )

    @type_safe
    def apply_filter(self                                                                  ,  # Apply filter logic to ratings
                     hash_ratings  : Dict[Safe_Str__Hash, Safe_Float__Text__Classification],  # Hash → rating mapping
                     filter_mode   : Enum__Classification__Filter_Mode                     ,  # Filter comparison mode
                     threshold     : Safe_Float                                            ,  # Primary threshold value
                     threshold_max : Safe_Float = None                                        # Max threshold (for BETWEEN)
                ) -> List[Safe_Str__Hash]:                                                    # Filtered hash list
        filtered = []

        for hash_key, rating_value in hash_ratings.items():

            if filter_mode == Enum__Classification__Filter_Mode.ABOVE:
                if rating_value > threshold:
                    filtered.append(hash_key)

            elif filter_mode == Enum__Classification__Filter_Mode.BELOW:
                if rating_value < threshold:
                    filtered.append(hash_key)

            elif filter_mode == Enum__Classification__Filter_Mode.EQUALS:
                if abs(rating_value - threshold) < 0.001:                      # Float comparison tolerance
                    filtered.append(hash_key)

            elif filter_mode == Enum__Classification__Filter_Mode.BETWEEN:
                if threshold_max is not None:
                    if threshold < rating_value < threshold_max:
                        filtered.append(hash_key)

        return filtered

    @type_safe
    def _build_filter_response(self,                                           # Build response based on output mode
                               filtered_hashes          : List[Safe_Str__Hash]                                 ,
                               hash_mapping             : Dict[Safe_Str__Hash, str]                            ,
                               hash_ratings             : Dict[Safe_Str__Hash, Safe_Float__Text__Classification],
                               classification_criteria  : Enum__Text__Classification__Criteria                 ,
                               output_mode              : Enum__Classification__Output_Mode                    ,
                               total_hashes             : Safe_UInt
                          ) -> Schema__Classification__Filter_Response:        # Complete filter response
        filtered_with_text    = None
        filtered_with_ratings = None

        if output_mode in [Enum__Classification__Output_Mode.HASHES_WITH_TEXT, Enum__Classification__Output_Mode.FULL_RATINGS]:
            filtered_with_text = {h: hash_mapping[h] for h in filtered_hashes if h in hash_mapping}

        if output_mode == Enum__Classification__Output_Mode.FULL_RATINGS:
            filtered_with_ratings = {h: hash_ratings[h] for h in filtered_hashes if h in hash_ratings}

        return Schema__Classification__Filter_Response(filtered_hashes         = filtered_hashes           ,
                                                      filtered_with_text      = filtered_with_text        ,
                                                      filtered_with_ratings   = filtered_with_ratings     ,
                                                      classification_criteria = classification_criteria   ,
                                                      output_mode             = output_mode               ,
                                                      total_hashes            = total_hashes              ,
                                                      filtered_count          = Safe_UInt(len(filtered_hashes)),
                                                      success                 = True                      )
