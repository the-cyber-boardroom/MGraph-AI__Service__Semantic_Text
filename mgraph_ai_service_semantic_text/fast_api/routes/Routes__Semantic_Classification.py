from fastapi                                                                                                        import HTTPException
from osbot_fast_api.api.routes.Fast_API__Routes                                                                     import Fast_API__Routes
from osbot_fast_api.api.schemas.safe_str.Safe_Str__Fast_API__Route__Tag                                             import Safe_Str__Fast_API__Route__Tag
from mgraph_ai_service_semantic_text.service.semantic_text.classification.Classification__Filter__Service           import Classification__Filter__Service
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Request                         import Schema__Classification__Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Response                        import Schema__Classification__Response
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Filter_Request                  import Schema__Classification__Filter_Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Filter_Response                 import Schema__Classification__Filter_Response
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Request          import Schema__Classification__Multi_Criteria_Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Response         import Schema__Classification__Multi_Criteria_Response
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Filter_Request   import Schema__Classification__Multi_Criteria_Filter_Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Filter_Response  import Schema__Classification__Multi_Criteria_Filter_Response


TAG__ROUTES_SEMANTIC_CLASSIFICATION   = 'semantic-classification'
ROUTES_PATHS__SEMANTIC_CLASSIFICATION = [f'/{TAG__ROUTES_SEMANTIC_CLASSIFICATION}' + '/single/rate'   ,  # Level 1: Rate all hashes
                                         f'/{TAG__ROUTES_SEMANTIC_CLASSIFICATION}' + '/single/filter' ,  # Level 1: Filter by threshold
                                         f'/{TAG__ROUTES_SEMANTIC_CLASSIFICATION}' + '/multi/rate'    ,  # Level 2: Rate by multiple criteria
                                         f'/{TAG__ROUTES_SEMANTIC_CLASSIFICATION}' + '/multi/filter'  ]  # Level 2: Filter by multiple criteria


class Routes__Semantic_Classification(Fast_API__Routes):                                            # FastAPI routes for semantic text classification
    tag                    : Safe_Str__Fast_API__Route__Tag    = TAG__ROUTES_SEMANTIC_CLASSIFICATION   # OpenAPI tag
    classification_service : Classification__Filter__Service                                        # Classification filter service

    # ========================================
    # Level 1: Single Criterion (Positivity)
    # ========================================

    def single__rate(self,                                                  # Rate all hashes by single criterion
                     request: Schema__Classification__Request               # Classification request
                ) -> Schema__Classification__Response:                      # Classification response with ratings

        response = self.classification_service.classify_all(request)

        if not response.success:
            raise HTTPException(status_code=500, detail="Classification failed")

        return response

    def single__filter(self,                                                    # Filter hashes by criterion threshold
                       request: Schema__Classification__Filter_Request          # Filter request
                  ) -> Schema__Classification__Filter_Response:                 # Filtered results

        response = self.classification_service.filter_by_criteria(request)

        if not response.success:
            raise HTTPException(status_code=500, detail="Filter failed")

        return response


    # ========================================
    # Level 2: Multiple Criteria
    # ========================================

    def multi__rate(self,                                                               # Rate all hashes by multiple criteria
                    request: Schema__Classification__Multi_Criteria_Request             # Multi-criteria classification request
               ) -> Schema__Classification__Multi_Criteria_Response:                    # Multi-criteria classification response

        response = self.classification_service.classify_all__multi_criteria(request)

        if not response.success:
            raise HTTPException(status_code=500, detail="Multi-criteria classification failed")

        return response


    def multi__filter(self,                                                             # Filter hashes by multiple criteria with AND/OR logic
                      request: Schema__Classification__Multi_Criteria_Filter_Request    # Multi-criteria filter request
                 ) -> Schema__Classification__Multi_Criteria_Filter_Response:           # Multi-criteria filtered results

        response = self.classification_service.filter_by_multi_criteria(request)

        if not response.success:
            raise HTTPException(status_code=500, detail="Multi-criteria filter failed")

        return response

    def setup_routes(self):                                                    # Register all route handlers
        self.add_route_post(self.single__rate  )                               # Level 1: Rate endpoint
        self.add_route_post(self.single__filter)                               # Level 1: Filter endpoint
        self.add_route_post(self.multi__rate   )                               # Level 2: Multi-criteria rate endpoint
        self.add_route_post(self.multi__filter )                               # Level 2: Multi-criteria filter endpoint
