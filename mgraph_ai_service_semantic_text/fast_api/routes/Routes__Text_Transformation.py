from fastapi                                                                                               import HTTPException
from osbot_fast_api.api.routes.Fast_API__Routes                                                            import Fast_API__Routes
from osbot_fast_api.api.schemas.safe_str.Safe_Str__Fast_API__Route__Tag                                    import Safe_Str__Fast_API__Route__Tag
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Transformation__Service             import Text__Transformation__Service
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Request          import Schema__Text__Transformation__Request
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Response         import Schema__Text__Transformation__Response
from mgraph_ai_service_semantic_text.schemas.routes.Schema__Text__Transformation__Request__XXX_Random      import Schema__Text__Transformation__Request__XXX_Random
from mgraph_ai_service_semantic_text.schemas.routes.Schema__Text__Transformation__Request__Hashes_Random   import Schema__Text__Transformation__Request__Hashes_Random
from mgraph_ai_service_semantic_text.schemas.routes.Schema__Text__Transformation__Request__ABCDE_By_Size   import Schema__Text__Transformation__Request__ABCDE_By_Size
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode         import Enum__Text__Transformation__Mode

TAG__ROUTES_TEXT_TRANSFORMATION   = 'text-transformation'
ROUTES_PATHS__TEXT_TRANSFORMATION = [f'/{TAG__ROUTES_TEXT_TRANSFORMATION}' + '/transform'                  ,  # Generic endpoint
                                     f'/{TAG__ROUTES_TEXT_TRANSFORMATION}' + '/transform/xxx-random'       ,  # Mode-specific endpoints
                                     f'/{TAG__ROUTES_TEXT_TRANSFORMATION}' + '/transform/hashes-random'    ,
                                     f'/{TAG__ROUTES_TEXT_TRANSFORMATION}' + '/transform/abcde-by-size'    ]

class Routes__Text_Transformation(Fast_API__Routes):                            # FastAPI routes for text transformation
    tag         : Safe_Str__Fast_API__Route__Tag    =  TAG__ROUTES_TEXT_TRANSFORMATION      # OpenAPI tag
    service     : Text__Transformation__Service                                             # Transformation service

    # ========================================
    # Generic Endpoint (Existing)
    # ========================================

    def transform(self,                                                         # Transform hash mapping endpoint
                  request: Schema__Text__Transformation__Request                # Transformation request
             ) -> Schema__Text__Transformation__Response:                       # Transformation response
        try:
            response = self.service.transform(request)

            if not response.success:
                raise HTTPException(status_code=500, detail=response.error_message)

            return response

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Transformation failed: {str(e)}")

    # ========================================
    # Mode-Specific Endpoints (New)
    # ========================================

    def transform__xxx_random(self,                                                             # XXX-Random transformation endpoint (convenience wrapper)
                              request: Schema__Text__Transformation__Request__XXX_Random        # XXX-Random specific request
                         ) -> Schema__Text__Transformation__Response:                           # Transformation response

        full_request = Schema__Text__Transformation__Request(hash_mapping            = request.hash_mapping                          ,
                                                             transformation_mode     = Enum__Text__Transformation__Mode.XXX_RANDOM   )

        return self.transform(full_request)

    def transform__hashes_random(self,                                                          # Hashes-Random transformation endpoint (convenience wrapper)
                                 request: Schema__Text__Transformation__Request__Hashes_Random  # Hashes-Random specific request
                            ) -> Schema__Text__Transformation__Response:                        # Transformation response

        full_request = Schema__Text__Transformation__Request(hash_mapping            = request.hash_mapping                          ,
                                                             transformation_mode     = Enum__Text__Transformation__Mode.HASHES_RANDOM)

        return self.transform(full_request)

    def transform__abcde_by_size(self,                                                          # ABCDE-By-Size transformation endpoint (convenience wrapper)
                                 request: Schema__Text__Transformation__Request__ABCDE_By_Size  # ABCDE-By-Size specific request
                            ) -> Schema__Text__Transformation__Response:                        # Transformation response
        # Note: num_groups parameter is accepted but uses engine default (5) in current implementation
        # Future enhancement will pass this through to the engine via engine_config parameter

        full_request = Schema__Text__Transformation__Request(hash_mapping            = request.hash_mapping                          ,
                                                             transformation_mode     = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE)

        return self.transform(full_request)

    def setup_routes(self):                                                     # Register all route handlers
        self.add_route_post(self.transform             )                       # Generic endpoint
        self.add_route_post(self.transform__xxx_random )                       # Mode-specific convenience endpoints
        self.add_route_post(self.transform__hashes_random)
        self.add_route_post(self.transform__abcde_by_size)