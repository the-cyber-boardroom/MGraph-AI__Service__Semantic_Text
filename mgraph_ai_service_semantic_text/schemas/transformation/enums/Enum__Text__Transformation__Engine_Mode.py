from enum import Enum


class Enum__Text__Transformation__Engine_Mode(str, Enum):                      # Engine modes for text transformation (matching classification pattern)
    RANDOM         = 'random'                                                   # Pure random transformation (non-deterministic)
    TEXT_HASH      = 'text-hash'                                                # Hash-based deterministic transformation
    AWS_COMPREHEND = 'aws-comprehend'                                           # AWS Comprehend ML-based transformation
    LLM            = 'llm'                                                      # LLM-based intelligent transformation (future)