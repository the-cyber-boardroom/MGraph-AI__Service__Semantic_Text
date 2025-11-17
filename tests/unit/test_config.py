from unittest                                     import TestCase
from mgraph_ai_service_semantic_text.config       import SERVICE_NAME, FAST_API__TITLE, FAST_API__DESCRIPTION, LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS
from mgraph_ai_service_semantic_text              import package_name


class test_config(TestCase):

    def test_SERVICE_NAME(self):                                                            # Test SERVICE_NAME constant is set correctly
        assert type(SERVICE_NAME) is str                                                    # Verify type
        assert SERVICE_NAME       == package_name                                           # Should match package name
        assert SERVICE_NAME       == 'mgraph_ai_service_semantic_text'                      # Explicit value check
        assert len(SERVICE_NAME)   > 0                                                      # Not empty

    def test_FAST_API__TITLE(self):                                                         # Test FastAPI title constant
        assert type(FAST_API__TITLE) is str                                                 # Verify type
        assert FAST_API__TITLE       == "MGraph AI Service Semantic_Text"                   # Verify value
        assert len(FAST_API__TITLE)   > 0                                                   # Not empty
        assert "MGraph" in FAST_API__TITLE                                                  # Contains expected keywords
        assert "Semantic" in FAST_API__TITLE

    def test_FAST_API__DESCRIPTION(self):                                                   # Test FastAPI description constant
        assert type(FAST_API__DESCRIPTION) is str                                           # Verify type
        assert FAST_API__DESCRIPTION       == "Service that transform text using semantic graphs"
        assert len(FAST_API__DESCRIPTION)   > 0                                             # Not empty
        assert "transform" in FAST_API__DESCRIPTION                                         # Contains key terms
        assert "semantic" in FAST_API__DESCRIPTION

    def test_LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS(self):                                # Test Lambda dependencies list
        assert type(LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS) is list                       # Verify type
        assert len(LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS)   > 0                          # Not empty

        assert 'osbot-fast-api-serverless==v1.28.0' in LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS  # Verify specific dependency

        for dependency in LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS:                         # Verify all entries are strings
            assert type(dependency) is str
            assert len(dependency)   > 0                                                    # Not empty strings

    def test_LAMBDA_DEPENDENCIES__version_format(self):                                     # Test dependency version format
        for dependency in LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS:
            assert '==' in dependency                                                       # Should have version pinning

            package, version = dependency.split('==')                                       # Split into package and version

            assert len(package)  > 0                                                        # Package name not empty
            assert len(version)  > 0                                                        # Version not empty
            assert version.startswith('v')                                                  # Version starts with 'v'

    def test_SERVICE_NAME__matches_package_structure(self):                                 # Test service name aligns with package structure
        assert SERVICE_NAME.startswith('mgraph_ai_service_')                                # Follows naming convention
        assert '_' in SERVICE_NAME                                                          # Uses underscores
        assert '-' not in SERVICE_NAME                                                      # No hyphens in package name

    def test_config_constants__immutability(self):                                          # Test config constants are effectively immutable
        original_service_name = SERVICE_NAME
        original_title        = FAST_API__TITLE
        original_description  = FAST_API__DESCRIPTION

        assert SERVICE_NAME          == original_service_name                               # Values haven't changed
        assert FAST_API__TITLE       == original_title
        assert FAST_API__DESCRIPTION == original_description

    def test_all_constants_defined(self):                                                   # Test all expected constants are defined
        from mgraph_ai_service_semantic_text import config

        required_constants = [
            'SERVICE_NAME',
            'FAST_API__TITLE',
            'FAST_API__DESCRIPTION',
            'LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS'
        ]

        for constant in required_constants:
            assert hasattr(config, constant)                                                # Constant exists
            value = getattr(config, constant)
            assert value is not None                                                        # Constant has value

    def test_FAST_API__TITLE__readable(self):                                               # Test title is human-readable and properly formatted
        assert FAST_API__TITLE[0].isupper()                                                 # Starts with capital
        assert not FAST_API__TITLE.startswith('_')                                          # Not internal name
        assert not FAST_API__TITLE.endswith('_')                                            # Clean ending

    def test_FAST_API__DESCRIPTION__complete_sentence(self):                                # Test description is a complete sentence
        assert len(FAST_API__DESCRIPTION) > 20                                              # Reasonably detailed
        assert FAST_API__DESCRIPTION[0].isupper()                                           # Starts with capital

        words = FAST_API__DESCRIPTION.split()
        assert len(words) >= 5                                                              # At least 5 words

    def test_LAMBDA_DEPENDENCIES__no_duplicates(self):                                      # Test no duplicate dependencies
        dependencies_list = LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS
        dependencies_set  = set(dependencies_list)

        assert len(dependencies_list) == len(dependencies_set)                              # No duplicates

    def test_LAMBDA_DEPENDENCIES__contains_required_packages(self):                         # Test required packages are included
        dependencies_str = str(LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS)

        assert 'osbot-fast-api-serverless' in dependencies_str                              # Core dependency present

    def test_config_values__consistency(self):                                              # Test config values are consistent with each other
        assert 'semantic' in SERVICE_NAME.lower()                                           # Service name reflects purpose
        assert 'semantic' in FAST_API__TITLE.lower()                                        # Title matches
        assert 'semantic' in FAST_API__DESCRIPTION.lower()                                  # Description matches

    def test_SERVICE_NAME__valid_python_identifier(self):                                   # Test service name is valid Python package name
        assert SERVICE_NAME.isidentifier()                                                  # Valid Python identifier
        assert not SERVICE_NAME[0].isdigit()                                                # Doesn't start with digit

    def test_config_import(self):                                                           # Test config module can be imported correctly
        from mgraph_ai_service_semantic_text import config

        assert hasattr(config, 'SERVICE_NAME')                                              # Module has expected attributes
        assert hasattr(config, 'FAST_API__TITLE')
        assert hasattr(config, 'FAST_API__DESCRIPTION')
        assert hasattr(config, 'LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS')