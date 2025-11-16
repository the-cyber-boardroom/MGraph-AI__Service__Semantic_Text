from unittest                                                                                   import TestCase
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria         import Enum__Text__Classification__Criteria


class test_Enum__Text__Classification__Criteria(TestCase):

    def test__enum_values(self):                                                # Test all enum values exist and have correct string values
        assert Enum__Text__Classification__Criteria.POSITIVE.value == 'positive'
        assert Enum__Text__Classification__Criteria.NEGATIVE.value == 'negative'
        assert Enum__Text__Classification__Criteria.NEUTRAL.value  == 'neutral'
        assert Enum__Text__Classification__Criteria.MIXED.value    == 'mixed'

    def test__enum_members(self):                                               # Test all expected members exist
        expected_members = {'POSITIVE', 'NEGATIVE', 'NEUTRAL', 'MIXED'}
        actual_members   = {member.name for member in Enum__Text__Classification__Criteria}

        assert actual_members == expected_members

    def test__enum_count(self):                                                 # Test total number of enum members (matches AWS Comprehend sentiment scores)
        assert len(Enum__Text__Classification__Criteria) == 4

    def test__string_conversion(self):                                          # Test that enum can be compared with strings
        assert Enum__Text__Classification__Criteria.POSITIVE == 'positive'
        assert Enum__Text__Classification__Criteria.NEGATIVE == 'negative'
        assert Enum__Text__Classification__Criteria.NEUTRAL  == 'neutral'
        assert Enum__Text__Classification__Criteria.MIXED    == 'mixed'

    def test__enum_from_string(self):                                           # Test creating enum from string value
        assert Enum__Text__Classification__Criteria('positive') == Enum__Text__Classification__Criteria.POSITIVE
        assert Enum__Text__Classification__Criteria('negative') == Enum__Text__Classification__Criteria.NEGATIVE
        assert Enum__Text__Classification__Criteria('neutral')  == Enum__Text__Classification__Criteria.NEUTRAL
        assert Enum__Text__Classification__Criteria('mixed')    == Enum__Text__Classification__Criteria.MIXED

    def test__enum_iteration(self):                                             # Test iterating over enum members
        criteria = list(Enum__Text__Classification__Criteria)

        assert len(criteria) == 4
        assert Enum__Text__Classification__Criteria.POSITIVE in criteria
        assert Enum__Text__Classification__Criteria.NEGATIVE in criteria
        assert Enum__Text__Classification__Criteria.NEUTRAL in criteria
        assert Enum__Text__Classification__Criteria.MIXED in criteria

    def test__enum_uniqueness(self):                                            # Test all enum values are unique
        values = [criterion.value for criterion in Enum__Text__Classification__Criteria]
        assert len(values) == len(set(values))                                  # No duplicates

    def test__aws_comprehend_compatibility(self):                               # Test enum values match AWS Comprehend sentiment score names
        # AWS Comprehend returns sentiment scores as: Positive, Negative, Neutral, Mixed
        # Our enum values should match (lowercase)
        aws_score_names = {'positive', 'negative', 'neutral', 'mixed'}
        enum_values = {criterion.value for criterion in Enum__Text__Classification__Criteria}

        assert enum_values == aws_score_names