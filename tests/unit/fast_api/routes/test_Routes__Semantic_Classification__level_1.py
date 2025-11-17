from unittest                                                                                             import TestCase
from fastapi                                                                                              import FastAPI
from osbot_utils.testing.__                                                                               import __
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria                   import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Engine_Mode                import Enum__Text__Classification__Engine_Mode
from mgraph_ai_service_semantic_text.fast_api.routes.Routes__Semantic_Classification                      import Routes__Semantic_Classification
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Request               import Schema__Classification__Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Filter_Request        import Schema__Classification__Filter_Request
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode       import Enum__Classification__Output_Mode
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode       import Enum__Classification__Filter_Mode
from mgraph_ai_service_semantic_text.service.semantic_text.classification.Classification__Filter__Service import Classification__Filter__Service


class test_Routes__Semantic_Classification(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app         = FastAPI()
        cls.routes      = Routes__Semantic_Classification(app=cls.app).setup()
        cls.engine_mode = Enum__Text__Classification__Engine_Mode.TEXT_HASH

    def test__setUpClass(self):
        with self.routes as _:
            assert type(_)                        is Routes__Semantic_Classification
            assert _.routes_paths()               == ['/{engine_mode}/filter'      ,
                                                      '/{engine_mode}/multi/filter',
                                                      '/{engine_mode}/multi/rate'  ,
                                                      '/{engine_mode}/rate'        ]
            assert _.tag                          == 'semantic-classification'
            assert type(_.classification_service) is Classification__Filter__Service
            assert _.app                          == self.app

    # ========================================
    # engine_mode__rate Tests (Level 1: Single Criterion)
    # ========================================

    def test__engine_mode__rate__basic(self):                                  # Test basic rating endpoint returns all 4 criteria
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World",
                        Safe_Str__Hash("def1234567"): "Test Text"}

        request = Schema__Classification__Request(hash_mapping = hash_mapping)

        response = self.routes.engine_mode__rate(self.engine_mode, request)

        assert response.success           is True
        assert response.total_hashes      == 2
        assert len(response.hash_ratings) == 2

        # Now returns all 4 criteria for each hash
        assert response.obj() == __(hash_ratings = __(abc1234567 = __(positive = 0.61575136853258      ,
                                                                      negative = 0.06092177291188416   ,
                                                                      neutral  = 0.2944552357407734    ,
                                                                      mixed    = 0.028871622814762493  ),
                                                      def1234567 = __(positive = 0.2842339724966105    ,
                                                                      negative = 0.25290528762347475   ,
                                                                      neutral  = 0.1380980050358319    ,
                                                                      mixed    = 0.3247627348440829    )),
                                    total_hashes = 2   ,
                                    success      = True)

    def test__engine_mode__rate__empty(self):                                  # Test rating with empty mapping
        request = Schema__Classification__Request(hash_mapping = {})

        response = self.routes.engine_mode__rate(self.engine_mode, request)

        assert response.success      is True
        assert response.total_hashes == 0
        assert response.hash_ratings == {}

    def test__engine_mode__rate__single_hash(self):                            # Test rating with single hash
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Only text"}

        request = Schema__Classification__Request(hash_mapping = hash_mapping)

        response = self.routes.engine_mode__rate(self.engine_mode, request)

        assert response.success             is True
        assert response.total_hashes        == 1
        assert len(response.hash_ratings)   == 1
        assert Safe_Str__Hash("abc1234567") in response.hash_ratings

    def test__engine_mode__rate__ratings_in_range(self):                       # Test that all ratings are within valid range (0.0-1.0)
        hash_mapping = {Safe_Str__Hash(f"a{i:09d}"): f"Text {i}" for i in range(10)}

        request = Schema__Classification__Request(hash_mapping = hash_mapping)

        response = self.routes.engine_mode__rate(self.engine_mode, request)

        assert response.success      is True
        assert response.total_hashes == 10

        for hash_key, ratings in response.hash_ratings.items():
            for criterion, rating in ratings.items():
                assert 0.0 <= float(rating) <= 1.0, f"Rating for {hash_key}/{criterion} is out of range: {rating}"

    # ========================================
    # engine_mode__filter Tests
    # ========================================

    def test__engine_mode__filter__hashes_only(self):                          # Test filter with HASHES_ONLY output mode
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Hello World"}

        request = Schema__Classification__Filter_Request(
            hash_mapping            = hash_mapping                                      ,
            classification_criteria = Enum__Text__Classification__Criteria.POSITIVE    ,
            filter_mode             = Enum__Classification__Filter_Mode.ABOVE          ,
            threshold               = Safe_Float(0.5)                                  ,
            output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.engine_mode__filter(self.engine_mode, request)

        assert response.success               is True
        assert response.filtered_count        == 1
        assert response.filtered_with_text    == {}
        assert response.filtered_with_ratings == {}

    def test__engine_mode__filter__with_text(self):                            # Test filter with HASHES_WITH_TEXT output mode
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        request = Schema__Classification__Filter_Request(
            hash_mapping            = hash_mapping                                      ,
            classification_criteria = Enum__Text__Classification__Criteria.POSITIVE    ,
            filter_mode             = Enum__Classification__Filter_Mode.ABOVE          ,
            threshold               = Safe_Float(0.4)                                  ,
            output_mode             = Enum__Classification__Output_Mode.HASHES_WITH_TEXT
        )

        response = self.routes.engine_mode__filter(self.engine_mode, request)

        assert response.success            is True
        assert response.filtered_count     == 1
        assert response.filtered_with_text is not None
        assert Safe_Str__Hash("abc1234567") in response.filtered_with_text

    def test__engine_mode__filter__full_ratings(self):                         # Test filter with FULL_RATINGS output mode
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        request = Schema__Classification__Filter_Request(
            hash_mapping            = hash_mapping                                      ,
            classification_criteria = Enum__Text__Classification__Criteria.POSITIVE    ,
            filter_mode             = Enum__Classification__Filter_Mode.ABOVE          ,
            threshold               = Safe_Float(0.4)                                  ,
            output_mode             = Enum__Classification__Output_Mode.FULL_RATINGS
        )

        response = self.routes.engine_mode__filter(self.engine_mode, request)

        assert response.success               is True
        assert response.filtered_count        == 1
        assert response.filtered_with_text    is not None
        assert response.filtered_with_ratings is not None

        # Full ratings include all 4 criteria
        ratings = response.filtered_with_ratings[Safe_Str__Hash("abc1234567")]
        assert len(ratings) == 4
        assert Enum__Text__Classification__Criteria.POSITIVE in ratings
        assert Enum__Text__Classification__Criteria.NEGATIVE in ratings
        assert Enum__Text__Classification__Criteria.NEUTRAL in ratings
        assert Enum__Text__Classification__Criteria.MIXED in ratings

    def test__engine_mode__filter__below_mode(self):                           # Test BELOW filter mode
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Text A",                # positive=0.3969413061449435
                        Safe_Str__Hash("def1234567"): "Text B"}                # positive=0.616592082616179

        request = Schema__Classification__Filter_Request(
            hash_mapping            = hash_mapping                                      ,
            classification_criteria = Enum__Text__Classification__Criteria.POSITIVE    ,
            filter_mode             = Enum__Classification__Filter_Mode.BELOW          ,
            threshold               = Safe_Float(0.5)                                  ,
            output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.engine_mode__filter(self.engine_mode, request)

        assert response.success        is True
        assert response.filtered_count == 1                                     # Only Text A passes (0.3969 < 0.5)
        assert Safe_Str__Hash("abc1234567") in response.filtered_hashes

    # ========================================
    # Edge Cases
    # ========================================

    def test__engine_mode__filter__empty_mapping(self):                        # Test with empty hash mapping
        request = Schema__Classification__Filter_Request(
            hash_mapping            = {}                                                ,
            classification_criteria = Enum__Text__Classification__Criteria.POSITIVE    ,
            filter_mode             = Enum__Classification__Filter_Mode.ABOVE          ,
            threshold               = Safe_Float(0.5)                                  ,
            output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.engine_mode__filter(self.engine_mode, request)

        assert response.success         is True
        assert response.total_hashes    == 0
        assert response.filtered_count  == 0
        assert response.filtered_hashes == []

    def test__engine_mode__filter__threshold_zero(self):                       # Test with threshold 0.0 (should include all)
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        request = Schema__Classification__Filter_Request(
            hash_mapping            = hash_mapping                                      ,
            classification_criteria = Enum__Text__Classification__Criteria.POSITIVE    ,
            filter_mode             = Enum__Classification__Filter_Mode.ABOVE          ,
            threshold               = Safe_Float(0.0)                                  ,
            output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.engine_mode__filter(self.engine_mode, request)

        assert response.success        is True
        assert response.filtered_count == 1

    def test__engine_mode__filter__threshold_one(self):                        # Test with threshold 1.0 (should include none)
        hash_mapping = {Safe_Str__Hash("abc1234567"): "Test"}

        request = Schema__Classification__Filter_Request(
            hash_mapping            = hash_mapping                                      ,
            classification_criteria = Enum__Text__Classification__Criteria.POSITIVE    ,
            filter_mode             = Enum__Classification__Filter_Mode.ABOVE          ,
            threshold               = Safe_Float(1.0)                                  ,
            output_mode             = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.engine_mode__filter(self.engine_mode, request)

        assert response.success        is True
        assert response.filtered_count == 0

    def test__engine_mode__filter__multiple_hashes(self):                      # Test with multiple hashes - deterministic
        hash_mapping = {Safe_Str__Hash(f"a{i:09d}"): f"Text {i}" for i in range(20)}

        request = Schema__Classification__Filter_Request(
            hash_mapping            = hash_mapping                                      ,
            classification_criteria = Enum__Text__Classification__Criteria.POSITIVE    ,
            filter_mode             = Enum__Classification__Filter_Mode.ABOVE          ,
            threshold               = Safe_Float(0.5)                                  ,
            output_mode             = Enum__Classification__Output_Mode.FULL_RATINGS
        )

        response = self.routes.engine_mode__filter(self.engine_mode, request)

        assert response.success      is True
        assert response.total_hashes == 20

        # With deterministic hash engine, we get consistent results
        assert response.filtered_count > 0
        assert response.filtered_count < 20