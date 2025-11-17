from unittest                                                                                                   import TestCase
from fastapi                                                                                                    import FastAPI
from osbot_utils.testing.__                                                                                     import __
from osbot_utils.type_safe.primitives.core.Safe_Float                                                           import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                              import Safe_Str__Hash
from mgraph_ai_service_semantic_text.fast_api.routes.Routes__Text_Transformation                                import Routes__Text_Transformation
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Request               import Schema__Text__Transformation__Request
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Request__Convenience  import Schema__Text__Transformation__Request__Convenience
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Response              import Schema__Text__Transformation__Response
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode              import Enum__Text__Transformation__Mode
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Engine_Mode       import Enum__Text__Transformation__Engine_Mode
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Criterion_Filter            import Schema__Classification__Criterion_Filter
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Logic_Operator          import Enum__Classification__Logic_Operator
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode             import Enum__Classification__Filter_Mode
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria                         import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Transformation__Service                  import Text__Transformation__Service


class test_Routes__Text_Transformation(TestCase):

    @classmethod
    def setUpClass(cls):                                                        # Setup shared test objects (called once)
        cls.app    = FastAPI()
        cls.routes = Routes__Text_Transformation(app=cls.app).setup()

    def test__init__(self):                                                     # Test route initialization and Type_Safe structure
        with self.routes as _:
            assert type(_)         is Routes__Text_Transformation               # Verify type
            assert _.tag           == 'text-transformation'                     # Verify tag
            assert type(_.service) is Text__Transformation__Service             # Verify service injection
            assert _.app           is self.app                                  # Verify app reference

    def test__routes_registered(self):                                          # Test both unified and convenience routes registered
        with self.routes as _:
            routes = _.routes_paths()
            assert routes == [ '/transform',
                               '/{engine_mode}/{transformation_mode}/{criteria}/{filter_mode}/{threshold}']

    # ========================================
    # Unified transform() Tests - No Filtering
    # ========================================

    def test__transform__xxx_random__no_filters(self):                          # Test unified endpoint: XXX_RANDOM mode without filters
        hash_mapping = { Safe_Str__Hash("abc1234567"): "Hello World",
                         Safe_Str__Hash("def1234567"): "Test Text"  }

        with Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                  ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.XXX) as request:

            response = self.routes.transform(request)

            with response as _:
                assert type(_)              is Schema__Text__Transformation__Response
                assert _.success            is True
                assert _.transformation_mode == Enum__Text__Transformation__Mode.XXX
                assert _.total_hashes       == 2
                assert _.transformed_hashes == 2                                # All transformed (no filters)      # todo: review this pattern of transforming all if no filters are provided (shouldn't it be 50% transformation)
                assert _.error_message      is None
                assert _.obj()              == __( error_message=None,
                                                   transformed_mapping=__(abc1234567='xxxxx xxxxx', def1234567='xxxx xxxx'),
                                                   transformation_mode='xxx',
                                                   success=True,
                                                   total_hashes=2,
                                                   transformed_hashes=2)

    def test__transform__hashes_random__no_filters(self):                       # Test unified endpoint: HASHES_RANDOM mode without filters
        hash_mapping = { Safe_Str__Hash("abc1234567"): "Hello World" }

        with Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                      ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.HASHES) as request:

            response = self.routes.transform(request)

            assert response.obj() == __(error_message       = None                                           ,
                                        transformed_mapping = __(abc1234567='abc1234567')                    ,   # Hash replaces text
                                        transformation_mode = 'hashes'                                       ,
                                        success             = True                                           ,
                                        total_hashes        = 1                                              ,
                                        transformed_hashes  = 1                                              )

    def test__transform__abcde_by_size__no_filters(self):                       # Test unified endpoint: ABCDE_BY_SIZE mode without filters
        hash_mapping = { Safe_Str__Hash("aaa1234567"): "Hello World"   ,
                         Safe_Str__Hash("bbb1234567"): "Short"          ,
                         Safe_Str__Hash("ccc1234567"): "Medium text"    }

        with Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                      ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE   ) as request:

            response = self.routes.transform(request)

            with response as _:
                assert _.success             is True
                assert _.transformation_mode == Enum__Text__Transformation__Mode.ABCDE_BY_SIZE
                assert _.total_hashes        == 3
                assert _.transformed_hashes  == 3                               # ABCDE always transforms all

                assert type(_) is Schema__Text__Transformation__Response
                assert _.obj() == __(  error_message=None,
                                       transformed_mapping=__(bbb1234567='aaaaa',
                                                              aaa1234567='bbbbb bbbbb',
                                                              ccc1234567='cccccc cccc'),
                                       transformation_mode='abcde-by-size',
                                       success=True,
                                       total_hashes=3,
                                       transformed_hashes=3)

    # ========================================
    # Unified transform() Tests - With Filtering
    # ========================================

    def test__transform__with_text_hash_engine__single_filter(self):            # Test unified endpoint with TEXT_HASH engine and single filter
        hash_mapping = { Safe_Str__Hash("abc1234567"): "Negative text",         # negative: 0.3630613175290631,
                         Safe_Str__Hash("def1234567"): "Positive text!" }       # negative: 0.16752469006093718,

        criterion_filters = [
            Schema__Classification__Criterion_Filter(criterion    = Enum__Text__Classification__Criteria.NEGATIVE  ,
                                                     filter_mode  = Enum__Classification__Filter_Mode.ABOVE        ,
                                                     threshold    = 0.17                                           ) # since Positive text! is 0.16
        ]
        # todo: review the usage of Enum__Text__Transformation__Mode.XXX_RANDOM here since, shouldn't this be XXX , since it is the engine mode that determines if the data is random or not
        with Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                      ,
                                                   engine_mode         = Enum__Text__Transformation__Engine_Mode.TEXT_HASH ,
                                                   criterion_filters   = criterion_filters                                 ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.XXX) as request:

            response = self.routes.transform(request)

            with response as _:
                assert _.success             is True
                assert _.total_hashes        == 2
                assert _.transformed_hashes  <= 2                               # Some or all filtered
                assert type(_)               is Schema__Text__Transformation__Response
                assert _.obj()               == __(error_message=None,
                                                   transformed_mapping=__(abc1234567='xxxxxxxx xxxx',           # negative text is filtered route
                                                                          def1234567='Positive text!'),
                                                   transformation_mode='xxx',
                                                   success=True,
                                                   total_hashes=2,
                                                   transformed_hashes=1)

    def test__transform__with_random_engine__multiple_filters__and_logic(self):  # Test unified endpoint with RANDOM engine, multiple filters, AND logic
        hash_mapping = { Safe_Str__Hash("aaa1234567"): "Text one",          # "positive": 0.11043511098057315, "negative": 0.30999034951537785,
                         Safe_Str__Hash("bbb1234567"): "Text two" ,         # "positive": 0.40453102961918197, "negative": 0.16978138222849085,
                         Safe_Str__Hash("ccc1234567"): "Text three" }       # "positive": 0.3602774700130064,  "negative": 0.13459222505901056,

        criterion_filters = [
            Schema__Classification__Criterion_Filter(criterion    = Enum__Text__Classification__Criteria.NEGATIVE  ,
                                                    filter_mode  = Enum__Classification__Filter_Mode.ABOVE        ,
                                                    threshold    = 0.13                                           ),        # matches all of them
            Schema__Classification__Criterion_Filter(criterion    = Enum__Text__Classification__Criteria.POSITIVE  ,
                                                    filter_mode  = Enum__Classification__Filter_Mode.BELOW        ,
                                                    threshold    = 0.4                                            )]         # matches two

        with Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                      ,
                                                   engine_mode         = Enum__Text__Transformation__Engine_Mode.TEXT_HASH ,
                                                   criterion_filters   = criterion_filters                                 ,
                                                   logic_operator      = Enum__Classification__Logic_Operator.AND          ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.XXX) as request:

            response = self.routes.transform(request)

            with response as _:
                assert _.success      is True
                assert _.total_hashes == 3
                assert _.obj()        == __(error_message=None,
                                            transformed_mapping=__(aaa1234567='xxxx xxx',
                                                                   bbb1234567='Text two',
                                                                   ccc1234567='xxxx xxxxx'),
                                            transformation_mode='xxx',
                                            success=True,
                                            total_hashes=3,
                                            transformed_hashes=2)

    def test__transform__with_text_hash_engine__multiple_filters__or_logic(self):  # Test unified endpoint with TEXT_HASH engine, multiple filters, OR logic
        hash_mapping = { Safe_Str__Hash("abc1234567"): "Test text" }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(criterion    = Enum__Text__Classification__Criteria.NEGATIVE  ,
                                                    filter_mode  = Enum__Classification__Filter_Mode.ABOVE        ,
                                                    threshold    = 0.8                                            ),
            Schema__Classification__Criterion_Filter(criterion    = Enum__Text__Classification__Criteria.POSITIVE  ,
                                                    filter_mode  = Enum__Classification__Filter_Mode.ABOVE        ,
                                                    threshold    = 0.8                                            )
        ]

        with Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                      ,
                                                   engine_mode         = Enum__Text__Transformation__Engine_Mode.TEXT_HASH ,
                                                   criterion_filters   = criterion_filters                                 ,
                                                   logic_operator      = Enum__Classification__Logic_Operator.OR           ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.XXX) as request:

            response = self.routes.transform(request)

            assert response.success is True
            assert response.obj() == __(error_message=None,
                                        transformed_mapping=__(abc1234567='Test text'),
                                        transformation_mode='xxx',
                                        success=True,
                                        total_hashes=1,
                                        transformed_hashes=0)

    def test__transform__abcde_ignores_filters(self):                           # CRITICAL: Verify ABCDE mode ignores all filters and transforms everything
        hash_mapping = { Safe_Str__Hash("a123456789"): "A" ,
                         Safe_Str__Hash("b123456789"): "BB" }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(criterion    = Enum__Text__Classification__Criteria.NEGATIVE  ,
                                                    filter_mode  = Enum__Classification__Filter_Mode.ABOVE        ,
                                                    threshold    = 0.9                                            )
        ]

        with Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                      ,
                                                   engine_mode         = Enum__Text__Transformation__Engine_Mode.TEXT_HASH ,
                                                   criterion_filters   = criterion_filters                                 ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE   ) as request:

            response = self.routes.transform(request)

            with response as _:
                assert _.success             is True
                assert _.total_hashes        == 2
                assert _.transformed_hashes  == 2                               # ALL transformed despite filters
                assert _.obj()                == __(error_message=None,
                                                    transformed_mapping=__(a123456789='a', b123456789='bb'),
                                                    transformation_mode='abcde-by-size',
                                                    success=True,
                                                    total_hashes=2,
                                                    transformed_hashes=2)

    # ========================================
    # Convenience Route Tests
    # ========================================

    def test__transform__convenience__basic_negative_filter(self):              # Test convenience route with negative sentiment filter
        hash_mapping = { Safe_Str__Hash("abc1234567"): "Negative text",         # negative: 0.3630613175290631,
                         Safe_Str__Hash("def1234567"): "Positive text!" }       # negative: 0.16752469006093718,


        with Schema__Text__Transformation__Request__Convenience(hash_mapping = hash_mapping) as request:

            response = self.routes.transform__convenience(
                engine_mode          = Enum__Text__Transformation__Engine_Mode.TEXT_HASH       ,
                transformation_mode  = Enum__Text__Transformation__Mode.XXX             ,
                criteria             = Enum__Text__Classification__Criteria.NEGATIVE           ,
                filter_mode          = Enum__Classification__Filter_Mode.ABOVE                 ,
                threshold            = Safe_Float(0.17)                                        ,    # above def1234567 value of 0.167
                request              = request
            )

            with response as _:
                assert _.success      is True
                assert _.total_hashes == 2
                assert _.obj()        == __(error_message=None,
                                            transformed_mapping = __(abc1234567='xxxxxxxx xxxx',
                                                                     def1234567='Positive text!'),
                                            transformation_mode = 'xxx',
                                            success             = True,
                                            total_hashes        = 2,
                                            transformed_hashes  = 1)

    def test__transform__convenience__positive_below_threshold(self):           # Test convenience route filtering by positive sentiment below threshold
        hash_mapping = { Safe_Str__Hash("abc1234567"): "Neutral content",
                         Safe_Str__Hash("def1234567"): "Positive content" }

        with Schema__Text__Transformation__Request__Convenience(hash_mapping = hash_mapping) as request:

            response = self.routes.transform__convenience(
                engine_mode          = Enum__Text__Transformation__Engine_Mode.TEXT_HASH       ,
                transformation_mode  = Enum__Text__Transformation__Mode.HASHES          ,
                criteria             = Enum__Text__Classification__Criteria.POSITIVE           ,
                filter_mode          = Enum__Classification__Filter_Mode.BELOW                 ,
                threshold            = Safe_Float(0.4)                                          ,
                request              = request
            )

            assert response.success is True
            assert response.obj()  == __(error_message=None,
                                         transformed_mapping=__(abc1234567='abc1234567',            # transformed
                                                                def1234567='Positive content'),
                                         transformation_mode='hashes'   ,
                                         success=True,
                                         total_hashes=2,
                                         transformed_hashes=1)

    def test__transform__convenience__abcde_ignores_filters(self):              # CRITICAL: Verify convenience route ABCDE mode also ignores filters
        hash_mapping = { Safe_Str__Hash("aaaaa12345"): "Hi"                                ,
                         Safe_Str__Hash("bbbbb12345"): "This is medium text"               ,
                         Safe_Str__Hash("ccccc12345"): "This is a longer piece of text"    }

        with Schema__Text__Transformation__Request__Convenience(hash_mapping = hash_mapping) as request:

            response = self.routes.transform__convenience(
                engine_mode          = Enum__Text__Transformation__Engine_Mode.RANDOM          ,
                transformation_mode  = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE          ,
                criteria             = Enum__Text__Classification__Criteria.POSITIVE           ,   # Ignored
                filter_mode          = Enum__Classification__Filter_Mode.ABOVE                 ,   # Ignored
                threshold            = Safe_Float(0.9)                                          ,   # Ignored
                request              = request
            )

            with response as _:
                assert _.success             is True
                assert _.total_hashes        == 3
                assert _.transformed_hashes  == 3                               # All transformed (ABCDE ignores filters)
                assert _.obj()               == __(error_message=None,
                                                   transformed_mapping=__(aaaaa12345='aa',
                                                                          bbbbb12345='bbbb bb bbbbbb bbbb',
                                                                          ccccc12345='cccc cc c cccccc ccccc cc cccc'),
                                                   transformation_mode='abcde-by-size',
                                                   success=True,
                                                   total_hashes=3,
                                                   transformed_hashes=3)

    def test__transform__convenience__all_engine_modes(self):                   # Test convenience route works with all engine modes
        hash_mapping = { Safe_Str__Hash("aaaa123456"): "Test content" }
        engine_modes = [
            Enum__Text__Transformation__Engine_Mode.TEXT_HASH     ,
            Enum__Text__Transformation__Engine_Mode.RANDOM
        ]

        #load_dotenv()
        #engine_modes.append(Enum__Text__Transformation__Engine_Mode.AWS_COMPREHEND)               # this needs AWS env

        for engine_mode in engine_modes:
            with Schema__Text__Transformation__Request__Convenience(hash_mapping = hash_mapping) as request:

                response = self.routes.transform__convenience(
                    engine_mode          = engine_mode                                          ,
                    transformation_mode  = Enum__Text__Transformation__Mode.XXX          ,
                    criteria             = Enum__Text__Classification__Criteria.NEGATIVE        ,
                    filter_mode          = Enum__Classification__Filter_Mode.ABOVE              ,
                    threshold            = Safe_Float(0.5)                                      ,
                    request              = request
                )

                assert response.success is True, f"Failed for engine_mode: {engine_mode}"

    def test__transform__convenience__all_transformation_modes(self):           # Test convenience route works with all transformation modes
        hash_mapping = { Safe_Str__Hash("aaaa123456"): "Test content" }

        transformation_modes = [
            Enum__Text__Transformation__Mode.XXX     ,
            Enum__Text__Transformation__Mode.HASHES  ,
            Enum__Text__Transformation__Mode.ABCDE_BY_SIZE
        ]

        for transformation_mode in transformation_modes:
            with Schema__Text__Transformation__Request__Convenience(hash_mapping = hash_mapping) as request:

                response = self.routes.transform__convenience(
                    engine_mode          = Enum__Text__Transformation__Engine_Mode.TEXT_HASH    ,
                    transformation_mode  = transformation_mode                                  ,
                    criteria             = Enum__Text__Classification__Criteria.NEGATIVE        ,
                    filter_mode          = Enum__Classification__Filter_Mode.ABOVE              ,
                    threshold            = Safe_Float(0.5)                                      ,
                    request              = request
                )

                assert response.success is True, f"Failed for transformation_mode: {transformation_mode}"

    def test__transform__convenience__threshold_boundaries(self):               # Test convenience route with threshold boundary values
        hash_mapping = { Safe_Str__Hash("aaaa123456"): "Test content" }

        thresholds = [Safe_Float(0.0), Safe_Float(0.5), Safe_Float(1.0)]

        for threshold in thresholds:
            with Schema__Text__Transformation__Request__Convenience(hash_mapping = hash_mapping) as request:

                response = self.routes.transform__convenience(
                    engine_mode          = Enum__Text__Transformation__Engine_Mode.TEXT_HASH    ,
                    transformation_mode  = Enum__Text__Transformation__Mode.XXX          ,
                    criteria             = Enum__Text__Classification__Criteria.POSITIVE        ,
                    filter_mode          = Enum__Classification__Filter_Mode.ABOVE              ,
                    threshold            = threshold                                            ,
                    request              = request
                )

                assert response.success is True, f"Failed for threshold: {threshold}"

    def test___build_full_request(self):                                        # Test internal helper method converts convenience params correctly
        hash_mapping = { Safe_Str__Hash("aaaa123456"): "Test text" }

        with self.routes as _:
            full_request = _._build_full_request(
                hash_mapping        = hash_mapping                                          ,
                engine_mode         = Enum__Text__Transformation__Engine_Mode.TEXT_HASH    ,
                transformation_mode = Enum__Text__Transformation__Mode.XXX          ,
                criteria            = Enum__Text__Classification__Criteria.NEGATIVE        ,
                filter_mode         = Enum__Classification__Filter_Mode.ABOVE              ,
                threshold           = Safe_Float(0.7)
            )

            assert type(full_request)                is Schema__Text__Transformation__Request
            assert full_request.hash_mapping         == hash_mapping
            assert full_request.engine_mode          == Enum__Text__Transformation__Engine_Mode.TEXT_HASH
            assert full_request.transformation_mode  == Enum__Text__Transformation__Mode.XXX
            assert len(full_request.criterion_filters) == 1

            criterion_filter = full_request.criterion_filters[0]
            assert criterion_filter.criterion    == Enum__Text__Classification__Criteria.NEGATIVE
            assert criterion_filter.filter_mode  == Enum__Classification__Filter_Mode.ABOVE
            assert criterion_filter.threshold    == 0.7

    # ========================================
    # Edge Cases
    # ========================================

    def test__transform__empty_mapping(self):                                   # Test unified endpoint handles empty hash mapping
        with Schema__Text__Transformation__Request(hash_mapping        = {}                                            ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.XXX) as request:

            response = self.routes.transform(request)

            assert response.obj() == __(error_message       = None          ,
                                       transformed_mapping = __()           ,
                                       transformation_mode = 'xxx'   ,
                                       success             = True           ,
                                       total_hashes        = 0              ,
                                       transformed_hashes  = 0              )

    def test__transform__empty_criterion_filters__transforms_all(self):         # Test empty filters list causes all hashes to be transformed
        hash_mapping = { Safe_Str__Hash("abc1234567"): "Hello" }

        with Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                      ,
                                                   engine_mode         = Enum__Text__Transformation__Engine_Mode.TEXT_HASH ,
                                                   criterion_filters   = []                                                ,  # Empty list
                                                   transformation_mode = Enum__Text__Transformation__Mode.XXX) as request:

            response = self.routes.transform(request)

            with response as _:
                assert _.success             is True
                assert _.transformed_hashes  == 1                               # All transformed

    def test__transform__convenience__empty_mapping(self):                      # Test convenience route handles empty hash mapping
        with Schema__Text__Transformation__Request__Convenience(hash_mapping = {}) as request:

            response = self.routes.transform__convenience(
                engine_mode          = Enum__Text__Transformation__Engine_Mode.TEXT_HASH    ,
                transformation_mode  = Enum__Text__Transformation__Mode.XXX          ,
                criteria             = Enum__Text__Classification__Criteria.NEGATIVE        ,
                filter_mode          = Enum__Classification__Filter_Mode.ABOVE              ,
                threshold            = Safe_Float(0.5)                                      ,
                request              = request
            )

            assert response.obj() == __(error_message       = None          ,
                                       transformed_mapping = __()           ,
                                       transformation_mode = 'xxx'   ,
                                       success             = True           ,
                                       total_hashes        = 0              ,
                                       transformed_hashes  = 0              )

    # ========================================
    # Transformation Verification Tests
    # ========================================

    def test__transform__xxx_random__verification(self):                        # Verify xxx mode actually transforms text correctly
        hash_mapping = { Safe_Str__Hash("abc1234567"): "Hello World" }

        with Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.XXX) as request:

            response = self.routes.transform(request)

            transformed_text = response.transformed_mapping[Safe_Str__Hash("abc1234567")]
            assert transformed_text != "Hello World"                            # Should be different
            assert 'x' in transformed_text                                      # Should contain x's
            assert ' ' in transformed_text                                      # Should preserve space

    def test__transform__hashes_random__verification(self):                     # Verify Hashes-Random mode shows hash values
        hash_mapping = { Safe_Str__Hash("abc1234567"): "Hello World" }

        with Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                    ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.HASHES) as request:

            response = self.routes.transform(request)

            transformed_text = response.transformed_mapping[Safe_Str__Hash("abc1234567")]
            assert transformed_text == "abc1234567"                             # Should show hash

    def test__transform__abcde_by_size__verification(self):                     # Verify ABCDE-By-Size mode groups by length
        hash_mapping = { Safe_Str__Hash("aaa1234567"): "Hi"           ,        # Short
                         Safe_Str__Hash("bbb1234567"): "Hello World"  }        # Long

        with Schema__Text__Transformation__Request(hash_mapping        = hash_mapping                                    ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE  ) as request:

            response = self.routes.transform(request)

            transformed_short = response.transformed_mapping[Safe_Str__Hash("aaa1234567")]
            transformed_long  = response.transformed_mapping[Safe_Str__Hash("bbb1234567")]

            assert transformed_short != "Hi"                                    # Should be transformed
            assert transformed_long  != "Hello World"                           # Should be transformed
            assert 'a' in transformed_short or 'b' in transformed_short         # Should have group letter
            assert ' ' in transformed_long                                      # Should preserve space

    def test__transform__convenience__xxx_random__verification(self):           # Verify convenience route XXX transformation works
        hash_mapping = { Safe_Str__Hash("aaaa123456"): "Hello, World!" }

        with Schema__Text__Transformation__Request__Convenience(hash_mapping = hash_mapping) as request:

            response = self.routes.transform__convenience(
                engine_mode          = Enum__Text__Transformation__Engine_Mode.TEXT_HASH    ,
                transformation_mode  = Enum__Text__Transformation__Mode.XXX          ,
                criteria             = Enum__Text__Classification__Criteria.NEGATIVE        ,
                filter_mode          = Enum__Classification__Filter_Mode.ABOVE              ,
                threshold            = Safe_Float(0.0)                                      ,   # Low threshold = all transformed
                request              = request
            )

            if response.transformed_hashes > 0:                                 # If any were transformed
                transformed = response.transformed_mapping[Safe_Str__Hash("aaaa123456")]
                if 'x' in transformed:                                          # If this one was transformed
                    assert ', ' in transformed                                  # Punctuation preserved
                    assert '!' in transformed                                   # Exclamation preserved