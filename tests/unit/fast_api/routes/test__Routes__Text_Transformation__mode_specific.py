from unittest                                                                                               import TestCase
from fastapi                                                                                                import FastAPI
from osbot_utils.type_safe.primitives.core.Safe_Float                                                       import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                          import Safe_Str__Hash
from mgraph_ai_service_semantic_text.fast_api.routes.Routes__Text_Transformation                            import Routes__Text_Transformation, ROUTES_PATHS__TEXT_TRANSFORMATION
from mgraph_ai_service_semantic_text.schemas.routes.Schema__Text__Transformation__Request__ABCDE_By_Size    import Schema__Text__Transformation__Request__ABCDE_By_Size
from mgraph_ai_service_semantic_text.schemas.routes.Schema__Text__Transformation__Request__Hashes_Random    import Schema__Text__Transformation__Request__Hashes_Random
from mgraph_ai_service_semantic_text.schemas.routes.Schema__Text__Transformation__Request__XXX_Random       import Schema__Text__Transformation__Request__XXX_Random
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode          import Enum__Text__Transformation__Mode


class test__Routes__Text_Transformation__mode_specific(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.app                 = FastAPI()
        cls.text_transformation = Routes__Text_Transformation(app=cls.app).setup()

    def test__setUpClass(self):
        with self.text_transformation as _:
            assert type(_)          is Routes__Text_Transformation
            assert _.routes_paths() == [ '/transform'               ,
                                         '/transform/abcde-by-size' ,
                                         '/transform/hashes-random' ,
                                         '/transform/xxx-random'    ]

    # ========================================
    # XXX-Random Endpoint Tests
    # ========================================

    def test__transform__xxx_random__basic(self):                               # Basic xxx-random transformation
        with self.text_transformation as _:

            request = Schema__Text__Transformation__Request__XXX_Random(hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"})
            response = _.transform__xxx_random(request)

            assert response.success             is True
            assert response.transformation_mode == Enum__Text__Transformation__Mode.XXX_RANDOM
            assert response.total_hashes        == 1
            assert Safe_Str__Hash("abc1234567") in response.transformed_mapping

    def test__transform__xxx_random__empty_mapping(self):                       # Edge case: empty input
        with self.text_transformation as _:

            request = Schema__Text__Transformation__Request__XXX_Random(hash_mapping={})

            response = _.transform__xxx_random(request)

            assert response.success             is True
            assert response.total_hashes        == 0
            assert response.transformed_hashes  == 0
            assert response.transformed_mapping == {}

    def test__transform__xxx_random__full_randomness(self):                     # Edge case: 100% transformation
        with self.text_transformation as _:

            request = Schema__Text__Transformation__Request__XXX_Random(hash_mapping={ Safe_Str__Hash("abc4567890"): "Hello",
                                                                                       Safe_Str__Hash("abc4567891"): "World"})

            response = _.transform__xxx_random(request)

            assert response.success is True
            assert response.total_hashes == 2
            assert response.transformed_hashes >= 1                             # At least 1 should be transformed

    def test__transform__xxx_random__preserves_structure(self):                 # Verify structure preservation
        with self.text_transformation as _:
            request          = Schema__Text__Transformation__Request__XXX_Random(hash_mapping={Safe_Str__Hash("abc4567890"): "Hello, World!"})
            response         = _.transform__xxx_random(request)
            transformed_text = response.transformed_mapping[Safe_Str__Hash("abc4567890")]
            assert response.success is True
            assert transformed_text == 'xxxxx, xxxxx!'
            assert ", "             in transformed_text                                     # Punctuation and space preserved
            assert "!"              in transformed_text                                      # Exclamation preserved

    # ========================================
    # Hashes-Random Endpoint Tests
    # ========================================

    def test__transform__hashes_random__basic(self):                            # Basic hashes-random transformation
        with self.text_transformation as _:

            request = Schema__Text__Transformation__Request__Hashes_Random(hash_mapping={Safe_Str__Hash("abc1234567"): "Test content"})

            response = _.transform__hashes_random(request)

            assert response.success is True
            assert response.transformation_mode == Enum__Text__Transformation__Mode.HASHES_RANDOM
            assert response.total_hashes == 1

    def test__transform__hashes_random__empty_mapping(self):                    # Edge case: empty input
        with self.text_transformation as _:

            request = Schema__Text__Transformation__Request__Hashes_Random(hash_mapping={})

            response = _.transform__hashes_random(request)

            assert response.success is True
            assert response.total_hashes == 0
            assert response.transformed_hashes == 0

    def test__transform__hashes_random__shows_hashes(self):                     # Verify hashes are shown
        with self.text_transformation as _:

            hash_key = Safe_Str__Hash("abc4567890")
            request = Schema__Text__Transformation__Request__Hashes_Random(hash_mapping={hash_key: "Some text"})

            response = _.transform__hashes_random(request)

            assert response.success is True
            # Either original text or hash string
            result = response.transformed_mapping[hash_key]
            assert result == "Some text" or result == str(hash_key)

    def test__transform__hashes_random__multiple_hashes(self):                  # Multiple hash entries
        with self.text_transformation as _:

            request = Schema__Text__Transformation__Request__Hashes_Random(
                hash_mapping={Safe_Str__Hash("abc4567890"): "First",
                              Safe_Str__Hash("abc4567891"): "Second",
                              Safe_Str__Hash("abc4567892"): "Third"})

            response = _.transform__hashes_random(request)

            assert response.success is True
            assert response.total_hashes == 3
            assert response.transformed_hashes >= 1

    # ========================================
    # ABCDE-By-Size Endpoint Tests
    # ========================================

    def test__transform__abcde_by_size__basic(self):                            # Basic abcde-by-size transformation
        with self.text_transformation as _:

            request = Schema__Text__Transformation__Request__ABCDE_By_Size(
                hash_mapping={Safe_Str__Hash("abc4567890"): "Test"})

            response = _.transform__abcde_by_size(request)

            assert response.success is True
            assert response.transformation_mode == Enum__Text__Transformation__Mode.ABCDE_BY_SIZE
            assert response.total_hashes == 1

    def test__transform__abcde_by_size__empty_mapping(self):                    # Edge case: empty input
        with self.text_transformation as _:

            request = Schema__Text__Transformation__Request__ABCDE_By_Size(hash_mapping={})

            response = _.transform__abcde_by_size(request)

            assert response.success is True
            assert response.total_hashes == 0
            assert response.transformed_hashes == 0

    def test__transform__abcde_by_size__uses_letters(self):                     # Verify letter replacement
        with self.text_transformation as _:

            request = Schema__Text__Transformation__Request__ABCDE_By_Size(
                hash_mapping={
                    Safe_Str__Hash("abc4567890"): "Short",
                    Safe_Str__Hash("abc4567891"): "Medium text here",
                    Safe_Str__Hash("abc4567892"): "A"
                })

            response = _.transform__abcde_by_size(request)

            assert response.success is True
            assert response.total_hashes == 3
            # Verify transformed texts contain only letters from a-e
            for text in response.transformed_mapping.values():
                alphas = [c for c in text if c.isalpha()]
                if alphas:
                    assert all(c in 'abcde' for c in alphas)

    def test__transform__abcde_by_size__num_groups_parameter(self):             # Test num_groups parameter (currently uses default)
        with self.text_transformation as _:

            request = Schema__Text__Transformation__Request__ABCDE_By_Size(
                hash_mapping={Safe_Str__Hash("abc4567890"): "Text"},
                num_groups=Safe_UInt(7)                                         # Note: currently ignored, uses default 5
            )

            response = _.transform__abcde_by_size(request)

            assert response.success is True
            # Future enhancement: verify 7 groups are actually used

    def test__transform__abcde_by_size__preserves_structure(self):              # Verify structure preservation
        with self.text_transformation as _:

            request = Schema__Text__Transformation__Request__ABCDE_By_Size(hash_mapping={Safe_Str__Hash("abc4567890"): "Hello, World!"})

            response = _.transform__abcde_by_size(request)

            assert response.success is True
            transformed = response.transformed_mapping[Safe_Str__Hash("abc4567890")]
            assert transformed == 'aaaaa, aaaaa!'
            assert ", " in transformed                                          # Punctuation and space preserved
            assert "!" in transformed                                           # Exclamation preserved

    # ========================================
    # Cross-Endpoint Consistency Tests
    # ========================================

    def test__all_endpoints__return_same_response_structure(self):              # Verify consistent response structure
        with self.text_transformation as _:

            hash_mapping = {Safe_Str__Hash("abc4567890"): "Sample text"}

            # Test each endpoint
            request_xxx = Schema__Text__Transformation__Request__XXX_Random(
                hash_mapping=hash_mapping
            )
            response_xxx = _.transform__xxx_random(request_xxx)

            request_hashes = Schema__Text__Transformation__Request__Hashes_Random(
                hash_mapping=hash_mapping
            )
            response_hashes = _.transform__hashes_random(request_hashes)

            request_abcde = Schema__Text__Transformation__Request__ABCDE_By_Size(
                hash_mapping=hash_mapping
            )
            response_abcde = _.transform__abcde_by_size(request_abcde)

            # All should have same response structure
            assert hasattr(response_xxx, 'success')
            assert hasattr(response_xxx, 'transformation_mode')
            assert hasattr(response_xxx, 'total_hashes')
            assert hasattr(response_xxx, 'transformed_hashes')
            assert hasattr(response_xxx, 'transformed_mapping')

            assert hasattr(response_hashes, 'success')
            assert hasattr(response_abcde, 'success')

    def test__all_endpoints__handle_empty_input(self):                          # All endpoints handle empty input correctly
        with self.text_transformation as _:

            empty_mapping = {}

            request_xxx = Schema__Text__Transformation__Request__XXX_Random(hash_mapping=empty_mapping)
            response_xxx = _.transform__xxx_random(request_xxx)
            assert response_xxx.success is True

            request_hashes = Schema__Text__Transformation__Request__Hashes_Random(hash_mapping=empty_mapping)
            response_hashes = _.transform__hashes_random(request_hashes)
            assert response_hashes.success is True

            request_abcde = Schema__Text__Transformation__Request__ABCDE_By_Size(hash_mapping=empty_mapping)
            response_abcde = _.transform__abcde_by_size(request_abcde)
            assert response_abcde.success is True