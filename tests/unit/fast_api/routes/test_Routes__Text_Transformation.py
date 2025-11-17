from unittest                                                                                            import TestCase
from fastapi                                                                                             import FastAPI
from osbot_utils.testing.__                                                                              import __
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                       import Safe_Str__Hash
from mgraph_ai_service_semantic_text.fast_api.routes.Routes__Text_Transformation                         import Routes__Text_Transformation
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Request        import Schema__Text__Transformation__Request
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Response       import Schema__Text__Transformation__Response
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode       import Enum__Text__Transformation__Mode
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Engine_Mode import Enum__Text__Transformation__Engine_Mode
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Criterion_Filter      import Schema__Classification__Criterion_Filter
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Logic_Operator    import Enum__Classification__Logic_Operator
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode       import Enum__Classification__Filter_Mode
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria                   import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Transformation__Service           import Text__Transformation__Service


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

    def test__routes_registered(self):                                          # Test unified route is registered
        with self.routes as _:
            routes = _.routes_paths()
            assert routes   == [ '/transform' ]                                 # Only unified endpoint

    # ========================================
    # Unified transform() Tests - No Filtering
    # ========================================

    def test__transform__xxx_random__no_filters(self):                          # Test unified transform with XXX_RANDOM mode (no filters)
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World",
                        Safe_Str__Hash("def1234567"): "Test Text"}

        request = Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                  ,
                                                        transformation_mode = Enum__Text__Transformation__Mode.XXX_RANDOM   )

        response = self.routes.transform(request)

        assert type(response) is Schema__Text__Transformation__Response
        assert response.success is True
        assert response.transformation_mode == Enum__Text__Transformation__Mode.XXX_RANDOM
        assert response.total_hashes == 2
        assert response.transformed_hashes == 2                                 # All transformed (no filters)

    def test__transform__hashes_random__no_filters(self):                       # Test unified transform with HASHES_RANDOM mode (no filters)
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"}

        request = Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                      ,
                                                        transformation_mode = Enum__Text__Transformation__Mode.HASHES_RANDOM    )

        response = self.routes.transform(request)

        assert response.success is True
        assert response.transformation_mode == Enum__Text__Transformation__Mode.HASHES_RANDOM
        assert response.obj() == __(error_message       = None,
                                    transformed_mapping = __(abc1234567='abc1234567'),
                                    transformation_mode = 'hashes-random',
                                    success             = True,
                                    total_hashes        = 1,
                                    transformed_hashes  = 1)

    def test__transform__abcde_by_size__no_filters(self):                       # Test unified transform with ABCDE_BY_SIZE mode (no filters)
        hash_mapping = {Safe_Str__Hash("aaa1234567"): "Hello World",
                        Safe_Str__Hash("bbb1234567"): "Short",
                        Safe_Str__Hash("ccc1234567"): "Medium text"}

        request = Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                      ,
                                                        transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE   )

        response = self.routes.transform(request)

        assert response.success is True
        assert response.transformation_mode == Enum__Text__Transformation__Mode.ABCDE_BY_SIZE
        assert response.total_hashes == 3
        assert response.transformed_hashes == 3                                 # ABCDE always transforms all

    # ========================================
    # Unified transform() Tests - With Filtering
    # ========================================

    def test__transform__with_text_hash_engine__single_filter(self):            # Test unified transform with TEXT_HASH engine and filtering
        hash_mapping = {
            Safe_Str__Hash("abc1234567"): "Negative text",
            Safe_Str__Hash("def1234567"): "Positive text"
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion    = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode  = Enum__Classification__Filter_Mode.ABOVE,
                threshold    = 0.5
            )
        ]

        request = Schema__Text__Transformation__Request(
            hash_mapping        = hash_mapping,
            engine_mode         = Enum__Text__Transformation__Engine_Mode.TEXT_HASH,
            criterion_filters   = criterion_filters,
            transformation_mode = Enum__Text__Transformation__Mode.XXX_RANDOM
        )

        response = self.routes.transform(request)

        assert response.success is True
        assert response.total_hashes == 2
        assert response.transformed_hashes <= 2                                 # Some or all filtered

    def test__transform__with_random_engine__multiple_filters__and_logic(self):  # Test unified transform with RANDOM engine, multiple filters, AND logic
        hash_mapping = {
            Safe_Str__Hash("aaa1234567"): "Text one",
            Safe_Str__Hash("bbb1234567"): "Text two"
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion    = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode  = Enum__Classification__Filter_Mode.ABOVE,
                threshold    = 0.3
            ),
            Schema__Classification__Criterion_Filter(
                criterion    = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode  = Enum__Classification__Filter_Mode.BELOW,
                threshold    = 0.5
            )
        ]

        request = Schema__Text__Transformation__Request(
            hash_mapping        = hash_mapping,
            engine_mode         = Enum__Text__Transformation__Engine_Mode.RANDOM,
            criterion_filters   = criterion_filters,
            logic_operator      = Enum__Classification__Logic_Operator.AND,
            transformation_mode = Enum__Text__Transformation__Mode.XXX_RANDOM
        )

        response = self.routes.transform(request)

        assert response.success is True
        assert response.total_hashes == 2

    def test__transform__with_text_hash_engine__multiple_filters__or_logic(self):  # Test unified transform with TEXT_HASH engine, multiple filters, OR logic
        hash_mapping = {
            Safe_Str__Hash("abc1234567"): "Test text"
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion    = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode  = Enum__Classification__Filter_Mode.ABOVE,
                threshold    = 0.8
            ),
            Schema__Classification__Criterion_Filter(
                criterion    = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode  = Enum__Classification__Filter_Mode.ABOVE,
                threshold    = 0.8
            )
        ]

        request = Schema__Text__Transformation__Request(
            hash_mapping        = hash_mapping,
            engine_mode         = Enum__Text__Transformation__Engine_Mode.TEXT_HASH,
            criterion_filters   = criterion_filters,
            logic_operator      = Enum__Classification__Logic_Operator.OR,
            transformation_mode = Enum__Text__Transformation__Mode.XXX_RANDOM
        )

        response = self.routes.transform(request)

        assert response.success is True

    def test__transform__abcde_ignores_filters(self):                           # CRITICAL: ABCDE mode ignores filters
        hash_mapping = {
            Safe_Str__Hash("a123456789"): "A",
            Safe_Str__Hash("b123456789"): "BB"
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion    = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode  = Enum__Classification__Filter_Mode.ABOVE,
                threshold    = 0.9
            )
        ]

        request = Schema__Text__Transformation__Request(
            hash_mapping        = hash_mapping,
            engine_mode         = Enum__Text__Transformation__Engine_Mode.TEXT_HASH,
            criterion_filters   = criterion_filters,
            transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE
        )

        response = self.routes.transform(request)

        # ABCDE ignores filters - all transformed
        assert response.success is True
        assert response.total_hashes == 2
        assert response.transformed_hashes == 2                                 # ALL transformed despite filters

    # ========================================
    # Edge Cases
    # ========================================

    def test__transform__empty_mapping(self):                                   # Test with empty hash mapping
        request = Schema__Text__Transformation__Request(hash_mapping        = {}                                            ,
                                                        transformation_mode = Enum__Text__Transformation__Mode.XXX_RANDOM   )

        response = self.routes.transform(request)

        assert response.success is True
        assert response.total_hashes == 0
        assert response.transformed_hashes == 0

    def test__transform__empty_criterion_filters__transforms_all(self):         # Test empty filters transforms all
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello"}

        request = Schema__Text__Transformation__Request(
            hash_mapping        = hash_mapping,
            engine_mode         = Enum__Text__Transformation__Engine_Mode.TEXT_HASH,
            criterion_filters   = [],                                           # Empty list
            transformation_mode = Enum__Text__Transformation__Mode.XXX_RANDOM
        )

        response = self.routes.transform(request)

        assert response.success is True
        assert response.transformed_hashes == 1                                 # All transformed

    # ========================================
    # Transformation Verification Tests
    # ========================================

    def test__transform__xxx_random__verification(self):                        # Test XXX-Random actually transforms text
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"}

        request = Schema__Text__Transformation__Request(hash_mapping          = hash_mapping                                ,
                                                        transformation_mode   = Enum__Text__Transformation__Mode.XXX_RANDOM)

        response = self.routes.transform(request)

        # Check transformation occurred
        transformed_text = response.transformed_mapping[Safe_Str__Hash("abc1234567")]
        assert transformed_text != "Hello World"                                # Should be different
        assert 'x' in transformed_text                                          # Should contain x's

    def test__transform__hashes_random__verification(self):                     # Test Hashes-Random shows hash values
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"}

        request = Schema__Text__Transformation__Request(hash_mapping          = hash_mapping                                    ,
                                                        transformation_mode   = Enum__Text__Transformation__Mode.HASHES_RANDOM  )

        response = self.routes.transform(request)

        # Check transformation occurred
        transformed_text = response.transformed_mapping[Safe_Str__Hash("abc1234567")]
        assert transformed_text == "abc1234567"                                 # Should show hash

    def test__transform__abcde_by_size__verification(self):                     # Test ABCDE-By-Size groups by length
        hash_mapping = {Safe_Str__Hash("aaa1234567"): "Hi",                     # Short
                        Safe_Str__Hash("bbb1234567"): "Hello World"}            # Long

        request = Schema__Text__Transformation__Request(hash_mapping          = hash_mapping                                    ,
                                                        transformation_mode   = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE  )

        response = self.routes.transform(request)

        # Check transformation occurred
        transformed_short = response.transformed_mapping[Safe_Str__Hash("aaa1234567")]
        transformed_long  = response.transformed_mapping[Safe_Str__Hash("bbb1234567")]

        assert transformed_short != "Hi"
        assert transformed_long != "Hello World"
        assert 'a' in transformed_short or 'b' in transformed_short             # Should have group letter
