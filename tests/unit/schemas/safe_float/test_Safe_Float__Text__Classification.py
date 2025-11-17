import re
import pytest
from unittest                                                                            import TestCase
from mgraph_ai_service_semantic_text.schemas.safe_float.Safe_Float__Text__Classification import Safe_Float__Text__Classification


class test_Safe_Float__Text__Classification(TestCase):

    def test__init__valid_values(self):                                         # Test initialization with valid values (0.0-1.0)
        value_0   = Safe_Float__Text__Classification(0.0)
        value_mid = Safe_Float__Text__Classification(0.5)
        value_1   = Safe_Float__Text__Classification(1.0)

        assert float(value_0)   == 0.0
        assert float(value_mid) == 0.5
        assert float(value_1)   == 1.0

    def test__init__boundary_values(self):                                      # Test boundary values
        min_value = Safe_Float__Text__Classification(0.0)
        max_value = Safe_Float__Text__Classification(1.0)

        assert float(min_value) == 0.0
        assert float(max_value) == 1.0

    def test__init__invalid_below_range(self):                                  # Test values below 0.0 are rejected
        error_message =  "Safe_Float__Text__Classification must be >= 0, got -0.1"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Float__Text__Classification(-0.1)

    def test__init__invalid_above_range(self):                                  # Test values above 1.0 are rejected
        error_message = "Safe_Float__Text__Classification must be <= 1, got 1.1"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Float__Text__Classification(1.1)

    def test__range_validation(self):                                           # Test range is 0.0 to 1.0
        # Valid values
        Safe_Float__Text__Classification(0.0 )
        Safe_Float__Text__Classification(0.25)
        Safe_Float__Text__Classification(0.5 )
        Safe_Float__Text__Classification(0.75)
        Safe_Float__Text__Classification(1.0 )

        # Invalid values
        with pytest.raises(ValueError):
            Safe_Float__Text__Classification(-0.01)

        with pytest.raises(ValueError):
            Safe_Float__Text__Classification(1.01)

    def test__comparison_with_float(self):                                      # Test comparison with regular floats
        value = Safe_Float__Text__Classification(0.5)

        assert value == 0.5
        assert value != 0.6
        assert value > 0.4
        assert value < 0.6
        assert value >= 0.5
        assert value <= 0.5

    def test__comparison_with_another_safe_float(self):                         # Test comparison with another Safe_Float instance
        value1 = Safe_Float__Text__Classification(0.5)
        value2 = Safe_Float__Text__Classification(0.5)
        value3 = Safe_Float__Text__Classification(0.6)

        assert value1 == value2
        assert value1 != value3
        assert value1 < value3
        assert value3 > value1

    def test__arithmetic_operations(self):                                      # Test basic arithmetic operations
        value1 = Safe_Float__Text__Classification(0.3)
        value2 = Safe_Float__Text__Classification(0.2)

        # Addition
        result_add = value1 + value2
        assert float(result_add) == 0.5

        # Subtraction
        result_sub = value1 - value2
        assert float(result_sub) == 0.1

    def test__string_representation(self):                                      # Test string conversion
        value = Safe_Float__Text__Classification(0.75)

        assert str(value) == "0.75"

    def test__precision_handling(self):                                         # Test handling of high-precision values
        value = Safe_Float__Text__Classification(0.123456789)

        assert float(value) == 0.123456789

    def test__sentiment_score_use_case(self):                                   # Test typical sentiment score values
        # Typical sentiment scores from AWS Comprehend
        positive = Safe_Float__Text__Classification(0.85)
        negative = Safe_Float__Text__Classification(0.05)
        neutral  = Safe_Float__Text__Classification(0.08)
        mixed    = Safe_Float__Text__Classification(0.02)

        # Verify they sum to ~1.0 (allowing for rounding)
        total = positive + negative + neutral + mixed
        assert abs(float(total) - 1.0) < 0.01

    def test__type_safety(self):                                                # Test that type is preserved
        value = Safe_Float__Text__Classification(0.5)

        assert type(value) is Safe_Float__Text__Classification
        assert isinstance(value, Safe_Float__Text__Classification)