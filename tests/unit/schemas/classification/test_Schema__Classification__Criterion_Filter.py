from unittest                                                                                           import TestCase
from osbot_utils.testing.__                                                                             import __
from osbot_utils.type_safe.primitives.core.Safe_Float                                                   import Safe_Float
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria         import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode     import Enum__Classification__Filter_Mode
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Criterion_Filter    import Schema__Classification__Criterion_Filter


class test_Schema__Classification__Criterion_Filter(TestCase):

    def test__init__(self):                                                    # Test auto-initialization
        with Schema__Classification__Criterion_Filter() as _:
            assert _.criterion       is None
            assert _.filter_mode     is None
            assert _.threshold       == 0
            assert _.threshold_max   is None
            assert type(_).__name__  == 'Schema__Classification__Criterion_Filter'

    def test__with_basic_filter(self):                                         # Test with basic ABOVE filter
        with Schema__Classification__Criterion_Filter(
            criterion   = Enum__Text__Classification__Criteria.POSITIVE      ,
            filter_mode = Enum__Classification__Filter_Mode.ABOVE              ,
            threshold   = Safe_Float(0.7)
        ) as _:
            assert _.criterion     == Enum__Text__Classification__Criteria.POSITIVE
            assert _.filter_mode   == Enum__Classification__Filter_Mode.ABOVE
            assert _.threshold     == 0.7
            assert _.threshold_max is None

    def test__with_between_filter(self):                                       # Test with BETWEEN filter using threshold_max
        with Schema__Classification__Criterion_Filter(
            criterion     = Enum__Text__Classification__Criteria.NEGATIVE    ,
            filter_mode   = Enum__Classification__Filter_Mode.BETWEEN          ,
            threshold     = Safe_Float(0.3)                                     ,
            threshold_max = Safe_Float(0.7)
        ) as _:
            assert _.criterion     == Enum__Text__Classification__Criteria.NEGATIVE
            assert _.filter_mode   == Enum__Classification__Filter_Mode.BETWEEN
            assert _.threshold     == 0.3
            assert _.threshold_max == 0.7

    def test__obj(self):                                                       # Test .obj() serialization
        filter_obj = Schema__Classification__Criterion_Filter(
            criterion   = Enum__Text__Classification__Criteria.NEUTRAL            ,
            filter_mode = Enum__Classification__Filter_Mode.BELOW              ,
            threshold   = Safe_Float(0.5)
        )

        assert filter_obj.obj() == __(criterion     = 'neutral'     ,
                                      filter_mode   = 'below'    ,
                                      threshold     = 0.5        ,
                                      threshold_max = None       )

    def test__all_filter_modes(self):                                          # Test all filter mode options
        for filter_mode in Enum__Classification__Filter_Mode:
            criterion_filter = Schema__Classification__Criterion_Filter(
                criterion   = Enum__Text__Classification__Criteria.MIXED     ,
                filter_mode = filter_mode                                       ,
                threshold   = Safe_Float(0.5)
            )
            assert criterion_filter.filter_mode == filter_mode

    def test__all_criteria(self):                                              # Test all criteria options
        for criterion in Enum__Text__Classification__Criteria:
            criterion_filter = Schema__Classification__Criterion_Filter(
                criterion   = criterion                                         ,
                filter_mode = Enum__Classification__Filter_Mode.ABOVE          ,
                threshold   = Safe_Float(0.5)
            )
            assert criterion_filter.criterion == criterion