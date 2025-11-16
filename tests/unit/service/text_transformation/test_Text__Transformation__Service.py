import pytest
from enum                                                                                                 import Enum
from unittest                                                                                             import TestCase
from osbot_utils.testing.__ import __, __SKIP__
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                            import type_safe
from osbot_utils.utils.Objects                                                                            import base_classes
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Transformation__Service            import Text__Transformation__Service
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Grouping__Service                  import Text__Grouping__Service
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Selection__Service                 import Text__Selection__Service
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Request         import Schema__Text__Transformation__Request
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Response        import Schema__Text__Transformation__Response
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode        import Enum__Text__Transformation__Mode


class test_Text__Transformation__Service(TestCase):

    def test__init__(self):                                                         # Test auto-initialization of Text__Transformation__Service
        with Text__Transformation__Service() as _:
            assert type(_)                           is Text__Transformation__Service
            assert base_classes(_)                   == [Type_Safe, object]
            assert type(_.text_grouping)             is Text__Grouping__Service
            assert type(_.text_selection)            is Text__Selection__Service

    def test_setup(self):                                                           # Test setup initializes engines with shared services
        with Text__Transformation__Service() as _:
            _.setup()

            assert _.engine__xxx_random.text_selection      is _.text_selection
            assert _.engine__hashes_random.text_selection   is _.text_selection
            assert _.engine__abcde_by_size.text_grouping    is _.text_grouping

    def test_transform__xxx_random__in_osbot_utils_type_safe_method(self):                                           # Test xxx-random transformation
        hash_mapping = { Safe_Str__Hash("abc1234567") : "Hello" ,
                         Safe_Str__Hash("def1234567") : "World" }

        request = Schema__Text__Transformation__Request(hash_mapping          = hash_mapping                                ,
                                                        transformation_mode   = Enum__Text__Transformation__Mode.XXX_RANDOM )

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(request)

            assert response.obj()                     == __(error_message       = None                  ,
                                                            transformed_mapping = __SKIP__,
                                                            transformation_mode = 'xxx-random'          ,
                                                            success             = True                  ,
                                                            total_hashes        = 2                     ,
                                                            transformed_hashes  = __SKIP__              )
            assert type(response)                     is Schema__Text__Transformation__Response
            assert response.success                   is True
            assert response.transformation_mode       == Enum__Text__Transformation__Mode.XXX_RANDOM
            assert response.total_hashes              == 2
            assert response.transformed_hashes        >= 0

    def test_transform__hashes_random(self):                                        # Test hashes-random transformation
        hash_mapping = {
            Safe_Str__Hash("abc1234567") : "Hello"                                  ,
            Safe_Str__Hash("def1234567") : "World"                                  ,
        }

        request = Schema__Text__Transformation__Request(
            hash_mapping          = hash_mapping                                  ,
            transformation_mode   = Enum__Text__Transformation__Mode.HASHES_RANDOM)

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(request)

            assert response.success                   is True
            assert response.transformation_mode       == Enum__Text__Transformation__Mode.HASHES_RANDOM
            assert response.transformed_hashes        >= 0
            #assert "abc1234567" in [str(v) for v in response.transformed_mapping.values()]

    def test_transform__abcde_by_size(self):                                        # Test abcde-by-size transformation
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

    def test_transform__empty_mapping(self):                                        # Test with empty hash mapping
        request = Schema__Text__Transformation__Request(
            hash_mapping          = {}                                                                  ,
            transformation_mode   = Enum__Text__Transformation__Mode.XXX_RANDOM                         )

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(request)

            assert response.success                   is True
            assert response.total_hashes              == 0
            assert response.transformed_hashes        == 0
            assert response.transformed_mapping       == {}

    def test_transform__null_mapping(self):                                       # Test error handling during transformation
        invalid_request = Schema__Text__Transformation__Request(
            hash_mapping          = None                                                                ,
            transformation_mode   = Enum__Text__Transformation__Mode.XXX_RANDOM                         )

        with Text__Transformation__Service() as _:
            _.setup()
            response = _.transform(invalid_request)

            assert response.obj() == __(error_message       = None        ,
                                        transformed_mapping = __()        ,
                                        transformation_mode = 'xxx-random',
                                        success             = True        ,     # todo: see if this is the correct return value for an null or empty hash_mapping
                                        total_hashes        = 0           ,
                                        transformed_hashes  = 0           )

    def test_get_engine__all_modes(self):                                           # Test getting engines for all transformation modes
        with Text__Transformation__Service() as _:
            _.setup()

            engine_xxx    = _._get_engine(Enum__Text__Transformation__Mode.XXX_RANDOM)
            engine_hashes = _._get_engine(Enum__Text__Transformation__Mode.HASHES_RANDOM)
            engine_abcde  = _._get_engine(Enum__Text__Transformation__Mode.ABCDE_BY_SIZE)

            assert engine_xxx    is _.engine__xxx_random
            assert engine_hashes is _.engine__hashes_random
            assert engine_abcde  is _.engine__abcde_by_size

    def test__regression__type_safe_method__enum_conversion(self):
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
