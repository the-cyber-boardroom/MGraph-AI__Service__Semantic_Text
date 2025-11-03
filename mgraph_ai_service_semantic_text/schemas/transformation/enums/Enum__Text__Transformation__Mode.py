from enum import Enum


class Enum__Text__Transformation__Mode(str, Enum):                                  # Text transformation modes for semantic analysis
    XXX_RANDOM         = 'xxx-random'                                               # Randomly mask ~50% of text with 'x' characters
    HASHES_RANDOM      = 'hashes-random'                                            # Randomly show ~50% of text as hash values
    ABCDE_BY_SIZE      = 'abcde-by-size'                                            # Group text by length, replace with letters (a,b,c,d,e)