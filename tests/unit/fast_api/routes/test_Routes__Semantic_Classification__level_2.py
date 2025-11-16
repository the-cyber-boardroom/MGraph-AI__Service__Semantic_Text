import pytest
import json
import re
from enum                                                                                                            import Enum
from typing                                                                                                          import Dict
from unittest                                                                                                        import TestCase
from fastapi                                                                                                         import FastAPI
from osbot_utils.testing.Stdout                                                                                      import Stdout
from osbot_utils.testing.__                                                                                          import __
from osbot_utils.type_safe.Type_Safe                                                                                 import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                                import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                                   import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Response          import Schema__Classification__Multi_Criteria_Response
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria                      import Enum__Text__Classification__Criteria
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
        cls.app    = FastAPI()
        cls.routes = Routes__Semantic_Classification(app=cls.app).setup()

    def test__setUpClass(self):
        with self.routes as _:
            assert type(_)          is Routes__Semantic_Classification
            assert _.routes_paths() == ['/multi/filter', '/multi/rate', '/single/filter', '/single/rate']
            assert _.tag            == 'semantic-classification'

    # ========================================
    # classify__multi__rate Tests
    # ========================================

    def test__classify__multi__rate__basic(self):                              # Test basic multi-criteria rating with deterministic values
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World",           # Using actual hash from engine
                        Safe_Str__Hash("f1feeaa3d6"): "Test Text"}             # Using actual hash from engine

        request = Schema__Classification__Multi_Criteria_Request(
            hash_mapping            = hash_mapping                                     ,
            classification_criteria = [Enum__Text__Classification__Criteria.POSITIVE,
                                       Enum__Text__Classification__Criteria.NEGATIVE,     # values can be provided using the enum value
                                       'bias'                                         ])    # or as a string :)

        response = self.routes.multi__rate(request)
        assert type(response)                   is Schema__Classification__Multi_Criteria_Response
        assert response.success                 is True
        assert response.total_hashes            == 2
        assert len(response.hash_ratings)       == 2
        assert response.classification_criteria == [Enum__Text__Classification__Criteria.POSITIVE,
                                                    Enum__Text__Classification__Criteria.NEGATIVE,
                                                    Enum__Text__Classification__Criteria.NEUTRAL      ]

        # Deterministic values from hash-based engine (from reference guide)
        assert response.obj()                   == __(hash_ratings = __(b10a8db164 = __(positivity = 0.7478,
                                                                                        negativity = 0.1102,
                                                                                        bias       = 0.2316),
                                                                        f1feeaa3d6 = __(positivity = 0.508 ,
                                                                                        negativity = 0.3946,
                                                                                        bias       = 0.9818)),
                                                       classification_criteria = ['positivity', 'negativity', 'bias'],
                                                       total_hashes            = 2                                    ,
                                                       success                 = True                                 )
        assert response.json() == {'classification_criteria' : ['positivity' , 'negativity' , 'bias']     ,
                                   'hash_ratings'            : {'b10a8db164' : { 'bias'      : 0.2316     ,
                                                                                 'negativity': 0.1102     ,
                                                                                 'positivity': 0.7478}    ,
                                                               'f1feeaa3d6'  : { 'bias'       : 0.9818    ,
                                                                                 'negativity' : 0.3946    ,
                                                                                 'positivity' : 0.5080}}  ,
                                   'success'                 : True                                       ,
                                   'total_hashes'            : 2                                          }

    def test__classify__multi__rate__empty(self):                              # Test with empty mapping
        request = Schema__Classification__Multi_Criteria_Request(hash_mapping            = {}                                                                    ,
                                                                 classification_criteria = [Enum__Text__Classification__Criteria.POSITIVE])

        response = self.routes.multi__rate(request)

        assert response.success      is True
        assert response.total_hashes == 0
        assert response.hash_ratings == {}

    def test__classify__multi__rate__single_criterion(self):                   # Test with single criterion
        hash_mapping = { Safe_Str__Hash("0cbc6611f5"): "Test"}                 # Using actual hash: Test → 0cbc6611f5
        request      = Schema__Classification__Multi_Criteria_Request(hash_mapping            = hash_mapping                                 ,
                                                                      classification_criteria = [Enum__Text__Classification__Criteria.MIXED])
        response     = self.routes.multi__rate(request)

        assert response.total_hashes      == 1
        assert len(response.hash_ratings) == 1
        assert response.obj()             == __(hash_ratings            = __(_0cbc6611f5 = __(urgency=0.7786)),  # From reference: Test → urgency: 0.7786 (note that .obj() will convert '0cbc6611f5' to '_0cbc6611f5' so that we have a valid python variable name)
                                                classification_criteria = ['urgency']                         ,
                                                total_hashes            = 1                                   ,
                                                success                 = True                                )

        assert response.json() == {  'classification_criteria' : ['urgency']                             ,
                                     'hash_ratings'            : {'0cbc6611f5' : {'urgency' : 0.7786}}   ,
                                     'success'                 : True                                    ,
                                     'total_hashes'            : 1                                       }


    def test__classify__multi__rate__all_criteria(self):                       # Test with all 4 criteria
        hash_mapping = {Safe_Str__Hash("1ba249ca59"): "Sample text"}           # Using actual hash: Sample text → 1ba249ca59

        request = Schema__Classification__Multi_Criteria_Request(hash_mapping            = hash_mapping                                                          ,
                                                                 classification_criteria = [Enum__Text__Classification__Criteria.POSITIVE,
                                                                                            'negativity'                                   ,
                                                                                            'bias'                                         ,
                                                                                            Enum__Text__Classification__Criteria.MIXED   ])

        response = self.routes.multi__rate(request)

        assert response.success           is True
        assert response.total_hashes      == 1
        assert len(response.hash_ratings) == 1

        # All ratings should be present
        ratings = response.hash_ratings[Safe_Str__Hash("1ba249ca59")]
        assert Enum__Text__Classification__Criteria.POSITIVE in ratings
        assert Enum__Text__Classification__Criteria.NEGATIVE in ratings
        assert Enum__Text__Classification__Criteria.NEUTRAL       in ratings
        assert Enum__Text__Classification__Criteria.MIXED    in ratings

        # From reference guide: Sample text → pos:0.9569, neg:0.1469, bias:0.2887, urg:0.7091
        assert ratings.obj()  == __(positivity = 0.9569 ,
                                    negativity = 0.1469 ,
                                    bias       = 0.2887 ,
                                    urgency    = 0.7091 )
        assert response.obj() == __(hash_ratings             = __(_1ba249ca59 = __(positivity = 0.9569 ,
                                                                                   negativity = 0.1469 ,
                                                                                   bias       = 0.2887 ,
                                                                                   urgency    = 0.7091)) ,
                                    classification_criteria  = ['positivity', 'negativity', 'bias', 'urgency'] ,
                                    total_hashes             = 1                                                ,
                                    success                  = True                                             )


    # ========================================
    # classify__multi__filter Tests - AND Logic
    # ========================================

    def test__classify__multi__filter__and__basic(self):                       # Test AND logic with 2 criteria

        hash_mapping = {Safe_Str__Hash("b5ead10d6e"): "Positive text",              # From reference guide: Positive text → pos:0.4332, neg:0.5403
                        Safe_Str__Hash("9204d57da8"): "Another text"}               #                       Another text  → pos:0.3018, neg:0.7096

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.6)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.BELOW          ,
                threshold   = Safe_Float(0.6)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(hash_mapping      = hash_mapping                                    ,
                                                                        criterion_filters = criterion_filters                              ,
                                                                        logic_operator    = Enum__Classification__Logic_Operator.AND       ,
                                                                        output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY)

        response = self.routes.multi__filter(request)

        # Analysis:
        # b5ead10d6e: pos=0.4332 > 0.6? NO, neg=0.5403 < 0.6? YES → FAIL (AND requires both)
        # 9204d57da8: pos=0.3018 > 0.6? NO, neg=0.7096 < 0.6? NO → FAIL
        assert response.success            is True
        assert response.logic_operator     == Enum__Classification__Logic_Operator.AND
        assert response.total_hashes       == 2
        assert response.filtered_count     == 0                                 # No hash satisfies BOTH conditions
        assert response.filtered_hashes    == []

        assert response.obj() == __(filtered_with_text       = None                                        ,
                                    filtered_with_ratings    = None                                        ,
                                    filtered_hashes          = []                                          ,
                                    criteria_used            = ['positivity', 'negativity']               ,
                                    logic_operator           = 'and'                                       ,
                                    output_mode              = 'hashes-only'                               ,
                                    total_hashes             = 2                                           ,
                                    filtered_count           = 0                                           ,
                                    success                  = True                                        )

    def test__classify__multi__filter__and__both_match(self):                   # Test AND logic where both criteria match
        hash_mapping = {Safe_Str__Hash("eb5deeca9c"): "Text B"}                 # From reference: Text B → pos:0.8374, neg:0.7441

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.5)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.5)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                    ,
            criterion_filters = criterion_filters                              ,
            logic_operator    = Enum__Classification__Logic_Operator.AND       ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.multi__filter(request)

        # Analysis: pos=0.8374 > 0.5 ✓, neg=0.7441 > 0.5 ✓ → MATCH
        assert response.success            is True
        assert response.filtered_count     == 1
        assert response.filtered_hashes    == [Safe_Str__Hash("eb5deeca9c")]
        assert response.obj()              == __(filtered_hashes         = ['eb5deeca9c']              ,
                                                 filtered_with_text      = None                        ,
                                                 filtered_with_ratings   = None                        ,
                                                 criteria_used           = ['positivity', 'negativity'],
                                                 logic_operator          = 'and'                       ,
                                                 output_mode             = 'hashes-only'               ,
                                                 total_hashes            = 1                           ,
                                                 filtered_count          = 1                           ,
                                                 success                 = True                        )

    def test__classify__multi__filter__and__with_text(self):                   # Test AND logic with text output
        # From reference: Test content → pos:0.6355, bias:0.3099
        hash_mapping = {Safe_Str__Hash("8bfa8e0684"): "Test content"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.5)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEUTRAL        ,
                filter_mode = Enum__Classification__Filter_Mode.BELOW          ,
                threshold   = Safe_Float(0.5)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                    ,
            criterion_filters = criterion_filters                              ,
            logic_operator    = Enum__Classification__Logic_Operator.AND       ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_WITH_TEXT
        )

        response = self.routes.multi__filter(request)

        # Analysis: pos=0.6355 > 0.5 ✓, bias=0.3099 < 0.5 ✓ → MATCH
        assert response.success               is True
        assert response.filtered_count        == 1
        assert response.filtered_with_text    is not None
        assert response.filtered_with_ratings is None
        assert response.filtered_with_text    == {Safe_Str__Hash("8bfa8e0684"): "Test content"}

        assert response.obj()                 == __(filtered_with_text       = __(_8bfa8e0684 = 'Test content')         ,
                                                    filtered_with_ratings    = None                                     ,
                                                    filtered_hashes          = ['8bfa8e0684']                           ,
                                                    criteria_used            = ['positivity', 'bias']                  ,
                                                    logic_operator           = 'and'                                    ,
                                                    output_mode              = 'hashes-with-text'                       ,
                                                    total_hashes             = 1                                        ,
                                                    filtered_count           = 1                                        ,
                                                    success                  = True                                     )

        assert response.json()                == {'criteria_used'          : ['positivity', 'bias']                         ,
                                                  'filtered_count'         : 1                                              ,
                                                  'filtered_hashes'        : ['8bfa8e0684']                                 ,
                                                  'filtered_with_ratings'  : None                                           ,
                                                  'filtered_with_text'     : {Safe_Str__Hash('8bfa8e0684') : 'Test content'} ,
                                                  'logic_operator'         : 'and'                                          ,
                                                  'output_mode'            : 'hashes-with-text'                             ,
                                                  'success'                : True                                           ,
                                                  'total_hashes'           : 1                                              }


    def test__classify__multi__filter__and__full_ratings(self):                # Test AND logic with full ratings output
        # From reference: Text → pos:0.9776
        hash_mapping = {Safe_Str__Hash("9dffbf69ff"): "Text"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.5)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                    ,
            criterion_filters = criterion_filters                              ,
            logic_operator    = Enum__Classification__Logic_Operator.AND       ,
            output_mode       = Enum__Classification__Output_Mode.FULL_RATINGS
        )

        response = self.routes.multi__filter(request)

        # Analysis: pos=0.9776 > 0.5 ✓ → MATCH
        assert response.success               is True
        assert response.filtered_with_text    is not None
        assert response.filtered_with_ratings is not None
        assert response.obj()                 == __(filtered_hashes       = ['9dffbf69ff']                                      ,
                                                     filtered_with_text    = __(_9dffbf69ff='Text')                         ,
                                                     filtered_with_ratings = __(_9dffbf69ff=__(positivity=0.9776)),
                                                     criteria_used         = ['positivity']                                     ,
                                                     logic_operator        = 'and'                                              ,
                                                     output_mode           = 'full-ratings'                                     ,
                                                     total_hashes          = 1                                                  ,
                                                     filtered_count        = 1                                                  ,
                                                     success               = True                                               )

    # ========================================
    # classify__multi__filter Tests - OR Logic
    # ========================================

    def test__classify__multi__filter__or__basic(self):                        # Test OR logic with 2 criteria
        # From reference guide:
        # High positive → pos:0.5667, neg:0.6083
        # High negative → pos:0.5421, neg:0.7642
        # Low both      → pos:0.1844, neg:0.3436
        hash_mapping = {Safe_Str__Hash("c3d45f8fe6"): "High positive",
                        Safe_Str__Hash("58537f27d7"): "High negative",
                        Safe_Str__Hash("b0a2013306"): "Low both"     }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(criterion   = Enum__Text__Classification__Criteria.POSITIVE  ,
                                                     filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                                                     threshold   = Safe_Float(0.7)),
            Schema__Classification__Criterion_Filter(criterion   = Enum__Text__Classification__Criteria.NEGATIVE  ,
                                                     filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                                                     threshold   = Safe_Float(0.7))]

        request = Schema__Classification__Multi_Criteria_Filter_Request(hash_mapping      = hash_mapping                                    ,
                                                                        criterion_filters = criterion_filters                              ,
                                                                        logic_operator    = Enum__Classification__Logic_Operator.OR        ,
                                                                        output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY)

        response = self.routes.multi__filter(request)

        # Analysis (OR logic - any condition passes):
        # c3d45f8fe6: pos=0.5667 > 0.7? NO, neg=0.6083 > 0.7? NO → FAIL
        # 58537f27d7: pos=0.5421 > 0.7? NO, neg=0.7642 > 0.7? YES → MATCH
        # b0a2013306: pos=0.1844 > 0.7? NO, neg=0.3436 > 0.7? NO → FAIL
        assert response.success            is True
        assert response.logic_operator     == Enum__Classification__Logic_Operator.OR
        assert response.total_hashes       == 3
        assert response.filtered_count     == 1
        assert response.filtered_hashes    == [Safe_Str__Hash("58537f27d7")]

        assert response.obj()              == __(filtered_with_text       = None                                        ,
                                                 filtered_with_ratings    = None                                        ,
                                                 filtered_hashes          = ['58537f27d7']                              ,
                                                 criteria_used            = ['positivity', 'negativity']               ,
                                                 logic_operator           = 'or'                                        ,
                                                 output_mode              = 'hashes-only'                               ,
                                                 total_hashes             = 3                                           ,
                                                 filtered_count           = 1                                           ,
                                                 success                  = True                                        )


    def test__classify__multi__filter__or__multiple_matches(self):             # Test OR logic with multiple matches
        # From reference: Text A → pos:0.4814, neg:0.5114
        #                Text B → pos:0.8374, neg:0.7441
        hash_mapping = {Safe_Str__Hash("b840f6f2ae"): "Text A",
                        Safe_Str__Hash("eb5deeca9c"): "Text B"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.4)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.4)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                    ,
            criterion_filters = criterion_filters                              ,
            logic_operator    = Enum__Classification__Logic_Operator.OR        ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.multi__filter(request)

        # Analysis (OR logic):
        # b840f6f2ae: pos=0.4814 > 0.4 ✓ or neg=0.5114 > 0.4 ✓ → MATCH
        # eb5deeca9c: pos=0.8374 > 0.4 ✓ or neg=0.7441 > 0.4 ✓ → MATCH
        assert response.success        is True
        assert response.filtered_count == 2
        assert set(response.filtered_hashes) == {Safe_Str__Hash("b840f6f2ae"), Safe_Str__Hash("eb5deeca9c")}
        assert response.obj() == __(filtered_with_text       = None                                              ,
                                    filtered_with_ratings    = None                                              ,
                                    filtered_hashes          = ['b840f6f2ae', 'eb5deeca9c']                      ,
                                    criteria_used            = ['positivity', 'negativity']                     ,
                                    logic_operator           = 'or'                                              ,
                                    output_mode              = 'hashes-only'                                     ,
                                    total_hashes             = 2                                                 ,
                                    filtered_count           = 2                                                 ,
                                    success                  = True                                              )


    def test__classify__multi__filter__or__no_matches(self):                   # Test OR logic with no matches
        # From reference: Text → pos:0.9776, neg:0.5651
        hash_mapping = {Safe_Str__Hash("9dffbf69ff"): "Text"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.BELOW          ,  # Changed to BELOW for no match
                threshold   = Safe_Float(0.5)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.BELOW          ,  # Changed to BELOW for no match
                threshold   = Safe_Float(0.5)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                    ,
            criterion_filters = criterion_filters                              ,
            logic_operator    = Enum__Classification__Logic_Operator.OR        ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.multi__filter(request)

        # Analysis: pos=0.9776 < 0.5? NO, neg=0.5651 < 0.5? NO → NO MATCH
        assert response.success        is True
        assert response.filtered_count == 0
        assert response.filtered_hashes == []

    # ========================================
    # Complex Filter Mode Tests
    # ========================================

    def test__classify__multi__filter__between_mode(self):                     # Test BETWEEN filter mode in multi-criteria
        # From reference: Test text → pos:0.5506
        hash_mapping = {Safe_Str__Hash("aaaf7028b8"): "Test text"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion     = Enum__Text__Classification__Criteria.POSITIVE,
                filter_mode   = Enum__Classification__Filter_Mode.BETWEEN      ,
                threshold     = Safe_Float(0.5)                                 ,
                threshold_max = Safe_Float(0.6)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                    ,
            criterion_filters = criterion_filters                              ,
            logic_operator    = Enum__Classification__Logic_Operator.AND       ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.multi__filter(request)

        # Analysis: 0.5 < 0.5506 < 0.6 ✓ → MATCH
        assert response.success         is True
        assert response.filtered_count  == 1
        assert response.filtered_hashes == [Safe_Str__Hash("aaaf7028b8")]
        assert response.obj()           == __( filtered_with_text       = None                                        ,
                                               filtered_with_ratings    = None                                        ,
                                               filtered_hashes          = ['aaaf7028b8']                              ,
                                               criteria_used            = ['positivity']                              ,
                                               logic_operator           = 'and'                                       ,
                                               output_mode              = 'hashes-only'                               ,
                                               total_hashes             = 1                                           ,
                                               filtered_count           = 1                                           ,
                                               success                  = True                                        )


    def test__classify__multi__filter__mixed_modes(self):                      # Test mixing ABOVE and BELOW modes
        # From reference: Balanced text → pos:0.7643, neg:0.7631
        hash_mapping = {Safe_Str__Hash("c298542a7f"): "Balanced text"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.6)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.BELOW          ,
                threshold   = Safe_Float(0.8)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                    ,
            criterion_filters = criterion_filters                              ,
            logic_operator    = Enum__Classification__Logic_Operator.AND       ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.multi__filter(request)

        # Analysis: pos=0.7643 > 0.6 ✓, neg=0.7631 < 0.8 ✓ → MATCH
        assert response.success        is True
        assert response.filtered_count == 1
        assert response.obj()          == __(filtered_with_text       = None                         ,
                                             filtered_with_ratings    = None                         ,
                                             filtered_hashes          = ['c298542a7f']               ,
                                             criteria_used            = ['positivity', 'negativity'] ,
                                             logic_operator           = 'and'                        ,
                                             output_mode              = 'hashes-only'                ,
                                             total_hashes             = 1                            ,
                                             filtered_count           = 1                            ,
                                             success                  = True                         )


    # ========================================
    # Edge Cases
    # ========================================

    def test__classify__multi__filter__empty_mapping(self):                    # Test with empty hash mapping
        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = {}                                              ,
            criterion_filters = [Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.5)
            )]                                                                  ,
            logic_operator    = Enum__Classification__Logic_Operator.AND       ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.multi__filter(request)

        assert response.success         is True
        assert response.total_hashes    == 0
        assert response.filtered_count  == 0
        assert response.filtered_hashes == []

    def test__classify__multi__filter__single_filter(self):                    # Test with single filter (edge of multi-criteria)
        # From reference: Text → pos:0.9776
        hash_mapping = {Safe_Str__Hash("9dffbf69ff"): "Text"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.5)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                    ,
            criterion_filters = criterion_filters                              ,
            logic_operator    = Enum__Classification__Logic_Operator.AND       ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.multi__filter(request)

        # Analysis: pos=0.9776 > 0.5 ✓ → MATCH
        assert response.success        is True
        assert response.filtered_count == 1

    # ========================================
    # Deterministic Multiple Hashes Tests
    # ========================================

    def test__classify__multi__filter__deterministic_results(self):            # Test deterministic results with multiple hashes
        # From reference guide with correct hashes:
        # Text 0 → 20c8b16b2a: pos:0.7645, neg:0.7672
        # Text 1 → 161a6b3572: pos:0.7402, neg:0.0745
        # Text 2 → 48e47cee20: pos:0.4943, neg:0.9681
        # Text 3 → 0d96bbc2ec: pos:0.3426, neg:0.2576
        # Text 4 → c133c1f81c: pos:0.6403, neg:0.9734
        hash_mapping = {
            Safe_Str__Hash("20c8b16b2a"): "Text 0",
            Safe_Str__Hash("161a6b3572"): "Text 1",
            Safe_Str__Hash("48e47cee20"): "Text 2",
            Safe_Str__Hash("0d96bbc2ec"): "Text 3",
            Safe_Str__Hash("c133c1f81c"): "Text 4"
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.6)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.6)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                    ,
            criterion_filters = criterion_filters                              ,
            logic_operator    = Enum__Classification__Logic_Operator.AND       ,
            output_mode       = Enum__Classification__Output_Mode.FULL_RATINGS
        )

        response = self.routes.multi__filter(request)

        assert response.success        is True
        assert response.total_hashes   == 5

        # Analysis (AND logic - both conditions must be true):
        # 20c8b16b2a: pos=0.7645 > 0.6 ✓, neg=0.7672 > 0.6 ✓ → MATCH
        # 161a6b3572: pos=0.7402 > 0.6 ✓, neg=0.0745 > 0.6 ✗ → NO MATCH
        # 48e47cee20: pos=0.4943 > 0.6 ✗, neg=0.9681 > 0.6 ✓ → NO MATCH
        # 0d96bbc2ec: pos=0.3426 > 0.6 ✗, neg=0.2576 > 0.6 ✗ → NO MATCH
        # c133c1f81c: pos=0.6403 > 0.6 ✓, neg=0.9734 > 0.6 ✓ → MATCH
        # Expected: 20c8b16b2a, c133c1f81c (count: 2)

        assert response.filtered_count == 2
        assert set(response.filtered_hashes) == {Safe_Str__Hash("20c8b16b2a"),
                                                  Safe_Str__Hash("c133c1f81c")}

    def test__classify__multi__filter__three_criteria_and(self):               # Test with three criteria using AND
        # From reference: Balanced text → pos:0.7643, neg:0.7631, bias:0.6116
        hash_mapping = {Safe_Str__Hash("c298542a7f"): "Balanced text"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.6)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVE  ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.6)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEUTRAL        ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.6)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping                                    ,
            criterion_filters = criterion_filters                              ,
            logic_operator    = Enum__Classification__Logic_Operator.AND       ,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.multi__filter(request)

        # Analysis: pos=0.7643 > 0.6 ✓, neg=0.7631 > 0.6 ✓, bias=0.6116 > 0.6 ✓ → MATCH
        assert response.success is True
        assert response.filtered_count == 1

    # ========================================
    # Regression Tests
    # ========================================

    def test__regression__dict__json__enum__conversion(self):                  # FIXED in OSBot_Utils 3.26.0
        class An_Enum(str, Enum):
            A = 'A'
            B = 'B'
            C = 'C'

        class An_Class(Type_Safe):
            an_dict : Dict[An_Enum, int]

        assert An_Class()                .obj ()  == __(  an_dict = __())
        assert An_Class()                .json()  ==   { 'an_dict': {}  }
        assert An_Class(an_dict={'A': 42}).obj()  == __(  an_dict = __(A= 42))
        assert An_Class(an_dict={'A': 42}).json() ==   { 'an_dict': {  'A': 42}}

        assert An_Enum.A                                                    == 'A'
        assert type(An_Class(an_dict={'A': 42}).json())                     is dict
        assert json.dumps(An_Class(an_dict={'A': 42}).json())               == '{"an_dict": {"A": 42}}'
        assert An_Class.from_json(An_Class(an_dict={'A': 42}).json()).obj() == __(an_dict=__(A=42))
        assert An_Class.from_json({ 'an_dict': {  An_Enum.A: 42}}   ).obj() == __(an_dict=__(A=42))
        assert An_Class.from_json({ 'an_dict': {  'A'      : 42}}   ).obj() == __(an_dict=__(A=42))

        with Stdout() as stdout:
            print(An_Class(an_dict={'A': 42}).json())
        assert stdout.value() == "{'an_dict': {'A': 42}}\n"

        error_message = "assert {'an_dict': {'A': 42}} == {}\n  \n  Left contains 1 more item:\n  {'an_dict': {'A': 42}}\n  \n  Full diff:\n  - {}\n  + {\n  +     'an_dict': {\n  +         'A': 42,\n  +     },\n  + }"
        with pytest.raises(AssertionError, match=re.escape(error_message)):
            assert An_Class(an_dict={'A': 42}).json() == {}

        assert An_Class(an_dict={An_Enum.A: 42}).obj()       == __(an_dict=__(A=42))
        assert An_Class(an_dict={An_Enum.A: 42}).json()      == {'an_dict': {'A': 42}}
        assert str(An_Class(an_dict={An_Enum.A: 42}).json()) == "{'an_dict': {'A': 42}}"
        assert repr(An_Class(an_dict={An_Enum.A: 42}).json()) == "{'an_dict': {'A': 42}}"

    def test__regression__edge_case_on_dict_enum__part_2(self):                # Test enum key conversion in nested dicts
        hash_rating = { Enum__Text__Classification__Criteria.POSITIVE : 0.0 }
        hash_ratings = {Safe_Str__Hash('b10a8db164'): hash_rating}
        response = Schema__Classification__Multi_Criteria_Response(hash_ratings=hash_ratings)

        assert response.obj() == __(hash_ratings            = __(b10a8db164=__(positivity=0.0)),
                                    classification_criteria = []    ,
                                    total_hashes            = 0     ,
                                    success                 = False )

        assert response.hash_ratings.obj() == __(b10a8db164=__(positivity=0.0))
        assert response.hash_ratings.json() == {'b10a8db164': {'positivity': 0.0}}

        assert json.dumps(response.hash_ratings) == '{"b10a8db164": {"positivity": 0.0}}'
        assert str(response.hash_ratings)        == ("{Safe_Str__Hash('b10a8db164'): "
                                                     "{<Enum__Text__Classification__Criteria.POSITIVE: 'positivity'>: "
                                                     'Safe_Float__Text__Classification(0.0)}}')
        assert repr(response.hash_ratings)      == ("{Safe_Str__Hash('b10a8db164'): "
                                                     "{<Enum__Text__Classification__Criteria.POSITIVE: 'positivity'>: "
                                                     'Safe_Float__Text__Classification(0.0)}}')