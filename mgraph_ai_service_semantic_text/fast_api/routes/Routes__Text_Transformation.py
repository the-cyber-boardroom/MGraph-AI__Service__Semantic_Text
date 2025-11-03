from fastapi                                                                                                 import APIRouter, HTTPException
from osbot_utils.type_safe.Type_Safe                                                                     import Type_Safe
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Transformation__Service           import Text__Transformation__Service
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Request        import Schema__Text__Transformation__Request
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Response       import Schema__Text__Transformation__Response


class Routes__Text_Transformation(Type_Safe):                                       # FastAPI routes for text transformation
    router      : APIRouter                                                         # FastAPI router
    tag         : str                       = 'text-transformation'                 # OpenAPI tag
    service     : Text__Transformation__Service                                     # Transformation service

    def setup(self) -> 'Routes__Text_Transformation':                              # Setup routes and service
        self.router = APIRouter(tags=[self.tag])
        self.service.setup()
        self.setup_routes()
        return self

    def setup_routes(self):                                                         # Register all route handlers
        self.router.add_api_route('/transform'                         ,
                                  self.transform                        ,
                                  methods  = ['POST']                   ,
                                  response_model = Schema__Text__Transformation__Response)

    async def transform(self,                                                       # Transform hash mapping endpoint
                        request: Schema__Text__Transformation__Request              # Transformation request
                       ) -> Schema__Text__Transformation__Response:                 # Transformation response
        try:
            response = self.service.transform(request)

            if not response.success:
                raise HTTPException(status_code=500, detail=response.error_message)

            return response

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Transformation failed: {str(e)}")