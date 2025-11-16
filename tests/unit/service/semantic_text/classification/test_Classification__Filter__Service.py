from unittest                                                                                               import TestCase

from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text import Safe_Str__Comprehend__Text
from osbot_utils.testing.__ import __
from osbot_utils.type_safe.primitives.core.Safe_Float                                                       import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                          import Safe_Str__Hash

from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Engine_Mode import Enum__Text__Classification__Engine_Mode
#from mgraph_ai_service_semantic_text.service.semantic_text.Semantic_Text__Service                           import Semantic_Text__Service
from mgraph_ai_service_semantic_text.service.semantic_text.classification.Classification__Filter__Service   import Classification__Filter__Service
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria                     import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Request                 import Schema__Classification__Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Response                import Schema__Classification__Response
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Filter_Request          import Schema__Classification__Filter_Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Filter_Response         import Schema__Classification__Filter_Response
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode         import Enum__Classification__Output_Mode
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode         import Enum__Classification__Filter_Mode
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__Factory import Semantic_Text__Engine__Factory


class test_Classification__Filter__Service(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.classification_filter_service = Classification__Filter__Service()
        cls.engine_mode                   = Enum__Text__Classification__Engine_Mode.TEXT_HASH

    def test__init__(self):                                                    # Test service initialization
        with self.classification_filter_service as _:
            assert type(_)                is Classification__Filter__Service
            assert type(_.engine_factory) is Semantic_Text__Engine__Factory

    # ========================================
    # classify_all() Tests
    # ========================================

    def test__classify_all__basic(self):                                       # Test basic classification of all hashes
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World",
                        Safe_Str__Hash("def1234567"): "Test Text"}

        request = Schema__Classification__Request(hash_mapping = hash_mapping)

        response = self.classification_filter_service.classify_all(request     = request         ,
                                                                   engine_mode = self.engine_mode)

        assert type(response)               is Schema__Classification__Response
        assert response.success             is True
        assert response.total_hashes        == 2
        assert len(response.hash_ratings)   == 2
        assert Safe_Str__Hash("abc1234567") in response.hash_ratings
        assert Safe_Str__Hash("def1234567") in response.hash_ratings
        assert response.obj()               == __(hash_ratings = __(abc1234567=__(positive = 0.61575136853258    ,
                                                                                  negative = 0.060921772911884164,
                                                                                  neutral  = 0.2944552357407734  ,
                                                                                  mixed    = 0.028871622814762493),
                                                                    def1234567=__(positive = 0.2842339724966105  ,
                                                                                  negative = 0.25290528762347475 ,
                                                                                  neutral  = 0.1380980050358319  ,
                                                                                  mixed    = 0.3247627348440829  )),
                                                  total_hashes = 2,
                                                  success      = True)

    def test__classify_all__empty_mapping(self):                               # Test with empty hash mapping
        request = Schema__Classification__Request(hash_mapping = {})

        response = self.classification_filter_service.classify_all(request     = request         ,
                                                                   engine_mode = self.engine_mode)

        assert response.success       is True
        assert response.total_hashes  == 0
        assert response.hash_ratings  == {}

    def test__classify_all__single_hash(self):                                 # Test with single hash
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Single text"}

        request = Schema__Classification__Request(hash_mapping = hash_mapping)

        response = self.classification_filter_service.classify_all(request     = request        ,
                                                                   engine_mode = self.engine_mode)

        assert response.success              is True
        assert response.total_hashes         == 1
        assert len(response.hash_ratings)    == 1

    # ========================================
    # filter_by_criteria() Tests - ABOVE mode
    # ========================================

    def test__filter_by_criteria__above__hashes_only(self):                    # Test ABOVE filter with HASHES_ONLY output
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Positive text..",
                        Safe_Str__Hash("def1234567"): "Negative text."}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVE,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(0.5)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response = self.classification_filter_service.filter_by_criteria(request     = request         ,
                                                                         engine_mode = self.engine_mode)

        assert type(response)                 is Schema__Classification__Filter_Response
        assert response.success               is True
        assert response.total_hashes          == 2
        assert response.filtered_count        == 1
        assert response.output_mode           == Enum__Classification__Output_Mode.HASHES_ONLY
        assert response.filtered_with_text    == {}
        assert response.filtered_with_ratings == {}
        assert response.obj()                 == __(filtered_hashes         = ['abc1234567'] ,
                                                    filtered_with_text      = __()           ,
                                                    filtered_with_ratings   = __()           ,
                                                    classification_criteria = 'positive'     ,
                                                    output_mode             = 'hashes-only'  ,
                                                    total_hashes            = 2              ,
                                                    filtered_count          = 1              ,
                                                    success                 = True           )


    def test__filter_by_criteria__above__with_text(self):                      # Test ABOVE filter with HASHES_WITH_TEXT output
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVE,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(0.0)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_WITH_TEXT)

        response = self.classification_filter_service.filter_by_criteria(request     = request         ,
                                                                         engine_mode = self.engine_mode)

        assert response.success               is True
        assert response.filtered_with_text    == {Safe_Str__Hash('abc1234567'): Safe_Str__Comprehend__Text('Test')}
        assert response.filtered_with_ratings == {}
        assert response.obj()                 == __(filtered_hashes           = ['abc1234567']           ,
                                                    filtered_with_text         = __(abc1234567 = 'Test') ,
                                                    filtered_with_ratings      = __()                    ,
                                                    classification_criteria    = 'positive'              ,
                                                    output_mode                = 'hashes-with-text'      ,
                                                    total_hashes               = 1                       ,
                                                    filtered_count             = 1                       ,
                                                    success                    = True                    )


    def test__filter_by_criteria__above__full_ratings(self):                   # Test ABOVE filter with FULL_RATINGS output
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVE,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(0.4)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.FULL_RATINGS)

        response = self.classification_filter_service.filter_by_criteria(request     = request         ,
                                                                         engine_mode = self.engine_mode)

        assert response.success               is True
        assert response.filtered_with_text    is not None
        assert response.filtered_with_ratings is not None
        assert response.obj()                 == __(filtered_hashes           = ['abc1234567']                                   ,
                                                    filtered_with_text        = __(abc1234567 = 'Test')                          ,
                                                    filtered_with_ratings     = __(abc1234567 = __(positive = 0.42570156363259815 ,
                                                                                                   negative = 0.10598529564046805 ,
                                                                                                   neutral  = 0.22108315211763488 ,
                                                                                                   mixed    = 0.24722998860929896)),
                                                    classification_criteria   = 'positive'                                       ,
                                                    output_mode               = 'full-ratings'                                   ,
                                                    total_hashes              = 1                                                ,
                                                    filtered_count            = 1                                                ,
                                                    success                   = True                                             )


    # ========================================
    # filter_by_criteria() Tests - BELOW mode
    # ========================================

    def test__filter_by_criteria__below(self):                                  # Test BELOW filter mode
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Text A",                 # positive=0.3969413061449435
                        Safe_Str__Hash("def1234567"): "Text B"}                 # positive=0.616592082616179

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVE,
                                                         filter_mode             = Enum__Classification__Filter_Mode.BELOW        ,
                                                         threshold               = Safe_Float(0.5)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.FULL_RATINGS )

        response = self.classification_filter_service.filter_by_criteria(request     = request         ,
                                                                         engine_mode = self.engine_mode)

        assert response.success        is True
        assert response.total_hashes   == 2
        assert response.filtered_count >= 0
        assert response.filtered_count <= 2
        assert response.obj()          == __(filtered_hashes           = ['abc1234567']                                     ,
                                             filtered_with_text        = __(abc1234567 = 'Text A')                          ,
                                             filtered_with_ratings     = __(abc1234567 = __(positive = 0.3969413061449435  ,
                                                                                            negative = 0.3216221181225315  ,
                                                                                            neutral  = 0.18664462202626986 ,
                                                                                            mixed    = 0.09479195370625516)),
                                             classification_criteria   = 'positive'                                         ,
                                             output_mode               = 'full-ratings'                                     ,
                                             total_hashes              = 2                                                  ,
                                             filtered_count            = 1                                                  ,
                                             success                   = True                                               )


    # ========================================
    # filter_by_criteria() Tests - BETWEEN mode
    # ========================================

    def test__filter_by_criteria__between(self):                                # Test BETWEEN filter mode
        hash_mapping = {Safe_Str__Hash("aaa1234567"): "Text A",                 # positive=0.3969413061449435,
                        Safe_Str__Hash("bbb1234567"): "Text B",                 # positive=0.616592082616179,
                        Safe_Str__Hash("ccc1234567"): "Text C"}                 # positive=0.1645044724838576,

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVE,
                                                         filter_mode             = Enum__Classification__Filter_Mode.BETWEEN      ,
                                                         threshold               = Safe_Float(0.3)                                ,
                                                         threshold_max           = Safe_Float(0.7)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.FULL_RATINGS )

        response = self.classification_filter_service.filter_by_criteria(request     = request         ,
                                                                         engine_mode = self.engine_mode)

        assert response.success        is True
        assert response.total_hashes   == 3
        assert response.filtered_count == 2
        assert response.filtered_count == 2
        assert response.obj()          == __(filtered_hashes           = ['aaa1234567', 'bbb1234567']                       ,
                                             filtered_with_text        = __(aaa1234567 = 'Text A'                           ,
                                                                           bbb1234567  = 'Text B')                          ,
                                             filtered_with_ratings     = __(aaa1234567 = __(positive = 0.3969413061449435  ,
                                                                                            negative = 0.3216221181225315  ,
                                                                                            neutral  = 0.18664462202626986 ,
                                                                                            mixed    = 0.09479195370625516),
                                                                           bbb1234567  = __(positive = 0.616592082616179   ,
                                                                                            negative = 0.062444061962134256,
                                                                                            neutral  = 0.05301204819277109 ,
                                                                                            mixed    = 0.26795180722891565 )),
                                             classification_criteria   = 'positive'                                         ,
                                             output_mode               = 'full-ratings'                                     ,
                                             total_hashes              = 3                                                  ,
                                             filtered_count            = 2                                                  ,
                                             success                   = True                                               )


    # ========================================
    # filter_by_criteria() Tests - EQUALS mode
    # ========================================

    def test__filter_by_criteria__equals(self):                                     # Test EQUALS filter mode
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Text"}                       # positive=0.6001957083944922,

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                  ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVE ,
                                                         filter_mode             = Enum__Classification__Filter_Mode.EQUALS      ,
                                                         threshold               = Safe_Float(0.600)                ,
                                                         output_mode             = Enum__Classification__Output_Mode.FULL_RATINGS )

        response = self.classification_filter_service.filter_by_criteria(request     = request         ,
                                                                         engine_mode = self.engine_mode)

        assert response.success is True
        assert response.obj()   == __( filtered_hashes           = ['abc1234567']                                   ,
                                       filtered_with_text        = __(abc1234567 = 'Text')                          ,
                                       filtered_with_ratings     = __(abc1234567 = __(positive = 0.6001957083944922 ,
                                                                                      negative = 0.22848955056965123,
                                                                                      neutral  = 0.11148388900538198,
                                                                                      mixed    = 0.059830852030474585)),
                                       classification_criteria   = 'positive'                                       ,
                                       output_mode               = 'full-ratings'                                   ,
                                       total_hashes              = 1                                                ,
                                       filtered_count            = 1                                                ,
                                       success                   = True                                             )



        def check_tolerance(tolerance, should_match):
            request.threshold = tolerance
            response_2        =  self.classification_filter_service.filter_by_criteria(request = request,engine_mode = self.engine_mode)
            assert (response_2.obj() == response.obj()) is should_match

        # todo: check why there is some performance impact of running these tests
        #       (without the ones below the test runs in 4ms , with the tests in runs in 14ms)
        # these will still match because we are within the value of FLOAT__CLASSIFICATION__FILTER__EQUALS__TOLERANCE (which is 0.001
        check_tolerance(tolerance=0.6001957083944922, should_match=True)
        check_tolerance(tolerance=0.60019570839449  , should_match=True)
        check_tolerance(tolerance=0.60019570839     , should_match=True)
        check_tolerance(tolerance=0.60019570        , should_match=True)
        check_tolerance(tolerance=0.60019           , should_match=True)
        check_tolerance(tolerance=0.60109           , should_match=True)
        check_tolerance(tolerance=0.601             , should_match=True)
        check_tolerance(tolerance=0.5992            , should_match=True)

        # these dot not match because they are outside the tolerance of 0.001
        check_tolerance(tolerance=0.602             , should_match=False)
        check_tolerance(tolerance=0.599             , should_match=False)
        check_tolerance(tolerance=0.599             , should_match=False)
        check_tolerance(tolerance=0.59              , should_match=False)
        check_tolerance(tolerance=0.61              , should_match=False)


    # ========================================
    # Edge Cases
    # ========================================

    def test__filter_by_criteria__empty_mapping(self):                         # Test with empty hash mapping
        request = Schema__Classification__Filter_Request(hash_mapping            = {}                                              ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVE,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(0.5)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response = self.classification_filter_service.filter_by_criteria(request     = request         ,
                                                                         engine_mode = self.engine_mode)

        assert response.success         is True
        assert response.total_hashes    == 0
        assert response.filtered_count  == 0
        assert response.filtered_hashes == []

    def test__filter_by_criteria__threshold_extremes(self):                    # Test with extreme threshold values
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        # Test threshold = 0.0 (should include all)
        request_zero = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                              classification_criteria = Enum__Text__Classification__Criteria.POSITIVE,
                                                              filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                              threshold               = Safe_Float(0.0)                                ,
                                                              output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response_zero = self.classification_filter_service.filter_by_criteria(request     = request_zero    ,
                                                                              engine_mode = self.engine_mode)
        assert response_zero.success        is True
        assert response_zero.filtered_count == 1

        # Test threshold = 1.0 (should include none)
        request_one = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                             classification_criteria = Enum__Text__Classification__Criteria.POSITIVE,
                                                             filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                             threshold               = Safe_Float(1.0)                                ,
                                                             output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response_one = self.classification_filter_service.filter_by_criteria(request     = request_one     ,
                                                                             engine_mode = self.engine_mode)
        assert response_one.success       is True
        assert response_one.filtered_count == 0
