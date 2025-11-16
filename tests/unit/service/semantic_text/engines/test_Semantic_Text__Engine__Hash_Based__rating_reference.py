from unittest                                                                                        import TestCase
from osbot_utils.testing.__                                                                          import __
from osbot_utils.type_safe.Type_Safe                                                                 import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict import Type_Safe__Dict
from osbot_utils.utils.Objects                                                                       import base_types
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria      import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Engine_Mode   import Enum__Text__Classification__Engine_Mode
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine             import Semantic_Text__Engine
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__Hash_Based import Semantic_Text__Engine__Hash_Based


class test_Semantic_Text__Engine__Hash_Based__rating_reference(TestCase):
    """
    Test the deterministic hash-based classification engine.

    IMPORTANT: This test also serves as a RATING REFERENCE GUIDE for other tests.
    The mappings in test__rating_reference_guide() show the exact ratings that will be
    returned for specific text/hash combinations used throughout the test suite.
    """

    @classmethod
    def setUpClass(cls):
        cls.engine = Semantic_Text__Engine__Hash_Based()

    def test__init(self):                                                      # Test initialization and setup
        with self.engine as _:
            assert type(_)                          is Semantic_Text__Engine__Hash_Based
            assert _.engine_mode                    == Enum__Text__Classification__Engine_Mode.TEXT_HASH
            assert _.obj()                          == __(engine_mode='text_hash')
            assert base_types(_)                    == [ Semantic_Text__Engine, Type_Safe, object]

    def test__classify_text__basic(self):                                      # Test basic text classification
        result = self.engine.classify_text(text = "Hello World")
        assert type(result) is Type_Safe__Dict
        assert result.obj() == __(positive = 0.61575136853258       ,          # Deterministic hash
                                  negative = 0.06092177291188416    ,
                                  neutral  = 0.2944552357407734     ,
                                  mixed    = 0.028871622814762493   )

        assert Enum__Text__Classification__Criteria.POSITIVE in result
        assert float(result[Enum__Text__Classification__Criteria.POSITIVE]) == 0.61575136853258 # Deterministic rating

        total = result['positive'] + result['negative'] + result['neutral'] + result['mixed']       # the sum of all ratings should be 1
        assert total == 1
        # todo: see if we don't need to also have this data
        # assert result.text                                      == "Hello World"
        # assert result.text__hash                                == "b10a8db164"                    # Deterministic hash
        # assert result.engine_mode                               == Enum__Text__Classification__Engine_Mode.TEXT_HASH
        # assert len(result.text__classification)                 == 1
        # assert Enum__Text__Classification__Criteria.POSITIVE  in result.text__classification
        #assert float(result.text__classification[Enum__Text__Classification__Criteria.POSITIVE]) == 0.7478





    def test__hash_score_for_criterion__deterministic(self):                  # Test that hash_score_for_criterion is deterministic
        text     = "Sample text"
        criteria = Enum__Text__Classification__Criteria.POSITIVE

        # Call multiple times
        rating1 = self.engine.hash_score_for_criterion(text, criteria)
        rating2 = self.engine.hash_score_for_criterion(text, criteria)
        rating3 = self.engine.hash_score_for_criterion(text, criteria)

        # All should be identical
        assert float(rating1) == float(rating2) == float(rating3)
        assert float(rating1) == 0.1136                             # these values are not normalised
        assert rating1        == 0.1136


    def test__hash_score_for_criterion__range(self):                          # Test that ratings are within valid range
        test_texts = [
            "Hello World",
            "Test Text",
            "Sample text",
            "Another text",
            "Short",
            "Very long text with many words and characters",
            ""
        ]

        for text in test_texts:
            for criteria in Enum__Text__Classification__Criteria:
                rating = self.engine.hash_score_for_criterion(text, criteria)
                rating_float = float(rating)

                # Must be in range [0.0, 1.0]
                assert 0.0 <= rating_float <= 1.0, f"Rating {rating_float} out of range for text '{text}' and criteria {criteria}"

    def test__hash_score_for_criterion__distribution(self):                   # Test that ratings are well-distributed
        """
        Test that the hash-based classification produces well-distributed ratings
        across the 0.0-1.0 range (not clustered in one area)
        """
        test_texts = [f"Text {i}" for i in range(100)]
        criteria = Enum__Text__Classification__Criteria.POSITIVE

        ratings = [float(self.engine.hash_score_for_criterion(text, criteria)) for text in test_texts]

        # Check distribution across quartiles
        q1 = sum(1 for r in ratings if 0.00 <= r < 0.25)
        q2 = sum(1 for r in ratings if 0.25 <= r < 0.50)
        q3 = sum(1 for r in ratings if 0.50 <= r < 0.75)
        q4 = sum(1 for r in ratings if 0.75 <= r <= 1.00)

        # Each quartile should have at least 15% of values (allowing for statistical variance)
        assert q1 >= 15, f"Q1 too small: {q1}"
        assert q2 >= 15, f"Q2 too small: {q2}"
        assert q3 >= 15, f"Q3 too small: {q3}"
        assert q4 >= 15, f"Q4 too small: {q4}"

    # ========================================
    # RATING REFERENCE GUIDE
    # ========================================

    def test__rating_reference_guide__basic_hashes(self):                      # Reference guide for basic test hashes (Level 1 & 2)
        """
        RATING REFERENCE GUIDE - Basic Hashes

        These are the deterministic ratings used in Level 1 and Level 2 tests.
        Use this as a reference when writing or debugging tests.
        """

        # abc1234567 - "Hello World"
        result = self.engine.classify_text("Hello World")
        assert result.obj() == __(positive = 0.61575136853258        ,
                                  negative = 0.06092177291188416    ,
                                  neutral  = 0.2944552357407734     ,
                                  mixed    = 0.028871622814762493   )

        # def1234567 - "Test Text"
        result = self.engine.classify_text("Test Text")
        assert result.obj() == __(positive = 0.2842339724966105     ,
                                  negative = 0.25290528762347475    ,
                                  neutral  = 0.1380980050358319     ,
                                  mixed    = 0.3247627348440829     )



    def test__rating_reference_guide__level_2_filter_tests(self):              # Reference guide for Level 2 filter test hashes
        """
        RATING REFERENCE GUIDE - Level 2 Filter Tests

        Hash/text combinations used in multi-criteria filter tests.
        """

        # 1ba249ca59 - "Sample text" (used in test__classify__multi__rate__all_criteria)
        mappings = [
            ("1ba249ca59", "Sample text", { Enum__Text__Classification__Criteria.POSITIVE: 0.05257312106627175,
                                            Enum__Text__Classification__Criteria.NEGATIVE: 0.4057293594964828 ,
                                            Enum__Text__Classification__Criteria.NEUTRAL : 0.3871714179933358 ,
                                            Enum__Text__Classification__Criteria.MIXED   : 0.15452610144390966
            }),

            # b5ead10d6e - "Positive text" (used in test__classify__multi__filter__and__basic)
            ("b5ead10d6e", "Positive text", { 'mixed': 0.11676211642020685,
                                              'negative': 0.3533635353449013,
                                              'neutral': 0.11800153859304215,
                                              'positive': 0.41187280964184975}),

            # 9204d57da8 - "Another text"
            ("9204d57da8", "Another text", {  'mixed': 0.5798831815839203,
                                              'negative': 0.10333276069403882,
                                              'neutral': 0.10238790585809998,
                                              'positive': 0.2143961518639409}
),

            # 8bfa8e0684 - "Test content"
            ("8bfa8e0684", "Test content", {  'mixed': 0.2142907675981606,
                                              'negative': 0.5133356915458083,
                                              'neutral': 0.21995047753802618,
                                              'positive': 0.052423063318004955}),

            # c5dd1b2697 - "Sample" (used in test__classify__multi__filter__and__full_ratings)
            ("c5dd1b2697", "Sample"      , {  'mixed': 0.12681744749596122,
                                              'negative': 0.21267020540041542,
                                              'neutral': 0.39464574198015234,
                                              'positive': 0.26586660512347104})]

        for expected_hash, text, expected_ratings in mappings:
            result = self.engine.classify_text(text)
            assert result == expected_ratings



    def test__rating_reference_guide__or_logic_tests(self):                    # Reference guide for OR logic test hashes
        """
        RATING REFERENCE GUIDE - OR Logic Tests
        """

        mappings = [
            # c3d45f8fe6 - "High positive"
            ("c3d45f8fe6", "High positive", { 'mixed': 0.14332995013459246,
                                              'negative': 0.2795110542341468,
                                              'neutral': 0.23216098142182603,
                                              'positive': 0.3449980142094347}),

            # 58537f27d7 - "High negative"
            ("58537f27d7", "High negative", { 'mixed': 0.22024530587522714,
                                              'negative': 0.3426711084191399,
                                              'neutral': 0.13056480920654148,
                                              'positive': 0.3065187764990915}),

            # b0a2013306 - "Low both"
            ("b0a2013306", "Low both", { 'mixed': 0.2795038997570643,
                                          'negative': 0.05108042449814602,
                                          'neutral': 0.3830072880705792,
                                          'positive': 0.28640838767421045}),

            # b840f6f2ae - "Text A"
            ("b840f6f2ae", "Text A", { 'mixed': 0.09479195370625516,
                                       'negative': 0.32162211812253144,
                                       'neutral': 0.18664462202626986,
                                       'positive': 0.3969413061449435}),

            # eb5deeca9c - "Text B"
            ("eb5deeca9c", "Text B", { 'mixed': 0.26795180722891565,
                                      'negative': 0.06244406196213425,
                                      'neutral': 0.05301204819277108,
                                      'positive': 0.616592082616179}),

            # 9dffbf69ff - "Text"
            ("9dffbf69ff", "Text", { 'mixed': 0.05983085203047459,
                                      'negative': 0.22848955056965123,
                                      'neutral': 0.11148388900538198,
                                      'positive': 0.6001957083944922})]

        for expected_hash, text, expected_ratings in mappings:
            result = self.engine.classify_text(text)
            assert result == expected_ratings

    def test__rating_reference_guide__filter_mode_tests(self):                 # Reference guide for filter mode test hashes
        """
        RATING REFERENCE GUIDE - Filter Mode Tests (BETWEEN, mixed modes)
        """

        # aaa0000012 - "Test text" (BETWEEN mode test)
        result = self.engine.classify_text("Test text")
        assert result.obj() == __( positive=0.26393868216095934,
                                   negative=0.08311699015123418,
                                   neutral=0.32785263938682163,
                                   mixed=0.3250916883009849)

        # aaa0000013 - "Balanced text" (mixed ABOVE/BELOW modes test)
        result = self.engine.classify_text("Balanced text")
        assert result.obj() == __( positive=0.11932369381438536,
                                   negative=0.43003649466438765,
                                   neutral=0.4421397884233381,
                                   mixed=0.008500023097888852)


        # aaa0000014 - "Test"
        result = self.engine.classify_text("Test")
        assert result.obj() == __( positive=0.4257015636325981,
                                   negative=0.10598529564046806,
                                   neutral=0.22108315211763488,
                                   mixed=0.24722998860929896)


    def test__rating_reference_guide__deterministic_multiple_hashes(self):     # Reference guide for deterministic multi-hash tests
        """
        RATING REFERENCE GUIDE - Deterministic Multiple Hash Test

        Used in test__classify__multi__filter__deterministic_results
        """

        mappings = [
            ("20c8b16b2a", "Text 0", { 'mixed': 0.20708697653014266,
  'negative': 0.09700874367234238,
  'neutral': 0.14974689369535205,
  'positive': 0.5461573861021629}),

            ("161a6b3572", "Text 1",{ 'mixed': 0.29291380222104707,
  'negative': 0.23966155473294554,
  'neutral': 0.39481755684822845,
  'positive': 0.07260708619777895}),

            ("48e47cee20", "Text 2", { 'mixed': 0.38793757450959143,
  'negative': 0.2363715183700011,
  'neutral': 0.3004768613850656,
  'positive': 0.07521404573534193}),

            ("0d96bbc2ec", "Text 3", { 'mixed': 0.30304736434654095,
  'negative': 0.17302413962981208,
  'neutral': 0.32292912942501234,
  'positive': 0.20099936659863465}
),

            ("c133c1f81c", "Text 4", { 'mixed': 0.23492981007431873,
  'negative': 0.2594549958711808,
  'neutral': 0.13835672997522708,
  'positive': 0.3672584640792733}
),
        ]

        for expected_hash, text, expected_ratings in mappings:
            result = self.engine.classify_text(text)

            assert result == expected_ratings

    def test__rating_reference_guide__summary_table(self):                     # Summary table of all ratings for quick reference
        """
        QUICK REFERENCE SUMMARY

        This test generates a summary table showing ALL hash/text/rating combinations
        used throughout the test suite. Use this for quick lookups.
        """

        all_mappings = [("b10a8db164", "Hello World"  , 0.61575136853258     , 0.06092177291188416 , 0.2944552357407734  , 0.028871622814762493 ),
                        ("f1feeaa3d6", "Test Text"    , 0.2842339724966105   , 0.25290528762347475 , 0.1380980050358319  , 0.3247627348440829   ),
                        ("1ba249ca59", "Sample text"  , 0.05257312106627175  , 0.4057293594964828  , 0.3871714179933358  , 0.15452610144390966  ),
                        ("b5ead10d6e", "Positive text", 0.41187280964184975  , 0.3533635353449013  , 0.11800153859304215 , 0.11676211642020685  ),
                        ("9204d57da8", "Another text" , 0.2143961518639409   , 0.10333276069403882 , 0.10238790585809998 , 0.5798831815839203   ),
                        ("8bfa8e0684", "Test content" , 0.052423063318004955 , 0.5133356915458083  , 0.21995047753802618 , 0.2142907675981606   ),
                        ("c5dd1b2697", "Sample"       , 0.26586660512347104  , 0.21267020540041542 , 0.39464574198015234 , 0.12681744749596122  ),
                        ("c3d45f8fe6", "High positive", 0.3449980142094347   , 0.2795110542341468  , 0.23216098142182603 , 0.14332995013459246  ),
                        ("58537f27d7", "High negative", 0.3065187764990915   , 0.3426711084191399  , 0.13056480920654148 , 0.22024530587522714  ),
                        ("b0a2013306", "Low both"     , 0.28640838767421045  , 0.05108042449814602 , 0.3830072880705792  , 0.2795038997570643   ),
                        ("b840f6f2ae", "Text A"       , 0.3969413061449435   , 0.32162211812253144 , 0.18664462202626986 , 0.09479195370625516  ),
                        ("eb5deeca9c", "Text B"       , 0.616592082616179    , 0.06244406196213425 , 0.05301204819277108 , 0.26795180722891565  ),
                        ("9dffbf69ff", "Text"         , 0.6001957083944922   , 0.22848955056965123 , 0.11148388900538198 , 0.05983085203047459  ),
                        ("aaaf7028b8", "Test text"    , 0.26393868216095934  , 0.08311699015123418 , 0.32785263938682163 , 0.3250916883009849   ),
                        ("c298542a7f", "Balanced text", 0.11932369381438536  , 0.43003649466438765 , 0.4421397884233381  , 0.008500023097888852 ),
                        ("0cbc6611f5", "Test"         , 0.4257015636325981   , 0.10598529564046806 , 0.22108315211763488 , 0.24722998860929896  ),
                        ("20c8b16b2a", "Text 0"       , 0.5461573861021629   , 0.09700874367234238 , 0.14974689369535205 , 0.20708697653014266  ),
                        ("161a6b3572", "Text 1"       , 0.07260708619777895  , 0.23966155473294554 , 0.39481755684822845 , 0.29291380222104707  ),
                        ("48e47cee20", "Text 2"       , 0.07521404573534193  , 0.2363715183700011  , 0.3004768613850656  , 0.38793757450959143  ),
                        ("0d96bbc2ec", "Text 3"       , 0.20099936659863465  , 0.17302413962981208 , 0.32292912942501234 , 0.30304736434654095  ),
                        ("c133c1f81c", "Text 4"       , 0.3672584640792733   , 0.2594549958711808  , 0.13835672997522708 , 0.23492981007431873  ),
                    ]




        # Verify all mappings
        for hash_id, text, pos, neg, bias, urg in all_mappings:
            result      = self.engine.classify_text(text)

            assert result[Enum__Text__Classification__Criteria.POSITIVE] == pos
            assert result[Enum__Text__Classification__Criteria.NEGATIVE] == neg
            assert result[Enum__Text__Classification__Criteria.NEUTRAL ] == bias
            assert result[Enum__Text__Classification__Criteria.MIXED   ] == urg