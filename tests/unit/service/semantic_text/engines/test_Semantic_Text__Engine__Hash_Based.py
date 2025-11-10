from unittest                                                                                        import TestCase
from osbot_utils.testing.__                                                                          import __
from mgraph_ai_service_semantic_text.service.schemas.Schema__Semantic_Text__Classification           import Schema__Semantic_Text__Classification
from mgraph_ai_service_semantic_text.service.schemas.enums.Enum__Text__Classification__Criteria      import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.service.schemas.safe_float.Safe_Float__Text__Classification     import Safe_Float__Text__Classification
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__Hash_Based import Semantic_Text__Engine__Hash_Based


class test_Semantic_Text__Engine__Hash_Based(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.hash_engine              = Semantic_Text__Engine__Hash_Based()
        cls.classification_criteria = Enum__Text__Classification__Criteria.POSITIVITY

    def test__init__(self):
        with self.hash_engine as _:
            assert type(_)        is Semantic_Text__Engine__Hash_Based
            assert _.engine_mode  == 'text_hash'
            assert _.obj()        == __(engine_mode          = 'text_hash'     ,
                                        semantic_text_hashes = __(hash_size=10))

    def test_hash_based_classification(self):                                  # Test hash-based classification returns valid rating
        with self.hash_engine as _:
            rating = _.hash_based_classification(text='abc', classification_criteria=self.classification_criteria)
            assert type(rating) is Safe_Float__Text__Classification
            assert 0 <= rating  <= 1
            assert rating       == 0.862

    def test_classify_text__deterministic(self):                               # Test that same text always produces same rating
        with self.hash_engine as _:
            result1 = _.classify_text(text='Hello World', classification_criteria=self.classification_criteria)
            result2 = _.classify_text(text='Hello World', classification_criteria=self.classification_criteria)
            result3 = _.classify_text(text='Hello World', classification_criteria=self.classification_criteria)

            assert result1.text__classification[Enum__Text__Classification__Criteria.POSITIVITY] == result2.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]       # All three should be identical
            assert result2.text__classification[Enum__Text__Classification__Criteria.POSITIVITY] == result3.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]
            assert result1.obj() == __(text__hash           = 'b10a8db164'  ,
                                       text                 = 'Hello World' ,
                                       text__classification = __(positivity=0.7478),
                                       engine_mode          = 'text_hash'   )
            assert result1.obj() == result2.obj()
            assert result1.obj() == result3.obj()


    def test_classify_text__known_values(self):                                # Test specific known hash values for regression testing
        with self.hash_engine as _:
            result_abc   = _.classify_text(text='abc'        , classification_criteria=self.classification_criteria)
            result_xyz   = _.classify_text(text='xyz'        , classification_criteria=self.classification_criteria)
            result_hello = _.classify_text(text='Hello World', classification_criteria=self.classification_criteria)

            # These values are deterministic based on MD5 hash
            assert result_abc.obj()   == __(text                 = 'abc'                  ,
                                            text__hash           = '900150983c'           ,
                                            text__classification = __(positivity = 0.862) ,
                                            engine_mode          = 'text_hash'            )

            assert result_xyz.obj()   == __(text                 = 'xyz'                 ,
                                            text__hash           = 'd16fb36f09'          ,
                                            text__classification = __(positivity = 0.7519),
                                            engine_mode          = 'text_hash'           )

            assert result_hello.obj() == __(text                 = 'Hello World'          ,
                                            text__hash           = 'b10a8db164'           ,
                                            text__classification = __(positivity = 0.7478 ),
                                            engine_mode          = 'text_hash'            )

    def test_classify_text__different_text_different_ratings(self):            # Test that different text produces different ratings
        with self.hash_engine as _:
            result1 = _.classify_text(text='Positive', classification_criteria=self.classification_criteria)
            result2 = _.classify_text(text='Negative', classification_criteria=self.classification_criteria)
            result3 = _.classify_text(text='Neutral' , classification_criteria=self.classification_criteria)

            rating1 = result1.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]
            rating2 = result2.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]
            rating3 = result3.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]

            # All should be different
            assert rating1 != rating2
            assert rating2 != rating3
            assert rating1 != rating3

            assert result1.obj() == __(text__hash              = '3289297424'                                                ,
                                       text                    = 'Positive'                                                  ,
                                       text__classification   = __(positivity = 0.3449) ,
                                       engine_mode             = 'text_hash'                                                 )

            assert type(rating1) is Safe_Float__Text__Classification
            assert rating1.obj() == __(min_value         = None     ,
                                       max_value         = None     ,
                                       allow_none        = True     ,
                                       allow_bool        = False    ,
                                       allow_str         = True     ,
                                       allow_int         = True     ,
                                       allow_inf         = False    ,
                                       strict_type       = False    ,
                                       decimal_places    = None     ,
                                       use_decimal       = True     ,
                                       epsilon           = 1e-09    ,
                                       round_output      = True     ,
                                       clamp_to_range    = False    )
            assert rating1 ==  0.3449
            assert rating2 ==  0.1429
            assert rating3 ==  0.4723


    def test_classify_text__different_criteria(self):                          # Test that same text with different criteria produces different ratings

        text = 'The same text'

        result_positivity = self.hash_engine.classify_text(text=text, classification_criteria=Enum__Text__Classification__Criteria.POSITIVITY)
        result_negativity = self.hash_engine.classify_text(text=text, classification_criteria=Enum__Text__Classification__Criteria.NEGATIVITY)
        result_bias       = self.hash_engine.classify_text(text=text, classification_criteria=Enum__Text__Classification__Criteria.BIAS      )

        rating_positivity = result_positivity.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]
        rating_negativity = result_negativity.text__classification[Enum__Text__Classification__Criteria.NEGATIVITY]
        rating_bias       = result_bias      .text__classification[Enum__Text__Classification__Criteria.BIAS      ]

        # Same text, different criteria should produce different ratings
        assert rating_positivity != rating_negativity
        assert rating_negativity != rating_bias
        assert rating_positivity != rating_bias
        assert rating_positivity == 0.9402
        assert rating_negativity == 0.9866
        assert rating_bias       == 0.7961

    def test_classify_text__ratings_in_range(self):                            # Test that all ratings are within valid range (0.0-1.0)
        with self.hash_engine as _:
            test_texts = ['Hello', 'World', 'Test', 'Classification', 'Random text',
                         'Short', 'A very long piece of text that should still produce a valid rating',
                         '123', 'Special !@#$%', '']

            for text in test_texts:
                result = _.classify_text(text=text, classification_criteria=self.classification_criteria)
                rating = result.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]
                assert 0.0 <= float(rating) <= 1.0, f"Rating {rating} for text '{text}' is out of range"

    def test_classify_text__empty_string(self):                                # Test with empty string
        with self.hash_engine as _:
            result = _.classify_text(text='', classification_criteria=self.classification_criteria)
            assert type(result) is Schema__Semantic_Text__Classification
            rating = result.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]
            assert 0.0 <= float(rating) <= 1.0

    def test_classify_text__special_characters(self):                          # Test with special characters
        with self.hash_engine as _:
            result1 = _.classify_text(text='Hello!', classification_criteria=self.classification_criteria)
            result2 = _.classify_text(text='Hello!', classification_criteria=self.classification_criteria)

            # Should be deterministic even with special chars
            rating1 = result1.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]
            rating2 = result2.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]
            assert rating1 == rating2

    def test_classify_text__unicode(self):                                     # Test with unicode characters
        with self.hash_engine as _:
            result1 = _.classify_text(text='Hello 世界', classification_criteria=self.classification_criteria)
            result2 = _.classify_text(text='Hello 世界', classification_criteria=self.classification_criteria)

            # Should be deterministic with unicode
            rating1 = result1.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]
            rating2 = result2.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]
            assert rating1 == rating2
            assert rating1 == 0.343

    def test_classify_text__whitespace_sensitive(self):                        # Test that whitespace differences matter
        with self.hash_engine as _:
            result1 = _.classify_text(text='Hello World' , classification_criteria=self.classification_criteria)
            result2 = _.classify_text(text='HelloWorld'  , classification_criteria=self.classification_criteria)
            result3 = _.classify_text(text='Hello  World', classification_criteria=self.classification_criteria)

            rating1 = result1.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]
            rating2 = result2.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]
            rating3 = result3.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]

            # All should be different (whitespace matters)
            assert rating1 != rating2
            assert rating2 != rating3
            assert rating1 != rating3
            assert rating1 == 0.7478
            assert rating1 == 0.7478
            assert rating1 == 0.7478

    def test_classify_text__case_sensitive(self):                              # Test that case differences matter
        with self.hash_engine as _:
            result1 = _.classify_text(text='hello', classification_criteria=self.classification_criteria)
            result2 = _.classify_text(text='Hello', classification_criteria=self.classification_criteria)
            result3 = _.classify_text(text='HELLO', classification_criteria=self.classification_criteria)

            rating1 = result1.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]
            rating2 = result2.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]
            rating3 = result3.text__classification[Enum__Text__Classification__Criteria.POSITIVITY]

            # All should be different (case matters)
            assert rating1 != rating2
            assert rating2 != rating3
            assert rating1 != rating3
            assert rating1 == 0.0768
            assert rating2 == 0.0118
            assert rating3 == 0.3518

    def test_hash_based_classification__distribution(self):                    # Test that ratings are reasonably distributed
        with self.hash_engine as _:
            ratings = []
            for i in range(100):
                rating = _.hash_based_classification(text=f'Text sample {i}', classification_criteria=self.classification_criteria)
                ratings.append(float(rating))

            # Check we have variety (not all the same)
            unique_ratings = len(set(ratings))
            assert unique_ratings > 50, f"Only {unique_ratings} unique ratings out of 100"

            # Check we cover the range reasonably
            min_rating = min(ratings)
            max_rating = max(ratings)
            assert min_rating < 0.3, f"Min rating {min_rating} should be lower"
            assert max_rating > 0.7, f"Max rating {max_rating} should be higher"