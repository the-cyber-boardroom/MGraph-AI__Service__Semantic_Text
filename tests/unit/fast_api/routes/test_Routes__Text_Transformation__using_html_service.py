from unittest                                                                                               import TestCase
from fastapi                                                                                                import FastAPI
from mgraph_ai_service_semantic_text.fast_api.routes.Routes__Text_Transformation                            import Routes__Text_Transformation
from mgraph_ai_service_semantic_text.schemas.routes.Schema__Text__Transformation__Request__ABCDE_By_Size    import Schema__Text__Transformation__Request__ABCDE_By_Size
from mgraph_ai_service_semantic_text.schemas.routes.Schema__Text__Transformation__Request__Hashes_Random    import Schema__Text__Transformation__Request__Hashes_Random
from mgraph_ai_service_semantic_text.schemas.routes.Schema__Text__Transformation__Request__XXX_Random       import Schema__Text__Transformation__Request__XXX_Random
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode          import Enum__Text__Transformation__Mode
from osbot_utils.testing.__                                                                                 import __
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                          import Safe_Str__Hash
from starlette.testclient                                                                                   import TestClient
from tests.unit.Semantic_Text__Service__Fast_API__Test_Objs                                                 import get__service__html__client


class test_Routes__Text_Transformation__using_html_service(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.app                 = FastAPI()
        cls.text_transformation = Routes__Text_Transformation(app=cls.app).setup()
        cls.client__html_service = get__service__html__client()

        cls.html_simple      = "<html><body>Hello World</body></html>"                          # todo: see if we should move these examples into static vars stored in a separate class or at the end of this test class
        cls.html_paragraph   = "<html><body><p>This is a test paragraph.</p></body></html>"
        cls.html_complex     = """
            <html>
                <head><title>Test Page</title></head>
                <body>
                    <h1>Welcome to MGraph</h1>
                    <p>This is a <b>bold</b> statement with <i>italic</i> text.</p>
                    <ul>
                        <li>First item</li>
                        <li>Second item</li>
                        <li>Third item</li>
                    </ul>
                    <div>
                        <span>Some nested content</span>
                        <a href="#">Click here</a>
                    </div>
                </body>
            </html>
        """
        cls.html_article = """
            <article>
                <header>
                    <h1>Understanding Semantic Text Analysis</h1>
                    <p class="subtitle">A comprehensive guide to text transformation</p>
                </header>
                <section>
                    <h2>Introduction</h2>
                    <p>Semantic text analysis is a powerful tool for understanding content.</p>
                    <p>It allows us to transform and <b>analyze text<b> in meaningful ways.</p>
                </section>
                <section>
                    <h2>Key Benefits</h2>
                    <ul>
                        <li>Privacy-preserving transformations</li>
                        <li>Structure-aware analysis</li>
                        <li>Scalable processing</li>
                    </ul>
                </section>
                <footer>
                    <p>Copyright 2025 MGraph AI</p>
                </footer>
            </article>
        """

    # ========================================
    # Helper Methods
    # ========================================

    def get_hash_mapping(self, html: str) -> dict:                              # Extract hash mapping from HTML
        payload  = dict(html=html)
        response = self.client__html_service.post('/html/to/text/hashes', json=payload)
        assert response.status_code == 200
        data = response.json()
        return data['hash_mapping']

    # todo: see if we do need this method since Type_Safe should handle these cases ok
    def convert_to_safe_hash_dict(self, hash_mapping: dict):                    # Convert dict to Safe_Str__Hash keys
        return {Safe_Str__Hash(k): v for k, v in hash_mapping.items()}

    # ========================================
    # test setup
    # ========================================

    def test__setUpClass(self):
        with self.text_transformation as _:
            assert type(_) is Routes__Text_Transformation
        assert type(self.client__html_service) is TestClient
        assert self.client__html_service.get('/docs').status_code == 200

    def test__client__html_service(self):
        payload     = dict(html="<html><body>some text <b>in bold</b></body></html>")
        response_1  = self.client__html_service.post('/html/to/text/nodes', json=payload)
        assert response_1.json() == { 'max_depth_reached' : False,
                                      'text_nodes'        : { '7d67718d23': {'tag': 'body', 'text': 'some text '},
                                                              'a247f7d958': {'tag': 'b', 'text': 'in bold'}},
                                      'total_nodes'       : 2 }

        response_2 = self.client__html_service.post('/html/to/dict/hashes', json=payload)
        assert response_2.json() == { 'hash_mapping': {'7d67718d23': 'some text ',
                                                       'a247f7d958': 'in bold'   },
                                      'html_dict': {'attrs': {},
                                                    'nodes': [{'attrs': {},
                                                               'nodes': [{'data': '7d67718d23', 'type': 'TEXT'},
                                                                         {'attrs': {},
                                                                          'nodes': [{'data': 'a247f7d958',
                                                                                     'type': 'TEXT'}],
                                                                          'tag': 'b'}],
                                                               'tag': 'body'}],
                                                    'tag': 'html'},
                                      'max_depth': 3,
                                      'max_depth_reached': False,
                                      'node_count': 5,
                                      'total_text_hashes': 2}

        response_3 = self.client__html_service.post('/html/to/text/hashes', json=payload)
        assert response_3.json() == {'hash_mapping': {'7d67718d23': 'some text ',
                                                      'a247f7d958': 'in bold'  },
                                                      'max_depth_reached': False,
                                                      'total_text_hashes': 2}


    # ========================================
    # XXX-Random Transformation Tests
    # ========================================

    def test__xxx_random__simple_html(self):                                    # Test xxx-random with simple HTML
        hash_mapping = self.get_hash_mapping(self.html_simple)
        assert len(hash_mapping) == 1                                           # Should have 1 text node: "Hello World"
        assert hash_mapping      == {'b10a8db164': 'Hello World'}

        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)
        request           = Schema__Text__Transformation__Request__XXX_Random(hash_mapping = safe_hash_mapping)                               # Transform all

        response = self.text_transformation.transform__xxx_random(request)

        assert response.success             is True
        assert response.transformation_mode == Enum__Text__Transformation__Mode.XXX_RANDOM
        assert response.total_hashes        == 1
        assert response.transformed_hashes  >= 1
        assert response.obj()               == __( error_message       = None                        ,
                                                   transformed_mapping = __(b10a8db164='xxxxx xxxxx'),
                                                   transformation_mode = 'xxx-random',
                                                   success             = True,
                                                   total_hashes        =  1   ,
                                                   transformed_hashes  = 1  )

        # Verify transformation preserves structure
        original_text    = list(hash_mapping.values())[0]
        hash_key         = Safe_Str__Hash(list(hash_mapping.keys())[0])
        transformed_text = response.transformed_mapping[hash_key]

        assert len(transformed_text) == len(original_text)                      # Same length
        assert transformed_text      != original_text                           # Actually transformed
        assert ' '                   in transformed_text                        # Space preserved
        assert transformed_text      == 'xxxxx xxxxx'

    def test__xxx_random__paragraph_html(self):                                 # Test xxx-random with paragraph
        hash_mapping = self.get_hash_mapping(self.html_paragraph)
        assert len(hash_mapping) == 1                                           # "This is a test paragraph."

        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)
        request = Schema__Text__Transformation__Request__XXX_Random(hash_mapping=safe_hash_mapping)                           # Transform ~50%


        response = self.text_transformation.transform__xxx_random(request)

        assert response.success is True
        assert response.total_hashes == 1

        # Check that punctuation is preserved
        transformed_text = list(response.transformed_mapping.values())[0]
        assert '.' in transformed_text                                          # Period preserved
        assert transformed_text == 'xxxx xx x xxxx xxxxxxxxx.'

    def test__xxx_random__complex_html(self):                                   # Test xxx-random with complex HTML
        hash_mapping = self.get_hash_mapping(self.html_complex)
        assert len(hash_mapping) > 5                                            # Multiple text nodes
        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)
        request = Schema__Text__Transformation__Request__XXX_Random(hash_mapping=safe_hash_mapping)

        response = self.text_transformation.transform__xxx_random(request)

        assert response.success is True
        assert response.transformation_mode == Enum__Text__Transformation__Mode.XXX_RANDOM
        assert response.total_hashes == len(hash_mapping)
        assert response.transformed_hashes > 0
        assert response.transformed_hashes <= response.total_hashes

        # Verify some text was transformed, some preserved
        assert response.transformed_hashes < response.total_hashes

    def test__xxx_random__article_html(self):                                   # Test xxx-random with article HTML
        hash_mapping = self.get_hash_mapping(self.html_article)
        original_count = len(hash_mapping)
        assert original_count > 10                                              # Should have many text nodes

        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)
        request = Schema__Text__Transformation__Request__XXX_Random(hash_mapping=safe_hash_mapping)

        response = self.text_transformation.transform__xxx_random(request)

        assert response.success            is True
        assert response.total_hashes       == original_count
        assert response.transformed_hashes >= 1

        # Verify all keys preserved
        assert set(response.transformed_mapping.keys()) == set(safe_hash_mapping.keys())

    # ========================================
    # Hashes-Random Transformation Tests
    # ========================================

    def test__hashes_random__simple_html(self):                                 # Test hashes-random with simple HTML
        hash_mapping = self.get_hash_mapping(self.html_simple)

        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)
        request = Schema__Text__Transformation__Request__Hashes_Random(hash_mapping=safe_hash_mapping)

        response = self.text_transformation.transform__hashes_random(request)

        assert response.success is True
        assert response.transformation_mode == Enum__Text__Transformation__Mode.HASHES_RANDOM
        assert response.total_hashes == 1
        assert response.transformed_hashes >= 1

        # Verify transformed text is either original or hash
        hash_key = Safe_Str__Hash(list(hash_mapping.keys())[0])
        transformed = response.transformed_mapping[hash_key]
        original = hash_mapping[list(hash_mapping.keys())[0]]

        assert transformed == original or transformed == str(hash_key)

    def test__hashes_random__complex_html__verify_hashes_shown(self):           # Test that hashes are actually shown
        hash_mapping = self.get_hash_mapping(self.html_complex)

        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)
        request = Schema__Text__Transformation__Request__Hashes_Random(hash_mapping=safe_hash_mapping)

        response = self.text_transformation.transform__hashes_random(request)

        assert response.success is True
        assert response.transformed_hashes >= 1

        # Count how many texts were replaced with their hashes
        hash_count = 0
        for hash_key, transformed_text in response.transformed_mapping.items():
            if transformed_text == str(hash_key):
                hash_count += 1

        assert hash_count > 0                                                   # At least some hashes shown

    def test__hashes_random__article_html__partial_transformation(self):        # Test partial transformation
        hash_mapping = self.get_hash_mapping(self.html_article)

        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)
        request = Schema__Text__Transformation__Request__Hashes_Random(hash_mapping=safe_hash_mapping)

        response = self.text_transformation.transform__hashes_random(request)

        assert response.success is True
        assert response.total_hashes == len(hash_mapping)

        # Verify mix of original and transformed
        original_count = 0
        hash_count = 0

        for hash_key, transformed_text in response.transformed_mapping.items():
            original_text = safe_hash_mapping[hash_key]
            if transformed_text == original_text:
                original_count += 1
            elif transformed_text == str(hash_key):
                hash_count += 1

        assert original_count + hash_count == response.total_hashes
        assert hash_count == response.transformed_hashes

    # ========================================
    # ABCDE-By-Size Transformation Tests
    # ========================================

    def test__abcde_by_size__simple_html(self):                                 # Test abcde-by-size with simple HTML
        hash_mapping = self.get_hash_mapping(self.html_simple)

        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)
        request = Schema__Text__Transformation__Request__ABCDE_By_Size(hash_mapping=safe_hash_mapping)

        response = self.text_transformation.transform__abcde_by_size(request)

        assert response.success is True
        assert response.transformation_mode == Enum__Text__Transformation__Mode.ABCDE_BY_SIZE
        assert response.total_hashes == 1

        # Verify text replaced with letters
        transformed_text = list(response.transformed_mapping.values())[0]
        alphas = [c for c in transformed_text if c.isalpha()]
        assert all(c in 'abcde' for c in alphas)                                # Only letters a-e used

    def test__abcde_by_size__complex_html__verify_grouping(self):               # Test that texts are grouped by length
        hash_mapping = self.get_hash_mapping(self.html_complex)

        # Get original text lengths
        text_lengths = {}
        for hash_key, text in hash_mapping.items():
            text_lengths[hash_key] = len(text)

        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)
        request = Schema__Text__Transformation__Request__ABCDE_By_Size(hash_mapping=safe_hash_mapping)

        response = self.text_transformation.transform__abcde_by_size(request)

        assert response.success is True
        assert response.transformed_hashes >= 1

        # Verify texts of similar length get same letter
        letter_groups = {}
        for hash_key, transformed_text in response.transformed_mapping.items():
            # Extract the letter used
            alphas = [c for c in transformed_text if c.isalpha()]
            if alphas:
                letter = alphas[0]
                if letter not in letter_groups:
                    letter_groups[letter] = []
                letter_groups[letter].append(str(hash_key))

        assert len(letter_groups) >= 1                                          # At least one group
        assert len(letter_groups) <= 5                                          # At most 5 groups (a-e)

    def test__abcde_by_size__article_html__full_transformation(self):           # Test with article HTML
        hash_mapping = self.get_hash_mapping(self.html_article)

        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)
        request = Schema__Text__Transformation__Request__ABCDE_By_Size(hash_mapping=safe_hash_mapping,
                                                                       num_groups=Safe_UInt(5))

        response = self.text_transformation.transform__abcde_by_size(request)

        assert response.success is True
        assert response.transformation_mode == Enum__Text__Transformation__Mode.ABCDE_BY_SIZE
        assert response.total_hashes == len(hash_mapping)
        assert response.transformed_hashes >= 1

        # Verify structure preserved (spaces and punctuation)
        for hash_key, transformed_text in response.transformed_mapping.items():
            original_text = safe_hash_mapping[hash_key]

            # Count spaces
            original_spaces = original_text.count(' ')
            transformed_spaces = transformed_text.count(' ')
            assert transformed_spaces == original_spaces                        # Spaces preserved

            # Check length matches
            assert len(transformed_text) == len(original_text)                  # Length preserved

    def test__abcde_by_size__varying_lengths(self):                             # Test texts with very different lengths
        html_varying = """
            <div>
                <span>A</span>
                <p>Short text</p>
                <p>This is a medium length paragraph with several words.</p>
                <p>This is a much longer paragraph that contains significantly more content and should be grouped differently based on its length.</p>
            </div>
        """

        hash_mapping = self.get_hash_mapping(html_varying)
        assert len(hash_mapping) >= 4                                           # At least 4 different texts

        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)
        request = Schema__Text__Transformation__Request__ABCDE_By_Size(hash_mapping=safe_hash_mapping)

        response = self.text_transformation.transform__abcde_by_size(request)

        assert response.success is True

        # Extract letters used for each text
        text_to_letter = {}
        for hash_key, transformed_text in response.transformed_mapping.items():
            alphas = [c for c in transformed_text if c.isalpha()]
            if alphas:
                text_to_letter[str(hash_key)] = alphas[0]

        # Verify different lengths got different letters
        unique_letters = set(text_to_letter.values())
        assert len(unique_letters) >= 2                                         # At least 2 different groups

    # ========================================
    # Cross-Mode Comparison Tests
    # ========================================

    def test__all_modes__same_html__different_transformations(self):            # Verify each mode produces different results
        hash_mapping = self.get_hash_mapping(self.html_complex)
        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)

        # Apply all three transformations
        request_xxx = Schema__Text__Transformation__Request__XXX_Random(hash_mapping=safe_hash_mapping)
        response_xxx = self.text_transformation.transform__xxx_random(request_xxx)

        request_hashes = Schema__Text__Transformation__Request__Hashes_Random(hash_mapping=safe_hash_mapping)
        response_hashes = self.text_transformation.transform__hashes_random(request_hashes)

        request_abcde = Schema__Text__Transformation__Request__ABCDE_By_Size(hash_mapping=safe_hash_mapping)
        response_abcde = self.text_transformation.transform__abcde_by_size(request_abcde)

        # All should succeed
        assert response_xxx.success is True
        assert response_hashes.success is True
        assert response_abcde.success is True

        # All should have same number of hashes
        assert response_xxx.total_hashes == len(hash_mapping)
        assert response_hashes.total_hashes == len(hash_mapping)
        assert response_abcde.total_hashes == len(hash_mapping)

        # Verify different transformation modes
        assert response_xxx.transformation_mode == Enum__Text__Transformation__Mode.XXX_RANDOM
        assert response_hashes.transformation_mode == Enum__Text__Transformation__Mode.HASHES_RANDOM
        assert response_abcde.transformation_mode == Enum__Text__Transformation__Mode.ABCDE_BY_SIZE

        # Verify transformations are actually different
        # Pick first hash and compare transformations
        first_hash = Safe_Str__Hash(list(hash_mapping.keys())[0])
        xxx_result = response_xxx.transformed_mapping[first_hash]
        hashes_result = response_hashes.transformed_mapping[first_hash]
        abcde_result = response_abcde.transformed_mapping[first_hash]

        # At least two should be different (they might randomly be same)
        unique_results = len({xxx_result, hashes_result, abcde_result})
        assert unique_results >= 2                                              # At least 2 different transformations

    # ========================================
    # Real-World Scenario Tests
    # ========================================

    def test__realistic_workflow__html_to_transformation_pipeline(self):        # Test complete workflow: HTML → hashes → transform
        # Step 1: Get HTML content (simulating from Mitmproxy)
        html_content = """
            <html>
                <body>
                    <header>
                        <h1>Privacy-Aware Testing</h1>
                    </header>
                    <main>
                        <p>This content should be transformed for testing.</p>
                        <p>Original content is preserved in hash mappings.</p>
                    </main>
                </body>
            </html>
        """

        # Step 2: Extract hash mapping (Mitmproxy calls HTML service)
        hash_mapping = self.get_hash_mapping(html_content)
        assert len(hash_mapping) >= 3                                           # Header + 2 paragraphs

        # Step 3: Transform hashes (Mitmproxy calls Semantic Text service)
        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)
        request = Schema__Text__Transformation__Request__XXX_Random(hash_mapping=safe_hash_mapping)

        response = self.text_transformation.transform__xxx_random(request)

        # Step 4: Verify transformation
        assert response.success is True
        assert response.total_hashes == len(hash_mapping)

        # Step 5: Verify transformed hashes can be mapped back
        for hash_key in safe_hash_mapping.keys():
            assert hash_key in response.transformed_mapping                     # All hashes present

    def test__realistic_workflow__semantic_structure_analysis(self):            # Test analyzing semantic structure without content
        # Use ABCDE to understand content structure by length
        structured_html = """
            <div>
                <h1>Title</h1>
                <p>This is a short intro.</p>
                <p>This is a much longer paragraph that contains significantly more detailed information about the topic being discussed.</p>
                <p>Another short line.</p>
                <p>And here we have another very long paragraph with lots of content that goes into great detail about various aspects of the subject matter at hand.</p>
            </div>
        """

        hash_mapping = self.get_hash_mapping(structured_html)
        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)

        request = Schema__Text__Transformation__Request__ABCDE_By_Size(hash_mapping=safe_hash_mapping)

        response = self.text_transformation.transform__abcde_by_size(request)

        assert response.success is True

        # Analyze structure: count texts by length group
        length_groups = {}
        for hash_key, transformed_text in response.transformed_mapping.items():
            alphas = [c for c in transformed_text if c.isalpha()]
            if alphas:
                letter = alphas[0]
                length_groups[letter] = length_groups.get(letter, 0) + 1

        # We should see different groups for different length texts
        assert len(length_groups) >= 2                                          # At least 2 different length groups
