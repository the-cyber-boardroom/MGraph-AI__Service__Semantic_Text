from typing                                                                                         import Dict
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                      import type_safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                        import Safe_Str__Text
from osbot_utils.utils.Misc                                                                         import random_number
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria             import Enum__Text__Classification__Criteria
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Engine_Mode          import Enum__Text__Classification__Engine_Mode
from mgraph_ai_service_semantic_text.schemas.safe_float.Safe_Float__Text__Classification            import Safe_Float__Text__Classification
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine            import Semantic_Text__Engine


class Semantic_Text__Engine__Random(Semantic_Text__Engine):                                                 # Pure random classification engine
    engine_mode : Enum__Text__Classification__Engine_Mode = Enum__Text__Classification__Engine_Mode.RANDOM  # Random mode

    @type_safe
    def classify_text(self                 ,                                                                # Generate random sentiment scores
                      text : Safe_Str__Text
                 ) -> Dict[Enum__Text__Classification__Criteria, Safe_Float__Text__Classification]:         # All 4 normalized scores (sum to 1.0)

        scores = self.generate_scores()                                                                     # Generate 4 random scores that sum to 1.0

        return scores

    def generate_scores(self                                                                                # Generate 4 random scores
                   ) -> Dict[Enum__Text__Classification__Criteria, Safe_Float__Text__Classification]:       # 4 scores summing to 1.0

        criteria_list = [Enum__Text__Classification__Criteria.POSITIVE ,        # Map samples to criteria in consistent order
                         Enum__Text__Classification__Criteria.NEGATIVE ,
                         Enum__Text__Classification__Criteria.NEUTRAL  ,
                         Enum__Text__Classification__Criteria.MIXED    ]

        scores = {}
        for criterion in criteria_list:
            value = random_number(0,100) / 100
            scores[criterion] = Safe_Float__Text__Classification(value)
        return scores
