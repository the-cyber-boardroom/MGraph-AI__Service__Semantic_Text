from unittest                                                                                            import TestCase
from osbot_utils.utils.Env                                                                               import set_env, del_env
from mgraph_ai_service_semantic_text.schemas.enums.Enum__Text__Classification__Engine_Mode               import Enum__Text__Classification__Engine_Mode
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine                 import Semantic_Text__Engine
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__AWS_Comprehend import Semantic_Text__Engine__AWS_Comprehend
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__Hash_Based     import Semantic_Text__Engine__Hash_Based
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__Random         import Semantic_Text__Engine__Random
from mgraph_ai_service_semantic_text.service.semantic_text.engines.Semantic_Text__Engine__Factory        import Semantic_Text__Engine__Factory


ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__BASE_URL  = "AUTH__SERVICE__AWS__COMPREHEND__BASE_URL"
ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_NAME  = "AUTH__SERVICE__AWS__COMPREHEND__KEY_NAME"
ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_VALUE = "AUTH__SERVICE__AWS__COMPREHEND__KEY_VALUE"


class test_Semantic_Text__Engine__Factory(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.factory = Semantic_Text__Engine__Factory()                         # Single factory instance for all tests

        cls._setup_aws_comprehend_env_vars()                                   # Setup AWS Comprehend env vars for testing

    @classmethod
    def tearDownClass(cls):
        cls._cleanup_aws_comprehend_env_vars()                                 # Cleanup env vars after tests

    @classmethod
    def _setup_aws_comprehend_env_vars(cls):                                   # Setup test environment variables
        set_env(ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__BASE_URL , "https://test.example.com")
        set_env(ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_NAME , "X-Test-Key"             )
        set_env(ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_VALUE, "test-key-value"         )

    @classmethod
    def _cleanup_aws_comprehend_env_vars(cls):                                 # Cleanup test environment variables
        del_env(ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__BASE_URL )
        del_env(ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_NAME )
        del_env(ENV_NAME__AUTH__SERVICE__AWS__COMPREHEND__KEY_VALUE)

    # ========================================
    # Factory Initialization Tests
    # ========================================

    def test__init__(self):                                                    # Test factory initialization
        factory = Semantic_Text__Engine__Factory()

        assert type(factory) is Semantic_Text__Engine__Factory

    # ========================================
    # Singleton Behavior Tests (@cache_on_self)
    # ========================================

    def test__engine__text_hash__singleton(self):                             # Test that text_hash engine is cached (same instance returned)
        engine1 = self.factory.engine__text_hash()
        engine2 = self.factory.engine__text_hash()

        assert engine1 is engine2                                              # Same instance (singleton via @cache_on_self)
        assert type(engine1) is Semantic_Text__Engine__Hash_Based
        assert engine1.engine_mode == Enum__Text__Classification__Engine_Mode.TEXT_HASH

    def test__engine__random__singleton(self):                                # Test that random engine is cached (same instance returned)
        engine1 = self.factory.engine__random()
        engine2 = self.factory.engine__random()

        assert engine1 is engine2                                              # Same instance
        assert type(engine1) is Semantic_Text__Engine__Random
        assert engine1.engine_mode == Enum__Text__Classification__Engine_Mode.RANDOM

    def test__engine__aws_comprehend__singleton(self):                        # Test that AWS Comprehend engine is cached (same instance returned)
        engine1 = self.factory.engine__aws_comprehend()
        engine2 = self.factory.engine__aws_comprehend()

        assert engine1 is engine2                                              # Same instance
        assert type(engine1) is Semantic_Text__Engine__AWS_Comprehend
        assert engine1.engine_mode == Enum__Text__Classification__Engine_Mode.AWS_COMPREHEND

    def test__different_engines_are_different_instances(self):                # Test that different engine types are different objects
        hash_engine   = self.factory.engine__text_hash()
        random_engine = self.factory.engine__random()
        aws_engine    = self.factory.engine__aws_comprehend()

        assert hash_engine   is not random_engine                              # Different instances
        assert hash_engine   is not aws_engine
        assert random_engine is not aws_engine

    # ========================================
    # Engine Creation Tests
    # ========================================

    def test__engine__text_hash__creation(self):                              # Test text_hash engine creation and properties
        engine = self.factory.engine__text_hash()

        assert type(engine) is Semantic_Text__Engine__Hash_Based
        assert isinstance(engine, Semantic_Text__Engine)                       # Inherits from base class
        assert engine.engine_mode == Enum__Text__Classification__Engine_Mode.TEXT_HASH
        assert hasattr(engine, 'classify_text')                                # Has required method

    def test__engine__random__creation(self):                                 # Test random engine creation and properties
        engine = self.factory.engine__random()

        assert type(engine) is Semantic_Text__Engine__Random
        assert isinstance(engine, Semantic_Text__Engine)
        assert engine.engine_mode == Enum__Text__Classification__Engine_Mode.RANDOM
        assert hasattr(engine, 'classify_text')

    def test__engine__aws_comprehend__creation(self):                         # Test AWS Comprehend engine creation and configuration
        engine = self.factory.engine__aws_comprehend()

        assert type(engine) is Semantic_Text__Engine__AWS_Comprehend
        assert isinstance(engine, Semantic_Text__Engine)
        assert engine.engine_mode == Enum__Text__Classification__Engine_Mode.AWS_COMPREHEND
        assert hasattr(engine, 'classify_text')

        assert engine.base_url     == "https://test.example.com"              # Loaded from env vars
        assert engine.api_key_name == "X-Test-Key"
        assert engine.api_key      == "test-key-value"

    # ========================================
    # get_engine() Routing Tests
    # ========================================

    def test__get_engine__text_hash(self):                                    # Test get_engine routing for TEXT_HASH mode
        engine = self.factory.get_engine(Enum__Text__Classification__Engine_Mode.TEXT_HASH)

        assert type(engine) is Semantic_Text__Engine__Hash_Based
        assert engine is self.factory.engine__text_hash()                      # Same instance as direct call

    def test__get_engine__random(self):                                       # Test get_engine routing for RANDOM mode
        engine = self.factory.get_engine(Enum__Text__Classification__Engine_Mode.RANDOM)

        assert type(engine) is Semantic_Text__Engine__Random
        assert engine is self.factory.engine__random()

    def test__get_engine__aws_comprehend(self):                               # Test get_engine routing for AWS_COMPREHEND mode
        engine = self.factory.get_engine(Enum__Text__Classification__Engine_Mode.AWS_COMPREHEND)

        assert type(engine) is Semantic_Text__Engine__AWS_Comprehend
        assert engine is self.factory.engine__aws_comprehend()

    def test__get_engine__returns_singleton_instances(self):                  # Test that get_engine returns cached singleton instances
        engine1 = self.factory.get_engine(Enum__Text__Classification__Engine_Mode.TEXT_HASH)
        engine2 = self.factory.get_engine(Enum__Text__Classification__Engine_Mode.TEXT_HASH)

        assert engine1 is engine2                                              # Same singleton instance

    # ========================================
    # Error Handling Tests
    # ========================================

    def test__get_engine__invalid_mode__raises_error(self):                   # Test that invalid engine mode raises ValueError
        with self.assertRaises(ValueError) as context:
            self.factory.get_engine(Enum__Text__Classification__Engine_Mode.LLM_SINGLE)  # Future mode not implemented

        error_message = str(context.exception)
        assert "Unsupported engine mode" in error_message
        assert "llm_single" in error_message
        assert "aws_comprehend" in error_message                               # Lists supported modes
        assert "text_hash" in error_message
        assert "random" in error_message

    def test__aws_comprehend__missing_env_vars__raises_error(self):           # Test AWS Comprehend engine fails without env vars
        self._cleanup_aws_comprehend_env_vars()                                # Remove env vars

        new_factory = Semantic_Text__Engine__Factory()                         # Create new factory

        with self.assertRaises(ValueError) as context:
            new_factory.engine__aws_comprehend()

        error_message = str(context.exception)
        assert "Missing required environment variables" in error_message
        assert "AWS Comprehend" in error_message

        self._setup_aws_comprehend_env_vars()                                  # Restore env vars for other tests

    # ========================================
    # Multiple Factory Instances Tests
    # ========================================

    def test__multiple_factories__independent_caches(self):                   # Test that multiple factory instances have independent caches
        factory1 = Semantic_Text__Engine__Factory()
        factory2 = Semantic_Text__Engine__Factory()

        engine1_hash = factory1.engine__text_hash()
        engine2_hash = factory2.engine__text_hash()

        assert engine1_hash is not engine2_hash                                # Different instances (different factories)
        assert type(engine1_hash) is Semantic_Text__Engine__Hash_Based
        assert type(engine2_hash) is Semantic_Text__Engine__Hash_Based

        assert factory1.engine__text_hash() is engine1_hash                    # But each factory caches its own
        assert factory2.engine__text_hash() is engine2_hash