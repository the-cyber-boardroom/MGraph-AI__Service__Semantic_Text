from unittest                                                                                               import TestCase
from osbot_utils.type_safe.primitives.core.Safe_Float                                                       import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                          import Safe_Str__Hash
from mgraph_ai_service_semantic_text.service.semantic_text.Semantic_Text__Service                           import Semantic_Text__Service
from mgraph_ai_service_semantic_text.service.semantic_text.classification.Classification__Filter__Service   import Classification__Filter__Service
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria                     import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Request                 import Schema__Classification__Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Response                import Schema__Classification__Response
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Filter_Request          import Schema__Classification__Filter_Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Filter_Response         import Schema__Classification__Filter_Response
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode         import Enum__Classification__Output_Mode
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode         import Enum__Classification__Filter_Mode


class test_Classification__Filter__Service(TestCase):

    @classmethod
    def setUpClass(cls):
        semantic_text_service          = Semantic_Text__Service().setup()
        cls.classification_filter_service = Classification__Filter__Service(semantic_text_service=semantic_text_service)

    def test__init__(self):                                                    # Test service initialization
        with self.classification_filter_service as _:
            assert type(_)                        is Classification__Filter__Service
            assert type(_.semantic_text_service) is Semantic_Text__Service

    # ========================================
    # classify_all() Tests
    # ========================================

    def test__classify_all__basic(self):                                       # Test basic classification of all hashes
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World",
                        Safe_Str__Hash("def1234567"): "Test Text"}

        request = Schema__Classification__Request(hash_mapping            = hash_mapping                                    ,
                                                  classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY)

        response = self.classification_filter_service.classify_all(request)

        assert type(response)                is Schema__Classification__Response
        assert response.success              is True
        assert response.total_hashes         == 2
        assert len(response.hash_ratings)    == 2
        assert Safe_Str__Hash("abc1234567") in response.hash_ratings
        assert Safe_Str__Hash("def1234567") in response.hash_ratings
        assert 0 <= response.hash_ratings[Safe_Str__Hash("abc1234567")] <= 1
        assert 0 <= response.hash_ratings[Safe_Str__Hash("def1234567")] <= 1

    def test__classify_all__empty_mapping(self):                               # Test with empty hash mapping
        request = Schema__Classification__Request(hash_mapping            = {}                                              ,
                                                  classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY)

        response = self.classification_filter_service.classify_all(request)

        assert response.success       is True
        assert response.total_hashes  == 0
        assert response.hash_ratings  == {}

    def test__classify_all__single_hash(self):                                 # Test with single hash
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Single text"}

        request = Schema__Classification__Request(hash_mapping            = hash_mapping                                    ,
                                                  classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY)

        response = self.classification_filter_service.classify_all(request)

        assert response.success              is True
        assert response.total_hashes         == 1
        assert len(response.hash_ratings)    == 1

    # ========================================
    # filter_by_criteria() Tests - ABOVE mode
    # ========================================

    def test__filter_by_criteria__above__hashes_only(self):                    # Test ABOVE filter with HASHES_ONLY output
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Positive text",
                        Safe_Str__Hash("def1234567"): "Negative text"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(0.5)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response = self.classification_filter_service.filter_by_criteria(request)

        assert type(response)               is Schema__Classification__Filter_Response
        assert response.success             is True
        assert response.total_hashes        == 2
        assert response.filtered_count      >= 0
        assert response.filtered_count      <= 2
        assert response.output_mode         == Enum__Classification__Output_Mode.HASHES_ONLY
        assert response.filtered_with_text  is None
        assert response.filtered_with_ratings is None

    def test__filter_by_criteria__above__with_text(self):                      # Test ABOVE filter with HASHES_WITH_TEXT output
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(0.0)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_WITH_TEXT)

        response = self.classification_filter_service.filter_by_criteria(request)

        assert response.success             is True
        assert response.filtered_with_text  is not None
        assert response.filtered_with_ratings is None

    def test__filter_by_criteria__above__full_ratings(self):                   # Test ABOVE filter with FULL_RATINGS output
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(0.0)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.FULL_RATINGS)

        response = self.classification_filter_service.filter_by_criteria(request)

        assert response.success               is True
        assert response.filtered_with_text    is not None
        assert response.filtered_with_ratings is not None

    # ========================================
    # filter_by_criteria() Tests - BELOW mode
    # ========================================

    def test__filter_by_criteria__below(self):                                 # Test BELOW filter mode
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Text A",
                        Safe_Str__Hash("def1234567"): "Text B"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.BELOW        ,
                                                         threshold               = Safe_Float(0.5)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response = self.classification_filter_service.filter_by_criteria(request)

        assert response.success        is True
        assert response.total_hashes   == 2
        assert response.filtered_count >= 0
        assert response.filtered_count <= 2

    # ========================================
    # filter_by_criteria() Tests - BETWEEN mode
    # ========================================

    def test__filter_by_criteria__between(self):                               # Test BETWEEN filter mode
        hash_mapping = {Safe_Str__Hash("aaa1234567"): "Text A",
                        Safe_Str__Hash("bbb1234567"): "Text B",
                        Safe_Str__Hash("ccc1234567"): "Text C"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.BETWEEN      ,
                                                         threshold               = Safe_Float(0.3)                                ,
                                                         threshold_max           = Safe_Float(0.7)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response = self.classification_filter_service.filter_by_criteria(request)

        assert response.success        is True
        assert response.total_hashes   == 3
        assert response.filtered_count >= 0
        assert response.filtered_count <= 3

    # ========================================
    # filter_by_criteria() Tests - EQUALS mode
    # ========================================

    def test__filter_by_criteria__equals(self):                                # Test EQUALS filter mode
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Text"}

        request = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.EQUALS       ,
                                                         threshold               = Safe_Float(0.5)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response = self.classification_filter_service.filter_by_criteria(request)

        assert response.success is True
        # EQUALS is unlikely to match due to random ratings, but should not error

    # ========================================
    # Edge Cases
    # ========================================

    def test__filter_by_criteria__empty_mapping(self):                         # Test with empty hash mapping
        request = Schema__Classification__Filter_Request(hash_mapping            = {}                                              ,
                                                         classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                         filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                         threshold               = Safe_Float(0.5)                                ,
                                                         output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response = self.classification_filter_service.filter_by_criteria(request)

        assert response.success        is True
        assert response.total_hashes   == 0
        assert response.filtered_count == 0
        assert response.filtered_hashes == []

    def test__filter_by_criteria__threshold_extremes(self):                    # Test with extreme threshold values
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        # Test threshold = 0.0 (should include all)
        request_zero = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                              classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                              filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                              threshold               = Safe_Float(0.0)                                ,
                                                              output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response_zero = self.classification_filter_service.filter_by_criteria(request_zero)
        assert response_zero.success       is True
        assert response_zero.filtered_count == 1

        # Test threshold = 1.0 (should include none)
        request_one = Schema__Classification__Filter_Request(hash_mapping            = hash_mapping                                    ,
                                                             classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY,
                                                             filter_mode             = Enum__Classification__Filter_Mode.ABOVE        ,
                                                             threshold               = Safe_Float(1.0)                                ,
                                                             output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY )

        response_one = self.classification_filter_service.filter_by_criteria(request_one)
        assert response_one.success       is True
        assert response_one.filtered_count == 0
