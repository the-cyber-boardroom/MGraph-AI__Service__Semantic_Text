from types                                                                                               import NoneType
from unittest                                                                                            import TestCase
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text                            import Safe_Str__Comprehend__Text
from osbot_utils.testing.__                                                                              import __
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                                    import Type_Safe__Dict
from osbot_utils.utils.Objects                                                                           import base_classes
from osbot_utils.type_safe.Type_Safe                                                                     import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                       import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.Schema__Semantic_Text__Classification                       import Schema__Semantic_Text__Classification
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria                  import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Engine_Mode               import Enum__Text__Classification__Engine_Mode
from mgraph_ai_service_semantic_text.schemas.safe_float.Safe_Float__Text__Classification                 import Safe_Float__Text__Classification
import pytest


class test_Schema__Semantic_Text__Classification(TestCase):

    @classmethod
    def setUpClass(cls):                                                                    # Setup shared test data once
        cls.sample_text          = "This is a test text for classification"
        cls.sample_hash          = Safe_Str__Hash("abc123def4")
        cls.sample_classification = {
            Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.75),
            Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.10),
            Enum__Text__Classification__Criteria.NEUTRAL : Safe_Float__Text__Classification(0.12),
            Enum__Text__Classification__Criteria.MIXED   : Safe_Float__Text__Classification(0.03)
        }
        cls.sample_engine_mode = Enum__Text__Classification__Engine_Mode.TEXT_HASH

    def test__init__(self):                                                                 # Test Type_Safe auto-initialization
        with Schema__Semantic_Text__Classification() as _:
            assert type(_)         is Schema__Semantic_Text__Classification                 # Verify type
            assert base_classes(_) == [Type_Safe, object]                                   # Verify inheritance

            assert type(_.text)                 is Safe_Str__Comprehend__Text                           # Verify field types
            assert type(_.text__hash)           in [Safe_Str__Hash, type(None)]             # Can be None initially
            assert type(_.text__classification) is Type_Safe__Dict
            assert type(_.engine_mode)          is NoneType

            assert _.text                       == ""                                       # Default values
            assert _.text__hash                 is None
            assert _.text__classification       == {}
            assert _.engine_mode                is None

    def test__init__with_all_fields(self):                                                  # Test initialization with all fields provided
        with Schema__Semantic_Text__Classification(text                 = self.sample_text          ,
                                                   text__hash           = self.sample_hash          ,
                                                   text__classification = self.sample_classification,
                                                   engine_mode          = self.sample_engine_mode   ) as _:

            assert _.text                 == self.sample_text                               # Verify all fields set correctly
            assert _.text__hash           == self.sample_hash
            assert _.text__classification == self.sample_classification
            assert _.engine_mode          == self.sample_engine_mode

            assert type(_.text)                 is Safe_Str__Comprehend__Text               # Verify types preserved
            assert type(_.text__hash)           is Safe_Str__Hash
            assert type(_.text__classification) is Type_Safe__Dict
            assert type(_.engine_mode)          is Enum__Text__Classification__Engine_Mode

    def test__init__with_text_only(self):                                                   # Test initialization with minimal fields
        text = "Sample text for testing"

        with Schema__Semantic_Text__Classification(text=text) as _:
            assert _.text                 == text
            assert _.text__hash           is None                                           # Optional field
            assert _.text__classification == {}                                             # Empty dict
            assert _.engine_mode          is None

    def test_text__auto_conversion_from_str(self):                                          # Test auto-conversion of text field from str
        raw_text = "Raw string input"

        with Schema__Semantic_Text__Classification(text=raw_text) as _:
            assert _.text      == raw_text                                                  # Value preserved
            assert type(_.text) is Safe_Str__Comprehend__Text                               # Auto-converted to Safe_Str__Comprehend__Text

    def test_text__hash__auto_conversion_from_str(self):                                    # Test auto-conversion of hash field from str
        raw_hash = "abcd123abc"

        with Schema__Semantic_Text__Classification(text="test", text__hash=raw_hash) as _:
            assert _.text__hash      == raw_hash                                            # Value preserved
            assert type(_.text__hash) is Safe_Str__Hash                                     # Auto-converted to Safe_Str__Hash

    def test_engine_mode__auto_conversion_from_str(self):                                   # Test auto-conversion of engine_mode from string
        engine_mode_str = "text_hash"

        with Schema__Semantic_Text__Classification(text        = "test"         ,
                                                   engine_mode = engine_mode_str) as _:
            assert _.engine_mode      == Enum__Text__Classification__Engine_Mode.TEXT_HASH  # Auto-converted to enum
            assert type(_.engine_mode) is Enum__Text__Classification__Engine_Mode

    def test_engine_mode__invalid_value(self):                                              # Test validation of engine_mode field
        with pytest.raises(ValueError) as exc_info:
            Schema__Semantic_Text__Classification(text="test", engine_mode="invalid_mode")

        assert "engine_mode" in str(exc_info.value).lower()                                 # Error should mention field

    def test_text__classification__with_all_criteria(self):                                 # Test classification dict with all four criteria
        classification = {
            Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.60),
            Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.20),
            Enum__Text__Classification__Criteria.NEUTRAL : Safe_Float__Text__Classification(0.15),
            Enum__Text__Classification__Criteria.MIXED   : Safe_Float__Text__Classification(0.05)
        }

        with Schema__Semantic_Text__Classification(text                 = "test text"    ,
                                                   text__classification = classification) as _:

            assert len(_.text__classification) == 4                                         # All four criteria present

            for criterion in Enum__Text__Classification__Criteria:                         # Verify all criteria exist
                assert criterion in _.text__classification
                assert type(_.text__classification[criterion]) is Safe_Float__Text__Classification

            total = sum(float(score) for score in _.text__classification.values())         # Scores should sum to 1.0
            assert 0.99 <= total <= 1.01

    def test_text__classification__with_partial_criteria(self):                             # Test classification with only some criteria
        classification = {
            Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.80),
            Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.20)
        }

        with Schema__Semantic_Text__Classification(text                 = "test text"    ,
                                                   text__classification = classification) as _:

            assert len(_.text__classification) == 2                                         # Only two criteria
            assert Enum__Text__Classification__Criteria.POSITIVE in _.text__classification
            assert Enum__Text__Classification__Criteria.NEGATIVE in _.text__classification

    def test_text__classification__score_boundaries(self):                                  # Test score values at boundaries (0.0 and 1.0)
        classification = {
            Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(1.0),
            Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.0),
            Enum__Text__Classification__Criteria.NEUTRAL : Safe_Float__Text__Classification(0.0),
            Enum__Text__Classification__Criteria.MIXED   : Safe_Float__Text__Classification(0.0)
        }

        with Schema__Semantic_Text__Classification(text                 = "test"         ,
                                                   text__classification = classification) as _:

            assert float(_.text__classification[Enum__Text__Classification__Criteria.POSITIVE]) == 1.0
            assert float(_.text__classification[Enum__Text__Classification__Criteria.NEGATIVE]) == 0.0
            assert float(_.text__classification[Enum__Text__Classification__Criteria.NEUTRAL ]) == 0.0
            assert float(_.text__classification[Enum__Text__Classification__Criteria.MIXED   ]) == 0.0

    def test_text__classification__invalid_score_above_max(self):                           # Test invalid score above 1.0
        with pytest.raises(ValueError):
            classification = {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(1.5)
            }
            Schema__Semantic_Text__Classification(text                 = "test"         ,
                                                  text__classification = classification)

    def test_text__classification__invalid_score_below_min(self):                           # Test invalid score below 0.0
        with pytest.raises(ValueError):
            classification = {
                Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(-0.1)
            }
            Schema__Semantic_Text__Classification(text                 = "test"         ,
                                                  text__classification = classification)

    def test_obj__comparison(self):                                                         # Test .obj() method for comprehensive comparison
        with Schema__Semantic_Text__Classification(text                 = self.sample_text          ,
                                                   text__hash           = self.sample_hash          ,
                                                   text__classification = self.sample_classification,
                                                   engine_mode          = self.sample_engine_mode   ) as _:

            assert _.obj() == __(  text__hash = self.sample_hash    ,
                                   text       = self.sample_text    ,
                                   text__classification = __(positive = 0.75,
                                                             negative = 0.1,
                                                             neutral = 0.12,
                                                             mixed   = 0.03),
                                   engine_mode        = self.sample_engine_mode)
            assert type(self.sample_classification) == dict
            assert self.sample_classification == { Enum__Text__Classification__Criteria.MIXED    : 0.03 ,
                                                   Enum__Text__Classification__Criteria.NEGATIVE : 0.1  ,
                                                   Enum__Text__Classification__Criteria.NEUTRAL  : 0.12 ,
                                                   Enum__Text__Classification__Criteria.POSITIVE : 0.75 ,
                                                  }
    def test_serialization_round_trip(self):                                                # Test serialization and deserialization preserves all data
        original = Schema__Semantic_Text__Classification(text                 = self.sample_text          ,
                                                         text__hash           = self.sample_hash          ,
                                                         text__classification = self.sample_classification,
                                                         engine_mode          = self.sample_engine_mode   )

        serialized   = original.json()                                                      # Serialize to JSON
        deserialized = Schema__Semantic_Text__Classification.from_json(serialized)          # Deserialize back

        assert deserialized.text                 == original.text                           # Verify all fields preserved
        assert deserialized.text__hash           == original.text__hash
        assert deserialized.engine_mode          == original.engine_mode

        for criterion in self.sample_classification.keys():                                 # Verify classification dict preserved
            assert criterion in deserialized.text__classification
            assert float(deserialized.text__classification[criterion]) == float(original.text__classification[criterion])

    def test_empty_text__classification(self):                                              # Test with empty classification dict
        with Schema__Semantic_Text__Classification(text                 = "test text",
                                                   text__classification = {}       ) as _:

            assert _.text__classification == {}
            assert type(_.text__classification) is Type_Safe__Dict
            assert len(_.text__classification)  == 0

    def test_different_engine_modes(self):                                                  # Test all available engine modes
        for engine_mode in Enum__Text__Classification__Engine_Mode:
            with Schema__Semantic_Text__Classification(text        = "test text",
                                                       engine_mode = engine_mode ) as _:
                assert _.engine_mode == engine_mode
                assert type(_.engine_mode) is Enum__Text__Classification__Engine_Mode

    def test_text__special_characters(self):                                                # Test text with special characters
        special_text = "Test with émojis 😀 and spëcial çharacters: @#$%^&*()"

        with Schema__Semantic_Text__Classification(text=special_text) as _:
            assert _.text == special_text                                                   # Special characters preserved
            assert type(_.text) is Safe_Str__Comprehend__Text

    def test_text__very_long(self):                                                         # Test with very long text
        long_text = "word " * 1000                                                          # 1000 words

        with Schema__Semantic_Text__Classification(text=long_text) as _:
            assert _.text      == long_text
            assert len(_.text) == len(long_text)

    def test_hash__format(self):                                                            # Test hash field accepts various hash formats
        test_hashes = [ "abc1234aaa",
                        "def456789a",
                        "0123456789",
                        "aaaaafffff"]

        for test_hash in test_hashes:
            with Schema__Semantic_Text__Classification(text       = "test"    ,
                                                       text__hash = test_hash ) as _:
                assert _.text__hash == test_hash
                assert type(_.text__hash) is Safe_Str__Hash

    def test_classification__auto_conversion_float_values(self):                            # Test classification accepts raw float values and converts them
        classification_raw = {
            Enum__Text__Classification__Criteria.POSITIVE: 0.75,                            # Raw float
            Enum__Text__Classification__Criteria.NEGATIVE: 0.25                             # Raw float
        }

        with Schema__Semantic_Text__Classification(text                 = "test"             ,
                                                   text__classification = classification_raw) as _:

            for criterion, score in _.text__classification.items():
                assert type(score) is Safe_Float__Text__Classification                      # Auto-converted to Safe_Float
                assert 0.0 <= float(score) <= 1.0

    def test_none_values(self):                                                             # Test handling of None values for optional fields
        with Schema__Semantic_Text__Classification(text       = "test text",
                                                   text__hash = None       ) as _:

            assert _.text       == "test text"
            assert _.text__hash is None                                                     # None preserved for optional field

    def test_obj__with_none_hash(self):                                                     # Test .obj() comparison with None hash value
        with Schema__Semantic_Text__Classification(text       = "test",
                                                   text__hash = None   ) as _:

            assert _.obj() == __(text                 = "test"                                   ,
                                text__hash           = None                                     ,
                                text__classification = __()                                       ,
                                engine_mode          = None)

    def test_multiple_instances__independence(self):                                        # Test multiple instances don't share state
        schema1 = Schema__Semantic_Text__Classification(text="text1", text__hash="aaa0000001")
        schema2 = Schema__Semantic_Text__Classification(text="text2", text__hash="bbb0000002")

        assert schema1.text       != schema2.text                                           # Independent text values
        assert schema1.text__hash != schema2.text__hash                                     # Independent hash values

        schema1.text__classification[Enum__Text__Classification__Criteria.POSITIVE] = Safe_Float__Text__Classification(0.9)

        assert len(schema1.text__classification) == 1                                       # Schema1 has classification
        assert len(schema2.text__classification) == 0                                       # Schema2 unaffected