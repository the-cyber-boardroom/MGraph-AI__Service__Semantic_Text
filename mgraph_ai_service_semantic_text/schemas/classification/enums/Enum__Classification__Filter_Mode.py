from enum import Enum


class Enum__Classification__Filter_Mode(str, Enum): # Filter comparison operations for classification criteria
    ABOVE   = 'above'                               # rating > threshold
    BELOW   = 'below'                               # rating < threshold
    BETWEEN = 'between'                             # min < rating < max
    EQUALS  = 'equals'                              # rating == value (exact match)
