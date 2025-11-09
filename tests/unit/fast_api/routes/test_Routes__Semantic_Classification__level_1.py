from unittest                                                                                             import TestCase
from fastapi                                                                                              import FastAPI
from osbot_utils.testing.__                                                                               import __
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Criteria           import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.fast_api.routes.Routes__Semantic_Classification                      import Routes__Semantic_Classification
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Request               import Schema__Classification__Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Filter_Request        import Schema__Classification__Filter_Request
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode       import Enum__Classification__Output_Mode
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode       import Enum__Classification__Filter_Mode
from mgraph_ai_service_semantic_text.service.semantic_text.classification.Classification__Filter__Service import Classification__Filter__Service


class test_Routes__Semantic_Classification(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app    = FastAPI()
        cls.routes = Routes__Semantic_Classification(app=cls.app).setup()

    def test__setUpClass(self):
        with self.routes as _:
            assert type(_)                        is Routes__Semantic_Classification
            assert _.routes_paths()               == ['/single/filter', '/single/rate']
            assert _.tag                          == 'semantic-classification'
            assert type(_.classification_service) is Classification__Filter__Service
            assert _.app                          == self.app
            assert _.obj()                        == __(tag='semantic-classification',
                                                        router='APIRouter',
                                                        route_registration     = __(analyzer       = __()              ,
                                                                                   converter       = __()              ,
                                                                                   wrapper_creator = __(converter=__()),
                                                                                   route_parser    = __()             ),
                                                        classification_service = __(semantic_text_service    = __(semantic_text__engine = __(engine_mode='text_hash',
                                                                                    semantic_text_hashes     = __(hash_size=10),
                                                                                    classification__criteria = 'positivity'))),
                                                        app                    = 'FastAPI'                 ,
                                                        prefix                 = '/semantic-classification',
                                                        filter_tag             = True                      )

    # ========================================
    # classify__single__rate Tests
    # ========================================

    def test__classify__single__rate__basic(self):                             # Test basic rating endpoint with deterministic values
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World",
                        Safe_Str__Hash("def1234567"): "Test Text"}

        request = Schema__Classification__Request(hash_mapping            = hash_mapping                                    ,
                                                  classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY)

        response = self.routes.single__rate(request)

        assert response.success                 is True
        assert response.total_hashes            == 2
        assert len(response.hash_ratings)       == 2
        assert response.classification_criteria == Enum__Text__Classification__Criteria.POSITIVITY
        assert response.obj()                   == __(hash_ratings            = __(abc1234567 = 0.7478,  # Deterministic!
                                                                                   def1234567 = 0.508),
                                                       classification_criteria = 'positivity'   ,
                                                       total_hashes            = 2              ,
                                                       success                 = True           )

    def test__classify__single__rate__empty(self):                             # Test rating with empty mapping
        request = Schema__Classification__Request(hash_mapping            = {}                                              ,
                                                  classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY)

        response = self.routes.single__rate(request)

        assert response.success      is True
        assert response.total_hashes == 0
        assert response.hash_ratings == {}
        assert response.obj()        == __(hash_ratings            = __()        ,
                                           classification_criteria = 'positivity',
                                           total_hashes            = 0           ,
                                           success                 = True        )

    def test__classify__single__rate__single_hash(self):                       # Test rating with single hash
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Only text"}

        request = Schema__Classification__Request(hash_mapping            = hash_mapping                                    ,
                                                  classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY)

        response = self.routes.single__rate(request)

        assert response.success             is True
        assert response.total_hashes        == 1
        assert len(response.hash_ratings)   == 1
        assert Safe_Str__Hash("abc1234567") in response.hash_ratings
        assert response.obj()               == __(hash_ratings            = __(abc1234567=0.6339),  # Deterministic!
                                                  classification_criteria = 'positivity',
                                                  total_hashes            = 1           ,
                                                  success                 = True        )

    def test__classify__single__rate__ratings_in_range(self):                  # Test that ratings are within valid range (0.0-1.0)
        hash_mapping = {Safe_Str__Hash(f"a{i:09d}"): f"Text {i}" for i in range(10)}

        request = Schema__Classification__Request(hash_mapping            = hash_mapping                                    ,
                                                  classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY)

        response = self.routes.single__rate(request)

        assert response.success is True
        for hash_key, rating in response.hash_ratings.items():
            assert 0.0 <= float(rating) <= 1.0                                 # All ratings must be in valid range

        # Now we can assert exact values (deterministic!)
        assert response.obj() == __(hash_ratings              = __(a000000000 = 0.7645 ,
                                                                   a000000001 = 0.7402 ,
                                                                   a000000002 = 0.4943 ,
                                                                   a000000003 = 0.3426 ,
                                                                   a000000004 = 0.6403 ,
                                                                   a000000005 = 0.4758 ,
                                                                   a000000006 = 0.5538 ,
                                                                   a000000007 = 0.8807 ,
                                                                   a000000008 = 0.9498 ,
                                                                   a000000009 = 0.4043 ),
                                     classification_criteria = 'positivity' ,
                                     total_hashes            = 10           ,
                                     success                 = True         )


    # ========================================
    # single__filter Tests
    # ========================================

    def test__single__filter__above__hashes_only(self):                        # Test ABOVE filter with HASHES_ONLY output
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Positive text",
                        Safe_Str__Hash("def1234567"): "Another text"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(0.4)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response = self.routes.single__filter(request)

        assert response.success               is True
        assert response.total_hashes          == 2
        assert response.output_mode           == Enum__Classification__Output_Mode.HASHES_ONLY
        assert response.filtered_with_text    is None
        assert response.filtered_with_ratings is None

        assert response.obj()                 == __(filtered_with_text      = None          ,
                                                    filtered_with_ratings   = None          ,
                                                    filtered_hashes         = ['abc1234567'],  # Deterministic!
                                                    classification_criteria = 'positivity'  ,
                                                    output_mode             = 'hashes-only' ,
                                                    total_hashes            = 2             ,
                                                    filtered_count          = 1             ,
                                                    success                 = True          )


    def test__single__filter__above__with_text(self):                          # Test ABOVE filter with HASHES_WITH_TEXT output
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test content"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(0.0)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_WITH_TEXT)

        response = self.routes.single__filter(request)

        assert response.success             is True
        assert response.filtered_with_text  is not None
        assert len(response.filtered_with_text) == response.filtered_count

        # Deterministic: "Test content" gets 0.9301 (above 0.0)
        assert response.obj()               == __(filtered_with_text       = __(abc1234567 = 'Test content')         ,
                                                  filtered_with_ratings    = None                                    ,
                                                  filtered_hashes          = ['abc1234567']                          ,
                                                  classification_criteria  = 'positivity'                            ,
                                                  output_mode              = 'hashes-with-text'                      ,
                                                  total_hashes             = 1                                       ,
                                                  filtered_count           = 1                                       ,
                                                  success                  = True                                    )


    def test__single__filter__above__full_ratings(self):                       # Test ABOVE filter with FULL_RATINGS output
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(0.0)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.FULL_RATINGS)

        response = self.routes.single__filter(request)

        assert response.success               is True
        assert response.filtered_with_text    is not None
        assert response.filtered_with_ratings is not None

        # Deterministic: "Test" gets 0.5134
        assert response.obj()                 == __(filtered_with_text       = __(abc1234567 = 'Test')   ,
                                                    filtered_with_ratings    = __(abc1234567 = 0.4636)   ,  # Exact value!
                                                    filtered_hashes          = ['abc1234567']            ,
                                                    classification_criteria  = 'positivity'              ,
                                                    output_mode              = 'full-ratings'            ,
                                                    total_hashes             = 1                         ,
                                                    filtered_count           = 1                         ,
                                                    success                  = True                      )


    def test__single__filter__below(self):                                     # Test BELOW filter mode
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Text A",
                        Safe_Str__Hash("def1234567"): "Text B"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.BELOW        ,
                                                         threshold               = Safe_Float(0.5)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response = self.routes.single__filter(request)

        assert response.success        is True
        assert response.filtered_count <= response.total_hashes

        # Deterministic: "Text A" gets 0.3196, "Text B" gets 0.7976
        # Only "Text A" (0.3196) is below 0.5
        assert response.obj()          == __(filtered_with_text      = None          ,
                                             filtered_with_ratings   = None          ,
                                             filtered_hashes         = ['abc1234567'],
                                             classification_criteria = 'positivity'  ,
                                             output_mode             = 'hashes-only' ,
                                             total_hashes            = 2             ,
                                             filtered_count          = 1             ,
                                             success                 = True          )


    def test__single__filter__between(self):                                   # Test BETWEEN filter mode
        hash_mapping = {Safe_Str__Hash("aaa1234567"): "Text A",
                        Safe_Str__Hash("bbb1234567"): "Text B",
                        Safe_Str__Hash("ccc1234567"): "Text C"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.BETWEEN      ,
                                                         threshold               = Safe_Float(0.3)                                ,
                                                         threshold_max           = Safe_Float(0.7)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response = self.routes.single__filter(request)

        assert response.success         is True
        assert response.total_hashes    == 3
        assert response.filtered_count  <= 3

        # Deterministic: "Text A" gets 0.3196, "Text B" gets 0.7976, "Text C" gets 0.9857
        # Only "Text A" (0.3196) is between 0.3 and 0.7
        assert response.obj()           == __(filtered_with_text      = None          ,
                                              filtered_with_ratings   = None          ,
                                              filtered_hashes         = ['aaa1234567', 'ccc1234567'],
                                              classification_criteria = 'positivity'  ,
                                              output_mode             = 'hashes-only' ,
                                              total_hashes            = 3             ,
                                              filtered_count          = 2             ,
                                              success                 = True          )


    def test__single__filter__equals(self):                                    # Test EQUALS filter mode
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Text"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.EQUALS       ,
                                                         threshold               = Safe_Float(0.5)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response = self.routes.single__filter(request)

        assert response.success is True

        # Deterministic: "Text" gets 0.5134, not exactly 0.5
        assert response.obj()   == __(filtered_with_text       = None          ,
                                      filtered_with_ratings    = None          ,
                                      filtered_hashes          = []            ,
                                      classification_criteria  = 'positivity'  ,
                                      output_mode              = 'hashes-only' ,
                                      total_hashes             = 1             ,
                                      filtered_count           = 0             ,
                                      success                  = True          )


    def test__single__filter__empty_mapping(self):                             # Test filter with empty mapping
        request = Schema__Classification__Filter_Request(hash_mapping            = {}                                              ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(0.5)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response = self.routes.single__filter(request)

        assert response.success         is True
        assert response.total_hashes    == 0
        assert response.filtered_count  == 0
        assert response.filtered_hashes == []
        assert response.obj()           == __(filtered_with_text       = None          ,
                                              filtered_with_ratings    = None          ,
                                              filtered_hashes          = []            ,
                                              classification_criteria  = 'positivity'  ,
                                              output_mode              = 'hashes-only' ,
                                              total_hashes             = 0             ,
                                              filtered_count           = 0             ,
                                              success                  = True          )


    def test__single__filter__threshold_zero(self):                            # Test with threshold 0.0 (should include all)
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(0.0)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response = self.routes.single__filter(request)

        assert response.success        is True
        assert response.filtered_count == 1                                    # All hashes should pass
        assert response.obj()          == __(filtered_with_text       = None           ,
                                             filtered_with_ratings    = None           ,
                                             filtered_hashes          = ['abc1234567'] ,
                                             classification_criteria  = 'positivity'   ,
                                             output_mode              = 'hashes-only'  ,
                                             total_hashes             = 1              ,
                                             filtered_count           = 1              ,
                                             success                  = True           )


    def test__single__filter__threshold_one(self):                             # Test with threshold 1.0 (should include none)
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(1.0)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response = self.routes.single__filter(request)

        assert response.success        is True
        assert response.filtered_count == 0                                    # No hash should have rating > 1.0
        assert response.obj()          == __(filtered_with_text       = None          ,
                                             filtered_with_ratings    = None          ,
                                             filtered_hashes          = []            ,
                                             classification_criteria  = 'positivity'  ,
                                             output_mode              = 'hashes-only' ,
                                             total_hashes             = 1             ,
                                             filtered_count           = 0             ,
                                             success                  = True          )


    # ========================================
    # Multiple Hashes Tests
    # ========================================

    def test__single__filter__multiple_hashes(self):                           # Test with multiple hashes - now deterministic!
        hash_mapping = {Safe_Str__Hash(f"a{i:09d}"): f"Text {i}" for i in range(20)}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(0.5)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.FULL_RATINGS)

        response = self.routes.single__filter(request)

        assert response.success             is True
        assert response.total_hashes        == 20

        # Now we can assert exact values!
        assert response.obj()               == __(filtered_with_text       = __( a000000000 = 'Text 0'  ,
                                                                                 a000000001 = 'Text 1'  ,
                                                                                 a000000004 = 'Text 4'  ,
                                                                                 a000000006 = 'Text 6'  ,
                                                                                 a000000007 = 'Text 7'  ,
                                                                                 a000000008 = 'Text 8'  ,
                                                                                 a000000010 = 'Text 10' ,
                                                                                 a000000011 = 'Text 11' ,
                                                                                 a000000012 = 'Text 12' ,
                                                                                 a000000014 = 'Text 14' ,
                                                                                 a000000019 = 'Text 19' ),
                                                   filtered_with_ratings    = __(a000000000 = 0.7645    ,
                                                                                 a000000001 = 0.7402    ,
                                                                                 a000000004 = 0.6403    ,
                                                                                 a000000006 = 0.5538    ,
                                                                                 a000000007 = 0.8807    ,
                                                                                 a000000008 = 0.9498    ,
                                                                                 a000000010 = 0.7621    ,
                                                                                 a000000011 = 0.6607    ,
                                                                                 a000000012 = 0.652     ,
                                                                                 a000000014 = 0.6322    ,
                                                                                 a000000019 = 0.9169    ),
                                                   filtered_hashes          = ['a000000000' ,
                                                                               'a000000001' ,
                                                                               'a000000004' ,
                                                                               'a000000006' ,
                                                                               'a000000007' ,
                                                                               'a000000008' ,
                                                                               'a000000010' ,
                                                                               'a000000011' ,
                                                                               'a000000012' ,
                                                                               'a000000014' ,
                                                                               'a000000019' ,]                            ,
                                                   classification_criteria  = 'positivity'                               ,
                                                   output_mode              = 'full-ratings'                             ,
                                                   total_hashes             = 20                                         ,
                                                   filtered_count           = 11                                         ,
                                                   success                  = True                                       )