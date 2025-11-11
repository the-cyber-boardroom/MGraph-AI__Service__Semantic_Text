from enum import Enum


class Enum__Text__Classification__Engine_Mode(str, Enum):
    LLM_SINGLE   = 'llm_single'
    LLM_MULTIPLE = 'llm_multiple'
    RANDOM       = 'random'
    TEXT_HASH    = 'text_hash'
