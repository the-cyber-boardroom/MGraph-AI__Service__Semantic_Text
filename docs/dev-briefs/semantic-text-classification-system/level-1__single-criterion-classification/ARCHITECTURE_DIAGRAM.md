# Level 1 Classification - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CALLER / CLIENT                                    │
│                                                                              │
│  Example Usage:                                                              │
│  1. Get ratings: POST /semantic-classification/single/rate                   │
│  2. Filter hashes: POST /semantic-classification/single/filter               │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                │ HTTP Request
                                │
┌───────────────────────────────▼──────────────────────────────────────────────┐
│                    FastAPI Layer (HTTP → Python)                             │
│                                                                              │
│  Routes__Semantic_Classification                                             │
│  ┌─────────────────────────────────────────────────────────────┐             │
│  │  classify__single__rate(request: Schema__Classification__Request)         │
│  │  classify__single__filter(request: Schema__Classification__Filter_Request)│
│  └─────────────────────────────────────────────────────────────┘             │
│                                                                              │
│  Input Schemas (Type_Safe):                                                  │
│  • Schema__Classification__Request                                           │
│  • Schema__Classification__Filter_Request                                    │
│      - filter_mode: ABOVE | BELOW | BETWEEN | EQUALS                         │
│      - output_mode: HASHES_ONLY | HASHES_WITH_TEXT | FULL_RATINGS            │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                │ Calls
                                │
┌───────────────────────────────▼──────────────────────────────────────────────┐
│                    Service Layer (Business Logic)                            │
│                                                                              │
│  Classification__Filter__Service                                             │
│  ┌─────────────────────────────────────────────────────────────┐             │
│  │  classify_all(request)                                      │             │
│  │    → Gets classification for each hash                      │             │
│  │                                                             │             │
│  │  filter_by_criteria(request)                                │             │
│  │    → Calls classify_all()                                   │             │
│  │    → Calls _apply_filter()                                  │             │
│  │    → Calls _build_filter_response()                         │             │
│  │                                                             │             │
│  │  _apply_filter(ratings, mode, threshold, threshold_max)     │             │
│  │    → Applies ABOVE/BELOW/BETWEEN/EQUALS logic               │             │
│  │                                                             │             │
│  │  _build_filter_response(filtered, mode)                     │             │
│  │    → Builds response based on output_mode                   │             │
│  └─────────────────────────────────────────────────────────────┘             │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                │ Uses
                                │
┌───────────────────────────────▼──────────────────────────────────────────────┐
│               Semantic Text Service (Existing Infrastructure)                │
│                                                                              │
│  Semantic_Text__Service                                                      │
│  ┌──────────────────────────────────────────────────────────────┐            │
│  │  classify_text(text: str) → Schema__Semantic_Text__Classification         │
│  │                                                              │            │
│  │  Returns:                                                    │            │
│  │  • text                                                      │            │
│  │  • text__hash                                                │            │
│  │  • text__classification = {                                  │            │
│  │      Enum__Text__Classification__Criteria.POSITIVITY: 0.73   │            │
│  │    }                                                         │            │
│  │  • engine_mode = 'random'                                    │            │
│  └──────────────────────────────────────────────────────────────┘            │
└───────────────────────────────┬──────────────────────────────────────────────┘
                                │
                                │ Uses
                                │
┌───────────────────────────────▼──────────────────────────────────────────────┐
│                   Classification Engine (Pluggable)                          │
│                                                                              │
│  Semantic_Text__Engine__Random (Current)                                     │
│  ┌──────────────────────────────────────────────────────────────┐            │
│  │  classify_text(text) → Schema__Semantic_Text__Classification │            │
│  │    • Generates random rating (0.0-1.0)                       │            │
│  │    • Deterministic based on text hash                        │            │
│  └──────────────────────────────────────────────────────────────┘            │
│                                                                              │
│  Future Engines (Pluggable):                                                 │
│  • Semantic_Text__Engine__Hash_Based                                         │
│  • Semantic_Text__Engine__Pre_Configured                                     │
│  • Semantic_Text__Engine__LLM_Single                                         │
│  • Semantic_Text__Engine__LLM_Multiple                                       │
└──────────────────────────────────────────────────────────────────────────────┘


DATA FLOW EXAMPLE: Filter Request
═══════════════════════════════════════════════════════════════════════════════

1. CALLER SENDS REQUEST
   POST /semantic-classification/single/filter
   {
     "hash_mapping": {
       "abc1234567": "Happy sunny day",
       "def1234567": "Terrible rainy day"
     },
     "classification_criteria": "positivity",
     "filter_mode": "above",
     "threshold": 0.5,
     "output_mode": "full-ratings"
   }
   │
   ▼
2. ROUTES LAYER validates request, calls service
   │
   ▼
3. CLASSIFICATION__FILTER__SERVICE
   │
   ├─► classify_all() → For each hash:
   │   │
   │   ├─► Semantic_Text__Service.classify_text("Happy sunny day")
   │   │   └─► Semantic_Text__Engine__Random.classify_text()
   │   │       └─► Returns: rating = 0.73
   │   │
   │   └─► Semantic_Text__Service.classify_text("Terrible rainy day")
   │       └─► Semantic_Text__Engine__Random.classify_text()
   │           └─► Returns: rating = 0.31
   │
   │   Result: {
   │     "abc1234567": 0.73,
   │     "def1234567": 0.31
   │   }
   │
   ├─► _apply_filter(ratings, "above", 0.5)
   │   │
   │   ├─► 0.73 > 0.5? YES → include "abc1234567"
   │   └─► 0.31 > 0.5? NO  → exclude "def1234567"
   │
   │   Result: ["abc1234567"]
   │
   └─► _build_filter_response(filtered, "full-ratings")
       │
       └─► Build response with text + ratings
   
   Final Response:
   {
     "filtered_hashes": ["abc1234567"],
     "filtered_with_text": {
       "abc1234567": "Happy sunny day"
     },
     "filtered_with_ratings": {
       "abc1234567": 0.73
     },
     "classification_criteria": "positivity",
     "output_mode": "full-ratings",
     "total_hashes": 2,
     "filtered_count": 1,
     "success": true
   }
   │
   ▼
4. ROUTES LAYER returns HTTP response
   │
   ▼
5. CALLER RECEIVES filtered results


SEPARATION OF CONCERNS
═══════════════════════════════════════════════════════════════════════════════

┌───────────────────────────────────────────┬─────────────────────────────────┐
│        TRANSFORMATION                     │      CLASSIFICATION             │
│        (Existing)                         │      (New - Level 1)            │
├───────────────────────────────────────────┼─────────────────────────────────┤
│ Routes__Text_Transformation               │ Routes__Semantic_Classification │
│   /text-transformation/transform          │   /semantic-classification/...  │
│   /text-transformation/transform/...      │                                 │
│                                           │                                 │
│ Text__Transformation__Service             │ Classification__Filter__Service │
│   - Transforms display of hashes          │   - Classifies & filters hashes │
│   - xxx-random, hashes-random, abcde      │   - ABOVE/BELOW/BETWEEN/EQUALS  │
│                                           │                                 │
│ Uses: Text__Selection, Text__Grouping     │ Uses: Semantic_Text__Service    │
└───────────────────────────────────────────┴─────────────────────────────────┘
                                │
                                │ Both can use independently OR together
                                ▼
                    ┌────────────────────────────┐
                    │   Semantic_Text__Service   │
                    │   (Shared Infrastructure)  │
                    │                            │
                    │   - classify_text()        │
                    │   - Pluggable engines      │
                    │   - Consistent interface   │
                    └────────────────────────────┘


FILTER MODES EXPLAINED
═══════════════════════════════════════════════════════════════════════════════

Given ratings: {"hash1": 0.2, "hash2": 0.5, "hash3": 0.8}

ABOVE (threshold=0.5)
  │
  ├─► 0.2 > 0.5? NO
  ├─► 0.5 > 0.5? NO
  └─► 0.8 > 0.5? YES ✓
  
  Result: ["hash3"]

BELOW (threshold=0.5)
  │
  ├─► 0.2 < 0.5? YES ✓
  ├─► 0.5 < 0.5? NO
  └─► 0.8 < 0.5? NO
  
  Result: ["hash1"]

BETWEEN (threshold=0.3, threshold_max=0.7)
  │
  ├─► 0.3 < 0.2 < 0.7? NO
  ├─► 0.3 < 0.5 < 0.7? YES ✓
  └─► 0.3 < 0.8 < 0.7? NO
  
  Result: ["hash2"]

EQUALS (threshold=0.5)
  │
  ├─► 0.2 == 0.5? NO
  ├─► 0.5 == 0.5? YES ✓
  └─► 0.8 == 0.5? NO
  
  Result: ["hash2"]


OUTPUT MODES EXPLAINED
═══════════════════════════════════════════════════════════════════════════════

Filtered hashes: ["hash1", "hash2"]
Original mapping: {"hash1": "Hello", "hash2": "World"}
Ratings: {"hash1": 0.7, "hash2": 0.9}

HASHES_ONLY
  {
    "filtered_hashes": ["hash1", "hash2"],
    "filtered_with_text": null,
    "filtered_with_ratings": null
  }

HASHES_WITH_TEXT
  {
    "filtered_hashes": ["hash1", "hash2"],
    "filtered_with_text": {
      "hash1": "Hello",
      "hash2": "World"
    },
    "filtered_with_ratings": null
  }

FULL_RATINGS
  {
    "filtered_hashes": ["hash1", "hash2"],
    "filtered_with_text": {
      "hash1": "Hello",
      "hash2": "World"
    },
    "filtered_with_ratings": {
      "hash1": 0.7,
      "hash2": 0.9
    }
  }


TYPE SAFETY FLOW
═══════════════════════════════════════════════════════════════════════════════

Input Validation (Type_Safe schemas)
  │
  ├─► Safe_Str__Hash ensures valid hash format (10 chars, alphanumeric)
  ├─► Safe_Float__Text__Classification ensures 0.0-1.0 range
  ├─► Safe_UInt ensures non-negative integers
  └─► Enum types ensure valid modes
  
Business Logic (Service layer)
  │
  └─► All parameters validated at boundary
      No need for runtime checks inside service
  
Output Validation (Type_Safe schemas)
  │
  └─► Response guaranteed to match schema
      Type-safe all the way through


EXTENSIBILITY POINTS
═══════════════════════════════════════════════════════════════════════════════

1. ADD NEW FILTER MODES
   Enum__Classification__Filter_Mode
   └─► Add: NOT_EQUALS, IN_LIST, PERCENTILE, etc.

2. ADD NEW OUTPUT MODES
   Enum__Classification__Output_Mode
   └─► Add: SEPARATED, COMBINED, JSON_GRAPH, etc.

3. ADD NEW CRITERIA
   Enum__Text__Classification__Criteria
   └─► Already has: POSITIVITY, NEGATIVITY, BIAS, URGENCY
   └─► Ready for Level 2!

4. ADD NEW ENGINES
   Semantic_Text__Engine
   └─► Hash_Based, Pre_Configured, LLM_Single, LLM_Multiple

5. ADD CACHING
   Classification__Filter__Service
   └─► Check cache before classify_text()
   └─► Store results after classification
   └─► TTL-based expiration
