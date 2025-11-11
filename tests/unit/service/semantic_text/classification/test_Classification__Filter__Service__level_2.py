from unittest                                                                                                       import TestCase
from osbot_utils.testing.__                                                                                         import __
from osbot_utils.type_safe.primitives.core.Safe_Float                                                               import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                                  import Safe_Str__Hash
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Criteria                     import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.service.schemas.safe_float.Safe_Float__Text__Classification                    import Safe_Float__Text__Classification
from mgraph_ai_service_semantic_text.service.semantic_text.Semantic_Text__Service                                   import Semantic_Text__Service
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
        cls.semantic_text_service    = Semantic_Text__Service().setup()
        cls.classification_service   = Classification__Filter__Service(semantic_text_service=cls.semantic_text_service)

    def test__init(self):
        with self.classification_service as _:
            assert type(_)                    is Classification__Filter__Service
            assert type(_.semantic_text_service) is Semantic_Text__Service

    # ========================================
    # classify_all__multi_criteria Tests
    # ========================================

    def test__classify_all__multi_criteria__basic(self):                       # Test basic multi-criteria classification
        # From reference: Hello World → pos:0.7478, neg:0.1102, bias:0.2316
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        request = Schema__Classification__Multi_Criteria_Request(
            hash_mapping            = hash_mapping,
            classification_criteria = [Enum__Text__Classification__Criteria.POSITIVITY,
                                       Enum__Text__Classification__Criteria.NEGATIVITY,
                                       Enum__Text__Classification__Criteria.BIAS]
        )

        response = self.classification_service.classify_all__multi_criteria(request)

        assert type(response) is Schema__Classification__Multi_Criteria_Response
        assert response.success is True
        assert response.total_hashes == 1
        assert len(response.hash_ratings) == 1

        ratings = response.hash_ratings[Safe_Str__Hash("b10a8db164")]
        assert Enum__Text__Classification__Criteria.POSITIVITY in ratings
        assert Enum__Text__Classification__Criteria.NEGATIVITY in ratings
        assert Enum__Text__Classification__Criteria.BIAS in ratings

        assert float(ratings[Enum__Text__Classification__Criteria.POSITIVITY]) == 0.7478
        assert float(ratings[Enum__Text__Classification__Criteria.NEGATIVITY]) == 0.1102
        assert float(ratings[Enum__Text__Classification__Criteria.BIAS]) == 0.2316

        assert ratings.obj() == __(positivity = 0.7478,
                                   negativity = 0.1102,
                                   bias       = 0.2316)

        assert response.obj() == __(hash_ratings             = __(b10a8db164 = __( positivity = 0.7478 ,
                                                                                   negativity = 0.1102 ,
                                                                                   bias       = 0.2316)) ,
                                       classification_criteria  = ['positivity', 'negativity', 'bias']   ,
                                       total_hashes             = 1                                       ,
                                       success                  = True                                    )


    def test__classify_all__multi_criteria__empty(self):                       # Test with empty mapping
        request = Schema__Classification__Multi_Criteria_Request(
            hash_mapping            = {},
            classification_criteria = [Enum__Text__Classification__Criteria.POSITIVITY]
        )

        response = self.classification_service.classify_all__multi_criteria(request)

        assert response.success is True
        assert response.total_hashes == 0
        assert response.hash_ratings == {}

    def test__classify_all__multi_criteria__single_criterion(self):            # Test with single criterion
        # From reference: Test → urgency:0.7786
        hash_mapping = {Safe_Str__Hash("0cbc6611f5"): "Test"}

        request = Schema__Classification__Multi_Criteria_Request(
            hash_mapping            = hash_mapping,
            classification_criteria = [Enum__Text__Classification__Criteria.URGENCY]
        )

        response = self.classification_service.classify_all__multi_criteria(request)

        assert response.success is True
        assert response.total_hashes == 1
        assert len(response.hash_ratings) == 1

        ratings = response.hash_ratings[Safe_Str__Hash("0cbc6611f5")]
        assert len(ratings) == 1
        assert float(ratings[Enum__Text__Classification__Criteria.URGENCY]) == 0.7786

        assert response.obj() == __(hash_ratings             = __(_0cbc6611f5 = __(urgency = 0.7786))   ,
                                    classification_criteria  = ['urgency']                              ,
                                    total_hashes             = 1                                        ,
                                    success                  = True                                     )


    def test__classify_all__multi_criteria__all_criteria(self):                # Test with all 4 criteria

        hash_mapping = {Safe_Str__Hash("1ba249ca59"): "Sample text"}                    # From reference: Sample text → pos:0.9569, neg:0.1469, bias:0.2887, urg:0.7091
        request      = Schema__Classification__Multi_Criteria_Request(hash_mapping            = hash_mapping,
                                                                      classification_criteria = [Enum__Text__Classification__Criteria.POSITIVITY,
                                                                                                 Enum__Text__Classification__Criteria.NEGATIVITY,
                                                                                                 Enum__Text__Classification__Criteria.BIAS      ,                                                                                            Enum__Text__Classification__Criteria.URGENCY   ])
        response     = self.classification_service.classify_all__multi_criteria(request)
        ratings      = response.hash_ratings[Safe_Str__Hash("1ba249ca59")]

        assert response.success                                                is True
        assert len(response.hash_ratings)                                      == 1
        assert len(ratings)                                                    == 4
        assert float(ratings[Enum__Text__Classification__Criteria.POSITIVITY]) == 0.9569
        assert float(ratings[Enum__Text__Classification__Criteria.NEGATIVITY]) == 0.1469
        assert float(ratings[Enum__Text__Classification__Criteria.BIAS      ]) == 0.2887
        assert float(ratings[Enum__Text__Classification__Criteria.URGENCY   ]) == 0.7091

        assert request.obj()  == __(hash_mapping             = __(_1ba249ca59 = 'Sample text')                 ,
                                    classification_criteria  = ['positivity', 'negativity', 'bias', 'urgency'])

        assert response.obj() == __(hash_ratings             = __(_1ba249ca59 = __(positivity = 0.9569 ,
                                                                                   negativity = 0.1469 ,
                                                                                   bias       = 0.2887 ,
                                                                                   urgency    = 0.7091)) ,
                                    classification_criteria  = ['positivity', 'negativity', 'bias', 'urgency'] ,
                                    total_hashes             = 1                                                ,
                                    success                  = True                                             )


    def test__classify_all__multi_criteria__multiple_hashes(self):             # Test with multiple hashes
        # From reference:
        # Hello World → pos:0.7478, neg:0.1102
        # Test Text   → pos:0.5080, neg:0.3946
        hash_mapping = { Safe_Str__Hash("b10a8db164"): "Hello World",
                         Safe_Str__Hash("f1feeaa3d6"): "Test Text"  }

        request = Schema__Classification__Multi_Criteria_Request(
            hash_mapping            = hash_mapping,
            classification_criteria = [Enum__Text__Classification__Criteria.POSITIVITY,
                                       Enum__Text__Classification__Criteria.NEGATIVITY]
        )

        response = self.classification_service.classify_all__multi_criteria(request)

        assert response.success is True
        assert response.total_hashes == 2
        assert len(response.hash_ratings) == 2

        assert response.obj() == __(hash_ratings=__(b10a8db164=__(positivity=0.7478, negativity=0.1102),
                                                    f1feeaa3d6=__(positivity=0.508 , negativity=0.3946)),
                                    classification_criteria=['positivity', 'negativity'],
                                    total_hashes=2,
                                    success=True)

    # ========================================
    # filter_by_multi_criteria Tests
    # ========================================

    def test__filter_by_multi_criteria__basic_and(self):                       # Test basic AND logic filtering

        hash_mapping = {Safe_Str__Hash("eb5deeca9c"): "Text B"}                 # From reference: Text B → pos:0.8374, neg:0.7441

        criterion_filters = [
            Schema__Classification__Criterion_Filter(criterion   = Enum__Text__Classification__Criteria.POSITIVITY ,
                                                     filter_mode = Enum__Classification__Filter_Mode.ABOVE         ,
                                                     threshold   = Safe_Float(0.7)                                 ),
            Schema__Classification__Criterion_Filter(criterion   = Enum__Text__Classification__Criteria.NEGATIVITY ,
                                                     filter_mode = Enum__Classification__Filter_Mode.ABOVE         ,
                                                     threshold   = Safe_Float(0.7)                                 )]

        request = Schema__Classification__Multi_Criteria_Filter_Request(hash_mapping      = hash_mapping                                 ,
                                                                        criterion_filters = criterion_filters                            ,
                                                                        logic_operator    = Enum__Classification__Logic_Operator.AND     ,
                                                                        output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY)

        response = self.classification_service.filter_by_multi_criteria(request)

        # Analysis: pos=0.8374 > 0.7 ✓, neg=0.7441 > 0.7 ✓ → MATCH
        assert response.success         is True
        assert response.filtered_count  == 1
        assert response.filtered_hashes == [Safe_Str__Hash("eb5deeca9c")]

        assert response.obj() == __(filtered_with_text       = None                                              ,
                                    filtered_with_ratings    = None                                              ,
                                    filtered_hashes          = ['eb5deeca9c']                                    ,
                                    criteria_used            = ['positivity', 'negativity']                     ,
                                    logic_operator           = 'and'                                             ,
                                    output_mode              = 'hashes-only'                                     ,
                                    total_hashes             = 1                                                 ,
                                    filtered_count           = 1                                                 ,
                                    success                  = True                                              )



    def test__filter_by_multi_criteria__basic_or(self):                        # Test basic OR logic filtering
        # From reference:
        # High positive → pos:0.5667, neg:0.6083
        # High negative → pos:0.5421, neg:0.7642
        hash_mapping = {Safe_Str__Hash("c3d45f8fe6") : "High positive" ,
                        Safe_Str__Hash("58537f27d7") : "High negative"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(criterion   = Enum__Text__Classification__Criteria.POSITIVITY ,
                                                     filter_mode = Enum__Classification__Filter_Mode.ABOVE         ,
                                                     threshold   = Safe_Float(0.7)                                  ),
            Schema__Classification__Criterion_Filter(criterion   = Enum__Text__Classification__Criteria.NEGATIVITY ,
                                                     filter_mode = Enum__Classification__Filter_Mode.ABOVE         ,
                                                     threshold   = Safe_Float(0.7)                                  )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(hash_mapping      = hash_mapping      ,
                                                                         criterion_filters = criterion_filters ,
                                                                         logic_operator    = Enum__Classification__Logic_Operator.OR ,
                                                                         output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY)

        response = self.classification_service.filter_by_multi_criteria(request)

        # Analysis (OR):
        # High positive: pos=0.5667 > 0.7? NO, neg=0.6083 > 0.7? NO → FAIL
        # High negative: pos=0.5421 > 0.7? NO, neg=0.7642 > 0.7? YES → MATCH
        assert response.success         is True
        assert response.filtered_count  == 1
        assert response.filtered_hashes == [Safe_Str__Hash("58537f27d7")]

        assert response.obj() == __(filtered_with_text       = None                                              ,
                                    filtered_with_ratings    = None                                              ,
                                    filtered_hashes          = ['58537f27d7']                                    ,
                                    criteria_used            = ['positivity', 'negativity']                     ,
                                    logic_operator           = 'or'                                              ,
                                    output_mode              = 'hashes-only'                                     ,
                                    total_hashes             = 2                                                 ,
                                    filtered_count           = 1                                                 ,
                                    success                  = True                                              )


    def test__filter_by_multi_criteria__output_modes(self):                    # Test different output modes
        # From reference: Text → pos:0.9776
        hash_mapping = {Safe_Str__Hash("9dffbf69ff") : "Text"}

        criterion_filters = [Schema__Classification__Criterion_Filter(criterion   = Enum__Text__Classification__Criteria.POSITIVITY ,
                                                                      filter_mode = Enum__Classification__Filter_Mode.ABOVE         ,
                                                                      threshold   = Safe_Float(0.5)                                  )]

        # Test HASHES_ONLY
        request_hashes = Schema__Classification__Multi_Criteria_Filter_Request(hash_mapping      = hash_mapping      ,
                                                                               criterion_filters = criterion_filters ,
                                                                               logic_operator    = Enum__Classification__Logic_Operator.AND ,
                                                                               output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY)

        response_hashes = self.classification_service.filter_by_multi_criteria(request_hashes)
        assert response_hashes.filtered_with_text    is None
        assert response_hashes.filtered_with_ratings is None

        # Test HASHES_WITH_TEXT
        request_text = Schema__Classification__Multi_Criteria_Filter_Request(hash_mapping      = hash_mapping      ,
                                                                              criterion_filters = criterion_filters ,
                                                                              logic_operator    = Enum__Classification__Logic_Operator.AND ,
                                                                              output_mode       = Enum__Classification__Output_Mode.HASHES_WITH_TEXT)

        response_text = self.classification_service.filter_by_multi_criteria(request_text)
        assert response_text.filtered_with_text                               is not None
        assert response_text.filtered_with_ratings                            is None
        assert response_text.filtered_with_text[Safe_Str__Hash("9dffbf69ff")] == "Text"

        # Test FULL_RATINGS
        request_full = Schema__Classification__Multi_Criteria_Filter_Request(hash_mapping      = hash_mapping      ,
                                                                             criterion_filters = criterion_filters ,
                                                                             logic_operator    = Enum__Classification__Logic_Operator.AND ,
                                                                             output_mode       = Enum__Classification__Output_Mode.FULL_RATINGS)

        response_full = self.classification_service.filter_by_multi_criteria(request_full)
        assert response_full.filtered_with_text    is not None
        assert response_full.filtered_with_ratings is not None
        assert float(response_full.filtered_with_ratings[Safe_Str__Hash("9dffbf69ff")]
                                                        [Enum__Text__Classification__Criteria.POSITIVITY]) == 0.9776

        assert request_text.obj() == __(output_mode        = 'hashes-with-text'                 ,
                                        hash_mapping        = __(_9dffbf69ff = 'Text')          ,
                                        criterion_filters   = [__(threshold_max = None          ,
                                                                 criterion      = 'positivity'  ,
                                                                 filter_mode    = 'above'       ,
                                                                 threshold      = 0.5)]         ,
                                        logic_operator      = 'and')

        assert response_text.obj() == __(filtered_with_text       = __(_9dffbf69ff = 'Text')      ,
                                         filtered_with_ratings    = None                          ,
                                         filtered_hashes          = ['9dffbf69ff']                ,
                                         criteria_used            = ['positivity']                ,
                                         logic_operator           = 'and'                         ,
                                         output_mode              = 'hashes-with-text'            ,
                                         total_hashes             = 1                             ,
                                         filtered_count           = 1                             ,
                                         success                  = True                          )

        assert request_full.obj() == __(output_mode        = 'full-ratings'                                   ,
                                       hash_mapping        = __(_9dffbf69ff = 'Text')                         ,
                                       criterion_filters   = [__(threshold_max = None                        ,
                                                                criterion      = 'positivity'               ,
                                                                filter_mode    = 'above'                    ,
                                                                threshold      = 0.5)]                       ,
                                       logic_operator      = 'and')

        assert response_full.obj() == __(filtered_with_text       = __(_9dffbf69ff = 'Text')                  ,
                                        filtered_with_ratings     = __(_9dffbf69ff = __(positivity = 0.9776)) ,
                                        filtered_hashes           = ['9dffbf69ff']                            ,
                                        criteria_used             = ['positivity']                           ,
                                        logic_operator            = 'and'                                     ,
                                        output_mode               = 'full-ratings'                            ,
                                        total_hashes              = 1                                         ,
                                        filtered_count            = 1                                         ,
                                        success                   = True                                      )



    # ========================================
    # _apply_and_filter Tests
    # ========================================


    def test___apply_and_filter__all_match(self):                              # Test AND filter where all hashes match all criteria
        # From reference: Text B → pos:0.8374, neg:0.7441
        hash_ratings = { Safe_Str__Hash("eb5deeca9c"): { Enum__Text__Classification__Criteria.POSITIVITY: Safe_Float__Text__Classification(0.8374),
                                                         Enum__Text__Classification__Criteria.NEGATIVITY: Safe_Float__Text__Classification(0.7441) } }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                                                     filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                                                     threshold   = Safe_Float(0.7)),
            Schema__Classification__Criterion_Filter(criterion   = Enum__Text__Classification__Criteria.NEGATIVITY,
                                                     filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                                                     threshold   = Safe_Float(0.7))]

        filtered = self.classification_service._apply_and_filter(hash_ratings, criterion_filters)

        assert len(filtered) == 1
        assert Safe_Str__Hash("eb5deeca9c") in filtered
        assert filtered == ['eb5deeca9c']

    def test___apply_and_filter__partial_match(self):                          # Test AND filter where hashes only partially match
        # From reference:
        # Text 0 → pos:0.7645, neg:0.7672 (both > 0.6)
        # Text 1 → pos:0.7402, neg:0.0745 (only pos > 0.6)
        hash_ratings = {
            Safe_Str__Hash("20c8b16b2a"): {
                Enum__Text__Classification__Criteria.POSITIVITY: Safe_Float__Text__Classification(0.7645),
                Enum__Text__Classification__Criteria.NEGATIVITY: Safe_Float__Text__Classification(0.7672)
            },
            Safe_Str__Hash("161a6b3572"): {
                Enum__Text__Classification__Criteria.POSITIVITY: Safe_Float__Text__Classification(0.7402),
                Enum__Text__Classification__Criteria.NEGATIVITY: Safe_Float__Text__Classification(0.0745)
            }
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.6)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.6)
            )
        ]

        filtered = self.classification_service._apply_and_filter(hash_ratings, criterion_filters)

        # Only Text 0 matches both conditions
        assert len(filtered) == 1
        assert Safe_Str__Hash("20c8b16b2a") in filtered

        #assert filtered == ['20c8b16b2a']

    def test___apply_and_filter__no_match(self):                               # Test AND filter where no hashes match all criteria
        # From reference: Positive text → pos:0.4332, neg:0.5403
        hash_ratings = {
            Safe_Str__Hash("b5ead10d6e"): {
                Enum__Text__Classification__Criteria.POSITIVITY: Safe_Float__Text__Classification(0.4332),
                Enum__Text__Classification__Criteria.NEGATIVITY: Safe_Float__Text__Classification(0.5403)
            }
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.6)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVITY,
                filter_mode = Enum__Classification__Filter_Mode.BELOW,
                threshold   = Safe_Float(0.5)
            )
        ]

        filtered = self.classification_service._apply_and_filter(hash_ratings, criterion_filters)

        # pos=0.4332 > 0.6? NO → FAIL (AND requires both)
        assert len(filtered) == 0

    # ========================================
    # _apply_or_filter Tests
    # ========================================

    def test___apply_or_filter__any_match(self):                               # Test OR filter where hashes match at least one criterion
        # From reference:
        # Text A → pos:0.4814, neg:0.5114
        # Text B → pos:0.8374, neg:0.7441
        hash_ratings = {
            Safe_Str__Hash("b840f6f2ae"): {
                Enum__Text__Classification__Criteria.POSITIVITY: Safe_Float__Text__Classification(0.4814),
                Enum__Text__Classification__Criteria.NEGATIVITY: Safe_Float__Text__Classification(0.5114)
            },
            Safe_Str__Hash("eb5deeca9c"): {
                Enum__Text__Classification__Criteria.POSITIVITY: Safe_Float__Text__Classification(0.8374),
                Enum__Text__Classification__Criteria.NEGATIVITY: Safe_Float__Text__Classification(0.7441)
            }
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.4)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.4)
            )
        ]

        filtered = self.classification_service._apply_or_filter(hash_ratings, criterion_filters)

        # Both match at least one criterion
        assert len(filtered) == 2

    def test___apply_or_filter__no_match(self):                                # Test OR filter where no hashes match any criteria
        # From reference: Low both → pos:0.1844, neg:0.3436
        hash_ratings = {
            Safe_Str__Hash("b0a2013306"): {
                Enum__Text__Classification__Criteria.POSITIVITY: Safe_Float__Text__Classification(0.1844),
                Enum__Text__Classification__Criteria.NEGATIVITY: Safe_Float__Text__Classification(0.3436)
            }
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.7)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.7)
            )
        ]

        filtered = self.classification_service._apply_or_filter(hash_ratings, criterion_filters)

        # pos=0.1844 > 0.7? NO, neg=0.3436 > 0.7? NO → NO MATCH
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
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.5)
            )],
            logic_operator    = Enum__Classification__Logic_Operator.AND,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.classification_service.filter_by_multi_criteria(request)

        assert response.success is True
        assert response.total_hashes == 0
        assert response.filtered_count == 0

    def test__filter_by_multi_criteria__three_criteria_and(self):              # Test AND logic with three criteria
        # From reference: Balanced text → pos:0.7643, neg:0.7631, bias:0.6116
        hash_mapping = {Safe_Str__Hash("c298542a7f"): "Balanced text"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.6)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.6)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.BIAS,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.6)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping,
            criterion_filters = criterion_filters,
            logic_operator    = Enum__Classification__Logic_Operator.AND,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.classification_service.filter_by_multi_criteria(request)

        # All three: pos=0.7643 > 0.6 ✓, neg=0.7631 > 0.6 ✓, bias=0.6116 > 0.6 ✓
        assert response.success is True
        assert response.filtered_count == 1