from unittest                                                                               import TestCase
from fastapi                                                                                import FastAPI
from mgraph_ai_service_semantic_text.fast_api.Semantic_Text__Service__Fast_API              import Semantic_Text__Service__Fast_API
from mgraph_ai_service_semantic_text.config                                                 import FAST_API__TITLE
from mgraph_ai_service_semantic_text.utils.Version                                          import version__mgraph_ai_service_semantic_text


class test_Semantic_Text__Service__Fast_API(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service = Semantic_Text__Service__Fast_API().setup()

    def test__init__(self):                                                     # Test service initialization
        with self.service as _:
            assert type(_) is Semantic_Text__Service__Fast_API
            assert type(_.app()) is FastAPI

    def test__setup(self):                                                      # Test setup method
        service = Semantic_Text__Service__Fast_API()
        result = service.setup()

        assert result is service                                                # Returns self for chaining
        assert service.app() is not None

    def test__fast_api__title(self):                                            # Test FastAPI title configuration
        title = self.service.fast_api__title()

        assert title == FAST_API__TITLE
        assert title == "MGraph AI Service Semantic_Text"

    def test__app_configuration(self):                                          # Test app is configured correctly
        app = self.service.app()

        assert app.title == FAST_API__TITLE
        assert app.version == str(version__mgraph_ai_service_semantic_text)

    def test__setup_fast_api_title_and_version(self):                          # Test title and version setup
        service = Semantic_Text__Service__Fast_API()
        service.setup_fast_api_title_and_version()

        app = service.app()
        assert app.title == FAST_API__TITLE
        assert app.version == str(version__mgraph_ai_service_semantic_text)

    def test__setup_routes(self):                                               # Test routes are registered
        service = Semantic_Text__Service__Fast_API().setup()
        app = service.app()

        # Get all registered routes
        routes = [route.path for route in app.routes]

        # Check that key routes exist
        assert any('/info'                    in route for route in routes)     # Routes__Info
        assert any('/text-transformation'     in route for route in routes)     # Routes__Text_Transformation
        assert any('/semantic-classification' in route for route in routes)     # Routes__Semantic_Classification
        assert any('/topic-classification'    in route for route in routes)     # Routes__Topic_Classification

    def test__enable_api_key(self):                                             # Test API key configuration
        with self.service as _:
            assert _.enable_api_key is False                                    # Currently disabled

    def test__handler(self):                                                    # Test handler method exists
        handler = self.service.handler()

        assert handler is not None
        assert callable(handler)

    def test__routes_registered(self):                                          # Test all expected route classes are registered
        service = Semantic_Text__Service__Fast_API().setup()

        # The service should have registered these route classes
        # We can verify by checking the app's router
        app = service.app()

        # Check routes contain expected paths
        route_paths = [route.path for route in app.routes]

        # Info routes
        assert any('/info' in path for path in route_paths)

        # Text transformation routes
        assert any('transform' in path for path in route_paths)

        # Semantic classification routes
        assert any('semantic-classification' in path for path in route_paths)

        # Topic classification routes
        assert any('topic-classification' in path for path in route_paths)

    def test__openapi_tags(self):                                               # Test OpenAPI tags are set
        app = self.service.app()

        # Get OpenAPI schema
        openapi_schema = app.openapi()

        assert 'info' in openapi_schema
        assert openapi_schema['info']['title'] == FAST_API__TITLE
        assert openapi_schema['info']['version'] == str(version__mgraph_ai_service_semantic_text)

    def test__context_manager(self):                                            # Test service works as context manager
        with Semantic_Text__Service__Fast_API() as service:
            assert type(service) is Semantic_Text__Service__Fast_API
            assert service.app() is not None