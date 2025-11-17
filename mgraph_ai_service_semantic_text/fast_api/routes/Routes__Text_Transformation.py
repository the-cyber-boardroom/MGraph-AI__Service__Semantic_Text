from fastapi                                                                                               import HTTPException
from osbot_fast_api.api.routes.Fast_API__Routes                                                            import Fast_API__Routes
from osbot_fast_api.api.schemas.safe_str.Safe_Str__Fast_API__Route__Tag                                    import Safe_Str__Fast_API__Route__Tag
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Transformation__Service             import Text__Transformation__Service
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Request          import Schema__Text__Transformation__Request
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Response         import Schema__Text__Transformation__Response

TAG__ROUTES_TEXT_TRANSFORMATION   = 'text-transformation'
ROUTES_PATHS__TEXT_TRANSFORMATION = [f'/{TAG__ROUTES_TEXT_TRANSFORMATION}' + '/transform']                 # Unified endpoint

class Routes__Text_Transformation(Fast_API__Routes):                            # FastAPI routes for text transformation
    tag         : Safe_Str__Fast_API__Route__Tag    =  TAG__ROUTES_TEXT_TRANSFORMATION      # OpenAPI tag
    service     : Text__Transformation__Service                                             # Transformation service

    def transform(self,                                                         # Transform hash mapping endpoint (unified with filtering support)
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

    def setup_routes(self):                                                     # Register all route handlers
        self.add_route_post(self.transform)                                     # Unified transformation endpoint
