# Supplementary Context: Integration Implementation Guide

**Purpose:** Fill gaps in Document 4 with critical details from Documents 1-3  
**Use With:** Document 4 (Technical Brief) + Full Mitmproxy Codebase Access  
**Version:** v0.6.8

---

## Section 1: Files to Remove (CRITICAL)

### 1.1 Complete Removal Checklist

**WCF Service Layer (Complete Removal):**
```
✗ service/wcf/Proxy__WCF__Service.py
✗ service/wcf/WCF__Request__Handler.py
✗ service/wcf/WCF__Cache__Integrator.py
✗ service/wcf/WCF__Command__Processor.py
✗ service/wcf/__init__.py
```

**WCF Schema Layer (Complete Removal):**
```
✗ schemas/wcf/Schema__WCF__Request.py
✗ schemas/wcf/Schema__WCF__Response.py
✗ schemas/wcf/__init__.py
✗ schemas/proxy/Enum__WCF__Command_Type.py
✗ schemas/proxy/Enum__WCF__Content_Type.py
```

**Local Transformation Layer (Complete Removal):**
```
✗ service/html/HTML__Transformation__Service__Local.py
✗ service/html/Text__Grouping__Service.py
```

**Methods to Remove from Existing Files:**
```python
# From HTML__Transformation__Service.py
✗ def _transform_locally(self, ...)
✗ def _error_result(self, ...)

# From Proxy__Debug__Service.py (if exists)
✗ def process_show_command(self, ...)  # WCF-related debug command
✗ Any references to Proxy__WCF__Service
```

**Imports to Remove:**
```python
# From any file that imports WCF or Local transformation services
✗ from mgraph_ai_service_mitmproxy.service.wcf.Proxy__WCF__Service import Proxy__WCF__Service
✗ from mgraph_ai_service_mitmproxy.service.html.HTML__Transformation__Service__Local import HTML__Transformation__Service__Local
✗ from mgraph_ai_service_mitmproxy.service.html.Text__Grouping__Service import Text__Grouping__Service
```

**Rationale:** WCF service is deprecated and all functionality is replaced by HTML Service + Semantic Text Service. Local transformation code duplicates what should be in Semantic Text Service.

---

## Section 2: Files to Create (Complete Paths)

### 2.1 Exact File Structure

**Schema Layer (7 files):**
```
mgraph_ai_service_mitmproxy/schemas/semantic_text/
├── __init__.py
├── Enum__Sentiment__Criterion.py
├── Enum__Filter__Mode.py
├── Enum__Logic__Operator.py
├── Schema__Sentiment__Criterion_Filter.py
├── Schema__Sentiment__Filter_Config.py
├── Schema__Semantic_Text__Request.py
└── Schema__Semantic_Text__Response.py
```

**Service Layer (2 files):**
```
mgraph_ai_service_mitmproxy/service/semantic_text/
├── __init__.py
├── Semantic_Text__Service__Client.py
└── Semantic_Text__Transformation__Service.py
```

**Constants (1 file):**
```
mgraph_ai_service_mitmproxy/service/consts/
└── consts__semantic_text.py
```

**Test Files:**
```
tests/unit/service/semantic_text/
├── __init__.py
├── test_Semantic_Text__Service__Client.py
└── test_Semantic_Text__Transformation__Service.py

tests/integration/
└── test_semantic_text_integration.py
```

---

## Section 3: Files to Modify (Integration Points)

### 3.1 File: `service/html/HTML__Transformation__Service.py`

**Current State:** Routes to HTML Service or Local transformation  
**Target State:** Routes to HTML Service or Semantic Text Service

**Changes Required:**

**1. Add New Dependencies:**
```python
from mgraph_ai_service_mitmproxy.service.semantic_text.Semantic_Text__Service__Client import Semantic_Text__Service__Client
from mgraph_ai_service_mitmproxy.service.semantic_text.Semantic_Text__Transformation__Service import Semantic_Text__Transformation__Service
from mgraph_ai_service_mitmproxy.schemas.semantic_text.Schema__Sentiment__Filter_Config import Schema__Sentiment__Filter_Config
```

**2. Update Class Definition:**
```python
class HTML__Transformation__Service(Type_Safe):
    """Orchestrates HTML transformations via HTML Service and Semantic Text Service"""
    html_service_client     : HTML__Service__Client
    semantic_text_client    : Semantic_Text__Service__Client        # NEW
    semantic_text_service   : Semantic_Text__Transformation__Service  # NEW
    cache_service           : Proxy__Cache__Service
    
    def setup(self) -> 'HTML__Transformation__Service':
        """Initialize all service clients"""
        self.html_service_client.setup()
        self.semantic_text_client.setup()                          # NEW
        self.semantic_text_service.setup()                         # NEW
        return self
```

**3. Update Method Signature:**
```python
def transform_html(self,
                  html_content: str,
                  mode: Enum__HTML__Transformation_Mode,
                  filter_config: Optional[Schema__Sentiment__Filter_Config] = None  # NEW
             ) -> str:
```

**4. Update Routing Logic:**
```python
def transform_html(self, html_content: str, mode: Enum__HTML__Transformation_Mode,
                  filter_config: Optional[Schema__Sentiment__Filter_Config] = None) -> str:
    
    # HTML Service modes (unchanged)
    if mode in [Enum__HTML__Transformation_Mode.DICT,
                Enum__HTML__Transformation_Mode.XXX,
                Enum__HTML__Transformation_Mode.HASHES,
                Enum__HTML__Transformation_Mode.ROUNDTRIP]:
        return self._transform_via_html_service(html_content, mode)
    
    # Semantic Text Service modes (NEW - replaces local transformations)
    if mode in [Enum__HTML__Transformation_Mode.XXX_RANDOM,
                Enum__HTML__Transformation_Mode.HASHES_RANDOM,
                Enum__HTML__Transformation_Mode.ABCDE_BY_SIZE]:
        return self._transform_via_semantic_text(html_content, mode, filter_config)  # NEW
    
    return html_content
```

**5. Add New Method (from Document 4 Part 4.3):**
```python
def _transform_via_semantic_text(self,
                                html_content: str,
                                mode: Enum__HTML__Transformation_Mode,
                                filter_config: Optional[Schema__Sentiment__Filter_Config]) -> str:
    """
    Transform via Semantic Text Service with optional filtering
    [Use complete implementation from Document 4 Part 4.3]
    """
```

**6. Remove Old Methods:**
```python
# DELETE these methods:
✗ def _transform_locally(self, ...)
✗ def _error_result(self, ...)
```

---

### 3.2 File: `service/proxy/Proxy__Cookie__Service.py`

**Current Methods:** (Keep these unchanged)
```python
def get_mitm_mode(self) -> Enum__HTML__Transformation_Mode:
    """Get transformation mode from cookie"""
    # Existing implementation
```

**New Methods to Add:**

```python
def get_mitm_mode_with_filters(self, cookies: Dict[str, str]) -> Tuple[Enum__HTML__Transformation_Mode, Optional[Schema__Sentiment__Filter_Config]]:
    """
    Parse mitm-mode cookie and extract mode + filter config
    
    Returns:
        (transformation_mode, filter_config)
    
    Examples:
        "xxx" → (XXX, None)
        "xxx-negative-filter;threshold=0.7" → (XXX, FilterConfig(...))
    """
    cookie_value = cookies.get("mitm-mode", "")
    
    if not cookie_value:
        return (Enum__HTML__Transformation_Mode.OFF, None)
    
    mode, filter_config = self._parse_mitm_cookie(cookie_value)
    return (mode, filter_config)

def _parse_mitm_cookie(self, cookie_value: str) -> Tuple[Enum__HTML__Transformation_Mode, Optional[Schema__Sentiment__Filter_Config]]:
    """
    [Use complete implementation from Document 4 Part 5.2]
    """

def _extract_mode_and_criteria(self, mode_part: str) -> Tuple[str, List[str]]:
    """
    [Use complete implementation from Document 4 Part 5.2]
    """

def _build_filter_config(self, filter_criteria: List[str], params: Dict[str, str]) -> Schema__Sentiment__Filter_Config:
    """
    [Use complete implementation from Document 4 Part 5.2]
    """
```

**Pattern to Follow:** Look at existing `get_mitm_mode()` method for:
- Cookie extraction pattern
- Error handling approach
- Return type conventions

---

### 3.3 File: `service/proxy/response/Proxy__Response__Service.py`

**Find Method:** `process_html_transformation()` or similar method that:
- Receives HTTP request/response
- Extracts cookies
- Calls `HTML__Transformation__Service.transform_html()`

**Changes Required:**

**Before:**
```python
# Current pattern (find this in the code)
mode = self.cookie_service.get_mitm_mode()
transformed_html = self.html_transformation_service.transform_html(
    html_content=response.body,
    mode=mode
)
```

**After:**
```python
# New pattern with filter config
mode, filter_config = self.cookie_service.get_mitm_mode_with_filters(request.cookies)
transformed_html = self.html_transformation_service.transform_html(
    html_content=response.body,
    mode=mode,
    filter_config=filter_config  # NEW
)
```

---

### 3.4 File: `schemas/html/Enum__HTML__Transformation_Mode.py`

**Add Helper Method:**
```python
class Enum__HTML__Transformation_Mode(str, Enum):
    """HTML transformation modes"""
    OFF = "off"
    DICT = "dict"
    XXX = "xxx"
    HASHES = "hashes"
    ROUNDTRIP = "roundtrip"
    XXX_RANDOM = "xxx-random"
    HASHES_RANDOM = "hashes-random"
    ABCDE_BY_SIZE = "abcde-by-size"
    
    # Add this new method:
    def to_semantic_text_mode(self) -> str:
        """Map HTML transformation mode to Semantic Text transformation mode"""
        mapping = {
            Enum__HTML__Transformation_Mode.XXX_RANDOM: "xxx",
            Enum__HTML__Transformation_Mode.HASHES_RANDOM: "hashes",
            Enum__HTML__Transformation_Mode.ABCDE_BY_SIZE: "abcde-by-size"
        }
        return mapping.get(self, self.value)
```

---

## Section 4: Code Patterns to Follow

### 4.1 Environment Variable Loading Pattern

**Reference:** Look at `HTML__Service__Client.setup()` method

**Pattern to Follow:**
```python
def setup(self) -> 'Semantic_Text__Service__Client':
    """Initialize client with environment variables"""
    # Pattern: Use os.getenv with fallback to class default
    self.base_url = os.getenv(
        "AUTH__TARGET_SERVER__SEMANTIC_TEXT_SERVICE__BASE_URL",
        self.base_url  # Fallback to class default
    )
    
    self.api_key = os.getenv(
        "AUTH__TARGET_SERVER__SEMANTIC_TEXT_SERVICE__KEY_VALUE",
        ""
    )
    
    # Validation
    if not self.api_key:
        raise ValueError("Semantic Text Service API key not configured")
    
    return self
```

**Environment Variables to Use:**
```bash
# Required
AUTH__TARGET_SERVER__SEMANTIC_TEXT_SERVICE__BASE_URL=https://semantic-text.dev.mgraph.ai
AUTH__TARGET_SERVER__SEMANTIC_TEXT_SERVICE__KEY_NAME=X-API-Key
AUTH__TARGET_SERVER__SEMANTIC_TEXT_SERVICE__KEY_VALUE=<your-api-key>

# Optional (only for aws_comprehend engine)
AUTH__SERVICE__AWS__COMPREHEND__BASE_URL=https://aws-comprehend.dev.mgraph.ai
AUTH__SERVICE__AWS__COMPREHEND__KEY_NAME=X-API-Key
AUTH__SERVICE__AWS__COMPREHEND__KEY_VALUE=<your-api-key>
```

---

### 4.2 HTTP Client Pattern

**Reference:** Look at `HTML__Service__Client` HTTP methods

**Pattern to Follow:**
```python
def _make_request(self, endpoint: str, payload: dict) -> dict:
    """Pattern for HTTP requests"""
    url = f"{self.base_url}{endpoint}"
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers=self.get_auth_headers(),
            timeout=self.timeout
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        raise Exception(f"Request to {url} timed out after {self.timeout}s")
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error {e.response.status_code}: {e.response.text}")
    
    except Exception as e:
        raise Exception(f"Request failed: {str(e)}")
```

---

### 4.3 Caching Pattern

**Reference:** Look at existing cache usage in transformation services

**Pattern to Follow:**
```python
def _build_cache_key(self, *args) -> str:
    """Build deterministic cache key"""
    import hashlib
    import json
    
    # Create dict of all parameters that affect output
    components = {
        "param1": value1,
        "param2": value2,
        # ... all relevant parameters
    }
    
    # Sort for determinism
    key_str = json.dumps(components, sort_keys=True)
    key_hash = hashlib.md5(key_str.encode()).hexdigest()[:16]
    
    return f"semantic-text/{category}/{key_hash}"

def _get_cached_result(self, cache_key: str) -> Optional[Any]:
    """Retrieve from cache with error handling"""
    try:
        result = self.cache_service.get(cache_key)
        if result:
            print(f"         >>> Cache HIT for {cache_key}")
        return result
    except Exception as e:
        print(f"         >>> Cache retrieval failed: {e}")
        return None

def _store_cached_result(self, cache_key: str, result: Any, ttl: int = 3600) -> None:
    """Store in cache with error handling"""
    try:
        self.cache_service.set(cache_key, result, ttl=ttl)
        print(f"         >>> Cached result: {cache_key}")
    except Exception as e:
        print(f"         >>> Cache storage failed: {e}")
```

**Cache TTL Strategy:**
```python
# From Document 1 Section 10.1
CACHE_TTL = {
    "text_hash": 86400 * 7,      # 7 days (deterministic)
    "aws_comprehend": 3600,       # 1 hour (can vary)
    "random": 300                 # 5 minutes (non-deterministic)
}
```

---

### 4.4 Logging Pattern

**Reference:** Look at existing logging in transformation services

**Pattern to Follow:**
```python
# Check if codebase uses print() or logger
# If print():
print(f"    🔄 Semantic Text: {mode} transformation (engine={engine_mode})")
print(f"       Filters: {len(filters)} criteria, logic={logic}")
print(f"       Processing {len(hash_mapping)} hashes...")
print(f"       Semantic Text took {duration_ms:.0f}ms")
print(f"       Transformed {changed}/{total} hashes")
print(f"    ✅ Transformation complete")

# If logger:
logger.info(f"Semantic Text transformation started", 
           extra={"mode": mode, "engine": engine_mode, "hash_count": len(hash_mapping)})
logger.info(f"Semantic Text transformation complete",
           extra={"duration_ms": duration_ms, "transformed": changed})
```

**Error Logging:**
```python
print(f"    ⚠️  Semantic Text Service error: {str(e)}")
print(f"    ⚠️  Falling back to original HTML")

# Or with logger:
logger.error(f"Semantic Text transformation failed", 
            extra={"error": str(e), "mode": mode}, 
            exc_info=True)
```

---

### 4.5 Type_Safe Conventions

**Reference:** Look at existing Type_Safe class definitions

**Pattern to Follow:**
```python
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash import Safe_Str__Hash
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text import Safe_Str__Text

class My_Schema(Type_Safe):
    """Docstring describing the schema"""
    field_name : Type_Annotation
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Custom validation if needed
```

**Common Type_Safe Types:**
```python
Safe_Float          # Float with validation
Safe_UInt           # Unsigned integer
Safe_Str__Hash      # Hash string (for hash IDs)
Safe_Str__Text      # Text string
Dict[Safe_Str__Hash, str]  # Hash mapping type
```

---

## Section 5: Error Handling and Resilience

### 5.1 Service Failure Handling

**Pattern from Document 1 Section 9.1:**

```python
def transform_text(self, ...):
    """Transform with error handling"""
    try:
        # Attempt transformation
        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        # Timeout: Return original unchanged
        print(f"    ⚠️  Semantic Text Service timeout after {self.timeout}s")
        return {"modified_hash_mapping": hash_mapping, "success": False}
        
    except requests.exceptions.HTTPError as e:
        # HTTP error: Return original unchanged
        print(f"    ⚠️  Semantic Text Service HTTP error: {e.response.status_code}")
        return {"modified_hash_mapping": hash_mapping, "success": False}
        
    except Exception as e:
        # Unknown error: Return original unchanged
        print(f"    ⚠️  Semantic Text Service error: {str(e)}")
        return {"modified_hash_mapping": hash_mapping, "success": False}
```

**Key Principle:** On any failure, return original content unchanged. Never fail the entire request.

---

### 5.2 Retry Logic for AWS Comprehend

**Pattern from Document 1 Section 9.2:**

```python
def transform_with_retry(self, request, max_retries=3):
    """Retry logic for transient failures (aws_comprehend only)"""
    
    # No retry for deterministic engines
    if request.get("engine_mode") in ["text_hash", "random"]:
        return self.transform_text(request)
    
    # Retry for aws_comprehend
    for attempt in range(max_retries):
        try:
            response = self.transform_text(request)
            if response.get("success"):
                return response
                
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"       Retry attempt {attempt + 1}/{max_retries} after {wait_time}s")
                time.sleep(wait_time)
                continue
            raise
    
    # Max retries exceeded
    return {
        "modified_hash_mapping": request["hash_mapping"],
        "success": False,
        "error_message": "Max retries exceeded"
    }
```

---

### 5.3 Invalid Configuration Handling

**Pattern from Document 1 Section 9.1:**

```python
def _parse_mitm_cookie(self, cookie_value: str):
    """Parse cookie with graceful error handling"""
    try:
        # Parse cookie
        mode, filter_config = self._extract_components(cookie_value)
        
        # Validate threshold
        if filter_config:
            for f in filter_config.criterion_filters:
                if not (0.0 <= f.threshold <= 1.0):
                    print(f"    ⚠️  Invalid threshold {f.threshold}, ignoring filters")
                    return (mode, None)
        
        return (mode, filter_config)
        
    except Exception as e:
        print(f"    ⚠️  Cookie parsing failed: {str(e)}")
        print(f"    ⚠️  Falling back to simple mode")
        # Extract just the base mode
        base_mode = cookie_value.split('-')[0] if '-' in cookie_value else cookie_value
        return (base_mode, None)
```

---

## Section 6: Performance and Optimization

### 6.1 Cache Key Strategy

**From Document 1 Section 10.1:**

```python
def _generate_cache_key(self, 
                       hash_mapping: Dict,
                       transformation_mode: str,
                       engine_mode: Optional[str],
                       criterion_filters: Optional[List],
                       logic_operator: str) -> str:
    """
    Generate unique cache key for transformation parameters.
    
    Key includes:
    - Hash set (not text values - for privacy)
    - Transformation mode
    - Engine mode
    - Filter configuration
    - Logic operator
    """
    import hashlib
    import json
    
    # Hash the hash_mapping keys (not values)
    hash_set = sorted(hash_mapping.keys())
    hash_set_str = ",".join(hash_set)
    hash_set_hash = hashlib.md5(hash_set_str.encode()).hexdigest()[:8]
    
    # Hash the filter configuration
    if criterion_filters:
        filters_str = json.dumps({
            "filters": criterion_filters,
            "logic": logic_operator
        }, sort_keys=True)
        filters_hash = hashlib.md5(filters_str.encode()).hexdigest()[:8]
    else:
        filters_hash = "nofilter"
    
    # Build cache key
    return f"semantic_text:{transformation_mode}:{engine_mode or 'none'}:{hash_set_hash}:{filters_hash}"
```

---

### 6.2 Cache TTL by Engine

**From Document 1 Section 10.1:**

```python
def _get_cache_ttl(self, engine_mode: str) -> int:
    """Get cache TTL based on engine mode"""
    TTL_MAP = {
        "text_hash": 86400 * 7,      # 7 days - deterministic, never changes
        "aws_comprehend": 3600,       # 1 hour - ML can vary slightly
        "random": 300                 # 5 minutes - non-deterministic
    }
    return TTL_MAP.get(engine_mode, 3600)  # Default: 1 hour
```

---

### 6.3 Performance Monitoring

**From Document 1 Section 11:**

```python
import time

def transform_text(self, ...):
    """Transform with performance tracking"""
    start_time = time.time()
    
    # ... transformation logic ...
    
    duration_ms = (time.time() - start_time) * 1000
    
    # Log performance
    print(f"       Semantic Text took {duration_ms:.0f}ms")
    
    # Track metrics (if metrics system exists)
    if hasattr(self, 'metrics'):
        self.metrics.record('semantic_text.transform.duration_ms', duration_ms, {
            'mode': transformation_mode,
            'engine': engine_mode,
            'has_filters': bool(criterion_filters)
        })
    
    return result
```

---

## Section 7: Testing Patterns

### 7.1 Pytest Fixture Pattern

**Reference:** Look at existing test files in `tests/`

**Pattern to Follow:**
```python
import pytest
from mgraph_ai_service_mitmproxy.service.semantic_text.Semantic_Text__Service__Client import Semantic_Text__Service__Client

class Test_Semantic_Text__Service__Client:
    
    @pytest.fixture
    def client(self):
        """Create test client with mock configuration"""
        client = Semantic_Text__Service__Client()
        # Mock environment variables if needed
        client.base_url = "https://semantic-text.dev.mgraph.ai"
        client.api_key = "test-api-key"
        client.timeout = 30.0
        return client
    
    @pytest.fixture
    def test_hash_mapping(self):
        """Test data fixture"""
        return {
            "b10a8db164": "Hello World",
            "f1feeaa3d6": "This is terrible"
        }
```

---

### 7.2 Deterministic Test Pattern

**From Document 4 Part 6:**

```python
# Use known text_hash values for assertions
KNOWN_SCORES = {
    "b10a8db164": {  # "Hello World"
        "positive": 0.6158,
        "negative": 0.0609,
        "neutral": 0.2945,
        "mixed": 0.0289
    }
}

def test_deterministic_classification():
    """Test that text_hash engine is deterministic"""
    ratings = client.rate_hashes(
        {"b10a8db164": "Hello World"},
        engine_mode="text_hash"
    )
    
    # Assert exact values (deterministic)
    assert abs(ratings["b10a8db164"]["positive"] - 0.6158) < 0.0001
```

---

### 7.3 Mock Pattern for External Services

**Pattern to Follow:**
```python
from unittest.mock import Mock, patch

def test_with_mocked_service():
    """Test with mocked Semantic Text Service"""
    
    # Create mock
    mock_response = Mock()
    mock_response.json.return_value = {
        "modified_hash_mapping": {"hash1": "xxxxx"},
        "success": True
    }
    mock_response.status_code = 200
    
    # Patch requests.post
    with patch('requests.post', return_value=mock_response) as mock_post:
        result = client.transform_text(hash_mapping, "xxx")
        
        # Assertions
        assert mock_post.called
        assert result["hash1"] == "xxxxx"
```

---

## Section 8: Integration Testing Requirements

### 8.1 Test Coverage Requirements

**From Document 1 Section 6.3:**

**Unit Tests (Target: >80% coverage):**
- [ ] `Semantic_Text__Service__Client`: All HTTP methods
- [ ] `Semantic_Text__Transformation__Service`: Orchestration + caching
- [ ] Cookie parsing logic: All format variants
- [ ] Schema validation: All edge cases

**Integration Tests:**
- [ ] End-to-end: HTML → Classification → Transformation → Reconstruction
- [ ] Filter logic: Single criterion, multi-criteria AND, multi-criteria OR
- [ ] Engine modes: text_hash, aws_comprehend (if configured), random
- [ ] Error scenarios: Service failure, timeout, invalid config

**Manual Tests:**
- [ ] Browser testing with real pages
- [ ] Cookie configurations: All format variants
- [ ] Performance: Response times, cache hit rates

---

### 8.2 Test Data

**Deterministic Test Hashes (text_hash engine):**

```python
TEST_HASH_REFERENCE = {
    "b10a8db164": {
        "text": "Hello World",
        "scores": {"positive": 0.6158, "negative": 0.0609, "neutral": 0.2945, "mixed": 0.0289},
        "dominant": "positive"
    },
    "f1feeaa3d6": {
        "text": "This is terrible",
        "scores": {"positive": 0.0234, "negative": 0.9123, "neutral": 0.0543, "mixed": 0.0100},
        "dominant": "negative"
    },
    "0cbc6611f5": {
        "text": "Neutral statement",
        "scores": {"positive": 0.2145, "negative": 0.1234, "neutral": 0.6321, "mixed": 0.0300},
        "dominant": "neutral"
    }
}
```

---

## Section 9: Validation Checklist

### 9.1 Pre-Deployment Validation

**Before deploying:**

**Code Removal:**
- [ ] All WCF service files deleted
- [ ] All WCF schema files deleted
- [ ] All local transformation files deleted
- [ ] All WCF imports removed
- [ ] All local transformation imports removed

**New Code:**
- [ ] All 7 schema files created
- [ ] All 2 service files created
- [ ] Constants file created
- [ ] All __init__.py files updated

**Integration Points:**
- [ ] `HTML__Transformation__Service` updated
- [ ] `Proxy__Cookie__Service` updated
- [ ] `Proxy__Response__Service` updated
- [ ] `Enum__HTML__Transformation_Mode` updated

**Testing:**
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All existing tests still pass (no regressions)
- [ ] New tests added for semantic text functionality

---

### 9.2 Post-Deployment Validation

**After deploying:**

**Functional:**
- [ ] xxx-random mode works
- [ ] hashes-random mode works
- [ ] abcde-by-size mode works
- [ ] Sentiment filtering works
- [ ] Multi-criteria filtering works
- [ ] Engine mode switching works

**Performance:**
- [ ] Transformation latency < 500ms (p95) for text_hash
- [ ] Cache hit rate > 70%
- [ ] No increase in error rates

**Integration:**
- [ ] HTML Service modes still work (DICT, XXX, HASHES, ROUNDTRIP)
- [ ] No breaking changes for existing clients

---

## Section 10: Common Pitfalls to Avoid

### 10.1 Import Errors

**Issue:** Incorrect import paths

**Solution:** Follow existing import patterns:
```python
# Correct (matches codebase structure):
from mgraph_ai_service_mitmproxy.service.semantic_text.Semantic_Text__Service__Client import Semantic_Text__Service__Client

# Wrong (hypothetical incorrect paths):
from service.semantic_text.Semantic_Text__Service__Client import Semantic_Text__Service__Client
from semantic_text.Semantic_Text__Service__Client import Semantic_Text__Service__Client
```

---

### 10.2 Type_Safe Validation

**Issue:** Forgetting to call `super().__init__(**kwargs)`

**Solution:**
```python
class My_Schema(Type_Safe):
    field: Safe_Float
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # ← REQUIRED
        # Custom validation here
```

---

### 10.3 Cache Key Collisions

**Issue:** Not including all parameters in cache key

**Solution:** Include EVERYTHING that affects output:
```python
# Include:
- hash_mapping keys (not values)
- transformation_mode
- engine_mode
- ALL criterion_filters
- logic_operator

# Don't include:
- timestamp
- request_id
- user_id (unless it affects output)
```

---

### 10.4 Filter Logic Confusion

**Issue:** Confusing AND vs OR logic

**Clarification:**
```python
# OR: Hash matches if ANY criterion matches
# (negative > 0.7) OR (positive < 0.2)
# → Matches if negative > 0.7 OR positive < 0.2

# AND: Hash matches if ALL criteria match  
# (negative > 0.7) AND (positive < 0.2)
# → Matches only if negative > 0.7 AND positive < 0.2
```

---

### 10.5 Engine Mode Defaults

**Issue:** Forgetting to default to text_hash

**Solution:**
```python
# Always default to text_hash if not specified
engine_mode = filter_config.engine_mode if filter_config else "text_hash"

# Or in cookie parsing:
engine_mode = params.get("engine", "text_hash")  # Default to text_hash
```

---

## Section 11: Final Implementation Order

### Recommended Sequence:

**Phase 1: Clean Up (Day 1)**
1. Remove all WCF service files
2. Remove all WCF schema files
3. Remove local transformation files
4. Remove deprecated methods
5. Remove stale imports
6. Verify existing tests still pass

**Phase 2: Schema Layer (Day 1)**
7. Create all 7 schema files
8. Write unit tests for schemas
9. Verify schema validation works

**Phase 3: Service Client (Day 2)**
10. Create `Semantic_Text__Service__Client`
11. Implement HTTP methods
12. Add error handling
13. Write unit tests with mocks

**Phase 4: Transformation Service (Day 2)**
14. Create `Semantic_Text__Transformation__Service`
15. Implement caching logic
16. Write unit tests

**Phase 5: Integration (Day 3)**
17. Update `HTML__Transformation__Service`
18. Update `Proxy__Cookie__Service`
19. Update `Proxy__Response__Service`
20. Update `Enum__HTML__Transformation_Mode`

**Phase 6: Testing (Day 4)**
21. Write integration tests
22. Test all transformation modes
23. Test all filter configurations
24. Verify existing functionality unchanged

**Phase 7: Validation (Day 5)**
25. Run full test suite
26. Manual testing in browser
27. Performance testing
28. Documentation updates

---

## Section 12: Questions to Ask Before Starting

When starting implementation, verify these aspects of the codebase:

1. **Project Structure:**
   - What's the exact path to `service/` directory?
   - What's the exact path to `schemas/` directory?
   - Is there a `tests/` directory structure?

2. **Existing Patterns:**
   - Show me `HTML__Service__Client` implementation
   - Show me `Proxy__Cache__Service` interface
   - Show me existing logging pattern (print vs logger)
   - Show me existing error handling patterns

3. **Type_Safe Usage:**
   - What Type_Safe types are already in use?
   - Are there existing Type_Safe schemas I can reference?
   - What's the import pattern for Type_Safe classes?

4. **Environment Variables:**
   - How are environment variables currently loaded?
   - Is there a config file or direct os.getenv?
   - Where should I document new environment variables?

5. **Testing Framework:**
   - What's the test runner? (pytest, unittest, etc.)
   - Are there existing fixtures I should follow?
   - What's the test file naming convention?

6. **Integration Points:**
   - Show me `Proxy__Response__Service.process_html_transformation()`
   - Show me how cookies are currently extracted
   - Show me how `HTML__Transformation__Service` is currently called
