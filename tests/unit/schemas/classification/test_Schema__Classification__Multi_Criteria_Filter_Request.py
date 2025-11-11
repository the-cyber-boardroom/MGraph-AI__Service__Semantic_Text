from unittest                                                                                                       import TestCase
from osbot_utils.testing.__                                                                                         import __
from osbot_utils.type_safe.primitives.core.Safe_Float                                                               import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                                  import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria                     import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Filter_Request   import Schema__Classification__Multi_Criteria_Filter_Request
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Criterion_Filter                import Schema__Classification__Criterion_Filter
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode                 import Enum__Classification__Filter_Mode
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Logic_Operator              import Enum__Classification__Logic_Operator
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode                 import Enum__Classification__Output_Mode


class test_Schema__Classification__Multi_Criteria_Filter_Request(TestCase):

    def test__init__(self):                                                    # Test auto-initialization
        with Schema__Classification__Multi_Criteria_Filter_Request() as _:
            assert _.hash_mapping      == {}
            assert _.criterion_filters == []
            assert _.logic_operator    is None
            assert _.output_mode       == Enum__Classification__Output_Mode.FULL_RATINGS
            assert type(_).__name__    == 'Schema__Classification__Multi_Criteria_Filter_Request'

    def test__with_single_filter_and_logic(self):                              # Test with single criterion filter and AND logic
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.5)
            )
        ]

        with Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping,
            criterion_filters = criterion_filters,
            logic_operator    = Enum__Classification__Logic_Operator.AND,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        ) as _:
            assert len(_.hash_mapping) == 1
            assert len(_.criterion_filters) == 1
            assert _.logic_operator == Enum__Classification__Logic_Operator.AND
            assert _.output_mode == Enum__Classification__Output_Mode.HASHES_ONLY

            first_filter = _.criterion_filters[0]
            assert first_filter.criterion == Enum__Text__Classification__Criteria.POSITIVITY
            assert first_filter.filter_mode == Enum__Classification__Filter_Mode.ABOVE
            assert float(first_filter.threshold) == 0.5

    def test__with_multiple_filters_and_logic(self):                           # Test with multiple criterion filters and AND logic
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.6)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVITY,
                filter_mode = Enum__Classification__Filter_Mode.BELOW,
                threshold   = Safe_Float(0.3)
            )
        ]

        with Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping,
            criterion_filters = criterion_filters,
            logic_operator    = Enum__Classification__Logic_Operator.AND,
            output_mode       = Enum__Classification__Output_Mode.FULL_RATINGS
        ) as _:
            assert len(_.criterion_filters) == 2
            assert _.logic_operator == Enum__Classification__Logic_Operator.AND

            assert _.criterion_filters[0].criterion == Enum__Text__Classification__Criteria.POSITIVITY
            assert _.criterion_filters[1].criterion == Enum__Text__Classification__Criteria.NEGATIVITY

    def test__with_or_logic(self):                                             # Test with OR logic operator
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.7)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.URGENCY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.7)
            )
        ]

        with Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping,
            criterion_filters = criterion_filters,
            logic_operator    = Enum__Classification__Logic_Operator.OR
        ) as _:
            assert _.logic_operator == Enum__Classification__Logic_Operator.OR
            assert len(_.criterion_filters) == 2

    def test__with_between_filter_mode(self):                                  # Test with BETWEEN filter mode
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion     = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode   = Enum__Classification__Filter_Mode.BETWEEN,
                threshold     = Safe_Float(0.5),
                threshold_max = Safe_Float(0.8)
            )
        ]

        with Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping,
            criterion_filters = criterion_filters,
            logic_operator    = Enum__Classification__Logic_Operator.AND
        ) as _:
            filter_obj = _.criterion_filters[0]
            assert filter_obj.filter_mode == Enum__Classification__Filter_Mode.BETWEEN
            assert float(filter_obj.threshold) == 0.5
            assert float(filter_obj.threshold_max) == 0.8

    def test__output_mode_default(self):                                       # Test default output mode
        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = {Safe_Str__Hash("b10a8db164"): "Test"},
            criterion_filters = [Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.5)
            )],
            logic_operator    = Enum__Classification__Logic_Operator.AND
        )

        assert request.output_mode == Enum__Classification__Output_Mode.FULL_RATINGS

    def test__output_mode_hashes_only(self):                                   # Test HASHES_ONLY output mode
        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = {Safe_Str__Hash("b10a8db164"): "Test"},
            criterion_filters = [Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.5)
            )],
            logic_operator    = Enum__Classification__Logic_Operator.AND,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        assert request.output_mode == Enum__Classification__Output_Mode.HASHES_ONLY

    def test__output_mode_hashes_with_text(self):                              # Test HASHES_WITH_TEXT output mode
        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = {Safe_Str__Hash("b10a8db164"): "Test"},
            criterion_filters = [Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.5)
            )],
            logic_operator    = Enum__Classification__Logic_Operator.AND,
            output_mode       = Enum__Classification__Output_Mode.HASHES_WITH_TEXT
        )

        assert request.output_mode == Enum__Classification__Output_Mode.HASHES_WITH_TEXT

    def test__multiple_hashes(self):                                           # Test with multiple hashes
        hash_mapping = {
            Safe_Str__Hash("b10a8db164"): "Hello World",
            Safe_Str__Hash("f1feeaa3d6"): "Test Text",
            Safe_Str__Hash("1ba249ca59"): "Sample text"
        }

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.5)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping,
            criterion_filters = criterion_filters,
            logic_operator    = Enum__Classification__Logic_Operator.AND
        )

        assert len(request.hash_mapping) == 3

    def test__three_criterion_filters(self):                                   # Test with three criterion filters
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Test"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.6)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.NEGATIVITY,
                filter_mode = Enum__Classification__Filter_Mode.BELOW,
                threshold   = Safe_Float(0.4)
            ),
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.BIAS,
                filter_mode = Enum__Classification__Filter_Mode.BELOW,
                threshold   = Safe_Float(0.5)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping,
            criterion_filters = criterion_filters,
            logic_operator    = Enum__Classification__Logic_Operator.AND
        )

        assert len(request.criterion_filters) == 3
        assert request.criterion_filters[0].criterion == Enum__Text__Classification__Criteria.POSITIVITY
        assert request.criterion_filters[1].criterion == Enum__Text__Classification__Criteria.NEGATIVITY
        assert request.criterion_filters[2].criterion == Enum__Text__Classification__Criteria.BIAS

    def test__obj(self):                                                       # Test .obj() serialization
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Test"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.5)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping,
            criterion_filters = criterion_filters,
            logic_operator    = Enum__Classification__Logic_Operator.AND,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        obj_data = request.obj()
        assert obj_data.hash_mapping      == __(b10a8db164='Test')
        assert obj_data.logic_operator    == 'and'
        assert obj_data.output_mode       == 'hashes-only'
        assert len(obj_data.criterion_filters) == 1

    def test__json_round_trip(self):                                           # Test JSON serialization round-trip
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Test"}

        criterion_filters = [
            Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.POSITIVITY,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE,
                threshold   = Safe_Float(0.5)
            )
        ]

        request = Schema__Classification__Multi_Criteria_Filter_Request(
            hash_mapping      = hash_mapping,
            criterion_filters = criterion_filters,
            logic_operator    = Enum__Classification__Logic_Operator.AND,
            output_mode       = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        json_data = request.json()
        restored  = Schema__Classification__Multi_Criteria_Filter_Request(**json_data)

        assert len(restored.hash_mapping) == 1
        assert len(restored.criterion_filters) == 1
        assert restored.logic_operator == Enum__Classification__Logic_Operator.AND
        assert restored.output_mode == Enum__Classification__Output_Mode.HASHES_ONLY