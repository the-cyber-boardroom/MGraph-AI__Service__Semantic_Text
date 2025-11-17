# Technical Brief: Semantic Text Service - Client API Guide

**Version:** v0.6.8  
**Date:** November 17, 2025  
**Target Audience:** Service Clients (Mitmproxy, HTML Service, LLM Integrations)  
**Document Type:** API Reference & Integration Guide  
**Service Name:** MGraph AI Semantic Text Service

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Service Overview](#2-service-overview)
3. [API Endpoints Reference](#3-api-endpoints-reference)
4. [Schema Reference](#4-schema-reference)
5. [Integration Patterns](#5-integration-patterns)
6. [Deterministic Test Reference Tables](#6-deterministic-test-reference-tables)
7. [Practical Examples](#7-practical-examples)
8. [Best Practices](#8-best-practices)
9. [Appendices](#9-appendices)

---

## 1. Executive Summary

The **Semantic Text Service** provides intelligent text classification and transformation capabilities for content filtering applications. The service enables clients to classify text by sentiment (positive, negative, neutral, mixed), filter content based on configurable criteria, and apply visual transformations to selected text.

### Key Capabilities

- **Sentiment Classification**: Analyze text using 4 sentiment scores (positive, negative, neutral, mixed)
- **Multi-Engine Support**: Choose between ML-powered (AWS Comprehend), deterministic (hash-based), or random engines
- **Content Filtering**: Filter text hashes based on sentiment thresholds with AND/OR logic
- **Text Transformation**: Apply visual transformations (masking, hashing, grouping) to filtered content
- **Deterministic Testing**: Use hash-based engine for reproducible, cost-free testing

### Primary Use Cases

1. **Content Moderation**: Filter negative/toxic content from web pages
2. **Sentiment Analysis**: Classify and route content based on emotional tone
3. **Privacy-Preserving Display**: Mask sensitive content while preserving structure
4. **A/B Testing**: Deterministically test filtering logic without ML costs
5. **Intelligent Content Transformation**: Apply visual changes only to specific sentiment categories

### Target Integrations

- **Mitmproxy Service**: HTTP proxy with intelligent content filtering
- **HTML Service**: Text extraction and reconstruction with sentiment-aware transformations
- **Content Management Systems**: Real-time sentiment-based content routing
- **LLM Applications**: Sentiment-aware prompt engineering and response filtering

---

## 2. Service Overview

### 2.1 Core Concepts

#### Hash Mappings

The service operates on **hash mappings** rather than raw text to enable:

- **Efficient processing**: Hash-based lookups and deduplication
- **Stateless operations**: No server-side text storage required
- **Privacy**: Client controls original text, server only sees hashes
- **Reconstruction**: Enables HTML/content reconstruction after transformation

**Format**: `Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]`

```python
# Example hash mapping
{
    "b10a8db164": "Hello World",
    "f1feeaa3d6": "This is terrible",
    "0cbc6611f5": "Neutral statement"
}
```

#### Classification Criteria

All classification operations return **4 sentiment scores** (range 0.0-1.0):

| Criterion | Description | AWS Comprehend Behavior |
|-----------|-------------|------------------------|
| `positive` | Positive sentiment score | Dominant for happy/optimistic text (>0.9) |
| `negative` | Negative sentiment score | Dominant for sad/critical text (>0.9) |
| `neutral` | Neutral sentiment score | Dominant for factual/objective text (>0.6) |
| `mixed` | Mixed sentiment score | Rarely dominant; indicates conflicting emotions |

**Important**: AWS Comprehend scores are **highly polarized** - one sentiment typically dominates (>0.6), others remain minimal (<0.3).

#### Engine Modes

Three classification engines available via path parameter `{engine_mode}`:

| Engine Mode | Type | Use Case | Cost | Determinism | Accuracy |
|-------------|------|----------|------|-------------|----------|
| `aws_comprehend` | ML-powered | Production sentiment analysis | $$ | Non-deterministic | High (real NLP) |
| `text_hash` | Hash-based | Testing, deterministic validation | Free | 100% Deterministic | N/A (pseudo-random) |
| `random` | Pure random | Quick prototyping, stress testing | Free | Non-deterministic | N/A (random) |

**Production Recommendation**: Use `text_hash` during development/testing, switch to `aws_comprehend` for production.

#### Filter Operations

**Filter Modes** (comparison operators):

- `above`: rating > threshold
- `below`: rating < threshold

**Logic Operators** (multi-criteria):

- `and`: All criteria must match (intersection)
- `or`: Any criterion must match (union)

**Output Modes** (response format):

- `hashes-only`: Return only hash IDs (minimal)
- `hashes-with-text`: Include original text
- `full-ratings`: Include text + all 4 sentiment scores

#### Transformation Modes

Three visual transformation modes for text:

| Mode | Description | Behavior | Example |
|------|-------------|----------|---------|
| `xxx` | Character masking | Replace alphanumeric with 'x', preserve punctuation/spaces | "Hello World!" → "xxxxx xxxxx!" |
| `hashes` | Hash display | Replace text with hash value | "Hello World" → "b10a8db164" |
| `abcde-by-size` | Length grouping | Group by text length, replace with letters (a,b,c,d,e) | Short texts → 'a', Long texts → 'e' |

---

### 2.2 Engine Mode Detailed Comparison

#### AWS Comprehend Engine (`aws_comprehend`)

**Purpose**: Production-grade ML sentiment analysis using AWS Comprehend API

**Characteristics**:
- Real natural language processing
- Highly accurate sentiment classification
- Context-aware (understands sarcasm, nuance to some extent)
- Supports multiple languages
- Non-deterministic (scores may vary slightly between calls)

**Cost Implications**:
- Charged per AWS Comprehend API call
- Batch processing available for efficiency
- Caching recommended for repeated texts

**Score Distribution**:
```python
# Typical AWS Comprehend output (highly polarized)
Positive text: {positive: 0.9903, negative: 0.0009, neutral: 0.0078, mixed: 0.0008}
Negative text: {positive: 0.0001, negative: 0.9965, neutral: 0.0022, mixed: 0.0009}
Neutral text:  {positive: 0.1627, negative: 0.1128, neutral: 0.6909, mixed: 0.0335}
```

**When to Use**:
- Production content filtering
- Real sentiment-based routing decisions
- User-facing content moderation
- Applications requiring accurate emotional tone detection

**Configuration**:
```bash
# Required environment variables
AUTH__SERVICE__AWS__COMPREHEND__BASE_URL=https://aws-comprehend.dev.mgraph.ai
AUTH__SERVICE__AWS__COMPREHEND__KEY_NAME=X-API-Key
AUTH__SERVICE__AWS__COMPREHEND__KEY_VALUE=<your-api-key>
```

---

#### Text Hash Engine (`text_hash`)

**Purpose**: Deterministic pseudo-random classification for testing and validation

**Characteristics**:
- 100% deterministic (same input → same output always)
- Hash-based score generation (MD5)
- No external API calls
- Free to use (no costs)
- Normalized score distribution (sums to 1.0)

**Algorithm**:
```python
# Simplified implementation
combined = f"{text}_{criterion}"
full_hash = md5(combined.encode()).hexdigest()
hash_int = int(full_hash[:16], 16)
rating = (hash_int % 10000) / 10000.0  # Range: 0.0-1.0
```

**Score Distribution**:
```python
# Example hash-based output (normalized)
"Hello World": {positive: 0.6158, negative: 0.0609, neutral: 0.2945, mixed: 0.0289}
"Test Text":   {positive: 0.2842, negative: 0.2529, neutral: 0.1381, mixed: 0.3248}
```

**When to Use**:
- Unit testing and integration testing
- CI/CD pipeline validation
- Cost-free development iterations
- Deterministic QA verification
- Performance benchmarking
- Documentation examples (reproducible)

**Advantages**:
- No configuration required
- Instant response (no network calls)
- Perfect for automated testing
- Reproducible results across environments

---

#### Random Engine (`random`)

**Purpose**: Pure random classification for prototyping and stress testing

**Characteristics**:
- Non-deterministic (different output each call)
- Normalized random distribution
- No external dependencies
- Free to use

**Score Generation**:
```python
# Simplified implementation
raw_scores = [random.uniform(0, 1) for _ in range(4)]
total = sum(raw_scores)
normalized = [score / total for score in raw_scores]  # Sums to 1.0
```

**When to Use**:
- Quick prototyping without ML setup
- Load testing (varies results)
- Demonstrating UI/UX with diverse data
- Stress testing filter logic

**Not Recommended For**:
- Production use
- Unit tests (non-deterministic)
- Deterministic validation

---

### 2.3 Service Configuration

**Base URL**: `https://semantic-text.dev.mgraph.ai`

**Authentication**: API Key via HTTP header

**Required Headers**:
```http
Content-Type: application/json
X-API-Key: <your-api-key>
```

**Environment Variables**:
```bash
# FastAPI Service Authentication
FAST_API__AUTH__API_KEY__NAME=X-API-Key
FAST_API__AUTH__API_KEY__VALUE=<your-service-api-key>

# AWS Comprehend Engine (required only for aws_comprehend mode)
AUTH__SERVICE__AWS__COMPREHEND__BASE_URL=https://aws-comprehend.dev.mgraph.ai
AUTH__SERVICE__AWS__COMPREHEND__KEY_NAME=X-API-Key
AUTH__SERVICE__AWS__COMPREHEND__KEY_VALUE=<comprehend-api-key>
```

---

## 3. API Endpoints Reference

### 3.1 Semantic Classification Routes

Base path: `/semantic-classification`

All routes require `{engine_mode}` path parameter: `aws_comprehend` | `text_hash` | `random`

---

#### 3.1.1 Rate All Hashes (Single Criterion - Legacy)

**Endpoint**: `POST /semantic-classification/{engine_mode}/rate`

**Purpose**: Classify all hashes and return all 4 sentiment scores for each hash.

**Note**: This endpoint is functionally identical to `/multi/rate` and exists for backwards compatibility.

**Path Parameters**:
- `engine_mode`: Classification engine (`aws_comprehend` | `text_hash` | `random`)

**Request Schema**:
```json
{
  "hash_mapping": {
    "b10a8db164": "Hello World",
    "f1feeaa3d6": "This is terrible"
  }
}
```

**Response Schema**:
```json
{
  "hash_ratings": {
    "b10a8db164": {
      "positive": 0.6158,
      "negative": 0.0609,
      "neutral": 0.2945,
      "mixed": 0.0289
    },
    "f1feeaa3d6": {
      "positive": 0.2842,
      "negative": 0.2529,
      "neutral": 0.1381,
      "mixed": 0.3248
    }
  },
  "total_hashes": 2,
  "success": true
}
```

**Python Type Definitions**:
```python
# Request
class Schema__Classification__Request(Type_Safe):
    hash_mapping: Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]

# Response
class Schema__Classification__Response(Type_Safe):
    hash_ratings: Dict[Safe_Str__Hash, 
                      Dict[Enum__Text__Classification__Criteria,
                           Safe_Float__Text__Classification]]
    total_hashes: Safe_UInt
    success: bool
```

**Use Cases**:
- Get sentiment scores for all text hashes
- Initial sentiment analysis before filtering
- Bulk classification for analytics

---

#### 3.1.2 Filter by Single Criterion

**Endpoint**: `POST /semantic-classification/{engine_mode}/filter`

**Purpose**: Filter hashes based on a single sentiment criterion and threshold.

**Path Parameters**:
- `engine_mode`: Classification engine (`aws_comprehend` | `text_hash` | `random`)

**Request Schema**:
```json
{
  "hash_mapping": {
    "b10a8db164": "Hello World",
    "f1feeaa3d6": "This is terrible",
    "0cbc6611f5": "Neutral statement"
  },
  "classification_criteria": "positive",
  "filter_mode": "above",
  "threshold": 0.5,
  "output_mode": "full-ratings"
}
```

**Request Fields**:
- `hash_mapping`: Dict of hash → text mappings
- `classification_criteria`: Criterion to filter by (`positive`|`negative`|`neutral`|`mixed`)
- `filter_mode`: Comparison operator (`above`|`below`)
- `threshold`: Float value (0.0-1.0)
- `output_mode`: Response format (`hashes-only`|`hashes-with-text`|`full-ratings`)

**Response Schema**:
```json
{
  "filtered_hashes": ["b10a8db164"],
  "filtered_with_text": {
    "b10a8db164": "Hello World"
  },
  "filtered_with_ratings": {
    "b10a8db164": {
      "positive": 0.6158,
      "negative": 0.0609,
      "neutral": 0.2945,
      "mixed": 0.0289
    }
  },
  "classification_criteria": "positive",
  "output_mode": "full-ratings",
  "total_hashes": 3,
  "filtered_count": 1,
  "success": true
}
```

**Python Type Definitions**:
```python
# Request
class Schema__Classification__Filter_Request(Type_Safe):
    hash_mapping: Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]
    classification_criteria: Enum__Text__Classification__Criteria
    filter_mode: Enum__Classification__Filter_Mode
    threshold: Safe_Float
    output_mode: Enum__Classification__Output_Mode

# Response
class Schema__Classification__Filter_Response(Type_Safe):
    filtered_hashes: List[Safe_Str__Hash]
    filtered_with_text: Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]
    filtered_with_ratings: Dict[Safe_Str__Hash, 
                               Dict[Enum__Text__Classification__Criteria,
                                    Safe_Float__Text__Classification]]
    classification_criteria: Enum__Text__Classification__Criteria
    output_mode: Enum__Classification__Output_Mode
    total_hashes: Safe_UInt
    filtered_count: Safe_UInt
    success: bool
```

**Use Cases**:
- Filter highly positive content (above 0.8)
- Remove negative content (above 0.7 negative score)
- Select neutral content for factual displays

**Example Filters**:
```python
# Filter positive content
filter_mode="above", threshold=0.7, criteria="positive"
# Result: Only hashes with positive > 0.7

# Filter out negative content
filter_mode="below", threshold=0.3, criteria="negative"
# Result: Only hashes with negative < 0.3
```

---

#### 3.1.3 Rate All Hashes (Multi-Criteria)

**Endpoint**: `POST /semantic-classification/{engine_mode}/multi/rate`

**Purpose**: Classify all hashes and return all 4 sentiment scores (identical to `/rate`).

**Path Parameters**:
- `engine_mode`: Classification engine (`aws_comprehend` | `text_hash` | `random`)

**Request Schema**:
```json
{
  "hash_mapping": {
    "b10a8db164": "Hello World",
    "f1feeaa3d6": "Test Text"
  }
}
```

**Response Schema**:
```json
{
  "hash_ratings": {
    "b10a8db164": {
      "positive": 0.6158,
      "negative": 0.0609,
      "neutral": 0.2945,
      "mixed": 0.0289
    },
    "f1feeaa3d6": {
      "positive": 0.2842,
      "negative": 0.2529,
      "neutral": 0.1381,
      "mixed": 0.3248
    }
  },
  "total_hashes": 2,
  "success": true
}
```

**Python Type Definitions**:
```python
# Request
class Schema__Classification__Multi_Criteria_Request(Type_Safe):
    hash_mapping: Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]

# Response
class Schema__Classification__Multi_Criteria_Response(Type_Safe):
    hash_ratings: Dict[Safe_Str__Hash,
                      Dict[Enum__Text__Classification__Criteria,
                           Safe_Float__Text__Classification]]
    total_hashes: Safe_UInt
    success: bool
```

**Note**: This endpoint always returns all 4 criteria regardless of input. It is functionally equivalent to `/rate` but uses the "multi-criteria" naming convention for consistency.

---

#### 3.1.4 Filter by Multiple Criteria (AND/OR Logic)

**Endpoint**: `POST /semantic-classification/{engine_mode}/multi/filter`

**Purpose**: Filter hashes using multiple sentiment criteria combined with AND/OR logic.

**Path Parameters**:
- `engine_mode`: Classification engine (`aws_comprehend` | `text_hash` | `random`)

**Request Schema**:
```json
{
  "hash_mapping": {
    "b10a8db164": "Hello World",
    "f1feeaa3d6": "This is terrible",
    "0cbc6611f5": "Mixed emotions here"
  },
  "criterion_filters": [
    {
      "criterion": "positive",
      "filter_mode": "above",
      "threshold": 0.5
    },
    {
      "criterion": "negative",
      "filter_mode": "below",
      "threshold": 0.2
    }
  ],
  "logic_operator": "and",
  "output_mode": "full-ratings"
}
```

**Request Fields**:
- `hash_mapping`: Dict of hash → text mappings
- `criterion_filters`: List of filter conditions
  - `criterion`: Sentiment criterion (`positive`|`negative`|`neutral`|`mixed`)
  - `filter_mode`: Comparison operator (`above`|`below`)
  - `threshold`: Float value (0.0-1.0)
- `logic_operator`: How to combine filters (`and`|`or`)
  - `and`: All filters must match (intersection)
  - `or`: Any filter can match (union)
- `output_mode`: Response format (`hashes-only`|`hashes-with-text`|`full-ratings`)

**Response Schema**:
```json
{
  "filtered_hashes": ["b10a8db164"],
  "filtered_with_text": {
    "b10a8db164": "Hello World"
  },
  "filtered_with_ratings": {
    "b10a8db164": {
      "positive": 0.6158,
      "negative": 0.0609,
      "neutral": 0.2945,
      "mixed": 0.0289
    }
  },
  "criteria_used": ["positive", "negative"],
  "logic_operator": "and",
  "output_mode": "full-ratings",
  "total_hashes": 3,
  "filtered_count": 1,
  "success": true
}
```

**Python Type Definitions**:
```python
# Request
class Schema__Classification__Multi_Criteria_Filter_Request(Type_Safe):
    hash_mapping: Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]
    criterion_filters: List[Schema__Classification__Criterion_Filter]
    logic_operator: Enum__Classification__Logic_Operator
    output_mode: Enum__Classification__Output_Mode

class Schema__Classification__Criterion_Filter(Type_Safe):
    criterion: Enum__Text__Classification__Criteria
    filter_mode: Enum__Classification__Filter_Mode
    threshold: Safe_Float

# Response
class Schema__Classification__Multi_Criteria_Filter_Response(Type_Safe):
    filtered_hashes: List[Safe_Str__Hash]
    filtered_with_text: Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]
    filtered_with_ratings: Dict[Safe_Str__Hash,
                               Dict[Enum__Text__Classification__Criteria,
                                    Safe_Float__Text__Classification]]
    criteria_used: List[Enum__Text__Classification__Criteria]
    logic_operator: Enum__Classification__Logic_Operator
    output_mode: Enum__Classification__Output_Mode
    total_hashes: Safe_UInt
    filtered_count: Safe_UInt
    success: bool
```

**Use Cases**:

**AND Logic Examples**:
```python
# Filter: High positive AND low negative (purely positive content)
criterion_filters = [
    {"criterion": "positive", "filter_mode": "above", "threshold": 0.7},
    {"criterion": "negative", "filter_mode": "below", "threshold": 0.1}
]
logic_operator = "and"
# Result: Only hashes that are very positive AND not negative

# Filter: Neutral AND not mixed (factual content)
criterion_filters = [
    {"criterion": "neutral", "filter_mode": "above", "threshold": 0.6},
    {"criterion": "mixed", "filter_mode": "below", "threshold": 0.1}
]
logic_operator = "and"
# Result: Clear neutral content without mixed emotions
```

**OR Logic Examples**:
```python
# Filter: High positive OR high neutral (non-negative content)
criterion_filters = [
    {"criterion": "positive", "filter_mode": "above", "threshold": 0.6},
    {"criterion": "neutral", "filter_mode": "above", "threshold": 0.6}
]
logic_operator = "or"
# Result: Hashes that are either positive or neutral

# Filter: Very negative OR very positive (polarized content)
criterion_filters = [
    {"criterion": "negative", "filter_mode": "above", "threshold": 0.8},
    {"criterion": "positive", "filter_mode": "above", "threshold": 0.8}
]
logic_operator = "or"
# Result: Strong emotional content (either direction)
```

---

### 3.2 Text Transformation Routes

Base path: `/text-transformation`

These endpoints combine sentiment-based filtering with visual text transformations.

---

#### 3.2.1 Unified Transformation Endpoint

**Endpoint**: `POST /text-transformation/transform`

**Purpose**: Transform hash mapping with optional sentiment-based filtering (two-phase operation).

**Phase 1**: Classification & Selection (optional)
- Classify text using specified `engine_mode`
- Apply `criterion_filters` with `logic_operator`
- Select hashes that match criteria

**Phase 2**: Visual Transformation
- Apply `transformation_mode` to selected hashes
- Preserve non-selected hashes unchanged

**Request Schema**:
```json
{
  "hash_mapping": {
    "b10a8db164": "Hello World",
    "f1feeaa3d6": "This is terrible",
    "0cbc6611f5": "Neutral statement"
  },
  "engine_mode": "text_hash",
  "criterion_filters": [
    {
      "criterion": "negative",
      "filter_mode": "above",
      "threshold": 0.5
    }
  ],
  "logic_operator": "and",
  "transformation_mode": "xxx"
}
```

**Request Fields**:
- `hash_mapping`: Dict of hash → text mappings (required)
- `engine_mode`: Classification engine (optional; if null, no filtering occurs)
  - Options: `aws_comprehend` | `text_hash` | `random` | `null`
- `criterion_filters`: List of filter conditions (optional; if empty, no filtering)
- `logic_operator`: How to combine filters (`and`|`or`) - default: `and`
- `transformation_mode`: Visual transformation to apply (required)
  - Options: `xxx` | `hashes` | `abcde-by-size`

**Response Schema**:
```json
{
  "transformed_mapping": {
    "b10a8db164": "Hello World",
    "f1feeaa3d6": "xxxx xx xxxxxxxx",
    "0cbc6611f5": "Neutral statement"
  },
  "transformation_mode": "xxx",
  "success": true,
  "total_hashes": 3,
  "transformed_hashes": 1,
  "error_message": null
}
```

**Python Type Definitions**:
```python
# Request
class Schema__Text__Transformation__Request(Type_Safe):
    hash_mapping: Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]
    engine_mode: Enum__Text__Transformation__Engine_Mode  # Optional
    criterion_filters: List[Schema__Classification__Criterion_Filter]  # Optional
    logic_operator: Enum__Classification__Logic_Operator
    transformation_mode: Enum__Text__Transformation__Mode

# Response
class Schema__Text__Transformation__Response(Type_Safe):
    transformed_mapping: Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]
    transformation_mode: Enum__Text__Transformation__Mode
    success: bool
    total_hashes: Safe_UInt
    transformed_hashes: Safe_UInt
    error_message: Optional[Safe_Str__Text]
```

**Transformation Modes**:

**Mode: `xxx` (Character Masking)**
```python
# Original: "Hello World!"
# Transformed: "xxxxx xxxxx!"
# Preserves: spaces, punctuation
# Replaces: alphanumeric characters → 'x'
```

**Mode: `hashes` (Hash Display)**
```python
# Original: "Hello World"
# Transformed: "b10a8db164"
# Replaces: entire text with hash value
```

**Mode: `abcde-by-size` (Length Grouping)**
```python
# Groups text by length into 5 buckets (a,b,c,d,e)
# Short texts → 'a'
# Medium texts → 'b', 'c', 'd'
# Long texts → 'e'
# Example: "Hi" → "aa", "Hello World!" → "aaaaa aaaaa!"
# Note: ALWAYS transforms ALL hashes (ignores filters)
```

**Special Behavior: ABCDE Mode**

The `abcde-by-size` transformation mode **ALWAYS transforms all hashes** regardless of filtering:

```json
{
  "engine_mode": "text_hash",
  "criterion_filters": [{"criterion": "negative", "filter_mode": "above", "threshold": 0.9}],
  "transformation_mode": "abcde-by-size"
}
```
Result: ALL hashes transformed to letters, filters ignored.

**Use Cases**:

**Scenario 1: Mask Negative Content**
```python
# Mask highly negative text while showing positive/neutral
engine_mode = "aws_comprehend"
criterion_filters = [{"criterion": "negative", "filter_mode": "above", "threshold": 0.7}]
transformation_mode = "xxx"
# Result: Negative text → "xxx", others unchanged
```

**Scenario 2: Hide Sensitive Content**
```python
# Replace specific content with hashes
engine_mode = "text_hash"
criterion_filters = [{"criterion": "neutral", "filter_mode": "below", "threshold": 0.3}]
transformation_mode = "hashes"
# Result: Non-neutral text → hash IDs, neutral unchanged
```

**Scenario 3: Deterministic Testing**
```python
# Test filtering logic without AWS costs
engine_mode = "text_hash"
criterion_filters = [{"criterion": "positive", "filter_mode": "above", "threshold": 0.5}]
transformation_mode = "xxx"
# Result: Deterministic, reproducible transformations
```

**Scenario 4: No Filtering (Transform All)**
```python
# Apply transformation without sentiment filtering
engine_mode = null
criterion_filters = []
transformation_mode = "xxx"
# Result: All hashes transformed
```

---

#### 3.2.2 Path Parameters Transformation Endpoint

**Endpoint**: `POST /text-transformation/transform/{engine_mode}/{transformation_mode}/{criteria}/{filter_mode}/{threshold}`

**Purpose**: Simplified single-criterion filtering with path parameters (alternative to unified endpoint).

**Path Parameters**:
- `engine_mode`: Classification engine (`aws_comprehend` | `text_hash` | `random`)
- `transformation_mode`: Transformation type (`xxx` | `hashes` | `abcde-by-size`)
- `criteria`: Single criterion (`positive` | `negative` | `neutral` | `mixed`)
- `filter_mode`: Comparison operator (`above` | `below`)
- `threshold`: Float value (0.0-1.0)

**Request Schema** (Simplified):
```json
{
  "hash_mapping": {
    "b10a8db164": "Hello World",
    "f1feeaa3d6": "This is terrible"
  }
}
```

**Example URL**:
```
POST /text-transformation/transform/text_hash/xxx/negative/above/0.5
```

**Python Type Definitions**:
```python
# Request (simplified - only hash_mapping required)
class Schema__Text__Transformation__Request__Path_Params(Type_Safe):
    hash_mapping: Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]

# Response (same as unified endpoint)
class Schema__Text__Transformation__Response(Type_Safe):
    transformed_mapping: Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]
    transformation_mode: Enum__Text__Transformation__Mode
    success: bool
    total_hashes: Safe_UInt
    transformed_hashes: Safe_UInt
    error_message: Optional[Safe_Str__Text]
```

**Behavior**:

This endpoint internally constructs a full request with single criterion filter:

```python
# Path params: /transform/text_hash/xxx/negative/above/0.7
# Internally becomes:
{
    "engine_mode": "text_hash",
    "criterion_filters": [
        {"criterion": "negative", "filter_mode": "above", "threshold": 0.7}
    ],
    "logic_operator": "and",  # Default (irrelevant for single criterion)
    "transformation_mode": "xxx"
}
```

**Use Cases**:
- Quick single-criterion transformations
- REST-friendly path-based filtering
- Simple integrations without complex request bodies

**Example Calls**:

```bash
# Mask highly negative content
POST /text-transformation/transform/aws_comprehend/xxx/negative/above/0.8

# Show hashes for non-positive content
POST /text-transformation/transform/text_hash/hashes/positive/below/0.3

# Group all by size (ABCDE always transforms all)
POST /text-transformation/transform/text_hash/abcde-by-size/positive/above/0.0
```

---

### 3.3 Service Info Routes

Base path: `/info`

---

#### 3.3.1 Service Version

**Endpoint**: `GET /info/version`

**Purpose**: Get service version information.

**Response**:
```json
{
  "version": "v0.6.8",
  "service": "mgraph_ai_service_semantic_text"
}
```

---

#### 3.3.2 Health Check

**Endpoint**: `GET /info/health`

**Purpose**: Verify service is running and responsive.

**Response**:
```json
{
  "status": "healthy"
}
```

---

## 4. Schema Reference

### 4.1 Core Data Types

#### Safe_Str__Hash

**Type**: String-based hash identifier  
**Format**: 10-character alphanumeric hash (lowercase)  
**Example**: `"b10a8db164"`, `"f1feeaa3d6"`  
**Purpose**: Unique identifier for text content

```python
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash import Safe_Str__Hash

hash_id = Safe_Str__Hash("b10a8db164")
```

---

#### Safe_Str__Comprehend__Text

**Type**: String content for AWS Comprehend processing  
**Format**: UTF-8 text string  
**Min Length**: 1 character  
**Max Length**: 5000 bytes (AWS Comprehend limit)  
**Purpose**: Text content to be classified or transformed

```python
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text import Safe_Str__Comprehend__Text

text = Safe_Str__Comprehend__Text("Hello World")
```

---

#### Safe_Float__Text__Classification

**Type**: Float score representing sentiment strength  
**Range**: 0.0 to 1.0 (inclusive)  
**Precision**: Up to 10 decimal places  
**Purpose**: Sentiment score for classification criteria

```python
from mgraph_ai_service_semantic_text.schemas.safe_float.Safe_Float__Text__Classification import Safe_Float__Text__Classification

score = Safe_Float__Text__Classification(0.6158)
```

---

### 4.2 Enums

#### Enum__Text__Classification__Engine_Mode

**Classification engines available**

| Value | Description | Use Case |
|-------|-------------|----------|
| `aws_comprehend` | AWS Comprehend ML | Production sentiment analysis |
| `text_hash` | Deterministic hash-based | Testing, reproducible results |
| `random` | Pure random | Prototyping, stress testing |

```python
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Engine_Mode import Enum__Text__Classification__Engine_Mode

engine = Enum__Text__Classification__Engine_Mode.TEXT_HASH
```

---

#### Enum__Text__Classification__Criteria

**Sentiment classification criteria (AWS Comprehend aligned)**

| Value | Description | Score Meaning |
|-------|-------------|---------------|
| `positive` | Positive sentiment | 0.0 = no positivity, 1.0 = very positive |
| `negative` | Negative sentiment | 0.0 = no negativity, 1.0 = very negative |
| `neutral` | Neutral sentiment | 0.0 = not neutral, 1.0 = completely neutral |
| `mixed` | Mixed sentiment | 0.0 = clear sentiment, 1.0 = very mixed |

```python
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Criteria import Enum__Text__Classification__Criteria

criterion = Enum__Text__Classification__Criteria.POSITIVE
```

---

#### Enum__Classification__Filter_Mode

**Filter comparison operators**

| Value | Operator | Meaning |
|-------|----------|---------|
| `above` | `>` | rating > threshold |
| `below` | `<` | rating < threshold |

```python
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Filter_Mode import Enum__Classification__Filter_Mode

filter_mode = Enum__Classification__Filter_Mode.ABOVE
```

---

#### Enum__Classification__Logic_Operator

**Multi-criteria combination logic**

| Value | Logic | Meaning |
|-------|-------|---------|
| `and` | Intersection | All criteria must match |
| `or` | Union | Any criterion can match |

```python
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Logic_Operator import Enum__Classification__Logic_Operator

logic = Enum__Classification__Logic_Operator.AND
```

---

#### Enum__Classification__Output_Mode

**Response format options for filter operations**

| Value | Includes | Use Case |
|-------|----------|----------|
| `hashes-only` | Hash IDs only | Minimal response, further processing |
| `hashes-with-text` | Hash IDs + original text | Content reconstruction |
| `full-ratings` | Hash IDs + text + all 4 scores | Complete analysis, debugging |

```python
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode import Enum__Classification__Output_Mode

output = Enum__Classification__Output_Mode.FULL_RATINGS
```

---

#### Enum__Text__Transformation__Mode

**Text transformation modes**

| Value | Description | Behavior |
|-------|-------------|----------|
| `xxx` | Character masking | Replace alphanumeric with 'x' |
| `hashes` | Hash display | Show hash ID instead of text |
| `abcde-by-size` | Length grouping | Group by size, replace with letters |

```python
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode import Enum__Text__Transformation__Mode

mode = Enum__Text__Transformation__Mode.XXX
```

---

### 4.3 Request/Response Schema Quick Reference

| Endpoint | Request Schema | Response Schema |
|----------|----------------|-----------------|
| `/semantic-classification/{engine}/rate` | `Schema__Classification__Request` | `Schema__Classification__Response` |
| `/semantic-classification/{engine}/filter` | `Schema__Classification__Filter_Request` | `Schema__Classification__Filter_Response` |
| `/semantic-classification/{engine}/multi/rate` | `Schema__Classification__Multi_Criteria_Request` | `Schema__Classification__Multi_Criteria_Response` |
| `/semantic-classification/{engine}/multi/filter` | `Schema__Classification__Multi_Criteria_Filter_Request` | `Schema__Classification__Multi_Criteria_Filter_Response` |
| `/text-transformation/transform` | `Schema__Text__Transformation__Request` | `Schema__Text__Transformation__Response` |
| `/text-transformation/transform/{params...}` | `Schema__Text__Transformation__Request__Path_Params` | `Schema__Text__Transformation__Response` |

---

## 5. Integration Patterns

### 5.1 Common Workflows

#### Workflow 1: Simple Sentiment Filtering

**Scenario**: Filter and display only positive content from web page

```python
# Step 1: Extract text and create hash mapping (client-side)
hash_mapping = {
    "abc1234567": "I love this product!",
    "def1234567": "This is terrible quality.",
    "ghi1234567": "Shipping was fast."
}

# Step 2: Classify and filter (call Semantic Text Service)
POST /semantic-classification/text_hash/filter
{
    "hash_mapping": hash_mapping,
    "classification_criteria": "positive",
    "filter_mode": "above",
    "threshold": 0.6,
    "output_mode": "hashes-only"
}

# Response:
{
    "filtered_hashes": ["abc1234567", "ghi1234567"],  # Only positive content
    "filtered_count": 2,
    "total_hashes": 3
}

# Step 3: Reconstruct HTML showing only filtered hashes (client-side)
# Display: "I love this product!" and "Shipping was fast."
# Hide: "This is terrible quality."
```

---

#### Workflow 2: Multi-Criteria Content Filtering

**Scenario**: Show only content that is positive AND not negative (purely positive)

```python
# Step 1: Create hash mapping
hash_mapping = {
    "aaa1111111": "Amazing experience!",
    "bbb2222222": "It's okay but could be better.",
    "ccc3333333": "Absolutely terrible."
}

# Step 2: Apply multi-criteria filter
POST /semantic-classification/aws_comprehend/multi/filter
{
    "hash_mapping": hash_mapping,
    "criterion_filters": [
        {
            "criterion": "positive",
            "filter_mode": "above",
            "threshold": 0.7
        },
        {
            "criterion": "negative",
            "filter_mode": "below",
            "threshold": 0.1
        }
    ],
    "logic_operator": "and",
    "output_mode": "full-ratings"
}

# Response:
{
    "filtered_hashes": ["aaa1111111"],  # Only purely positive
    "filtered_with_ratings": {
        "aaa1111111": {
            "positive": 0.95,
            "negative": 0.01,
            "neutral": 0.03,
            "mixed": 0.01
        }
    },
    "filtered_count": 1
}
```

---

#### Workflow 3: Transformation with Pre-Filtering

**Scenario**: Mask negative content while showing positive/neutral content

```python
# Step 1: Create hash mapping
hash_mapping = {
    "xxx1111111": "Great service!",
    "yyy2222222": "This is awful.",
    "zzz3333333": "Product arrived on time."
}

# Step 2: Transform with filtering
POST /text-transformation/transform
{
    "hash_mapping": hash_mapping,
    "engine_mode": "aws_comprehend",
    "criterion_filters": [
        {
            "criterion": "negative",
            "filter_mode": "above",
            "threshold": 0.7
        }
    ],
    "logic_operator": "and",
    "transformation_mode": "xxx"
}

# Response:
{
    "transformed_mapping": {
        "xxx1111111": "Great service!",           # Unchanged (not negative)
        "yyy2222222": "xxxx xx xxxxx.",           # Masked (negative)
        "zzz3333333": "Product arrived on time."  # Unchanged (not negative)
    },
    "transformed_hashes": 1
}

# Step 3: Reconstruct HTML with transformed content
# User sees: "Great service!" and "Product arrived on time."
# Negative content: "xxxx xx xxxxx."
```

---

#### Workflow 4: Deterministic Testing Pipeline

**Scenario**: CI/CD pipeline validation without AWS costs

```python
# Step 1: Create test hash mapping (deterministic)
test_mapping = {
    "b10a8db164": "Hello World",     # Known scores: pos=0.6158, neg=0.0609
    "f1feeaa3d6": "Test Text"        # Known scores: pos=0.2842, neg=0.2529
}

# Step 2: Test classification (text_hash engine)
POST /semantic-classification/text_hash/rate
{
    "hash_mapping": test_mapping
}

# Expected Response (deterministic):
{
    "hash_ratings": {
        "b10a8db164": {
            "positive": 0.6158,
            "negative": 0.0609,
            "neutral": 0.2945,
            "mixed": 0.0289
        },
        "f1feeaa3d6": {
            "positive": 0.2842,
            "negative": 0.2529,
            "neutral": 0.1381,
            "mixed": 0.3248
        }
    }
}

# Step 3: Validate expected results in test assertions
assert response["hash_ratings"]["b10a8db164"]["positive"] == 0.6158
assert response["hash_ratings"]["f1feeaa3d6"]["negative"] == 0.2529

# Step 4: Switch to AWS Comprehend for production (zero code changes)
# Change: engine_mode = "aws_comprehend"
```

---

### 5.2 Engine Mode Selection Strategy

#### Development Phase

**Use: `text_hash`**

Benefits:
- Free (no API costs)
- Instant response
- Deterministic (same input → same output)
- Perfect for unit tests
- Reproducible across environments

```python
# Development configuration
engine_mode = "text_hash"
```

---

#### Testing Phase

**Use: `text_hash`**

Benefits:
- Deterministic validation
- CI/CD pipeline compatible
- No external dependencies
- Fast test execution

```python
# Test configuration
def test_sentiment_filtering():
    engine_mode = "text_hash"
    # Deterministic assertions possible
    assert response["hash_ratings"]["b10a8db164"]["positive"] == 0.6158
```

---

#### Production Phase

**Use: `aws_comprehend`**

Benefits:
- Real ML sentiment analysis
- Accurate emotional tone detection
- Context-aware classification

```python
# Production configuration (zero code changes from testing)
engine_mode = "aws_comprehend"
# Logic remains identical, only accuracy improves
```

---

#### Prototyping Phase

**Use: `random`**

Benefits:
- Quick setup (no configuration)
- Diverse test data
- UI/UX experimentation

```python
# Prototype configuration
engine_mode = "random"
```

---

### 5.3 Error Handling

#### Common Error Responses

**400 Bad Request**: Invalid input

```json
{
  "detail": "Validation error: threshold must be between 0.0 and 1.0"
}
```

**401 Unauthorized**: Missing/invalid API key

```json
{
  "detail": "Invalid API key"
}
```

**500 Internal Server Error**: Service failure

```json
{
  "transformed_mapping": {},
  "success": false,
  "error_message": "Classification failed: AWS Comprehend service unavailable"
}
```

---

#### Retry Strategy

**AWS Comprehend Engine (Transient Failures)**:

```python
import time
from typing import Dict

def call_with_retry(endpoint: str, payload: Dict, max_retries: int = 3):
    """Retry AWS Comprehend calls on transient failures"""
    for attempt in range(max_retries):
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 500 and attempt < max_retries - 1:
                # AWS service transient error - retry with exponential backoff
                time.sleep(2 ** attempt)
                continue
            raise
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
```

**Text Hash/Random Engines (No Retry Needed)**:

```python
# Deterministic engines should never fail (unless validation errors)
response = requests.post(endpoint, json=payload)
response.raise_for_status()  # Only raises on validation errors (400)
```

---

#### Validation Errors

**Invalid Threshold**:
```python
# ❌ Invalid
threshold = 1.5  # Out of range

# ✅ Valid
threshold = 0.75
```

**Invalid Engine Mode**:
```python
# ❌ Invalid
POST /semantic-classification/invalid_engine/rate

# ✅ Valid
POST /semantic-classification/text_hash/rate
```

**Empty Hash Mapping**:
```python
# ✅ Valid (returns empty results, no error)
{
    "hash_mapping": {},
    "classification_criteria": "positive"
}

# Response:
{
    "filtered_hashes": [],
    "total_hashes": 0,
    "success": true
}
```

---

## 6. Deterministic Test Reference Tables

These tables provide **exact expected values** for the `text_hash` engine, enabling deterministic test assertions.

### 6.1 Text Hash Engine - Classification Scores

#### Reference Text: "Hello World"

| Hash | Text | Positive | Negative | Neutral | Mixed |
|------|------|----------|----------|---------|-------|
| `b10a8db164` | `Hello World` | `0.6158` | `0.0609` | `0.2945` | `0.0289` |

**Complete Scores**:
```json
{
  "b10a8db164": {
    "positive": 0.61575136853258,
    "negative": 0.06092177291188416,
    "neutral": 0.2944552357407734,
    "mixed": 0.028871622814762493
  }
}
```

**Test Usage**:
```python
def test_hello_world_classification():
    hash_mapping = {"b10a8db164": "Hello World"}
    response = classify(hash_mapping, engine_mode="text_hash")
    
    ratings = response["hash_ratings"]["b10a8db164"]
    assert float(ratings["positive"]) == 0.61575136853258
    assert float(ratings["negative"]) == 0.06092177291188416
    assert float(ratings["neutral"]) == 0.2944552357407734
    assert float(ratings["mixed"]) == 0.028871622814762493
```

---

#### Reference Text: "Test Text"

| Hash | Text | Positive | Negative | Neutral | Mixed |
|------|------|----------|----------|---------|-------|
| `f1feeaa3d6` | `Test Text` | `0.2842` | `0.2529` | `0.1381` | `0.3248` |

**Complete Scores**:
```json
{
  "f1feeaa3d6": {
    "positive": 0.2842339724966105,
    "negative": 0.25290528762347475,
    "neutral": 0.1380980050358319,
    "mixed": 0.3247627348440829
  }
}
```

---

#### Reference Text: "Test"

| Hash | Text | Positive | Negative | Neutral | Mixed |
|------|------|----------|----------|---------|-------|
| `0cbc6611f5` | `Test` | `0.4257` | `0.1060` | `0.2211` | `0.2472` |

**Complete Scores**:
```json
{
  "0cbc6611f5": {
    "positive": 0.4257015636325981,
    "negative": 0.10598529564046806,
    "neutral": 0.22108315211763488,
    "mixed": 0.24722998860929896
  }
}
```

---

#### Reference Text: "Sample text"

| Hash | Text | Positive | Negative | Neutral | Mixed |
|------|------|----------|----------|---------|-------|
| `1ba249ca59` | `Sample text` | `0.0526` | `0.4057` | `0.3872` | `0.1545` |

**Complete Scores**:
```json
{
  "1ba249ca59": {
    "positive": 0.05257312106627175,
    "negative": 0.4057293594964828,
    "neutral": 0.3871714179933358,
    "mixed": 0.15452610144390966
  }
}
```

---

#### Reference Text: "Positive text"

| Hash | Text | Positive | Negative | Neutral | Mixed |
|------|------|----------|----------|---------|-------|
| `b5ead10d6e` | `Positive text` | `0.4119` | `0.3534` | `0.1431` | `0.0916` |

**Complete Scores**:
```json
{
  "b5ead10d6e": {
    "positive": 0.41186440475956345,
    "negative": 0.3533909581228615,
    "neutral": 0.1431048438045345,
    "mixed": 0.09163979331304059
  }
}
```

---

#### Reference Text: "Another text"

| Hash | Text | Positive | Negative | Neutral | Mixed |
|------|------|----------|----------|---------|-------|
| `9204d57da8` | `Another text` | `0.2544` | `0.2451` | `0.1784` | `0.3221` |

**Complete Scores**:
```json
{
  "9204d57da8": {
    "positive": 0.25435712096893787,
    "negative": 0.24510699976352,
    "neutral": 0.1784076690697206,
    "mixed": 0.32212821019782156
  }
}
```

---

### 6.2 Text Hash Engine - Filter Testing

#### Test Case: Filter Positive Above 0.5

**Input**:
```json
{
  "hash_mapping": {
    "b10a8db164": "Hello World",    // positive: 0.6158 ✓
    "f1feeaa3d6": "Test Text",       // positive: 0.2842 ✗
    "0cbc6611f5": "Test"             // positive: 0.4257 ✗
  },
  "classification_criteria": "positive",
  "filter_mode": "above",
  "threshold": 0.5
}
```

**Expected Output**:
```json
{
  "filtered_hashes": ["b10a8db164"],
  "filtered_count": 1,
  "total_hashes": 3
}
```

---

#### Test Case: Filter Negative Below 0.2

**Input**:
```json
{
  "hash_mapping": {
    "b10a8db164": "Hello World",    // negative: 0.0609 ✓
    "f1feeaa3d6": "Test Text",       // negative: 0.2529 ✗
    "0cbc6611f5": "Test"             // negative: 0.1060 ✓
  },
  "classification_criteria": "negative",
  "filter_mode": "below",
  "threshold": 0.2
}
```

**Expected Output**:
```json
{
  "filtered_hashes": ["b10a8db164", "0cbc6611f5"],
  "filtered_count": 2,
  "total_hashes": 3
}
```

---

#### Test Case: Multi-Criteria AND Filter

**Input**:
```json
{
  "hash_mapping": {
    "b5ead10d6e": "Positive text",  // pos: 0.4119 ✓, neg: 0.3534 ✓
    "9204d57da8": "Another text"    // pos: 0.2544 ✗, neg: 0.2451 ✓
  },
  "criterion_filters": [
    {"criterion": "positive", "filter_mode": "above", "threshold": 0.3},
    {"criterion": "negative", "filter_mode": "above", "threshold": 0.2}
  ],
  "logic_operator": "and"
}
```

**Expected Output**:
```json
{
  "filtered_hashes": ["b5ead10d6e"],  // Both criteria match
  "filtered_count": 1,
  "total_hashes": 2
}
```

---

#### Test Case: Multi-Criteria OR Filter

**Input**:
```json
{
  "hash_mapping": {
    "b10a8db164": "Hello World",    // pos: 0.6158 ✓, neutral: 0.2945 ✗
    "1ba249ca59": "Sample text"     // pos: 0.0526 ✗, neutral: 0.3872 ✓
  },
  "criterion_filters": [
    {"criterion": "positive", "filter_mode": "above", "threshold": 0.5},
    {"criterion": "neutral", "filter_mode": "above", "threshold": 0.3}
  ],
  "logic_operator": "or"
}
```

**Expected Output**:
```json
{
  "filtered_hashes": ["b10a8db164", "1ba249ca59"],  // Both pass (different criteria)
  "filtered_count": 2,
  "total_hashes": 2
}
```

---

### 6.3 AWS Comprehend Engine - Reference Values

#### Reference Text: "Hello World"

**AWS Comprehend Scores** (approximate - may vary slightly):

```json
{
  "sentiment": "Positive",
  "score": {
    "positive": 0.573,   // ±0.01
    "negative": 0.002,   // ±0.001
    "neutral": 0.424,    // ±0.01
    "mixed": 0.001       // ±0.0005
  }
}
```

**Characteristics**:
- Dominant sentiment: Positive (57%)
- Secondary sentiment: Neutral (42%)
- Minimal negative/mixed (<1%)

**Test Usage** (with tolerance):
```python
def test_hello_world_aws_comprehend():
    response = classify("Hello World", engine_mode="aws_comprehend")
    scores = response["hash_ratings"][hash_id]
    
    # Use tolerance for AWS Comprehend (non-deterministic)
    assert 0.56 <= float(scores["positive"]) <= 0.58
    assert 0.00 <= float(scores["negative"]) <= 0.01
    assert 0.41 <= float(scores["neutral"]) <= 0.43
    assert 0.00 <= float(scores["mixed"]) <= 0.01
```

---

#### Reference Text: "test text"

**AWS Comprehend Scores** (approximate):

```json
{
  "sentiment": "Neutral",
  "score": {
    "positive": 0.016,   // ±0.01
    "negative": 0.014,   // ±0.01
    "neutral": 0.933,    // ±0.01
    "mixed": 0.037       // ±0.01
  }
}
```

**Characteristics**:
- Dominant sentiment: Neutral (93%)
- Very low positive/negative
- Factual/objective tone

---

#### Reference Text: "This is terrible and awful"

**AWS Comprehend Scores** (approximate):

```json
{
  "sentiment": "Negative",
  "score": {
    "positive": 0.000,   // ±0.001
    "negative": 0.9997,  // ±0.001
    "neutral": 0.0002,   // ±0.001
    "mixed": 0.00002     // ±0.0001
  }
}
```

**Characteristics**:
- Dominant sentiment: Negative (>99%)
- Extremely polarized (almost pure negative)
- Strong emotional language detected

---

### 6.4 Complete Reference Table

**Deterministic Test Data (Text Hash Engine)**

| Hash | Text | Positive | Negative | Neutral | Mixed | Primary |
|------|------|----------|----------|---------|-------|---------|
| `b10a8db164` | Hello World | 0.6158 | 0.0609 | 0.2945 | 0.0289 | Positive |
| `f1feeaa3d6` | Test Text | 0.2842 | 0.2529 | 0.1381 | 0.3248 | Mixed |
| `0cbc6611f5` | Test | 0.4257 | 0.1060 | 0.2211 | 0.2472 | Positive |
| `1ba249ca59` | Sample text | 0.0526 | 0.4057 | 0.3872 | 0.1545 | Negative |
| `b5ead10d6e` | Positive text | 0.4119 | 0.3534 | 0.1431 | 0.0916 | Positive |
| `9204d57da8` | Another text | 0.2544 | 0.2451 | 0.1784 | 0.3221 | Mixed |

**Note**: Primary = highest scoring criterion

---

## 7. Practical Examples

### 7.1 Example 1: Filter Positive Content (AWS Comprehend)

**Scenario**: Show only highly positive customer reviews

**Request**:
```bash
curl -X POST "https://semantic-text.dev.mgraph.ai/semantic-classification/aws_comprehend/filter" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "hash_mapping": {
      "aaa1111111": "This product is amazing! Best purchase ever!",
      "bbb2222222": "It'\''s okay, nothing special.",
      "ccc3333333": "Terrible quality, very disappointed."
    },
    "classification_criteria": "positive",
    "filter_mode": "above",
    "threshold": 0.8,
    "output_mode": "full-ratings"
  }'
```

**Response**:
```json
{
  "filtered_hashes": ["aaa1111111"],
  "filtered_with_text": {
    "aaa1111111": "This product is amazing! Best purchase ever!"
  },
  "filtered_with_ratings": {
    "aaa1111111": {
      "positive": 0.9903,
      "negative": 0.0009,
      "neutral": 0.0078,
      "mixed": 0.0008
    }
  },
  "classification_criteria": "positive",
  "output_mode": "full-ratings",
  "total_hashes": 3,
  "filtered_count": 1,
  "success": true
}
```

**Result**: Only "This product is amazing!" passes (positive=0.99 > 0.8)

---

### 7.2 Example 2: Deterministic Testing (Text Hash)

**Scenario**: CI/CD pipeline test with reproducible results

**Request**:
```bash
curl -X POST "https://semantic-text.dev.mgraph.ai/semantic-classification/text_hash/rate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "hash_mapping": {
      "b10a8db164": "Hello World",
      "f1feeaa3d6": "Test Text"
    }
  }'
```

**Response** (always identical):
```json
{
  "hash_ratings": {
    "b10a8db164": {
      "positive": 0.61575136853258,
      "negative": 0.06092177291188416,
      "neutral": 0.2944552357407734,
      "mixed": 0.028871622814762493
    },
    "f1feeaa3d6": {
      "positive": 0.2842339724966105,
      "negative": 0.25290528762347475,
      "neutral": 0.1380980050358319,
      "mixed": 0.3247627348440829
    }
  },
  "total_hashes": 2,
  "success": true
}
```

**Test Assertion**:
```python
def test_classification_deterministic():
    response = call_classification_service(
        hash_mapping={"b10a8db164": "Hello World"},
        engine_mode="text_hash"
    )
    
    # Exact assertion (no tolerance needed)
    assert response["hash_ratings"]["b10a8db164"]["positive"] == 0.61575136853258
    assert response["hash_ratings"]["b10a8db164"]["negative"] == 0.06092177291188416
```

---

### 7.3 Example 3: Multi-Criteria Filtering (AND Logic)

**Scenario**: Find content that is both positive AND not negative (purely positive)

**Request**:
```bash
curl -X POST "https://semantic-text.dev.mgraph.ai/semantic-classification/text_hash/multi/filter" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "hash_mapping": {
      "b10a8db164": "Hello World",
      "b5ead10d6e": "Positive text",
      "1ba249ca59": "Sample text"
    },
    "criterion_filters": [
      {
        "criterion": "positive",
        "filter_mode": "above",
        "threshold": 0.5
      },
      {
        "criterion": "negative",
        "filter_mode": "below",
        "threshold": 0.1
      }
    ],
    "logic_operator": "and",
    "output_mode": "hashes-only"
  }'
```

**Response**:
```json
{
  "filtered_hashes": ["b10a8db164"],
  "criteria_used": ["positive", "negative"],
  "logic_operator": "and",
  "output_mode": "hashes-only",
  "total_hashes": 3,
  "filtered_count": 1,
  "success": true
}
```

**Explanation**:
- `b10a8db164` ("Hello World"): positive=0.6158 (>0.5 ✓), negative=0.0609 (<0.1 ✓) → **PASS**
- `b5ead10d6e` ("Positive text"): positive=0.4119 (<0.5 ✗) → **FAIL**
- `1ba249ca59` ("Sample text"): negative=0.4057 (>0.1 ✗) → **FAIL**

---

### 7.4 Example 4: Text Transformation with Filtering

**Scenario**: Mask negative comments on a forum, show positive/neutral comments

**Request**:
```bash
curl -X POST "https://semantic-text.dev.mgraph.ai/text-transformation/transform" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "hash_mapping": {
      "aaa1111111": "Great discussion, learned a lot!",
      "bbb2222222": "This is stupid and makes no sense.",
      "ccc3333333": "Thanks for sharing the link."
    },
    "engine_mode": "aws_comprehend",
    "criterion_filters": [
      {
        "criterion": "negative",
        "filter_mode": "above",
        "threshold": 0.7
      }
    ],
    "logic_operator": "and",
    "transformation_mode": "xxx"
  }'
```

**Response**:
```json
{
  "transformed_mapping": {
    "aaa1111111": "Great discussion, learned a lot!",
    "bbb2222222": "xxxx xx xxxxxx xxx xxxxx xx xxxxx.",
    "ccc3333333": "Thanks for sharing the link."
  },
  "transformation_mode": "xxx",
  "success": true,
  "total_hashes": 3,
  "transformed_hashes": 1
}
```

**Result**:
- Positive comment: Unchanged
- Negative comment: Masked to "xxxx xx xxxxxx..."
- Neutral comment: Unchanged

---

### 7.5 Example 5: ABCDE Grouping by Size

**Scenario**: Group text by length and visualize structure

**Request**:
```bash
curl -X POST "https://semantic-text.dev.mgraph.ai/text-transformation/transform" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "hash_mapping": {
      "aaa1111111": "Hi",
      "bbb2222222": "Hello World",
      "ccc3333333": "This is a longer sentence with more words.",
      "ddd4444444": "Medium length text here."
    },
    "engine_mode": null,
    "criterion_filters": [],
    "transformation_mode": "abcde-by-size"
  }'
```

**Response**:
```json
{
  "transformed_mapping": {
    "aaa1111111": "aa",
    "bbb2222222": "bbbbb bbbbb",
    "ccc3333333": "dddd dd d dddddd dddddddd dddd dddd ddddd.",
    "ddd4444444": "cccccc cccccc cccc cccc."
  },
  "transformation_mode": "abcde-by-size",
  "success": true,
  "total_hashes": 4,
  "transformed_hashes": 4
}
```

**Explanation**:
- Group A (shortest): "Hi" → "aa"
- Group B: "Hello World" → "bbbbb bbbbb"
- Group C: "Medium length text here." → "cccccc cccccc cccc cccc."
- Group D (longest): "This is a longer..." → "dddd dd d dddddd..."

**Note**: ABCDE mode ALWAYS transforms all hashes (ignores filters)

---

### 7.6 Example 6: Path Parameters Endpoint

**Scenario**: Quick single-criterion filter using path params

**Request**:
```bash
curl -X POST "https://semantic-text.dev.mgraph.ai/text-transformation/transform/text_hash/xxx/negative/above/0.3" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "hash_mapping": {
      "b10a8db164": "Hello World",
      "1ba249ca59": "Sample text"
    }
  }'
```

**Response**:
```json
{
  "transformed_mapping": {
    "b10a8db164": "Hello World",        // negative=0.0609 (<0.3) - unchanged
    "1ba249ca59": "xxxxxx xxxx"         // negative=0.4057 (>0.3) - masked
  },
  "transformation_mode": "xxx",
  "success": true,
  "total_hashes": 2,
  "transformed_hashes": 1
}
```

**Path Parameters Breakdown**:
- `text_hash`: Engine mode
- `xxx`: Transformation mode
- `negative`: Criterion to filter
- `above`: Filter mode
- `0.3`: Threshold value

---

## 8. Best Practices

### 8.1 Testing Strategies

#### Deterministic Unit Tests

**Use**: `text_hash` engine for reproducible tests

```python
def test_positive_filter():
    """Deterministic test with text_hash engine"""
    hash_mapping = {"b10a8db164": "Hello World"}
    
    response = filter_hashes(
        hash_mapping=hash_mapping,
        engine_mode="text_hash",
        criteria="positive",
        threshold=0.5
    )
    
    # Exact assertions (no tolerance needed)
    assert response["filtered_count"] == 1
    assert "b10a8db164" in response["filtered_hashes"]
    assert response["filtered_with_ratings"]["b10a8db164"]["positive"] == 0.61575136853258
```

---

#### Integration Tests with AWS Comprehend

**Use**: Tolerance ranges for non-deterministic results

```python
def test_positive_filter_aws():
    """Integration test with AWS Comprehend (with tolerance)"""
    hash_mapping = {"abc1234567": "Hello World"}
    
    response = filter_hashes(
        hash_mapping=hash_mapping,
        engine_mode="aws_comprehend",
        criteria="positive",
        threshold=0.5
    )
    
    # Tolerance-based assertions
    assert response["filtered_count"] == 1
    positive_score = response["filtered_with_ratings"]["abc1234567"]["positive"]
    assert 0.55 <= positive_score <= 0.60  # ±5% tolerance
```

---

#### Test Data Recommendations

**Text Hash Engine Reference Data**:

```python
# Use known deterministic values from reference tables
TEST_DATA = {
    "b10a8db164": {
        "text": "Hello World",
        "expected": {
            "positive": 0.61575136853258,
            "negative": 0.06092177291188416,
            "neutral": 0.2944552357407734,
            "mixed": 0.028871622814762493
        }
    },
    "f1feeaa3d6": {
        "text": "Test Text",
        "expected": {
            "positive": 0.2842339724966105,
            "negative": 0.25290528762347475,
            "neutral": 0.1380980050358319,
            "mixed": 0.3247627348440829
        }
    }
}
```

---

### 8.2 Common Pitfalls

#### Pitfall 1: Forgetting Engine Mode Path Parameter

**❌ Wrong**:
```bash
POST /semantic-classification/rate
```

**✅ Correct**:
```bash
POST /semantic-classification/text_hash/rate
```

---

#### Pitfall 2: Misunderstanding AND vs OR Logic

**❌ Wrong Understanding**: "AND means both scores must be high"

```python
# This does NOT mean "both positive AND negative are high"
criterion_filters = [
    {"criterion": "positive", "filter_mode": "above", "threshold": 0.7},
    {"criterion": "negative", "filter_mode": "above", "threshold": 0.7}
]
logic_operator = "and"
# Result: Rarely matches (AWS scores are polarized!)
```

**✅ Correct Understanding**: "AND means all conditions must pass"

```python
# Correct: High positive AND low negative
criterion_filters = [
    {"criterion": "positive", "filter_mode": "above", "threshold": 0.7},
    {"criterion": "negative", "filter_mode": "below", "threshold": 0.1}
]
logic_operator = "and"
# Result: Purely positive content
```

---

#### Pitfall 3: Wrong Output Mode Selection

**❌ Wrong**: Using `hashes-only` when you need text reconstruction

```python
response = filter_hashes(
    hash_mapping=mapping,
    output_mode="hashes-only"
)

# ERROR: filtered_with_text is empty!
for hash_id in response["filtered_hashes"]:
    text = response["filtered_with_text"][hash_id]  # KeyError!
```

**✅ Correct**: Use appropriate output mode

```python
response = filter_hashes(
    hash_mapping=mapping,
    output_mode="hashes-with-text"  # or "full-ratings"
)

# SUCCESS: Text available
for hash_id in response["filtered_hashes"]:
    text = response["filtered_with_text"][hash_id]
```

---

#### Pitfall 4: Interpreting AWS Comprehend Scores Incorrectly

**❌ Wrong**: Expecting balanced scores

```python
# AWS Comprehend is polarized - one score dominates
# Example: "Great product!" 
# Expecting: {"positive": 0.5, "negative": 0.3, "neutral": 0.2}
# Reality:   {"positive": 0.99, "negative": 0.001, "neutral": 0.008}
```

**✅ Correct**: Expect polarization

```python
# Use single dominant criterion for filtering
if scores["positive"] > 0.7:
    category = "positive"
elif scores["negative"] > 0.7:
    category = "negative"
elif scores["neutral"] > 0.6:
    category = "neutral"
else:
    category = "mixed"
```

---

#### Pitfall 5: ABCDE Mode Ignores Filters

**❌ Wrong**: Expecting ABCDE to respect filters

```python
response = transform(
    hash_mapping=mapping,
    engine_mode="text_hash",
    criterion_filters=[{"criterion": "negative", "filter_mode": "above", "threshold": 0.7}],
    transformation_mode="abcde-by-size"
)
# Result: ALL hashes transformed (filters ignored!)
```

**✅ Correct**: Use xxx or hashes for filtered transformations

```python
response = transform(
    hash_mapping=mapping,
    engine_mode="text_hash",
    criterion_filters=[{"criterion": "negative", "filter_mode": "above", "threshold": 0.7}],
    transformation_mode="xxx"  # Respects filters
)
# Result: Only negative hashes transformed
```

---

## 9. Appendices

### Appendix A: Complete Schema Definitions

#### Schema__Classification__Request

```python
from osbot_utils.type_safe.Type_Safe import Type_Safe
from typing import Dict

class Schema__Classification__Request(Type_Safe):
    hash_mapping: Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]
```

---

#### Schema__Classification__Filter_Request

```python
class Schema__Classification__Filter_Request(Type_Safe):
    hash_mapping: Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]
    classification_criteria: Enum__Text__Classification__Criteria
    filter_mode: Enum__Classification__Filter_Mode
    threshold: Safe_Float
    output_mode: Enum__Classification__Output_Mode
```

---

#### Schema__Classification__Multi_Criteria_Filter_Request

```python
class Schema__Classification__Multi_Criteria_Filter_Request(Type_Safe):
    hash_mapping: Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]
    criterion_filters: List[Schema__Classification__Criterion_Filter]
    logic_operator: Enum__Classification__Logic_Operator
    output_mode: Enum__Classification__Output_Mode

class Schema__Classification__Criterion_Filter(Type_Safe):
    criterion: Enum__Text__Classification__Criteria
    filter_mode: Enum__Classification__Filter_Mode
    threshold: Safe_Float
```

---

#### Schema__Text__Transformation__Request

```python
class Schema__Text__Transformation__Request(Type_Safe):
    hash_mapping: Dict[Safe_Str__Hash, Safe_Str__Comprehend__Text]
    engine_mode: Enum__Text__Transformation__Engine_Mode  # Optional
    criterion_filters: List[Schema__Classification__Criterion_Filter]  # Optional
    logic_operator: Enum__Classification__Logic_Operator
    transformation_mode: Enum__Text__Transformation__Mode
```

---

### Appendix B: Environment Variables Reference

**FastAPI Service Authentication**:

```bash
# Service-level API key (required)
FAST_API__AUTH__API_KEY__NAME=X-API-Key
FAST_API__AUTH__API_KEY__VALUE=your-service-api-key-here
```

**AWS Comprehend Engine** (required only for `aws_comprehend` engine mode):

```bash
# AWS Comprehend service URL
AUTH__SERVICE__AWS__COMPREHEND__BASE_URL=https://aws-comprehend.dev.mgraph.ai

# AWS Comprehend API key header name
AUTH__SERVICE__AWS__COMPREHEND__KEY_NAME=X-API-Key

# AWS Comprehend API key value
AUTH__SERVICE__AWS__COMPREHEND__KEY_VALUE=your-comprehend-api-key-here
```

---

**Solution**:
```python
# Use xxx or hashes mode for filtered transformations
transformation_mode = "xxx"  # Not "abcde-by-size"
```

---

### Appendix C: API Quick Reference Card

**Base URL**: `https://semantic-text.dev.mgraph.ai`

**Authentication**: `X-API-Key` header

#### Semantic Classification

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/{engine}/rate` | POST | Get all 4 scores |
| `/{engine}/filter` | POST | Filter single criterion |
| `/{engine}/multi/rate` | POST | Get all 4 scores (multi) |
| `/{engine}/multi/filter` | POST | Filter multi-criteria |

#### Text Transformation

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/transform` | POST | Transform with filtering |
| `/transform/{params...}` | POST | Transform (path params) |

#### Engine Modes

| Mode | Type | Cost | Deterministic |
|------|------|------|---------------|
| `aws_comprehend` | ML | $$ | No |
| `text_hash` | Hash | Free | Yes |
| `random` | Random | Free | No |

#### Filter Modes

| Mode | Operator | Example |
|------|----------|---------|
| `above` | `>` | `score > 0.7` |
| `below` | `<` | `score < 0.3` |

#### Transformation Modes

| Mode | Behavior |
|------|----------|
| `xxx` | Mask characters |
| `hashes` | Show hash IDs |
| `abcde-by-size` | Group by length |

---

## Document End

**Version**: v0.6.8  
**Last Updated**: November 17, 2025  
**Feedback**: For questions or corrections, contact the MGraph AI team

---
