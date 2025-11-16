from unittest                                                                                           import TestCase
from fastapi                                                                                            import FastAPI
from osbot_utils.testing.__                                                                             import __
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                      import Safe_Str__Hash
from mgraph_ai_service_semantic_text.fast_api.routes.Routes__Text_Transformation                        import Routes__Text_Transformation
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Request       import Schema__Text__Transformation__Request
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Response      import Schema__Text__Transformation__Response
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode      import Enum__Text__Transformation__Mode
from mgraph_ai_service_semantic_text.schemas.routes.Schema__Text__Transformation__Request__XXX_Random   import Schema__Text__Transformation__Request__XXX_Random
from mgraph_ai_service_semantic_text.schemas.routes.Schema__Text__Transformation__Request__Hashes_Random import Schema__Text__Transformation__Request__Hashes_Random
from mgraph_ai_service_semantic_text.schemas.routes.Schema__Text__Transformation__Request__ABCDE_By_Size import Schema__Text__Transformation__Request__ABCDE_By_Size
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Transformation__Service          import Text__Transformation__Service


class test_Routes__Text_Transformation(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app    = FastAPI()
        cls.routes = Routes__Text_Transformation(app=cls.app).setup()

    def test__init__(self):                                                     # Test route initialization
        with self.routes as _:
            assert type(_)         is Routes__Text_Transformation
            assert _.tag           == 'text-transformation'
            assert type(_.service) is Text__Transformation__Service
            assert _.app           == self.app

    def test__routes_registered(self):                                          # Test all routes are registered
        with self.routes as _:
            routes = _.routes_paths()
            assert routes   == [ '/transform'              ,
                                 '/transform/abcde-by-size',
                                 '/transform/hashes-random',
                                 '/transform/xxx-random'   ]

    # ========================================
    # Generic transform() Tests
    # ========================================

    def test__transform__xxx_random(self):                                      # Test generic transform with XXX_RANDOM mode
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World",
                        Safe_Str__Hash("def1234567"): "Test Text"}

        request = Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                  ,
                                                        transformation_mode = Enum__Text__Transformation__Mode.XXX_RANDOM   ,
                                                        randomness_percentage = 0.5                                         )

        response = self.routes.transform(request)

        assert type(response) is Schema__Text__Transformation__Response
        assert response.success is True
        assert response.transformation_mode == Enum__Text__Transformation__Mode.XXX_RANDOM
        assert response.total_hashes == 2

    def test__transform__hashes_random(self):                                   # Test generic transform with HASHES_RANDOM mode
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"}

        request = Schema__Text__Transformation__Request(
            hash_mapping        = hash_mapping                                      ,
            transformation_mode = Enum__Text__Transformation__Mode.HASHES_RANDOM    ,
            randomness_percentage = 0.5
        )

        response = self.routes.transform(request)

        assert response.success is True
        assert response.transformation_mode == Enum__Text__Transformation__Mode.HASHES_RANDOM
        assert response.obj() == __(error_message       = None,
                                    transformed_mapping = __(abc1234567='abc1234567'),
                                    transformation_mode = 'hashes-random',
                                    success             = True,
                                    total_hashes        = 1,
                                    transformed_hashes  = 1)

    def test__transform__abcde_by_size(self):                                   # Test generic transform with ABCDE_BY_SIZE mode
        hash_mapping = {Safe_Str__Hash("aaa1234567"): "Hello World",
                        Safe_Str__Hash("bbb1234567"): "Short",
                        Safe_Str__Hash("ccc1234567"): "Medium text"}

        request = Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                      ,
                                                        transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE   ,
                                                        randomness_percentage = 1.0)

        response = self.routes.transform(request)

        assert response.success is True
        assert response.transformation_mode == Enum__Text__Transformation__Mode.ABCDE_BY_SIZE
        assert response.total_hashes == 3

    def test__transform__empty_mapping(self):                                   # Test with empty hash mapping
        request = Schema__Text__Transformation__Request(
            hash_mapping        = {}                                            ,
            transformation_mode = Enum__Text__Transformation__Mode.XXX_RANDOM   ,
            randomness_percentage = 0.5
        )

        response = self.routes.transform(request)

        assert response.success is True
        assert response.total_hashes == 0
        assert response.transformed_hashes == 0

    # ========================================
    # Mode-Specific Convenience Endpoints
    # ========================================

    def test__transform__xxx_random__convenience(self):                         # Test XXX-Random convenience endpoint
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"}

        request = Schema__Text__Transformation__Request__XXX_Random(
            hash_mapping          = hash_mapping,
            randomness_percentage = 0.5
        )

        response = self.routes.transform__xxx_random(request)

        assert type(response) is Schema__Text__Transformation__Response
        assert response.success is True
        assert response.transformation_mode == Enum__Text__Transformation__Mode.XXX_RANDOM

    def test__transform__hashes_random__convenience(self):                      # Test Hashes-Random convenience endpoint
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"}

        request = Schema__Text__Transformation__Request__Hashes_Random(
            hash_mapping          = hash_mapping,
            randomness_percentage = 0.5
        )

        response = self.routes.transform__hashes_random(request)

        assert response.success is True
        assert response.transformation_mode == Enum__Text__Transformation__Mode.HASHES_RANDOM

    def test__transform__abcde_by_size__convenience(self):                      # Test ABCDE-By-Size convenience endpoint
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World",
                        Safe_Str__Hash("def1234567"): "Short"}

        request = Schema__Text__Transformation__Request__ABCDE_By_Size(
            hash_mapping          = hash_mapping,
            randomness_percentage = 1.0,
            num_groups            = 5
        )

        response = self.routes.transform__abcde_by_size(request)

        assert response.success is True
        assert response.transformation_mode == Enum__Text__Transformation__Mode.ABCDE_BY_SIZE

    # ========================================
    # Randomness Percentage Tests
    # ========================================

    def test__bug__transform__randomness_0_percent(self):                            # Test with 0% randomness (no transformation)
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"}

        request = Schema__Text__Transformation__Request(hash_mapping          = hash_mapping                                ,
                                                        transformation_mode   = Enum__Text__Transformation__Mode.XXX_RANDOM ,
                                                        randomness_percentage = 0.0 )

        response = self.routes.transform(request)
        assert response.obj() == __(error_message=None,
                                    transformed_mapping=__(abc1234567='xxxxx xxxxx'),
                                    transformation_mode='xxx-random',
                                    success=True,
                                    total_hashes=1,
                                    transformed_hashes=1)
        assert response.success is True
        assert response.transformed_hashes != 0                     # BUG              # Nothing transformed
        assert response.transformed_hashes == 1                     # BUG


    def test__transform__randomness_100_percent(self):                          # Test with 100% randomness (all transformed)
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World",
                        Safe_Str__Hash("def1234567"): "Test"}

        request = Schema__Text__Transformation__Request(
            hash_mapping          = hash_mapping                                ,
            transformation_mode   = Enum__Text__Transformation__Mode.XXX_RANDOM ,
            randomness_percentage = 1.0
        )

        response = self.routes.transform(request)

        assert response.success is True
        assert response.transformed_hashes == 2                                 # All transformed

    # ========================================
    # Transformation Verification Tests
    # ========================================

    def test__transform__xxx_random__verification(self):                        # Test XXX-Random actually transforms text
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"}

        request = Schema__Text__Transformation__Request(
            hash_mapping          = hash_mapping                                ,
            transformation_mode   = Enum__Text__Transformation__Mode.XXX_RANDOM ,
            randomness_percentage = 1.0
        )

        response = self.routes.transform(request)

        # Check transformation occurred
        transformed_text = response.transformed_mapping[Safe_Str__Hash("abc1234567")]
        assert transformed_text != "Hello World"                                # Should be different
        assert 'x' in transformed_text                                          # Should contain x's

    def test__transform__hashes_random__verification(self):                     # Test Hashes-Random shows hash values
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"}

        request = Schema__Text__Transformation__Request(
            hash_mapping          = hash_mapping                                    ,
            transformation_mode   = Enum__Text__Transformation__Mode.HASHES_RANDOM  ,
            randomness_percentage = 1.0
        )

        response = self.routes.transform(request)

        # Check transformation occurred
        transformed_text = response.transformed_mapping[Safe_Str__Hash("abc1234567")]
        assert transformed_text == "abc1234567"                                 # Should show hash

    def test__transform__abcde_by_size__verification(self):                     # Test ABCDE-By-Size groups by length
        hash_mapping = {Safe_Str__Hash("aaa1234567"): "Hi",                     # Short
                        Safe_Str__Hash("bbb1234567"): "Hello World"}            # Long

        request = Schema__Text__Transformation__Request(
            hash_mapping          = hash_mapping                                    ,
            transformation_mode   = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE  ,
            randomness_percentage = 1.0
        )

        response = self.routes.transform(request)

        # Check transformation occurred
        transformed_short = response.transformed_mapping[Safe_Str__Hash("aaa1234567")]
        transformed_long  = response.transformed_mapping[Safe_Str__Hash("bbb1234567")]

        assert transformed_short != "Hi"
        assert transformed_long != "Hello World"
        assert 'a' in transformed_short or 'b' in transformed_short             # Should have group letter