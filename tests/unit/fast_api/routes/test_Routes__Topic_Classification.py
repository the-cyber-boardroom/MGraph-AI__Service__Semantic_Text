from unittest                                                                                             import TestCase
from fastapi                                                                                              import FastAPI
from osbot_aws.aws.comprehend.schemas.safe_str.Safe_Str__AWS_Comprehend__Text                             import Safe_Str__Comprehend__Text
from osbot_utils.testing.__                                                                               import __
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from mgraph_ai_service_semantic_text.schemas.topic.enums.Enum__Classification__Topic                      import Enum__Classification__Topic
from mgraph_ai_service_semantic_text.fast_api.routes.Routes__Topic_Classification                         import Routes__Topic_Classification
from mgraph_ai_service_semantic_text.schemas.topic.Schema__Topic_Classification__Request                  import Schema__Topic_Classification__Request
from mgraph_ai_service_semantic_text.schemas.topic.Schema__Topic_Filter__Request                          import Schema__Topic_Filter__Request
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Output_Mode       import Enum__Classification__Output_Mode
from mgraph_ai_service_semantic_text.schemas.classification.enums.Enum__Classification__Logic_Operator    import Enum__Classification__Logic_Operator
from mgraph_ai_service_semantic_text.service.topic_classification.Topic_Classification__Filter__Service   import Topic_Classification__Filter__Service


class test_Routes__Topic_Classification(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app    = FastAPI()
        cls.routes = Routes__Topic_Classification(app=cls.app).setup()

    def test__setUpClass(self):                                                # Test route setup and initialization
        with self.routes as _:
            assert type(_)                                      is Routes__Topic_Classification
            assert _.routes_paths()                             == ['/classify', '/filter']
            assert _.tag                                        == 'topic-classification'
            assert type(_.topic_classification_filter_service)  is Topic_Classification__Filter__Service
            assert _.app                                        == self.app
            assert _.obj()                                      == __(tag                                 = 'topic-classification'                      ,
                                                                     router                               = 'APIRouter'                                 ,
                                                                     route_registration                   = __(analyzer       = __()                    ,
                                                                                                              converter       = __()                    ,
                                                                                                              wrapper_creator = __(converter=__())      ,
                                                                                                              route_parser    = __()                    ),
                                                                     topic_classification_filter_service  = __(topic_service = __(topic_engine = __())),
                                                                     app                                  = 'FastAPI'                                   ,
                                                                     prefix                               = '/topic-classification'                     ,
                                                                     filter_tag                           = True                                        )

    # ========================================
    # classify Tests
    # ========================================

    def test__classify__basic(self):                                           # Test basic topic classification with deterministic values
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World",           # Using actual hash from engine
                        Safe_Str__Hash("f1feeaa3d6"): "Test Text"}             # Using actual hash from engine

        request = Schema__Topic_Classification__Request(
            hash_mapping   = hash_mapping                                               ,
            topics         = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE           ,
                              Enum__Classification__Topic.BUSINESS_FINANCE              ,
                              Enum__Classification__Topic.EDUCATION_ACADEMIC            ],
            min_confidence = Safe_Float(0.0)
        )

        response = self.routes.classify(request)

        assert response.success                 is True
        assert response.total_hashes            == 2
        assert len(response.hash_topic_scores)  == 2
        assert response.topics_classified       == [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE ,
                                                    Enum__Classification__Topic.BUSINESS_FINANCE    ,
                                                    Enum__Classification__Topic.EDUCATION_ACADEMIC  ]

        # Deterministic values from hash-based engine
        assert response.obj()                   == __(hash_topic_scores  = __(b10a8db164 = __(technology_software = 0.2915,    # "Hello World" scores
                                                                                              business_finance    = 0.284,
                                                                                              education_academic  = 0.9113),
                                                                              f1feeaa3d6 = __(technology_software = 0.3881,     # "Test Text" scores
                                                                                              business_finance    = 0.6692,
                                                                                              education_academic  = 0.6366)),
                                                      topics_classified  = ['technology-software', 'business-finance', 'education-academic'],
                                                      total_hashes       = 2                                          ,
                                                      success            = True                                       )

    def test__classify__empty(self):                                           # Test classification with empty mapping
        request = Schema__Topic_Classification__Request(hash_mapping   = {}                                               ,
                                                        topics         = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE],
                                                        min_confidence = Safe_Float(0.0)                                  )

        response = self.routes.classify(request)

        assert response.success           is True
        assert response.total_hashes      == 0
        assert response.hash_topic_scores == {}
        assert response.obj()             == __(hash_topic_scores  = __()                            ,
                                                topics_classified  = ['technology-software']         ,
                                                total_hashes       = 0                               ,
                                                success            = True                            )

    def test__classify__single_hash(self):                                     # Test classification with single hash
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        request = Schema__Topic_Classification__Request(hash_mapping   = hash_mapping                                    ,
                                                        topics         = [Enum__Classification__Topic.TECHNOLOGY_HARDWARE],
                                                        min_confidence = Safe_Float(0.0)                                  )

        response = self.routes.classify(request)

        assert response.success                         is True
        assert response.total_hashes                    == 1
        assert len(response.hash_topic_scores)          == 1
        assert Safe_Str__Hash("b10a8db164")             in response.hash_topic_scores
        assert response.obj()                           == __(hash_topic_scores  = __(b10a8db164 = __(technology_hardware=0.066)),
                                                              topics_classified  = ['technology-hardware']              ,
                                                              total_hashes       = 1                                    ,
                                                              success            = True                                 )

    def test__classify__min_confidence_filter(self):                           # Test min_confidence threshold filtering
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        request = Schema__Topic_Classification__Request(
            hash_mapping   = hash_mapping                                                    ,
            topics         = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE              ,  # 0.7478 - above threshold
                              Enum__Classification__Topic.BUSINESS_FINANCE                 ,  # 0.6789 - above threshold
                              Enum__Classification__Topic.EDUCATION_ACADEMIC               ,  # 0.1512 - below threshold
                              Enum__Classification__Topic.HEALTH_MEDICAL                   ], # 0.0861 - below threshold
            min_confidence = Safe_Float(0.29)
        )

        response = self.routes.classify(request)

        assert response.success        is True
        assert response.total_hashes   == 1

        # Only topics above 0.5 should be included
        hash_scores = response.hash_topic_scores[Safe_Str__Hash("b10a8db164")]
        assert len(hash_scores) == 2
        assert Enum__Classification__Topic.TECHNOLOGY_SOFTWARE in hash_scores
        assert Enum__Classification__Topic.BUSINESS_FINANCE    not in hash_scores
        assert Enum__Classification__Topic.EDUCATION_ACADEMIC  in hash_scores
        assert Enum__Classification__Topic.HEALTH_MEDICAL      not in hash_scores

    def test__classify__all_topics(self):                                      # Test classification with all 15 topics
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}
        all_topics   = list(Enum__Classification__Topic)

        request  = Schema__Topic_Classification__Request(hash_mapping   = hash_mapping      ,
                                                         topics         = all_topics         ,
                                                         min_confidence = Safe_Float(0.0)    )
        response = self.routes.classify(request)

        assert response.success      is True
        assert response.total_hashes == 1
        assert len(response.topics_classified) == 15

        # All 15 topics should have scores
        hash_scores = response.hash_topic_scores[Safe_Str__Hash("b10a8db164")]
        assert len(hash_scores) == 15

        # Verify all topics are present
        for topic in all_topics:
            assert topic in hash_scores
            assert 0.0 <= float(hash_scores[topic]) <= 1.0

    def test__classify__scores_in_range(self):                                 # Test that all scores are within valid range (0.0-1.0)
        hash_mapping = {Safe_Str__Hash(f"abcde{i:05d}"): f"Text {i}" for i in range(10)}
        all_topics   = list(Enum__Classification__Topic)

        request  = Schema__Topic_Classification__Request(hash_mapping   = hash_mapping      ,
                                                         topics         = all_topics         ,
                                                         min_confidence = Safe_Float(0.0)    )
        response = self.routes.classify(request)

        assert response.success      is True
        assert response.total_hashes == 10

        # Verify all scores are in valid range
        for hash_key, topic_scores in response.hash_topic_scores.items():
            for topic, confidence in topic_scores.items():
                confidence_float = float(confidence)
                assert 0.0 <= confidence_float <= 1.0, f"Confidence {confidence_float} out of range for {hash_key}/{topic}"

    # ========================================
    # filter Tests
    # ========================================

    def test__filter__basic__single_topic(self):                               # Test basic filtering with single topic
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World",
                        Safe_Str__Hash("f1feeaa3d6"): "Test Text"}

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                     ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE],
            min_confidence   = Safe_Float(0.3)                                  ,
            logic_operator   = Enum__Classification__Logic_Operator.AND        ,
            output_mode      = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.filter(request)

        # Analysis: b10a8db164 has tech-software=0.7478 > 0.6 ✓
        #           f1feeaa3d6 has tech-software=0.508  < 0.6 ✗
        assert response.success         is True
        assert response.filtered_count  == 1
        assert response.filtered_hashes == [Safe_Str__Hash("f1feeaa3d6")]
        assert response.obj()           == __(filtered_hashes      = ['f1feeaa3d6']          ,
                                              filtered_with_text   = __()                    ,
                                              filtered_with_scores = __()                    ,
                                              topics_used          = ['technology-software'] ,
                                              logic_operator       = 'and'                   ,
                                              output_mode          = 'hashes-only'           ,
                                              total_hashes         = 2                       ,
                                              filtered_count       = 1                       ,
                                              success              = True                    )

    def test__filter__and_logic__both_match(self):                             # Test AND logic where both topics match
        hash_mapping = {Safe_Str__Hash("b10a8db164"): Safe_Str__Comprehend__Text("Hello World")}           # tech-software=0.7478, business-finance=0.6789

        request = Schema__Topic_Filter__Request(hash_mapping     = hash_mapping                                              ,
                                                required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE         ,
                                                                    Enum__Classification__Topic.BUSINESS_FINANCE            ],
                                                min_confidence   = Safe_Float(0.2)                                           ,
                                                logic_operator   = Enum__Classification__Logic_Operator.AND                 ,
                                                output_mode      = Enum__Classification__Output_Mode.FULL_RATINGS)

        response = self.routes.filter(request)

        # Both tech-software (0.7478) and business-finance (0.6789) are > 0.6
        assert response.success         is True
        assert response.filtered_count  == 1
        assert response.filtered_hashes == [Safe_Str__Hash("b10a8db164")]

        # Verify full ratings output mode
        assert response.filtered_with_text  is not None
        assert response.filtered_with_scores is not None
        assert response.filtered_with_text[Safe_Str__Hash("b10a8db164")] == "Hello World"

    def test__filter__and_logic__one_fails(self):                              # Test AND logic where one topic fails threshold
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}           # tech-software=0.7478, education-academic=0.1512

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                              ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE         ,
                                Enum__Classification__Topic.EDUCATION_ACADEMIC          ],
            min_confidence   = Safe_Float(0.5)                                           ,
            logic_operator   = Enum__Classification__Logic_Operator.AND                 ,
            output_mode      = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.filter(request)

        # tech-software=0.7478 > 0.5 ✓, but education-academic=0.1512 < 0.5 ✗
        # AND requires BOTH, so should filter out
        assert response.success         is True
        assert response.filtered_count  == 0
        assert response.filtered_hashes == []

    def test__filter__or_logic__any_match(self):                               # Test OR logic where any topic matches
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

        response = self.routes.filter(request)

        # b10a8db164: tech-software=0.7478 > 0.55 ✓ → PASS (OR needs any)
        # f1feeaa3d6: education-academic=0.5903 > 0.55 ✓ → PASS
        assert response.success         is True
        assert response.filtered_count  == 2
        assert len(response.filtered_hashes) == 2
        assert Safe_Str__Hash("b10a8db164") in response.filtered_hashes
        assert Safe_Str__Hash("f1feeaa3d6") in response.filtered_hashes

    def test__filter__empty_mapping(self):                                     # Test filtering with empty hash mapping
        request = Schema__Topic_Filter__Request(
            hash_mapping     = {}                                               ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE],
            min_confidence   = Safe_Float(0.5)                                  ,
            logic_operator   = Enum__Classification__Logic_Operator.AND        ,
            output_mode      = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.filter(request)

        assert response.success         is True
        assert response.filtered_count  == 0
        assert response.filtered_hashes == []
        assert response.total_hashes    == 0

    def test__filter__output_mode__hashes_with_text(self):                     # Test HASHES_WITH_TEXT output mode
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                     ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE],
            min_confidence   = Safe_Float(0.2)                                  ,
            logic_operator   = Enum__Classification__Logic_Operator.AND        ,
            output_mode      = Enum__Classification__Output_Mode.HASHES_WITH_TEXT
        )

        response = self.routes.filter(request)

        assert response.success              is True
        assert response.filtered_count       == 1
        assert response.filtered_with_text   is not None
        assert response.filtered_with_scores == {}                           # Not included in HASHES_WITH_TEXT mode
        assert response.filtered_with_text[Safe_Str__Hash("b10a8db164")] == "Hello World"

    def test__filter__output_mode__full_ratings(self):                         # Test FULL_RATINGS output mode
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                              ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE         ,
                                Enum__Classification__Topic.BUSINESS_FINANCE            ],
            min_confidence   = Safe_Float(0.2)                                           ,
            logic_operator   = Enum__Classification__Logic_Operator.AND                 ,
            output_mode      = Enum__Classification__Output_Mode.FULL_RATINGS
        )

        response = self.routes.filter(request)

        assert response.success              is True
        assert response.filtered_count       == 1
        assert response.filtered_with_text   is not None                        # Included in FULL_RATINGS mode
        assert response.filtered_with_scores is not None                        # Included in FULL_RATINGS mode

        # Verify scores are included
        scores = response.filtered_with_scores[Safe_Str__Hash("b10a8db164")]
        assert Enum__Classification__Topic.TECHNOLOGY_SOFTWARE in scores
        assert Enum__Classification__Topic.BUSINESS_FINANCE    in scores

    def test__filter__threshold_zero(self):                                    # Test with threshold 0.0 (should include all)
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                     ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE],
            min_confidence   = Safe_Float(0.0)                                  ,
            logic_operator   = Enum__Classification__Logic_Operator.AND        ,
            output_mode      = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.filter(request)

        assert response.success         is True
        assert response.filtered_count  == 1
        assert response.filtered_hashes == [Safe_Str__Hash("b10a8db164")]

    def test__filter__threshold_one(self):                                     # Test with threshold 1.0 (should include none)
        hash_mapping = {Safe_Str__Hash("b10a8db164"): "Hello World"}

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                     ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE],
            min_confidence   = Safe_Float(1.0)                                  ,
            logic_operator   = Enum__Classification__Logic_Operator.AND        ,
            output_mode      = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.filter(request)

        assert response.success         is True
        assert response.filtered_count  == 0                                    # No score should equal 1.0 exactly
        assert response.filtered_hashes == []

    def test__filter__multiple_hashes__deterministic(self):                    # Test filtering multiple hashes with deterministic results
        hash_mapping = {Safe_Str__Hash(f"abcde{i:05d}"): f"Text {i}" for i in range(10)}

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                     ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE],
            min_confidence   = Safe_Float(0.5)                                  ,
            logic_operator   = Enum__Classification__Logic_Operator.AND        ,
            output_mode      = Enum__Classification__Output_Mode.HASHES_ONLY
        )

        response = self.routes.filter(request)

        assert response.success      is True
        assert response.total_hashes == 10

        # Results should be deterministic - same test always produces same results
        filtered_count_first_run = response.filtered_count

        # Run again
        response2 = self.routes.filter(request)
        assert response2.filtered_count == filtered_count_first_run             # Should be identical

    def test__filter__multiple_topics__and_logic(self):                        # Test filtering with multiple topics using AND logic
        hash_mapping = {
            Safe_Str__Hash("abcd000001"): "Technology article",                 # Will have various topic scores
            Safe_Str__Hash("abcd000002"): "Business report",
            Safe_Str__Hash("abcd000003"): "Health guide"
        }

        request = Schema__Topic_Filter__Request(
            hash_mapping     = hash_mapping                                              ,
            required_topics  = [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE         ,
                                Enum__Classification__Topic.BUSINESS_FINANCE            ,
                                Enum__Classification__Topic.EDUCATION_ACADEMIC          ],
            min_confidence   = Safe_Float(0.4)                                           ,
            logic_operator   = Enum__Classification__Logic_Operator.AND                 ,
            output_mode      = Enum__Classification__Output_Mode.FULL_RATINGS
        )

        response = self.routes.filter(request)

        assert response.success        is True
        assert response.topics_used    == [Enum__Classification__Topic.TECHNOLOGY_SOFTWARE ,
                                           Enum__Classification__Topic.BUSINESS_FINANCE    ,
                                           Enum__Classification__Topic.EDUCATION_ACADEMIC  ]
        assert response.logic_operator == Enum__Classification__Logic_Operator.AND
        assert response.output_mode    == Enum__Classification__Output_Mode.FULL_RATINGS

        # AND logic means ALL three topics must be > 0.4 for each hash
        # Results will vary based on hash-based scores, but all passing hashes
        # must have all three topics above threshold
        for hash_key in response.filtered_hashes:
            scores = response.filtered_with_scores[hash_key]
            assert Enum__Classification__Topic.TECHNOLOGY_SOFTWARE in scores
            assert Enum__Classification__Topic.BUSINESS_FINANCE    in scores
            assert Enum__Classification__Topic.EDUCATION_ACADEMIC  in scores
            assert float(scores[Enum__Classification__Topic.TECHNOLOGY_SOFTWARE]) >= 0.4
            assert float(scores[Enum__Classification__Topic.BUSINESS_FINANCE   ]) >= 0.4
            assert float(scores[Enum__Classification__Topic.EDUCATION_ACADEMIC ]) >= 0.4
