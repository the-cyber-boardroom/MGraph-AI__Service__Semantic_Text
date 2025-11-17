import pytest
from enum                                                                                                 import Enum
from unittest                                                                                             import TestCase
from osbot_utils.testing.__                                                                               import __
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                            import type_safe
from osbot_utils.utils.Objects                                                                            import base_classes
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Transformation__Service            import Text__Transformation__Service
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Grouping__Service                  import Text__Grouping__Service
from mgraph_ai_service_semantic_text.service.semantic_text.classification.Classification__Filter__Service import Classification__Filter__Service
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Request         import Schema__Text__Transformation__Request
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Response        import Schema__Text__Transformation__Response
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode        import Enum__Text__Transformation__Mode
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Engine_Mode import Enum__Text__Transformation__Engine_Mode
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Criterion_Filter      import Schema__Classification__Criterion_Filter
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Logic_Operator    import Enum__Classification__Logic_Operator
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode       import Enum__Classification__Filter_Mode
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria                   import Enum__Text__Classification__Criteria


class test_Text__Transformation__Service(TestCase):

    def test__init__(self):                                                         # Test auto-initialization of Text__Transformation__Service
        with Text__Transformation__Service() as _:
            assert type(_)                           is Text__Transformation__Service
            assert base_classes(_)                   == [Type_Safe, object]
            assert type(_.text_grouping)             is Text__Grouping__Service
            assert type(_.classification_service)    is Classification__Filter__Service  # NEW: Classification service instead of selection

    def test_setup(self):                                                           # Test setup initializes engines with shared services
        with Text__Transformation__Service() as _:
            _.setup()

            assert _.engine__abcde_by_size.text_grouping    is _.text_grouping

    # ========================================
    # Basic Transformation Tests (No Filtering)
    # ========================================

    def test_transform__xxx_random__no_filters(self):                               # Test xxx transformation without filters (transforms all)
        hash_mapping = { Safe_Str__Hash("abc1234567") : "Hello" ,
                         Safe_Str__Hash("def1234567") : "World" }

        request = Schema__Text__Transformation__Request(hash_mapping          = hash_mapping,
                                                        transformation_mode   = Enum__Text__Transformation__Mode.XXX)

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(request)

            assert type(response)                     is Schema__Text__Transformation__Response
            assert response.success                   is True
            assert response.transformation_mode       == Enum__Text__Transformation__Mode.XXX
            assert response.total_hashes              == 2
            assert response.transformed_hashes        == 2                          # All transformed (no filters)

    def test_transform__hashes__no_filters(self):                            # Test hashes transformation without filters
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,
        }

        request = Schema__Text__Transformation__Request(
            hash_mapping          = hash_mapping                                  ,
            transformation_mode   = Enum__Text__Transformation__Mode.HASHES)

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(request)

            assert response.success                   is True
            assert response.transformation_mode       == Enum__Text__Transformation__Mode.HASHES
            assert response.transformed_hashes        == 2                          # All transformed

    def test_transform__abcde_by_size__no_filters(self):                            # Test abcde-by-size transformation (always transforms all)
        hash_mapping = {
            Safe_Str__Hash("a123456789") : "A"                                       ,
            Safe_Str__Hash("b123456789") : "BB"                                      ,
            Safe_Str__Hash("c123456789") : "CCC"                                     ,
            Safe_Str__Hash("d123456789") : "DDDD"                                    ,
            Safe_Str__Hash("e123456789") : "EEEEE"                                   ,
        }

        request = Schema__Text__Transformation__Request(
            hash_mapping          = hash_mapping                                   ,
            transformation_mode   = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE )

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(request)

            assert response.success                   is True
            assert response.transformation_mode       == Enum__Text__Transformation__Mode.ABCDE_BY_SIZE
            assert response.total_hashes              == 5
            assert response.transformed_hashes        == 5                          # All grouped and transformed

    # ========================================
    # Filtering Tests (NEW - With engine_mode and criterion_filters)
    # ========================================

    def test_transform__with_text_hash_engine__filters_by_negative(self):           # Test filtering with TEXT_HASH engine
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Negative text"                           ,
            Safe_Str__Hash("def1234567") : "Positive text"                           ,
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion    = Enum__Text__Classification__Criteria.NEGATIVE        ,
                filter_mode  = Enum__Classification__Filter_Mode.ABOVE              ,
                threshold    = 0.5                                                   ,
            )
        ]

        request = Schema__Text__Transformation__Request(
            hash_mapping          = hash_mapping                                    ,
            engine_mode           = Enum__Text__Transformation__Engine_Mode.TEXT_HASH,
            criterion_filters     = criterion_filters                               ,
            transformation_mode   = Enum__Text__Transformation__Mode.XXX     )

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(request)

            assert response.success                   is True
            assert response.total_hashes              == 2
            assert response.transformed_hashes        <= 2                          # Some or all filtered

    def test_transform__with_random_engine__filters_randomly(self):                 # Test filtering with RANDOM engine
        hash_mapping = {
            Safe_Str__Hash("aaa1234567") : "Text one"                                ,
            Safe_Str__Hash("bbb1234567") : "Text two"                                ,
            Safe_Str__Hash("ccc1234567") : "Text three"                              ,
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion    = Enum__Text__Classification__Criteria.POSITIVE        ,
                filter_mode  = Enum__Classification__Filter_Mode.ABOVE              ,
                threshold    = 0.7                                                   ,
            )
        ]

        request = Schema__Text__Transformation__Request(
            hash_mapping          = hash_mapping                                    ,
            engine_mode           = Enum__Text__Transformation__Engine_Mode.RANDOM  ,
            criterion_filters     = criterion_filters                               ,
            transformation_mode   = Enum__Text__Transformation__Mode.XXX     )

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(request)

            assert response.success                   is True
            assert response.total_hashes              == 3
            assert response.transformed_hashes        >= 0                          # Random results

    def test_transform__with_and_logic__multiple_filters(self):                     # Test AND logic with multiple filters
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Test text"                               ,
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion    = Enum__Text__Classification__Criteria.NEGATIVE        ,
                filter_mode  = Enum__Classification__Filter_Mode.ABOVE              ,
                threshold    = 0.3                                                   ,
            ),
            Schema__Classification__Criterion_Filter(
                criterion    = Enum__Text__Classification__Criteria.POSITIVE        ,
                filter_mode  = Enum__Classification__Filter_Mode.BELOW              ,
                threshold    = 0.5                                                   ,
            ),
        ]

        request = Schema__Text__Transformation__Request(
            hash_mapping          = hash_mapping                                    ,
            engine_mode           = Enum__Text__Transformation__Engine_Mode.TEXT_HASH,
            criterion_filters     = criterion_filters                               ,
            logic_operator        = Enum__Classification__Logic_Operator.AND        ,
            transformation_mode   = Enum__Text__Transformation__Mode.XXX     )

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(request)

            assert response.success                   is True

    def test_transform__with_or_logic__multiple_filters(self):                      # Test OR logic with multiple filters
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Test text"                               ,
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion    = Enum__Text__Classification__Criteria.NEGATIVE        ,
                filter_mode  = Enum__Classification__Filter_Mode.ABOVE              ,
                threshold    = 0.8                                                   ,
            ),
            Schema__Classification__Criterion_Filter(
                criterion    = Enum__Text__Classification__Criteria.POSITIVE        ,
                filter_mode  = Enum__Classification__Filter_Mode.ABOVE              ,
                threshold    = 0.8                                                   ,
            ),
        ]

        request = Schema__Text__Transformation__Request(
            hash_mapping          = hash_mapping                                    ,
            engine_mode           = Enum__Text__Transformation__Engine_Mode.TEXT_HASH,
            criterion_filters     = criterion_filters                               ,
            logic_operator        = Enum__Classification__Logic_Operator.OR         ,
            transformation_mode   = Enum__Text__Transformation__Mode.XXX     )

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(request)

            assert response.success                   is True

    def test_transform__abcde_ignores_filters(self):                                # CRITICAL: ABCDE mode ignores filters, always transforms all
        hash_mapping = {
            Safe_Str__Hash("a123456789") : "A"                                       ,
            Safe_Str__Hash("b123456789") : "BB"                                      ,
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion    = Enum__Text__Classification__Criteria.NEGATIVE        ,
                filter_mode  = Enum__Classification__Filter_Mode.ABOVE              ,
                threshold    = 0.9                                                   ,
            )
        ]

        request = Schema__Text__Transformation__Request(
            hash_mapping          = hash_mapping                                    ,
            engine_mode           = Enum__Text__Transformation__Engine_Mode.TEXT_HASH,  # Engine mode provided
            criterion_filters     = criterion_filters                               ,   # Filters provided
            transformation_mode   = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE  )   # But ABCDE mode

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(request)

            # CRITICAL: ABCDE ignores filters - ALL hashes transformed
            assert response.success                   is True
            assert response.total_hashes              == 2
            assert response.transformed_hashes        == 2                          # ALL transformed despite filters

    # ========================================
    # Edge Cases
    # ========================================

    def test_transform__empty_mapping(self):                                        # Test with empty hash mapping
        request = Schema__Text__Transformation__Request(
            hash_mapping          = {}                                                                  ,
            transformation_mode   = Enum__Text__Transformation__Mode.XXX                         )

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(request)

            assert response.success                   is True
            assert response.total_hashes              == 0
            assert response.transformed_hashes        == 0
            assert response.transformed_mapping       == {}

    def test_transform__none_mapping(self):                                         # Test with None hash mapping
        invalid_request = Schema__Text__Transformation__Request(
            hash_mapping          = None                                                                ,
            transformation_mode   = Enum__Text__Transformation__Mode.XXX                         )

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(invalid_request)

            assert response.obj() == __(error_message       = None        ,
                                        transformed_mapping = __()        ,
                                        transformation_mode = 'xxx',
                                        success             = True        ,
                                        total_hashes        = 0           ,
                                        transformed_hashes  = 0           )

    def test_transform__empty_criterion_filters__transforms_all(self):              # Test empty criterion_filters list transforms all
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                   ,
        }

        request = Schema__Text__Transformation__Request(
            hash_mapping          = hash_mapping                                    ,
            engine_mode           = Enum__Text__Transformation__Engine_Mode.TEXT_HASH,
            criterion_filters     = []                                               ,  # Empty list
            transformation_mode   = Enum__Text__Transformation__Mode.XXX     )

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(request)

            assert response.success                   is True
            assert response.transformed_hashes        == 1                          # All transformed (empty filters = no filtering)

    # ========================================
    # Helper Method Tests
    # ========================================

    def test__get_engine__all_modes(self):                                           # Test getting engines for all transformation modes
        with Text__Transformation__Service() as _:
            _.setup()

            engine_xxx    = _._get_engine(Enum__Text__Transformation__Mode.XXX)
            engine_hashes = _._get_engine(Enum__Text__Transformation__Mode.HASHES)
            engine_abcde  = _._get_engine(Enum__Text__Transformation__Mode.ABCDE_BY_SIZE)

            assert engine_xxx    != engine_hashes
            assert engine_xxx    != engine_abcde
            assert engine_xxx    is _.engine__xxx_random
            assert engine_hashes is _.engine__hashes_random
            assert engine_abcde  is _.engine__abcde_by_size

    def test__regression__type_safe_method__enum_conversion(self):                  # Test enum conversion in type_safe methods
        class Enum__XYZ(str, Enum):
            ABC = 'abc'
            XYZ = 'xyz'

        @type_safe
        def an_method(an_enum: Enum__XYZ):
            return an_enum

        assert an_method(Enum__XYZ.ABC) == Enum__XYZ.ABC
        assert an_method(Enum__XYZ.XYZ) == Enum__XYZ.XYZ
        assert an_method('abc'        ) == Enum__XYZ.ABC
        assert an_method('xyz'        ) == Enum__XYZ.XYZ

    def test_get_engine__invalid_mode(self):                                        # Test error with invalid transformation mode
        with Text__Transformation__Service() as _:
            _.setup()

            error_message = "Parameter 'mode' expected type <enum 'Enum__Text__Transformation__Mode'>, but got <class 'str'>"
            with pytest.raises(ValueError, match=error_message) as e:
                _._get_engine("invalid-mode")

    def test_count_transformed_hashes__all_transformed(self):                       # Test counting when all hashes are transformed
        original_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,
        }

        transformed_mapping = {
            Safe_Str__Hash("abc1234567") : "xxxxx"                                  ,
            Safe_Str__Hash("def1234567") : "xxxxx"                                  ,
        }

        with Text__Transformation__Service() as _:
            count = _._count_transformed_hashes(original_mapping, transformed_mapping)
            assert count == 2

    def test_count_transformed_hashes__partial_transformed(self):                   # Test counting when some hashes are transformed
        original_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,
        }

        transformed_mapping = {
            Safe_Str__Hash("abc1234567") : "xxxxx"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,   # Not transformed
        }

        with Text__Transformation__Service() as _:
            count = _._count_transformed_hashes(original_mapping, transformed_mapping)
            assert count == 1

    def test_count_transformed_hashes__none_transformed(self):                      # Test counting when no hashes are transformed
        original_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,
        }

        transformed_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,
        }

        with Text__Transformation__Service() as _:
            count = _._count_transformed_hashes(original_mapping, transformed_mapping)
            assert count == 0
