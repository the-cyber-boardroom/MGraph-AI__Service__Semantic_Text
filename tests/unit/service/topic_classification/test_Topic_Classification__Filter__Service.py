from unittest                                                                                                       import TestCase
from osbot_utils.testing.__                                                                                         import __
from osbot_utils.type_safe.Type_Safe                                                                                import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                               import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                                import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                                  import Safe_Str__Hash
from osbot_utils.utils.Objects                                                                                      import base_types
from mgraph_ai_service_semantic_text.schemas.topic.enums.Enum__Classification__Topic                                import Enum__Classification__Topic
from mgraph_ai_service_semantic_text.schemas.topic.Schema__Topic_Classification__Request                            import Schema__Topic_Classification__Request
from mgraph_ai_service_semantic_text.schemas.topic.Schema__Topic_Filter__Request                                    import Schema__Topic_Filter__Request
from mgraph_ai_service_semantic_text.service.topic_classification.Topic_Classification__Filter__Service             import Topic_Classification__Filter__Service
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode                 import Enum__Classification__Output_Mode
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Logic_Operator              import Enum__Classification__Logic_Operator
from mgraph_ai_service_semantic_text.service.topic_classification.Topic_Classification__Service                     import Topic_Classification__Service
from mgraph_ai_service_semantic_text.service.topic_classification.engines.Topic_Classification__Engine__Hash_Based  import Topic_Classification__Engine__Hash_Based

class test_Topic_Classification__Filter__Service(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service = Topic_Classification__Filter__Service()

    def test__init(self):                                                      # Test initialization
        with self.service as _:
            assert type(_)                            is Topic_Classification__Filter__Service
            assert _.topic_service                    is not None
            assert base_types(_)                      == [Type_Safe, object]
            assert type(_.topic_service)              is Topic_Classification__Service
            assert type(_.topic_service.topic_engine) is Topic_Classification__Engine__Hash_Based

    # ========================================
    # classify_all Tests
    # ========================================

    def test__classify_all__basic(self):                                       # Test basic classification of all hashes
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World",
                        Safe_Str__Hash("f1feeaa3d6"): "Test Text"}

        request = Schema__Topic_Classification__Request(hash_mapping   = hash_mapping                                     ,
                                                        topics         = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE ,
                                                                          Enum__Classification__Topic.BUSINESS_FINANCE    ],
                                                        min_confidence = 0.0)

        response = self.service.classify_all(request)

        assert response.success                 is True
        assert response.total_hashes            == Safe_UInt(2)
        assert len(response.hash_topic_scores)  == 2
        assert response.topics_classified       == [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE,
                                                    Enum__Classification__Topic.BUSINESS_FINANCE   ]

        assert request .obj() == __(hash_mapping     = __(b10a8db164 = 'Hello World'             ,
                                                          f1feeaa3d6 = 'Test Text'               ),
                                    topics           = ['technology-software', 'business-finance'],
                                    min_confidence   = 0.0                                        )

        assert response.obj() == __(hash_topic_scores       = __(b10a8db164 = __(technology_software = 0.2915 ,
                                                                                 business_finance    = 0.284  ),
                                                                 f1feeaa3d6 = __(technology_software = 0.3881 ,
                                                                                 business_finance    = 0.6692)) ,
                                    topics_classified       = ['technology-software', 'business-finance']     ,
                                    total_hashes            = 2                                               ,
                                    success                 = True                                            )


    def test__classify_all__with_threshold(self):                             # Test classification with min_confidence threshold
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}           # tech-software=0.7478, business-finance=0.6789, education-academic=0.1512

        request = Schema__Topic_Classification__Request(hash_mapping   = hash_mapping                                     ,
                                                        topics         = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE ,
                                                                          Enum__Classification__Topic.BUSINESS_FINANCE    ,
                                                                          Enum__Classification__Topic.EDUCATION_ACADEMIC  ],
                                                        min_confidence = 0.29                                             )

        response = self.service.classify_all(request)

        assert response.success      is True
        assert response.total_hashes == Safe_UInt(1)

        # Only scores above 0.5 should be included
        hash_scores = response.hash_topic_scores[Safe_Str__Hash("b10a8db164")]
        assert len(hash_scores) == 2                                           # Only 2 topics above threshold
        assert Enum__Classification__Topic.TECHNOLOGY_SOFTWARE     in hash_scores
        assert Enum__Classification__Topic.EDUCATION_ACADEMIC      in hash_scores
        assert Enum__Classification__Topic.BUSINESS_FINANCE    not in hash_scores

        assert response.obj() == __(hash_topic_scores       = __(b10a8db164 = __(technology_software = 0.2915 ,
                                                                                 education_academic  = 0.9113)) ,
                                     topics_classified       = ['technology-software' ,
                                                                'business-finance'    ,
                                                                'education-academic'  ]                     ,
                                     total_hashes            = 1                                            ,
                                     success                 = True                                         )


    def test__classify_all__empty_mapping(self):                              # Test with empty hash mapping
        request = Schema__Topic_Classification__Request(hash_mapping   = {}                                                 ,
                                                        topics         = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE  ],
                                                        min_confidence = 0.0)

        response = self.service.classify_all(request)

        assert response.success           is True
        assert response.total_hashes      == Safe_UInt(0)
        assert response.hash_topic_scores == {}

    def test__classify_all__no_matches_above_threshold(self):                 # Test when no topics match threshold
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}           # education-academic=0.1512, health-medical=0.0861

        request = Schema__Topic_Classification__Request(hash_mapping   = hash_mapping                                    ,
                                                        topics         = [Enum__Classification__Topic.EDUCATION_ACADEMIC ,
                                                                          Enum__Classification__Topic.HEALTH_MEDICAL     ],
                                                        min_confidence = 0.915     )                                      # Both below threshold


        response = self.service.classify_all(request)

        assert response.success                 is True
        assert response.total_hashes            == Safe_UInt(1)
        assert Safe_Str__Hash("b10a8db164") not in response.hash_topic_scores       # Hash should not be in results since no topics above threshold

        assert response.obj() == __(hash_topic_scores       = __()                                          ,
                                    topics_classified       = ['education-academic', 'health-medical']     ,
                                    total_hashes            = 1                                             ,
                                    success                 = True                                          )



    # ========================================
    # filter_by_topics Tests - AND Logic
    # ========================================

    def test__filter_by_topics__and__basic(self):                             # Test AND logic with single topic
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World",           # tech-software=0.2915
                        Safe_Str__Hash("f1feeaa3d6"): "Test Text"}             # tech-software=0.3881

        request = Schema__Topic_Filter__Request(hash_mapping     = hash_mapping                                     ,
                                                required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE],
                                                min_confidence   = 0.3880                                           ,   # for "Test Text" -> tech-software=0.3881
                                                logic_operator   = Enum__Classification__Logic_Operator.AND         ,
                                                output_mode      = Enum__Classification__Output_Mode.HASHES_ONLY    )

        response = self.service.filter_by_topics(request)

        assert response.success         is True
        assert response.filtered_count  == Safe_UInt(1)
        assert response.filtered_hashes == [Safe_Str__Hash("f1feeaa3d6")]      # Only f1feeaa3d6 > 0.3880
        assert response.topics_used     == [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE]
        assert response.logic_operator  == Enum__Classification__Logic_Operator.AND

        assert response.obj() == __(filtered_with_text   = __()                    ,
                                    filtered_with_scores = __()                    ,
                                    filtered_hashes      = ['f1feeaa3d6']          ,
                                    topics_used          = ['technology-software'] ,
                                    logic_operator       = 'and'                   ,
                                    output_mode          = 'hashes-only'           ,
                                    total_hashes         = 2                       ,
                                    filtered_count       = 1                       ,
                                    success              = True                    )



    def test__filter_by_topics__and__both_match(self):                         # Test AND logic where both topics match
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}           # tech-software=0.2915, business-finance=0.284

        request = Schema__Topic_Filter__Request(hash_mapping     = hash_mapping                                      ,
                                                required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE  ,
                                                                    Enum__Classification__Topic.BUSINESS_FINANCE     ],
                                                min_confidence   = 0.283                                              ,
                                                logic_operator   = Enum__Classification__Logic_Operator.AND           ,
                                                output_mode      = Enum__Classification__Output_Mode.FULL_RATINGS     )

        response = self.service.filter_by_topics(request)

        # Both topics are > 0.283, so should pass
        assert response.success              is True
        assert response.filtered_count       == Safe_UInt(1)
        assert response.filtered_hashes      == [Safe_Str__Hash("b10a8db164")]

        # Verify full ratings output
        assert response.filtered_with_text   is not None
        assert response.filtered_with_scores is not None
        assert Safe_Str__Hash("b10a8db164") in response.filtered_with_text
        assert Safe_Str__Hash("b10a8db164") in response.filtered_with_scores

        assert response.obj() == __(filtered_with_text       = __(b10a8db164 = 'Hello World')                                             ,
                                    filtered_with_scores     = __(b10a8db164 = __(technology_software = 0.2915 ,
                                                                                  business_finance    = 0.284 )) ,
                                    filtered_hashes          = ['b10a8db164']                                                             ,
                                    topics_used              = ['technology-software', 'business-finance']                               ,
                                    logic_operator           = 'and'                                                                      ,
                                    output_mode              = 'full-ratings'                                                             ,
                                    total_hashes             = 1                                                                          ,
                                    filtered_count           = 1                                                                          ,
                                    success                  = True                                                                       )

    def test__filter_by_topics__and__one_fails(self):                         # Test AND logic where one topic fails
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}           # tech-software=0.7478, education-academic=0.1512

        request = Schema__Topic_Filter__Request(hash_mapping     = hash_mapping                                     ,
                                                required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE ,
                                                                    Enum__Classification__Topic.EDUCATION_ACADEMIC  ],
                                                min_confidence   = Safe_Float(0.5)                                  ,
                                                logic_operator   = Enum__Classification__Logic_Operator.AND         ,
                                                output_mode      = Enum__Classification__Output_Mode.HASHES_ONLY    )

        response = self.service.filter_by_topics(request)

        # tech-software passes (0.7478 > 0.5), but education-academic fails (0.1512 < 0.5)
        # AND requires BOTH to pass
        assert response.success         is True
        assert response.filtered_count  == Safe_UInt(0)
        assert response.filtered_hashes == []


    # ========================================
    # filter_by_topics Tests - OR Logic
    # ========================================

    def test__filter_by_topics__or__any_match(self):                          # Test OR logic where any topic matches
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World",           # tech-software=0.7478, education-academic=0.1512
                        Safe_Str__Hash("f1feeaa3d6"): "Test Text"}             # tech-software=0.508,  education-academic=0.5903

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                              ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE         ,
                                Enum__Classification__Topic.EDUCATION_ACADEMIC          ],
            min_confidence   = Safe_Float(0.55)                                          ,
            logic_operator   = Enum__Classification__Logic_Operator.OR                  ,
            output_mode      = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.service.filter_by_topics(request)

        # b10a8db164: tech-software=0.7478 > 0.55 → PASS
        # f1feeaa3d6: education-academic=0.5903 > 0.55 → PASS
        assert response.success         is True
        assert response.filtered_count  == Safe_UInt(2)
        assert len(response.filtered_hashes) == 2
        assert Safe_Str__Hash("b10a8db164") in response.filtered_hashes
        assert Safe_Str__Hash("f1feeaa3d6") in response.filtered_hashes

    def test__filter_by_topics__or__none_match(self):                         # Test OR logic where no topics match
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}           # business-marketing=0.3765, health-medical=0.2608

        request = Schema__Topic_Filter__Request(hash_mapping     = hash_mapping                                     ,
                                                required_topics  = [Enum__Classification__Topic.BUSINESS_MARKETING  ,
                                                                    Enum__Classification__Topic.HEALTH_MEDICAL     ],
                                                min_confidence   = Safe_Float(0.5)                                  ,
                                                logic_operator   = Enum__Classification__Logic_Operator.OR          ,
                                                output_mode      = Enum__Classification__Output_Mode.HASHES_ONLY    )

        response = self.service.filter_by_topics(request)

        # Neither topic is > 0.5
        assert response.success         is True
        assert response.filtered_count  == Safe_UInt(0)
        assert response.filtered_hashes == []

    # ========================================
    # Output Mode Tests
    # ========================================

    def test__filter_by_topics__output_mode__hashes_only(self):               # Test HASHES_ONLY output mode
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}          # TECHNOLOGY_SOFTWARE = 2915

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                     ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE],
            min_confidence   = Safe_Float(0.2)                                  ,
            logic_operator   = Enum__Classification__Logic_Operator.AND        ,
            output_mode      = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.service.filter_by_topics(request)

        assert response.success              is True
        assert response.filtered_with_text   == {}                            # Not included in HASHES_ONLY
        assert response.filtered_with_scores == {}                            # Not included in HASHES_ONLY
        assert len(response.filtered_hashes) == 1

    def test__filter_by_topics__output_mode__hashes_with_text(self):          # Test HASHES_WITH_TEXT output mode
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                     ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE],
            min_confidence   = Safe_Float(0.2)                                  ,
            logic_operator   = Enum__Classification__Logic_Operator.AND        ,
            output_mode      = Enum__Classification__Output_Mode.HASHES_WITH_TEXT
        )

        response = self.service.filter_by_topics(request)

        assert response.success              is True
        assert response.filtered_with_text   is not None                       # Included in HASHES_WITH_TEXT
        assert response.filtered_with_scores == {}                             # Not included in HASHES_WITH_TEXT
        assert response.filtered_with_text[Safe_Str__Hash("b10a8db164")] == "Hello World"

    def test__filter_by_topics__output_mode__full_ratings(self):              # Test FULL_RATINGS output mode
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                              ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE         ,
                                Enum__Classification__Topic.BUSINESS_FINANCE            ],
            min_confidence   = Safe_Float(0.2)                                           ,
            logic_operator   = Enum__Classification__Logic_Operator.AND                 ,
            output_mode      = Enum__Classification__Output_Mode.FULL_RATINGS
        )

        response = self.service.filter_by_topics(request)

        assert response.success              is True
        assert response.filtered_with_text   is not None                       # Included in FULL_RATINGS
        assert response.filtered_with_scores is not None                       # Included in FULL_RATINGS

        # Verify text
        assert response.filtered_with_text[Safe_Str__Hash("b10a8db164")] == "Hello World"

        # Verify scores
        scores = response.filtered_with_scores[Safe_Str__Hash("b10a8db164")]
        assert Enum__Classification__Topic.TECHNOLOGY_SOFTWARE in scores
        assert Enum__Classification__Topic.BUSINESS_FINANCE    in scores
        assert float(scores[Enum__Classification__Topic.TECHNOLOGY_SOFTWARE]) == 0.2915
        assert float(scores[Enum__Classification__Topic.BUSINESS_FINANCE   ]) == 0.284

    # ========================================
    # Edge Cases
    # ========================================

    def test__filter_by_topics__empty_mapping(self):                          # Test with empty hash mapping
        request = Schema__Topic_Filter__Request(
            hash_mapping     = {}                                               ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE],
            min_confidence   = Safe_Float(0.5)                                  ,
            logic_operator   = Enum__Classification__Logic_Operator.AND        ,
            output_mode      = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.service.filter_by_topics(request)

        assert response.success         is True
        assert response.filtered_count  == Safe_UInt(0)
        assert response.filtered_hashes == []
        assert response.total_hashes    == Safe_UInt(0)

    def test__filter_by_topics__threshold_zero(self):                         # Test with min_confidence 0.0
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                     ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE],
            min_confidence   = Safe_Float(0.0)                                  ,
            logic_operator   = Enum__Classification__Logic_Operator.AND        ,
            output_mode      = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.service.filter_by_topics(request)

        # All hashes should pass with threshold 0.0
        assert response.success         is True
        assert response.filtered_count  == Safe_UInt(1)
        assert response.filtered_hashes == [Safe_Str__Hash("b10a8db164")]

    def test__filter_by_topics__threshold_one(self):                          # Test with min_confidence 1.0
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                     ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE],
            min_confidence   = Safe_Float(1.0)                                  ,
            logic_operator   = Enum__Classification__Logic_Operator.AND        ,
            output_mode      = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.service.filter_by_topics(request)

        # No hash should have confidence == 1.0 exactly
        assert response.success         is True
        assert response.filtered_count  == Safe_UInt(0)
        assert response.filtered_hashes == []

    def test__filter_by_topics__multiple_hashes(self):                        # Test with multiple hashes
        hash_mapping = {Safe_Str__Hash(f"abcde{i:05d}"): f"Text {i}" for i in range(10)}

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                     ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE],
            min_confidence   = Safe_Float(0.5)                                  ,
            logic_operator   = Enum__Classification__Logic_Operator.AND        ,
            output_mode      = Enum__Classification__Output_Mode.FULL_RATINGS
        )

        response = self.service.filter_by_topics(request)

        assert response.success      is True
        assert response.total_hashes == Safe_UInt(10)

        # All filtered hashes should have tech-software > 0.5
        for hash_key in response.filtered_hashes:
            scores = response.filtered_with_scores[hash_key]
            assert Enum__Classification__Topic.TECHNOLOGY_SOFTWARE in scores
            assert float(scores[Enum__Classification__Topic.TECHNOLOGY_SOFTWARE]) >= 0.5

    def test__filter_by_topics__three_topics_and_logic(self):                 # Test AND logic with three topics
        hash_mapping = {Safe_Str__Hash("abcd000001"): "Technology business education text"}

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                              ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE         ,
                                Enum__Classification__Topic.BUSINESS_FINANCE            ,
                                Enum__Classification__Topic.EDUCATION_ACADEMIC          ],
            min_confidence   = Safe_Float(0.3)                                           ,
            logic_operator   = Enum__Classification__Logic_Operator.AND                 ,
            output_mode      = Enum__Classification__Output_Mode.FULL_RATINGS
        )

        response = self.service.filter_by_topics(request)

        assert response.success        is True
        assert response.topics_used    == [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE ,
                                           Enum__Classification__Topic.BUSINESS_FINANCE    ,
                                           Enum__Classification__Topic.EDUCATION_ACADEMIC  ]
        assert response.logic_operator == Enum__Classification__Logic_Operator.AND

        # If any hashes pass, they must have ALL three topics >= 0.3
        for hash_key in response.filtered_hashes:
            scores = response.filtered_with_scores[hash_key]
            assert Enum__Classification__Topic.TECHNOLOGY_SOFTWARE in scores
            assert Enum__Classification__Topic.BUSINESS_FINANCE    in scores
            assert Enum__Classification__Topic.EDUCATION_ACADEMIC  in scores
            assert float(scores[Enum__Classification__Topic.TECHNOLOGY_SOFTWARE]) >= 0.3
            assert float(scores[Enum__Classification__Topic.BUSINESS_FINANCE   ]) >= 0.3
            assert float(scores[Enum__Classification__Topic.EDUCATION_ACADEMIC ]) >= 0.3
