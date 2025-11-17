from unittest                                                                                                        import TestCase
from fastapi                                                                                                         import FastAPI
from osbot_utils.testing.__                                                                                          import __
from osbot_utils.type_safe.primitives.core.Safe_Float                                                                import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                                   import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Response          import Schema__Classification__Multi_Criteria_Response
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria                              import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Engine_Mode                           import Enum__Text__Classification__Engine_Mode
from mgraph_ai_service_semantic_text.fast_api.routes.Routes__Semantic_Classification                                 import Routes__Semantic_Classification
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Request           import Schema__Classification__Multi_Criteria_Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Filter_Request    import Schema__Classification__Multi_Criteria_Filter_Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Criterion_Filter                 import Schema__Classification__Criterion_Filter
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode                  import Enum__Classification__Output_Mode
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode                  import Enum__Classification__Filter_Mode
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Logic_Operator               import Enum__Classification__Logic_Operator


class test_Routes__Semantic_Classification__level_2(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app         = FastAPI()
        cls.routes      = Routes__Semantic_Classification(app=cls.app).setup()
        cls.engine_mode = Enum__Text__Classification__Engine_Mode.TEXT_HASH

    def test__setUpClass(self):
        with self.routes as _:
            assert type(_)          is Routes__Semantic_Classification
            assert _.routes_paths() == ['/{engine_mode}/filter'      ,
                                        '/{engine_mode}/multi/filter',
                                        '/{engine_mode}/multi/rate'  ,
                                        '/{engine_mode}/rate'        ]
            assert _.tag            == 'semantic-classification'

    # ========================================
    # engine_mode__multi__rate Tests
    # ========================================

    def test__engine_mode__multi__rate__basic(self):                           # Test basic multi-criteria rating (always returns all 4)
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World",
                        Safe_Str__Hash("f1feeaa3d6"): "Test Text"}

        request = Schema__Classification__Multi_Criteria_Request(hash_mapping = hash_mapping)

        response = self.routes.engine_mode__multi__rate(self.engine_mode, request)

        assert type(response)         is Schema__Classification__Multi_Criteria_Response
        assert response.success       is True
        assert response.total_hashes  == 2
        assert len(response.hash_ratings) == 2

        # Now always returns all 4 criteria
        assert response.obj() == __(hash_ratings = __(b10a8db164 = __(positive = 0.61575136853258     ,
                                                                      negative = 0.06092177291188416  ,
                                                                      neutral  = 0.2944552357407734   ,
                                                                      mixed    = 0.028871622814762493 ),
                                                      f1feeaa3d6 = __(positive = 0.2842339724966105   ,
                                                                      negative = 0.25290528762347475  ,
                                                                      neutral  = 0.1380980050358319   ,
                                                                      mixed    = 0.3247627348440829   )),
                                    total_hashes = 2   ,
                                    success      = True)

    def test__engine_mode__multi__rate__empty(self):                           # Test with empty mapping
        request = Schema__Classification__Multi_Criteria_Request(hash_mapping = {})

        response = self.routes.engine_mode__multi__rate(self.engine_mode, request)

        assert response.success      is True
        assert response.total_hashes == 0
        assert response.hash_ratings == {}

    def test__engine_mode__multi__rate__single_hash(self):                     # Test with single hash (returns all 4 criteria)
        hash_mapping = {Safe_Str__Hash("0cbc6611f5"): "Test"}
        request      = Schema__Classification__Multi_Criteria_Request(hash_mapping = hash_mapping)
        response     = self.routes.engine_mode__multi__rate(self.engine_mode, request)

        assert response.total_hashes      == 1
        assert len(response.hash_ratings) == 1

        # All 4 criteria returned
        ratings = response.hash_ratings[Safe_Str__Hash("0cbc6611f5")]
        assert len(ratings) == 4
        assert response.obj() == __(hash_ratings = __(_0cbc6611f5 = __(positive = 0.4257015636325981  ,
                                                                       negative = 0.10598529564046806 ,
                                                                       neutral  = 0.22108315211763488 ,
                                                                       mixed    = 0.24722998860929896 )),
                                    total_hashes = 1   ,
                                    success      = True)

    def test__engine_mode__multi__rate__all_criteria(self):                    # Test that all 4 criteria are automatically returned
        hash_mapping = {Safe_Str__Hash("1ba249ca59"): "Sample text"}

        request  = Schema__Classification__Multi_Criteria_Request(hash_mapping = hash_mapping)
        response = self.routes.engine_mode__multi__rate(self.engine_mode, request)

        assert response.success           is True
        assert response.total_hashes      == 1
        assert len(response.hash_ratings) == 1

        # All 4 criteria are present
        ratings = response.hash_ratings[Safe_Str__Hash("1ba249ca59")]
        assert Enum__Text__Classification__Criteria.POSITIVE in ratings
        assert Enum__Text__Classification__Criteria.NEGATIVE in ratings
        assert Enum__Text__Classification__Criteria.NEUTRAL in ratings
        assert Enum__Text__Classification__Criteria.MIXED in ratings

        # From reference: Sample text → pos:0.0526, neg:0.4057, neutral:0.3872, mixed:0.1545
        assert ratings.obj() == __(positive = 0.05257312106627175 ,
                                   negative = 0.4057293594964828  ,
                                   neutral  = 0.3871714179933358  ,
                                   mixed    = 0.15452610144390966 )

    # ========================================
    # engine_mode__multi__filter Tests - AND Logic
    # ========================================

    def test__engine_mode__multi__filter__and__basic(self):                    # Test AND logic with 2 criteria
        hash_mapping = {Safe_Str__Hash("b5ead10d6e"): "Positive text",
                        Safe_Str__Hash("9204d57da8"): "Another text"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.3)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.2)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                      ,
            criterion_filters = criterion_filters                                ,
            logic_operator    = Enum__Classification__Logic_Operator.AND         ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.engine_mode__multi__filter(self.engine_mode, request)

        assert response.success        is True
        assert response.logic_operator == Enum__Classification__Logic_Operator.AND
        assert response.total_hashes   == 2

    def test__engine_mode__multi__filter__and__both_match(self):               # Test AND logic where both criteria match
        hash_mapping = {Safe_Str__Hash("b5ead10d6e"): "Positive text"}  # pos:0.4119, neg:0.3534

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.3)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.3)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                      ,
            criterion_filters = criterion_filters                                ,
            logic_operator    = Enum__Classification__Logic_Operator.AND         ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.engine_mode__multi__filter(self.engine_mode, request)

        # pos=0.4119 > 0.3 ✓, neg=0.3534 > 0.3 ✓ → MATCH
        assert response.success            is True
        assert response.filtered_count     == 1
        assert response.filtered_hashes    == [Safe_Str__Hash("b5ead10d6e")]

    def test__engine_mode__multi__filter__and__with_text(self):                # Test AND logic with text output
        hash_mapping = {Safe_Str__Hash("8bfa8e0684"): "Test content"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.5)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEUTRAL ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.2)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                        ,
            criterion_filters = criterion_filters                                  ,
            logic_operator    = Enum__Classification__Logic_Operator.AND           ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_WITH_TEXT
        )

        response = self.routes.engine_mode__multi__filter(self.engine_mode, request)

        assert response.success            is True
        assert response.filtered_count     == 1
        assert response.filtered_with_text is not None
        assert Safe_Str__Hash("8bfa8e0684") in response.filtered_with_text

    def test__engine_mode__multi__filter__and__full_ratings(self):             # Test AND logic with full ratings output
        hash_mapping = {Safe_Str__Hash("b5ead10d6e"): "Positive text"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.3)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.3)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                      ,
            criterion_filters = criterion_filters                                ,
            logic_operator    = Enum__Classification__Logic_Operator.AND         ,
            output_mode       = Enum__Classification__Output_Mode.FULL_RATINGS
        )

        response = self.routes.engine_mode__multi__filter(self.engine_mode, request)

        assert response.success               is True
        assert response.filtered_count        == 1
        assert response.filtered_with_ratings is not None

        # Full ratings include all 4 criteria
        ratings = response.filtered_with_ratings[Safe_Str__Hash("b5ead10d6e")]
        assert len(ratings) == 4

    # ========================================
    # engine_mode__multi__filter Tests - OR Logic
    # ========================================

    def test__engine_mode__multi__filter__or__any_match(self):                 # Test OR logic where any criterion matches
        hash_mapping = {Safe_Str__Hash("b840f6f2ae"): "Text A"}  # pos:0.3969, neg:0.3216

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.7)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.3)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                      ,
            criterion_filters = criterion_filters                                ,
            logic_operator    = Enum__Classification__Logic_Operator.OR          ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.engine_mode__multi__filter(self.engine_mode, request)

        # pos=0.3969 > 0.7? NO, neg=0.3216 > 0.3 ✓ → MATCH (OR needs any)
        assert response.success        is True
        assert response.filtered_count == 1

    def test__engine_mode__multi__filter__or__no_match(self):                  # Test OR logic when no criteria match
        hash_mapping = {Safe_Str__Hash("58537f27d7"): "High negative"}  # pos:0.3065, neg:0.3427

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.7)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.7)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                      ,
            criterion_filters = criterion_filters                                ,
            logic_operator    = Enum__Classification__Logic_Operator.OR          ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.engine_mode__multi__filter(self.engine_mode, request)

        # pos=0.3065 > 0.7? NO, neg=0.3427 > 0.7? NO → NO MATCH
        assert response.success        is True
        assert response.filtered_count == 0

    # ========================================
    # Edge Cases
    # ========================================

    def test__engine_mode__multi__filter__empty_mapping(self):                 # Test with empty hash mapping
        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = {}                                                   ,
            criterion_filters = [Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.5)
            )],
            logic_operator    = Enum__Classification__Logic_Operator.AND            ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.engine_mode__multi__filter(self.engine_mode, request)

        assert response.success         is True
        assert response.total_hashes    == 0
        assert response.filtered_count  == 0

    def test__engine_mode__multi__filter__three_criteria_and(self):            # Test AND logic with three criteria
        hash_mapping = {Safe_Str__Hash("c298542a7f"): "Balanced text"}  # pos:0.1193, neg:0.4300, neutral:0.4421

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.1)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.4)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEUTRAL ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                threshold   = Safe_Float(0.4)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                      ,
            criterion_filters = criterion_filters                                ,
            logic_operator    = Enum__Classification__Logic_Operator.AND         ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.engine_mode__multi__filter(self.engine_mode, request)

        # All three: pos=0.1193 > 0.1 ✓, neg=0.4300 > 0.4 ✓, neutral=0.4421 > 0.4 ✓
        assert response.success        is True
        assert response.filtered_count == 1

    def test__engine_mode__multi__filter__multiple_output_modes(self):         # Test different output modes
        hash_mapping = {Safe_Str__Hash("c5dd1b2697"): "Sample"}

        criterion_filters = [Schema__Classification__Criterion_Filter(criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                                                                      filter_mode = Enum__Classification__Filter_Mode.ABOVE      ,
                                                                      threshold   = Safe_Float(0.2))]

        # Test HASHES_ONLY
        request_hashes = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                      ,
            criterion_filters = criterion_filters                                ,
            logic_operator    = Enum__Classification__Logic_Operator.AND         ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )
        response_hashes = self.routes.engine_mode__multi__filter(self.engine_mode, request_hashes)
        assert response_hashes.filtered_with_text    == {}
        assert response_hashes.filtered_with_ratings == {}

        # Test HASHES_WITH_TEXT
        request_text = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                        ,
            criterion_filters = criterion_filters                                  ,
            logic_operator    = Enum__Classification__Logic_Operator.AND           ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_WITH_TEXT
        )
        response_text = self.routes.engine_mode__multi__filter(self.engine_mode, request_text)
        assert response_text.filtered_with_text    is not None
        assert response_text.filtered_with_ratings == {}

        # Test FULL_RATINGS
        request_full = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                      ,
            criterion_filters = criterion_filters                                ,
            logic_operator    = Enum__Classification__Logic_Operator.AND         ,
            output_mode       = Enum__Classification__Output_Mode.FULL_RATINGS
        )
        response_full = self.routes.engine_mode__multi__filter(self.engine_mode, request_full)
        assert response_full.filtered_with_text     is not None
        assert response_full.filtered_with_ratings  is not None