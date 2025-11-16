from unittest                                                                           import TestCase
from mgraph_ai_service_semantic_text.schemas.topic.enums.Enum__Classification__Topic   import Enum__Classification__Topic


class test_Enum__Classification__Topic(TestCase):

    def test__enum_technology_topics(self):                                     # Test technology-related topics
        assert Enum__Classification__Topic.TECHNOLOGY_SOFTWARE.value == 'technology-software'
        assert Enum__Classification__Topic.TECHNOLOGY_HARDWARE.value == 'technology-hardware'
        assert Enum__Classification__Topic.TECHNOLOGY_AI_ML.value    == 'technology-ai_ml'

    def test__enum_business_topics(self):                                       # Test business-related topics
        assert Enum__Classification__Topic.BUSINESS_FINANCE.value     == 'business-finance'
        assert Enum__Classification__Topic.BUSINESS_MARKETING.value   == 'business-marketing'
        assert Enum__Classification__Topic.BUSINESS_OPERATIONS.value  == 'business-operations'

    def test__enum_health_topics(self):                                         # Test health-related topics
        assert Enum__Classification__Topic.HEALTH_MEDICAL.value  == 'health-medical'
        assert Enum__Classification__Topic.HEALTH_WELLNESS.value == 'health-wellness'
        assert Enum__Classification__Topic.HEALTH_MENTAL.value   == 'health-mental'

    def test__enum_education_topics(self):                                      # Test education-related topics
        assert Enum__Classification__Topic.EDUCATION_ACADEMIC.value == 'education-academic'
        assert Enum__Classification__Topic.EDUCATION_TRAINING.value == 'education-training'
        assert Enum__Classification__Topic.EDUCATION_ONLINE.value   == 'education-online'

    def test__enum_general_topics(self):                                        # Test general topics
        assert Enum__Classification__Topic.GENERAL_NEWS.value          == 'general-news'
        assert Enum__Classification__Topic.GENERAL_ENTERTAINMENT.value == 'general-entertainment'
        assert Enum__Classification__Topic.GENERAL_LIFESTYLE.value     == 'general-lifestyle'

    def test__enum_count(self):                                                 # Test total number of topics (3 per category × 5 categories = 15)
        assert len(Enum__Classification__Topic) == 15

    def test__enum_categories(self):                                            # Test topics are organized into categories
        all_topics = [topic.value for topic in Enum__Classification__Topic]

        # Technology (3 topics)
        technology_topics = [t for t in all_topics if t.startswith('technology-')]
        assert len(technology_topics) == 3

        # Business (3 topics)
        business_topics = [t for t in all_topics if t.startswith('business-')]
        assert len(business_topics) == 3

        # Health (3 topics)
        health_topics = [t for t in all_topics if t.startswith('health-')]
        assert len(health_topics) == 3

        # Education (3 topics)
        education_topics = [t for t in all_topics if t.startswith('education-')]
        assert len(education_topics) == 3

        # General (3 topics)
        general_topics = [t for t in all_topics if t.startswith('general-')]
        assert len(general_topics) == 3

    def test__string_conversion(self):                                          # Test enum to string conversion
        assert Enum__Classification__Topic.TECHNOLOGY_SOFTWARE == 'technology-software'
        assert Enum__Classification__Topic.HEALTH_MEDICAL == 'health-medical'
        assert Enum__Classification__Topic.GENERAL_NEWS == 'general-news'

    def test__enum_from_string(self):                                           # Test creating enum from string value
        assert Enum__Classification__Topic('technology-software') == Enum__Classification__Topic.TECHNOLOGY_SOFTWARE
        assert Enum__Classification__Topic('health-medical'     ) == Enum__Classification__Topic.HEALTH_MEDICAL
        assert Enum__Classification__Topic('general-news'       ) == Enum__Classification__Topic.GENERAL_NEWS

    def test__enum_uniqueness(self):                                            # Test all enum values are unique
        values = [topic.value for topic in Enum__Classification__Topic]
        assert len(values) == len(set(values))                                  # No duplicates

    def test__enum_iteration(self):                                             # Test iterating over all topics
        topics = list(Enum__Classification__Topic)

        assert len(topics) == 15
        assert Enum__Classification__Topic.TECHNOLOGY_SOFTWARE  in topics
        assert Enum__Classification__Topic.BUSINESS_FINANCE     in topics
        assert Enum__Classification__Topic.HEALTH_MEDICAL       in topics
        assert Enum__Classification__Topic.EDUCATION_ACADEMIC   in topics
        assert Enum__Classification__Topic.GENERAL_NEWS         in topics

    def test__naming_convention(self):                                          # Test naming convention (category-subcategory)
        print()
        for topic in Enum__Classification__Topic:
            value = topic.value
            assert '-' in value                                                 # Should contain hyphen
            parts = value.split('-')
            assert len(parts) == 2                                              # Should be category-subcategory
            assert parts[0] in ['technology', 'business', 'health', 'education', 'general']