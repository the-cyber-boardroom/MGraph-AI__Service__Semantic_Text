from unittest                                                                                                       import TestCase
from osbot_utils.testing.__                                                                                         import __
from osbot_utils.type_safe.primitives.core.Safe_Float                                                               import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                                  import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria                             import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Engine_Mode                          import Enum__Text__Classification__Engine_Mode
from mgraph_ai_service_semantic_text.schemas.safe_float.Safe_Float__Text__Classification                            import Safe_Float__Text__Classification
from mgraph_ai_service_semantic_text.service.semantic_text.classification.Classification__Filter__Service           import Classification__Filter__Service
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Request          import Schema__Classification__Multi_Criteria_Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Response         import Schema__Classification__Multi_Criteria_Response
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Filter_Request   import Schema__Classification__Multi_Criteria_Filter_Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Criterion_Filter                import Schema__Classification__Criterion_Filter
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode                 import Enum__Classification__Filter_Mode
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Logic_Operator              import Enum__Classification__Logic_Operator
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode                 import Enum__Classification__Output_Mode


class test_Classification__Filter__Service__level_2(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.classification_service   = Classification__Filter__Service()
        cls.engine_mode               = Enum__Text__Classification__Engine_Mode.TEXT_HASH    # Use hash-based engine for deterministic tests

    def test__init(self):
        with self.classification_service as _:
            assert type(_)                    is Classification__Filter__Service

    # ========================================
    # classify_all__multi_criteria Tests
    # ========================================

    def test__classify_all__multi_criteria__basic(self):                       # Test basic multi-criteria classification
        # From reference: Hello World → pos:0.6158, neg:0.0609, neutral:0.2945, mixed:0.0289
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        request = Schema__Classification__Multi_Criteria_Request(hash_mapping = hash_mapping)   # No classification_criteria field anymore!

        response = self.classification_service.classify_all__multi_criteria(request            ,
                                                                           engine_mode=self.engine_mode)    # Add engine_mode parameter

        assert type(response) is Schema__Classification__Multi_Criteria_Response
        assert response.success is True
        assert response.total_hashes == 1
        assert len(response.hash_ratings) == 1

        ratings = response.hash_ratings[Safe_Str__Hash("b10a8db164")]
        assert Enum__Text__Classification__Criteria.POSITIVE in ratings
        assert Enum__Text__Classification__Criteria.NEGATIVE in ratings
        assert Enum__Text__Classification__Criteria.NEUTRAL  in ratings
        assert Enum__Text__Classification__Criteria.MIXED    in ratings

        # Use reference values from test_Semantic_Text__Engine__Hash_Based__rating_reference.py
        assert float(ratings[Enum__Text__Classification__Criteria.POSITIVE]) == 0.61575136853258
        assert float(ratings[Enum__Text__Classification__Criteria.NEGATIVE]) == 0.06092177291188416
        assert float(ratings[Enum__Text__Classification__Criteria.NEUTRAL])  == 0.2944552357407734
        assert float(ratings[Enum__Text__Classification__Criteria.MIXED])    == 0.028871622814762493

        assert ratings.obj() == __(positive = 0.61575136853258       ,
                                   negative = 0.06092177291188416    ,
                                   neutral  = 0.2944552357407734     ,
                                   mixed    = 0.028871622814762493   )

        assert response.obj() == __(hash_ratings = __(b10a8db164 = __( positive = 0.61575136853258     ,
                                                                       negative = 0.06092177291188416  ,
                                                                       neutral  = 0.2944552357407734   ,
                                                                       mixed    = 0.028871622814762493)) ,
                                    total_hashes = 1                                                      ,
                                    success      = True                                                   )


    def test__classify_all__multi_criteria__empty(self):                       # Test with empty mapping
        request = Schema__Classification__Multi_Criteria_Request(hash_mapping = {})

        response = self.classification_service.classify_all__multi_criteria(request            ,
                                                                           engine_mode=self.engine_mode)

        assert response.success is True
        assert response.total_hashes == 0
        assert response.hash_ratings == {}

    def test__classify_all__multi_criteria__single_criterion(self):            # Test classification returns all 4 criteria
        # From reference: Test → positive:0.4257, negative:0.1060, neutral:0.2211, mixed:0.2472
        hash_mapping = {Safe_Str__Hash("0cbc6611f5"): "Test"}

        request = Schema__Classification__Multi_Criteria_Request(hash_mapping = hash_mapping)

        response = self.classification_service.classify_all__multi_criteria(request            ,
                                                                           engine_mode=self.engine_mode)

        assert response.success is True
        assert response.total_hashes == 1
        assert len(response.hash_ratings) == 1

        ratings = response.hash_ratings[Safe_Str__Hash("0cbc6611f5")]
        assert len(ratings) == 4                                               # Always returns ALL 4 criteria
        assert float(ratings[Enum__Text__Classification__Criteria.POSITIVE]) == 0.4257015636325981
        assert float(ratings[Enum__Text__Classification__Criteria.NEGATIVE]) == 0.10598529564046806
        assert float(ratings[Enum__Text__Classification__Criteria.NEUTRAL])  == 0.22108315211763488
        assert float(ratings[Enum__Text__Classification__Criteria.MIXED])    == 0.24722998860929896

        assert response.obj() == __(hash_ratings = __(_0cbc6611f5 = __(positive = 0.4257015636325981  ,
                                                                       negative = 0.10598529564046806 ,
                                                                       neutral  = 0.22108315211763488 ,
                                                                       mixed    = 0.24722998860929896))  ,
                                    total_hashes = 1                                                      ,
                                    success      = True                                                   )


    def test__classify_all__multi_criteria__all_criteria(self):                # Test with all 4 criteria returned automatically
        # From reference: Sample text → pos:0.0526, neg:0.4057, neutral:0.3872, mixed:0.1545
        hash_mapping = {Safe_Str__Hash("1ba249ca59"): "Sample text"}
        request      = Schema__Classification__Multi_Criteria_Request(hash_mapping = hash_mapping)
        response     = self.classification_service.classify_all__multi_criteria(request            ,
                                                                                engine_mode=self.engine_mode)
        ratings      = response.hash_ratings[Safe_Str__Hash("1ba249ca59")]

        assert response.success                                                 is True
        assert len(response.hash_ratings)                                       == 1
        assert len(ratings)                                                     == 4
        assert float(ratings[Enum__Text__Classification__Criteria.POSITIVE])  == 0.05257312106627175
        assert float(ratings[Enum__Text__Classification__Criteria.NEGATIVE])  == 0.4057293594964828
        assert float(ratings[Enum__Text__Classification__Criteria.NEUTRAL])   == 0.3871714179933358
        assert float(ratings[Enum__Text__Classification__Criteria.MIXED])     == 0.15452610144390966

        assert request.obj()  == __(hash_mapping = __(_1ba249ca59 = 'Sample text'))

        assert response.obj() == __(hash_ratings = __(_1ba249ca59 = __(positive = 0.05257312106627175 ,
                                                                       negative = 0.4057293594964828   ,
                                                                       neutral  = 0.3871714179933358   ,
                                                                       mixed    = 0.15452610144390966)) ,
                                    total_hashes = 1                                                     ,
                                    success      = True                                                  )


    def test__classify_all__multi_criteria__multiple_hashes(self):             # Test with multiple hashes
        # From reference:
        # Hello World → pos:0.6158, neg:0.0609, neutral:0.2945, mixed:0.0289
        # Test Text   → pos:0.2842, neg:0.2529, neutral:0.1381, mixed:0.3248
        hash_mapping = { Safe_Str__Hash("b10a8db164"): "Hello World",
                         Safe_Str__Hash("f1feeaa3d6"): "Test Text"  }

        request = Schema__Classification__Multi_Criteria_Request(hash_mapping = hash_mapping)

        response = self.classification_service.classify_all__multi_criteria(request            ,
                                                                           engine_mode=self.engine_mode)

        assert response.success is True
        assert response.total_hashes == 2
        assert len(response.hash_ratings) == 2

        # Check Hello World ratings
        ratings1 = response.hash_ratings[Safe_Str__Hash("b10a8db164")]
        assert float(ratings1[Enum__Text__Classification__Criteria.POSITIVE]) == 0.61575136853258
        assert float(ratings1[Enum__Text__Classification__Criteria.NEGATIVE]) == 0.06092177291188416

        # Check Test Text ratings
        ratings2 = response.hash_ratings[Safe_Str__Hash("f1feeaa3d6")]
        assert float(ratings2[Enum__Text__Classification__Criteria.POSITIVE]) == 0.2842339724966105
        assert float(ratings2[Enum__Text__Classification__Criteria.NEGATIVE]) == 0.25290528762347475

    # ========================================
    # filter_by_multi_criteria Tests
    # ========================================

    def test__filter_by_multi_criteria__basic_and(self):                       # Test basic AND filtering
        # From reference: Positive text → pos:0.4119, neg:0.3534
        hash_mapping = {Safe_Str__Hash("b5ead10d6e"): "Positive text"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                                                     filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                                                     threshold   = Safe_Float(0.3)),
            Schema__Classification__Criterion_Filter(criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                                                     filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                                                     threshold   = Safe_Float(0.2) )]

        request = Schema__Classification__Multi_Criteria_Filter_Request(hash_mapping      = hash_mapping,
                                                                        criterion_filters = criterion_filters,
                                                                        logic_operator    = Enum__Classification__Logic_Operator.AND,
                                                                        output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY)

        response = self.classification_service.filter_by_multi_criteria(request     = request         ,
                                                                        engine_mode = self.engine_mode)

        # pos=0.4119 > 0.3 ✓, neg=0.3534 > 0.2 ✓ → MATCH
        assert response.success                 is True
        assert response.filtered_count          == 1
        assert len(response.filtered_hashes)    == 1
        assert Safe_Str__Hash("b5ead10d6e")     in response.filtered_hashes




    def test__filter_by_multi_criteria__basic_or(self):                        # Test basic OR filtering
        # From reference: Another text → pos:0.2144, neg:0.1033
        hash_mapping = {Safe_Str__Hash("9204d57da8"): "Another text"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.2)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.5)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping,
            criterion_filters = criterion_filters,
            logic_operator    = Enum__Classification__Logic_Operator.OR,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.classification_service.filter_by_multi_criteria(request            ,
                                                                       engine_mode=self.engine_mode)

        # pos=0.2144 > 0.2 ✓ OR neg=0.1033 > 0.5? NO → MATCH (because of OR)
        assert response.success is True
        assert response.filtered_count == 1

    def test__filter_by_multi_criteria__output_modes(self):                    # Test different output modes
        # From reference: Sample → pos:0.2659, neg:0.2127
        hash_mapping = {Safe_Str__Hash("c5dd1b2697"): "Sample"}

        criterion_filters = [Schema__Classification__Criterion_Filter(
            criterion   = Enum__Text__Classification__Criteria.POSITIVE,
            filter_mode = Enum__Classification__Filter_Mode.ABOVE,
            threshold   = Safe_Float(0.2)
        )]

        # Test HASHES_ONLY
        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping,
            criterion_filters = criterion_filters,
            logic_operator    = Enum__Classification__Logic_Operator.AND,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )
        response = self.classification_service.filter_by_multi_criteria(request            ,
                                                                       engine_mode=self.engine_mode)
        assert response.filtered_with_text    == {}
        assert response.filtered_with_ratings == {}

        # Test HASHES_WITH_TEXT
        request.output_mode = Enum__Classification__Output_Mode.HASHES_WITH_TEXT
        response = self.classification_service.filter_by_multi_criteria(request            ,
                                                                       engine_mode=self.engine_mode)
        assert response.filtered_with_text    is not None
        assert Safe_Str__Hash("c5dd1b2697")   in response.filtered_with_text
        assert response.filtered_with_ratings == {}

        # Test FULL_RATINGS
        request.output_mode = Enum__Classification__Output_Mode.FULL_RATINGS
        response = self.classification_service.filter_by_multi_criteria(request            ,
                                                                       engine_mode=self.engine_mode)
        assert response.filtered_with_text is not None
        assert response.filtered_with_ratings is not None
        assert Safe_Str__Hash("c5dd1b2697") in response.filtered_with_ratings

    # ========================================
    # _apply_multi_criteria_filter Tests
    # ========================================

    def test___apply_and_filter__all_match(self):                              # Test AND filter when all criteria match
        # From reference: Positive text → pos:0.4119, neg:0.3534
        hash_ratings = {
            Safe_Str__Hash("b5ead10d6e"): {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.41187280964184975),
                Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.3533635353449013)
            }
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.3)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.3)
            )
        ]

        filtered = self.classification_service._apply_and_filter(hash_ratings, criterion_filters)

        # pos=0.4119 > 0.3 ✓, neg=0.3534 > 0.3 ✓ → MATCH
        assert len(filtered) == 1
        assert Safe_Str__Hash("b5ead10d6e") in filtered

    def test___apply_and_filter__no_match(self):                               # Test AND filter when one criterion fails
        # From reference: High negative → pos:0.3065, neg:0.3427
        hash_ratings = {
            Safe_Str__Hash("58537f27d7"): {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.3065187764990915),
                Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.3426711084191399)
            }
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.5)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.3)
            )
        ]

        filtered = self.classification_service._apply_and_filter(hash_ratings, criterion_filters)

        # pos=0.3065 > 0.5? NO → NO MATCH (AND requires all)
        assert len(filtered) == 0

    def test___apply_and_filter__partial_match(self):                          # Test AND filter with partial match
        # From reference: Test content → pos:0.0524, neg:0.5133
        hash_ratings = {
            Safe_Str__Hash("8bfa8e0684"): {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.052423063318004955),
                Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.5133356915458083),
                Enum__Text__Classification__Criteria.NEUTRAL:  Safe_Float__Text__Classification(0.21995047753802618)
            }
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.BELOW,
                threshold   = Safe_Float(0.1)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.5)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEUTRAL,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.2)
            )
        ]

        filtered = self.classification_service._apply_and_filter(hash_ratings, criterion_filters)

        # pos=0.0524 < 0.1 ✓, neg=0.5133 > 0.5 ✓, neutral=0.2200 > 0.2 ✓ → MATCH
        assert len(filtered) == 1

    def test___apply_or_filter__any_match(self):                               # Test OR filter when any criterion matches
        # From reference: Text A → pos:0.3969, neg:0.3216
        hash_ratings = {
            Safe_Str__Hash("b840f6f2ae"): {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.3969413061449435),
                Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.32162211812253144)
            }
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.7)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.3)
            )
        ]

        filtered = self.classification_service._apply_or_filter(hash_ratings, criterion_filters)

        # pos=0.3969 > 0.7? NO, neg=0.3216 > 0.3 ✓ → MATCH (OR needs any)
        assert len(filtered) == 1

    def test___apply_or_filter__no_match(self):                                # Test OR filter when no criteria match
        # From reference: High negative → pos:0.3065, neg:0.3427
        hash_ratings = {
            Safe_Str__Hash("58537f27d7"): {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.3065187764990915),
                Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.3426711084191399)
            }
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.7)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.7)
            )
        ]

        filtered = self.classification_service._apply_or_filter(hash_ratings, criterion_filters)

        # pos=0.3065 > 0.7? NO, neg=0.3427 > 0.7? NO → NO MATCH
        assert len(filtered) == 0

    # ========================================
    # _check_filter_match Tests
    # ========================================

    def test___check_filter_match__above(self):                                # Test ABOVE filter mode
        assert self.classification_service._check_filter_match(
            rating_value  = 0.8,
            filter_mode   = Enum__Classification__Filter_Mode.ABOVE,
            threshold     = 0.5
        ) is True

        assert self.classification_service._check_filter_match(
            rating_value  = 0.3,
            filter_mode   = Enum__Classification__Filter_Mode.ABOVE,
            threshold     = 0.5
        ) is False

    def test___check_filter_match__below(self):                                # Test BELOW filter mode
        assert self.classification_service._check_filter_match(
            rating_value  = 0.3,
            filter_mode   = Enum__Classification__Filter_Mode.BELOW,
            threshold     = 0.5
        ) is True

        assert self.classification_service._check_filter_match(
            rating_value  = 0.8,
            filter_mode   = Enum__Classification__Filter_Mode.BELOW,
            threshold     = 0.5
        ) is False

    def test___check_filter_match__equals(self):                               # Test EQUALS filter mode
        assert self.classification_service._check_filter_match(
            rating_value  = 0.5,
            filter_mode   = Enum__Classification__Filter_Mode.EQUALS,
            threshold     = 0.5
        ) is True

        assert self.classification_service._check_filter_match(
            rating_value  = 0.5001,
            filter_mode   = Enum__Classification__Filter_Mode.EQUALS,
            threshold     = 0.5
        ) is True  # Within 0.001 tolerance

        assert self.classification_service._check_filter_match(
            rating_value  = 0.51,
            filter_mode   = Enum__Classification__Filter_Mode.EQUALS,
            threshold     = 0.5
        ) is False

    def test___check_filter_match__between(self):                              # Test BETWEEN filter mode
        assert self.classification_service._check_filter_match(
            rating_value  = 0.6,
            filter_mode   = Enum__Classification__Filter_Mode.BETWEEN,
            threshold     = 0.5,
            threshold_max = 0.7
        ) is True

        assert self.classification_service._check_filter_match(
            rating_value  = 0.5,
            filter_mode   = Enum__Classification__Filter_Mode.BETWEEN,
            threshold     = 0.5,
            threshold_max = 0.7
        ) is False  # Not strictly between

        assert self.classification_service._check_filter_match(
            rating_value  = 0.7,
            filter_mode   = Enum__Classification__Filter_Mode.BETWEEN,
            threshold     = 0.5,
            threshold_max = 0.7
        ) is False  # Not strictly between

        assert self.classification_service._check_filter_match(
            rating_value  = 0.8,
            filter_mode   = Enum__Classification__Filter_Mode.BETWEEN,
            threshold     = 0.5,
            threshold_max = 0.7
        ) is False

    # ========================================
    # Edge Cases
    # ========================================

    def test__filter_by_multi_criteria__empty_mapping(self):                   # Test with empty hash mapping
        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = {},
            criterion_filters = [Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.5)
            )],
            logic_operator    = Enum__Classification__Logic_Operator.AND,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.classification_service.filter_by_multi_criteria(request            ,
                                                                       engine_mode=self.engine_mode)

        assert response.success is True
        assert response.total_hashes == 0
        assert response.filtered_count == 0

    def test__filter_by_multi_criteria__three_criteria_and(self):              # Test AND logic with three criteria
        # From reference: Balanced text → pos:0.1193, neg:0.4300, neutral:0.4421
        hash_mapping = {Safe_Str__Hash("c298542a7f"): "Balanced text"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.1)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.4)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEUTRAL,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.4)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping,
            criterion_filters = criterion_filters,
            logic_operator    = Enum__Classification__Logic_Operator.AND,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.classification_service.filter_by_multi_criteria(request            ,
                                                                       engine_mode=self.engine_mode)

        # All three: pos=0.1193 > 0.1 ✓, neg=0.4300 > 0.4 ✓, neutral=0.4421 > 0.4 ✓
        assert response.success is True
        assert response.filtered_count == 1