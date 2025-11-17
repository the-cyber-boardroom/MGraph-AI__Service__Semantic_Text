from unittest                                                                                   import TestCase
from osbot_utils.testing.__                                                                     import __
from osbot_utils.type_safe.primitives.core.Safe_UInt                                            import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash              import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria         import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.safe_float.Safe_Float__Text__Classification        import Safe_Float__Text__Classification
from mgraph_ai_service_semantic_text.schemas.classification.Schema__Classification__Response    import Schema__Classification__Response


class test_Schema__Classification__Response(TestCase):

    def test__init__(self):                                                    # Test auto-initialization
        with Schema__Classification__Response() as _:
            assert _.hash_ratings            == {}
            assert type(_.total_hashes)      is Safe_UInt
            assert _.success                 is False
            assert type(_).__name__          == 'Schema__Classification__Response'

    def test__with_success_response(self):                                     # Test successful classification response
        hash_ratings = {Safe_Str__Hash("abc1234567"): {"positive": Safe_Float__Text__Classification(0.8)},
                        Safe_Str__Hash("def1234567"): {"positive": Safe_Float__Text__Classification(0.3)}}

        with Schema__Classification__Response(hash_ratings            = hash_ratings                                   ,
                                              total_hashes            = Safe_UInt(2)                                   ,
                                              success                 = True                                           ) as _:
            assert _.success                 is True
            assert _.total_hashes            == 2
            assert len(_.hash_ratings)       == 2
            assert _.hash_ratings[Safe_Str__Hash("abc1234567")]["positive"] == 0.8
            assert _.hash_ratings[Safe_Str__Hash("def1234567")]["positive"] == 0.3

    def test__obj_comparison(self):                                            # Test .obj() method for state verification
        hash_ratings = {Safe_Str__Hash("abc1234567"): {"positive": Safe_Float__Text__Classification(0.5)}}

        with Schema__Classification__Response(hash_ratings            = hash_ratings                                   ,
                                              total_hashes            = Safe_UInt(1)                                   ,
                                              success                 = True                                           ) as _:
            assert _.obj() == __(hash_ratings            = __(abc1234567 = __(positive=0.5))  ,
                                 total_hashes            = 1                                      ,
                                 success                 = True                                   )

    def test__json_round_trip(self):                                           # Test JSON serialization round-trip
        hash_ratings = {Safe_Str__Hash("abc1234567"): {"positive": Safe_Float__Text__Classification(0.7)}}

        with Schema__Classification__Response(hash_ratings            = hash_ratings                                   ,
                                              total_hashes            = Safe_UInt(1)                                   ,
                                              success                 = True                                           ) as _:
            json_data = _.json()
            restored  = Schema__Classification__Response(**json_data)
            assert restored.obj() == __(hash_ratings=__(abc1234567=__(positive=0.7)),
                                        total_hashes=1, success=True)

            assert restored.success                 == True
            assert restored.total_hashes            == 1
            assert restored.hash_ratings            == {Safe_Str__Hash('abc1234567'): {Enum__Text__Classification__Criteria.POSITIVE: Safe_Float__Text__Classification(0.7) }}
