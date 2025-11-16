from unittest                                                                                               import TestCase
from osbot_utils.testing.__                                                                                 import __
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                          import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria                     import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.safe_float.Safe_Float__Text__Classification                    import Safe_Float__Text__Classification
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Multi_Criteria_Response import Schema__Classification__Multi_Criteria_Response


class test_Schema__Classification__Multi_Criteria_Response(TestCase):

    def test__init__(self):                                                    # Test auto-initialization
        with Schema__Classification__Multi_Criteria_Response() as _:
            assert _.hash_ratings            == {}
            assert _.total_hashes            == 0
            assert _.success                 is False
            assert type(_).__name__          == 'Schema__Classification__Multi_Criteria_Response'

    def test__with_single_hash_single_criterion(self):                         # Test with one hash and one criterion
        hash_ratings = {
            Safe_Str__Hash("b10a8db164"): {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.7478)
            }
        }

        with Schema__Classification__Multi_Criteria_Response(
            hash_ratings            = hash_ratings,
            total_hashes            = Safe_UInt(1),
            success                 = True
        ) as _:
            assert len(_.hash_ratings) == 1
            assert _.total_hashes == 1
            assert _.success is True

            ratings = _.hash_ratings[Safe_Str__Hash("b10a8db164")]
            assert Enum__Text__Classification__Criteria.POSITIVE in ratings
            assert float(ratings[Enum__Text__Classification__Criteria.POSITIVE]) == 0.7478

    def test__with_single_hash_multiple_criteria(self):                        # Test with one hash and multiple criteria
        hash_ratings = {
            Safe_Str__Hash("b10a8db164"): {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.7478),
                Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.1102),
                Enum__Text__Classification__Criteria.NEUTRAL:       Safe_Float__Text__Classification(0.2316)
            }
        }

        with Schema__Classification__Multi_Criteria_Response(
            hash_ratings            = hash_ratings,
            total_hashes            = Safe_UInt(1),
            success                 = True
        ) as _:
            assert len(_.hash_ratings) == 1

            ratings = _.hash_ratings[Safe_Str__Hash("b10a8db164")]
            assert len(ratings) == 3
            assert float(ratings[Enum__Text__Classification__Criteria.POSITIVE]) == 0.7478
            assert float(ratings[Enum__Text__Classification__Criteria.NEGATIVE]) == 0.1102
            assert float(ratings[Enum__Text__Classification__Criteria.NEUTRAL      ]) == 0.2316

    def test__with_multiple_hashes(self):                                      # Test with multiple hashes
        hash_ratings = {
            Safe_Str__Hash("b10a8db164"): {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.7478),
                Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.1102)
            },
            Safe_Str__Hash("f1feeaa3d6"): {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.5080),
                Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.3946)
            }
        }

        with Schema__Classification__Multi_Criteria_Response(
            hash_ratings            = hash_ratings,
            total_hashes            = Safe_UInt(2),
            success                 = True
        ) as _:
            assert len(_.hash_ratings) == 2
            assert _.total_hashes == 2

            ratings1 = _.hash_ratings[Safe_Str__Hash("b10a8db164")]
            assert float(ratings1[Enum__Text__Classification__Criteria.POSITIVE]) == 0.7478
            assert float(ratings1[Enum__Text__Classification__Criteria.NEGATIVE]) == 0.1102

            ratings2 = _.hash_ratings[Safe_Str__Hash("f1feeaa3d6")]
            assert float(ratings2[Enum__Text__Classification__Criteria.POSITIVE]) == 0.5080
            assert float(ratings2[Enum__Text__Classification__Criteria.NEGATIVE]) == 0.3946

    def test__obj(self):                                                       # Test .obj() serialization
        hash_ratings = {
            Safe_Str__Hash("b10a8db164"): {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.7478)
            }
        }

        response = Schema__Classification__Multi_Criteria_Response(
            hash_ratings            = hash_ratings,
            total_hashes            = Safe_UInt(1),
            success                 = True
        )

        assert response.obj() == __(hash_ratings            = __(b10a8db164=__(positive=0.7478)),
                                    total_hashes            = 1                                    ,
                                    success                 = True                                 )

    def test__json(self):                                                      # Test .json() serialization
        hash_ratings = {
            Safe_Str__Hash("b10a8db164"): {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.7478),
                Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.1102)
            }
        }

        response = Schema__Classification__Multi_Criteria_Response(
            hash_ratings            = hash_ratings,
            total_hashes            = Safe_UInt(1),
            success                 = True
        )

        json_data = response.json()

        assert json_data['success'] is True
        assert json_data['total_hashes'] == 1
        assert 'b10a8db164' in json_data['hash_ratings']
        assert json_data['hash_ratings']['b10a8db164']['positive'] == 0.7478
        assert json_data['hash_ratings']['b10a8db164']['negative'] == 0.1102

    def test__empty_response(self):                                            # Test with empty hash ratings
        response = Schema__Classification__Multi_Criteria_Response(
            hash_ratings            = {},
            total_hashes            = Safe_UInt(0),
            success                 = True
        )

        assert response.hash_ratings == {}
        assert response.total_hashes == 0
        assert response.success is True

    def test__all_criteria(self):                                              # Test with all 4 criteria
        hash_ratings = {
            Safe_Str__Hash("1ba249ca59"): {
                Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.9569),
                Enum__Text__Classification__Criteria.NEGATIVE: Safe_Float__Text__Classification(0.1469),
                Enum__Text__Classification__Criteria.NEUTRAL:       Safe_Float__Text__Classification(0.2887),
                Enum__Text__Classification__Criteria.MIXED:    Safe_Float__Text__Classification(0.7091)
            }
        }

        response = Schema__Classification__Multi_Criteria_Response(
            hash_ratings            = hash_ratings,
            total_hashes            = Safe_UInt(1),
            success                 = True
        )

        ratings = response.hash_ratings[Safe_Str__Hash("1ba249ca59")]
        assert len(ratings) == 4

    def test__success_false(self):                                             # Test with success=False
        response = Schema__Classification__Multi_Criteria_Response(
            hash_ratings            = {},
            total_hashes            = Safe_UInt(0),
            success                 = False
        )

        assert response.success is False
        assert response.hash_ratings == {}
        assert response.total_hashes == 0