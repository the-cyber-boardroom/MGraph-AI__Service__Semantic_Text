from typing                                                                                                                     import Dict
from osbot_utils.type_safe.Type_Safe                                                                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                                            import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                                              import Safe_Str__Hash
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                                                                  import type_safe
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Grouping__Service                                        import Text__Grouping__Service
from mgraph_ai_service_semantic_text.service.text_transformation.Text__Selection__Service                                       import Text__Selection__Service
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine                           import Text__Transformation__Engine
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine__XXX_Random               import Text__Transformation__Engine__XXX_Random
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine__Hashes_Random            import Text__Transformation__Engine__Hashes_Random
from mgraph_ai_service_semantic_text.service.text_transformation.engines.Text__Transformation__Engine__ABCDE_By_Size            import Text__Transformation__Engine__ABCDE_By_Size
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Request                               import Schema__Text__Transformation__Request
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Response                              import Schema__Text__Transformation__Response
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode                              import Enum__Text__Transformation__Mode


class Text__Transformation__Service(Type_Safe):                                     # Main orchestrator for text transformations
    text_grouping              : Text__Grouping__Service                            # Service for grouping text by criteria
    text_selection             : Text__Selection__Service                           # Service for random selection
    engine__xxx_random         : Text__Transformation__Engine__XXX_Random           # Engine for xxx-random mode
    engine__hashes_random      : Text__Transformation__Engine__Hashes_Random        # Engine for hashes-random mode
    engine__abcde_by_size      : Text__Transformation__Engine__ABCDE_By_Size        # Engine for abcde-by-size mode

    def setup(self) -> 'Text__Transformation__Service':                            # Initialize all engines with shared services
        self.engine__xxx_random.text_selection    = self.text_selection
        self.engine__hashes_random.text_selection = self.text_selection
        self.engine__abcde_by_size.text_grouping  = self.text_grouping
        self.engine__abcde_by_size.setup()
        return self

    @type_safe
    def transform(self,                                                             # Transform hash mapping according to request
                  request: Schema__Text__Transformation__Request                    # Transformation request
             ) -> Schema__Text__Transformation__Response:                           # Transformation response
        try:
            engine                       = self._get_engine(request.transformation_mode)
            engine.randomness_percentage = request.randomness_percentage
            transformed_mapping          = engine.transform(request.hash_mapping)
            total_hashes                 = Safe_UInt(len(request.hash_mapping))
            transformed_hashes           = Safe_UInt(self._count_transformed_hashes(request.hash_mapping, transformed_mapping))

            return Schema__Text__Transformation__Response(transformed_mapping = transformed_mapping         ,
                                                          transformation_mode = request.transformation_mode ,
                                                          success             = True                        ,
                                                          total_hashes        = total_hashes                ,
                                                          transformed_hashes  = transformed_hashes          )

        except Exception as e:
            return Schema__Text__Transformation__Response(transformed_mapping = request.hash_mapping                 ,
                                                          transformation_mode = request.transformation_mode          ,
                                                          success             = False                                ,
                                                          total_hashes        = Safe_UInt(len(request.hash_mapping)) ,
                                                          transformed_hashes  = Safe_UInt(0)                         ,
                                                          error_message       = f"Transformation failed: {str(e)}"   )

    @type_safe
    def _get_engine(self,                                                           # Get transformation engine for mode
                    mode: Enum__Text__Transformation__Mode                          # Transformation mode
               ) -> Text__Transformation__Engine:                                   # Transformation engine
        engines = { Enum__Text__Transformation__Mode.XXX_RANDOM    : self.engine__xxx_random    ,
                    Enum__Text__Transformation__Mode.HASHES_RANDOM : self.engine__hashes_random ,
                    Enum__Text__Transformation__Mode.ABCDE_BY_SIZE : self.engine__abcde_by_size }

        engine = engines.get(mode)
        if not engine:
            raise ValueError(f"Unknown transformation mode: {mode}")

        return engine

    # todo: see what Safe_Str_* should be used instead of str in original_mapping and original_mapping
    @type_safe
    def _count_transformed_hashes(self,                                             # Count how many hashes were actually transformed
                                  original_mapping    : Dict[Safe_Str__Hash, str],  # Original hash mapping
                                  transformed_mapping : Dict[Safe_Str__Hash, str]   # Transformed hash mapping
                             ) -> Safe_UInt:                                        # Number of transformed hashes
        count = 0
        for hash_key, original_text in original_mapping.items():
            if hash_key in transformed_mapping and transformed_mapping[hash_key] != original_text:
                count += 1
        return count