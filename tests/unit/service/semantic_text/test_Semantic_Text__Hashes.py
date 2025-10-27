from unittest                                                                    import TestCase

from osbot_utils.type_safe.primitives.safe_str.cryptography.hashes.Safe_Str__Hash import Safe_Str__Hash

from mgraph_ai_service_semantic_text.service.semantic_text.Semantic_Text__Hashes import Semantic_Text__Hashes


class test_Semantic_Text__Hashes(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.text_hashes = Semantic_Text__Hashes()

    def test__init__(self):
        with self.text_hashes as _:
            assert type(_) is Semantic_Text__Hashes


    def test_hash__for_text(self):
        with self.text_hashes as _:
            assert type(_.hash__for_text('abc')) is Safe_Str__Hash
            assert _.hash__for_text('...') == '2f43b42fd8'
            assert _.hash__for_text('abc') == '900150983c'
            assert _.hash__for_text('123') == '202cb962ac'
