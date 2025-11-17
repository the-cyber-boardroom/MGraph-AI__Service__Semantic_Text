from unittest                                                                                       import TestCase
from fastapi                                                                                        import FastAPI
from osbot_utils.testing.__                                                                         import __, __SKIP__
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash                  import Safe_Str__Hash
from starlette.testclient                                                                           import TestClient
from mgraph_ai_service_semantic_text.fast_api.routes.Routes__Text_Transformation                    import Routes__Text_Transformation
from mgraph_ai_service_semantic_text.schemas.transformation.Schema__Text__Transformation__Request   import Schema__Text__Transformation__Request
from mgraph_ai_service_semantic_text.schemas.transformation.enums.Enum__Text__Transformation__Mode  import Enum__Text__Transformation__Mode
from tests.unit.Semantic_Text__Service__Fast_API__Test_Objs                                         import get__service__html__client


class test_Routes__Text_Transformation__using_html_service(TestCase):

    @classmethod
    def setUpClass(cls) -> None:                                                # Setup shared test objects (called once)
        cls.app                     = FastAPI()
        cls.text_transformation     = Routes__Text_Transformation(app=cls.app).setup()
        cls.client__html_service    = get__service__html__client()

        cls.html_simple      = "<html><body>Hello World</body></html>"
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

    def get_hash_mapping(self, html: str) -> dict:                              # Extract hash mapping from HTML using HTML service
        payload  = dict(html=html)
        response = self.client__html_service.post('/html/to/text/hashes', json=payload)
        assert response.status_code == 200
        data = response.json()
        return data['hash_mapping']

    def convert_to_safe_hash_dict(self, hash_mapping: dict):                    # Convert dict to Safe_Str__Hash keys (Type_Safe handles this but explicit for clarity)
        return {Safe_Str__Hash(k): v for k, v in hash_mapping.items()}

    # ========================================
    # Test Setup Verification
    # ========================================

    def test__setUpClass(self):                                                 # Verify test class setup completed correctly
        with self.text_transformation as _:
            assert type(_) is Routes__Text_Transformation
        assert type(self.client__html_service) is TestClient
        assert self.client__html_service.get('/docs').status_code == 200        # HTML service is up

    def test__client__html_service(self):                                       # Verify HTML service is working and returns expected structure
        payload     = dict(html="<html><body>some text <b>in bold</b></body></html>")
        response_1  = self.client__html_service.post('/html/to/text/nodes', json=payload)

        assert response_1.json() == { 'max_depth_reached' : False                                      ,
                                      'text_nodes'        : { '7d67718d23': {'tag': 'body', 'text': 'some text '},
                                                              'a247f7d958': {'tag': 'b', 'text': 'in bold'}   },
                                      'total_nodes'       : 2                                           }

        response_2 = self.client__html_service.post('/html/to/dict/hashes', json=payload)
        result_2   = response_2.json()
        assert result_2['hash_mapping']     == {'7d67718d23': 'some text ', 'a247f7d958': 'in bold'}
        assert result_2['total_text_hashes'] == 2

        response_3 = self.client__html_service.post('/html/to/text/hashes', json=payload)
        assert response_3.json() == {'hash_mapping'       : {'7d67718d23': 'some text ', 'a247f7d958': 'in bold'},
                                     'max_depth_reached'  : False                                               ,
                                     'total_text_hashes'  : 2                                                   }

    # ========================================
    # xxx Transformation Tests
    # ========================================

    def test__transform__xxx_random__simple_html(self):                         # Test xxx transformation with simple HTML
        hash_mapping = self.get_hash_mapping(self.html_simple)
        assert len(hash_mapping) == 1                                           # Should have 1 text node: "Hello World"
        assert hash_mapping      == {'b10a8db164': 'Hello World'}

        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                          ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.XXX) as request:

            response = self.text_transformation.transform(request)

            assert response.obj() == __(error_message       = None                        ,
                                       transformed_mapping = __(b10a8db164='xxxxx xxxxx') ,
                                       transformation_mode = 'xxx'                 ,
                                       success             = True                         ,
                                       total_hashes        = 1                            ,
                                       transformed_hashes  = 1                            )

    def test__transform__xxx_random__complex_html(self):                        # Test xxx with complex multi-node HTML
        hash_mapping      = self.get_hash_mapping(self.html_complex)
        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                          ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.XXX) as request:

            response = self.text_transformation.transform(request)

            with response as _:
                assert _.success      is True
                assert _.total_hashes == len(hash_mapping)

                for hash_key, transformed_text in _.transformed_mapping.items():   # Verify all text nodes transformed
                    assert hash_key in safe_hash_mapping                           # All original hashes present
                    if transformed_text != safe_hash_mapping[hash_key]:            # If transformed
                        assert 'x' in transformed_text                             # Should contain x's

                assert response.obj() == __(error_message=None,
                                            transformed_mapping=__(_094cf2ae96='xxxx xxxx',
                                                                   _9f6c1a3ffc='xxxxxxx xx xxxxxx',
                                                                   _658bbd823c='xxxx xx x ',
                                                                   _69dcab4a73='xxxx',
                                                                   _78aa26e3ec=' xxxxxxxxx xxxx ',
                                                                   _030c5b6d1e='xxxxxx',
                                                                   _2d99d326cd=' xxxx.',
                                                                   f1ef59ee34='xxxxx xxxx',
                                                                   _4e864ad0c1='xxxxxx xxxx',
                                                                   _1267f9f89a='xxxxx xxxx',
                                                                   _14c3c2854c='xxxx xxxxxx xxxxxxx',
                                                                   _936ccdb971='xxxxx xxxx'),
                                            transformation_mode='xxx',
                                            success=True,
                                            total_hashes=12,
                                            transformed_hashes=12)

    def test__transform__xxx_random__preserves_structure(self):                 # Test xxx preserves HTML structure (punctuation, spaces)
        html_with_structure = "<p>Hello, World! How are you?</p>"
        hash_mapping        = self.get_hash_mapping(html_with_structure)
        safe_hash_mapping   = self.convert_to_safe_hash_dict(hash_mapping)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                          ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.XXX) as request:

            response = self.text_transformation.transform(request)

            for hash_key, transformed_text in response.transformed_mapping.items():
                if 'x' in transformed_text:                                    # If this was transformed
                    assert ', ' in transformed_text or '!' in transformed_text or '?' in transformed_text   # Punctuation preserved

            assert response.obj() == __(error_message=None,
                                        transformed_mapping=__(b26ffe6849='xxxxx, xxxxx! xxx xxx xxx?'),
                                        transformation_mode='xxx',
                                        success=True,
                                        total_hashes=1,
                                        transformed_hashes=1)

    # ========================================
    # Hashes-Random Transformation Tests
    # ========================================

    def test__transform__hashes_random__simple_html(self):                      # Test Hashes-Random shows hash values
        hash_mapping      = self.get_hash_mapping(self.html_simple)
        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                              ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.HASHES) as request:

            response = self.text_transformation.transform(request)

            with response as _:
                assert _.success             is True
                assert _.transformation_mode == Enum__Text__Transformation__Mode.HASHES
                assert _.total_hashes        == 1
                assert _.transformed_hashes  == 1

                first_hash = list(safe_hash_mapping.keys())[0]
                assert _.transformed_mapping[first_hash] == str(first_hash)    # Hash replaces text

                assert response.obj() == __(error_message=None,
                                            transformed_mapping=__(b10a8db164='b10a8db164'),
                                            transformation_mode='hashes',
                                            success=True,
                                            total_hashes=1,
                                            transformed_hashes=1)

    def test__transform__hashes_random__complex_html(self):                     # Test Hashes-Random with multiple text nodes
        hash_mapping      = self.get_hash_mapping(self.html_complex)
        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                              ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.HASHES) as request:

            response = self.text_transformation.transform(request)

            with response as _:
                assert _.success      is True
                assert _.total_hashes == len(hash_mapping)

                for hash_key, transformed_text in _.transformed_mapping.items():
                    if transformed_text != safe_hash_mapping[hash_key]:        # If transformed
                        assert transformed_text == str(hash_key)               # Should show hash value

                assert _.obj() == __(error_message=None,
                                     transformed_mapping=__(_094cf2ae96='094cf2ae96',
                                                            _9f6c1a3ffc='9f6c1a3ffc',
                                                            _658bbd823c='658bbd823c',
                                                            _69dcab4a73='69dcab4a73',
                                                            _78aa26e3ec='78aa26e3ec',
                                                            _030c5b6d1e='030c5b6d1e',
                                                            _2d99d326cd='2d99d326cd',
                                                            f1ef59ee34='f1ef59ee34',
                                                            _4e864ad0c1='4e864ad0c1',
                                                            _1267f9f89a='1267f9f89a',
                                                            _14c3c2854c='14c3c2854c',
                                                            _936ccdb971='936ccdb971'),
                                     transformation_mode='hashes',
                                     success=True,
                                     total_hashes=12,
                                     transformed_hashes=12)

    # ========================================
    # ABCDE-By-Size Transformation Tests
    # ========================================

    def test__transform__abcde_by_size__simple_html(self):                      # Test ABCDE groups by text length
        hash_mapping      = self.get_hash_mapping(self.html_simple)
        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                              ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE  ) as request:

            response = self.text_transformation.transform(request)

            assert response.obj() == __(error_message=None,
                                        transformed_mapping=__(b10a8db164='aaaaa aaaaa'),
                                        transformation_mode='abcde-by-size',
                                        success=True,
                                        total_hashes=1,
                                        transformed_hashes=1)

            first_hash        = list(safe_hash_mapping.keys())[0]
            transformed_text  = response.transformed_mapping[first_hash]
            assert transformed_text != safe_hash_mapping[first_hash]           # Should be transformed
            assert any(c in transformed_text for c in 'abcde')                 # Should contain group letter

    def test__transform__abcde_by_size__complex_html(self):                     # Test ABCDE with multiple lengths
        hash_mapping      = self.get_hash_mapping(self.html_complex)
        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                              ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE  ) as request:

            response = self.text_transformation.transform(request)

            with response as _:
                assert _.success             is True
                assert _.total_hashes        == len(hash_mapping)
                assert _.transformed_hashes  == len(hash_mapping)              # ABCDE transforms ALL

                letters_used = set()
                for hash_key, transformed_text in _.transformed_mapping.items():
                    alphas = [c for c in transformed_text if c.isalpha()]
                    if alphas:
                        letters_used.add(alphas[0])

                assert len(letters_used) >= 2                                  # At least 2 different length groups

    def test__transform__abcde_by_size__preserves_structure(self):              # Test ABCDE preserves punctuation and spaces
        html_with_structure = "<p>Hello, World!</p>"
        hash_mapping        = self.get_hash_mapping(html_with_structure)
        safe_hash_mapping   = self.convert_to_safe_hash_dict(hash_mapping)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                              ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE  ) as request:

            response = self.text_transformation.transform(request)

            first_hash       = list(safe_hash_mapping.keys())[0]
            transformed_text = response.transformed_mapping[first_hash]

            assert ', ' in transformed_text                                    # Comma and space preserved
            assert '!'  in transformed_text                                    # Exclamation preserved

    def test__transform__abcde_by_size__varying_lengths(self):                  # Test ABCDE with texts of very different lengths
        html_varying = """
            <div>
                <span>A</span>
                <p>Short text</p>
                <p>This is a medium length paragraph with several words.</p>
                <p>This is a much longer paragraph that contains significantly more content and should be grouped differently based on its length.</p>
            </div>
        """

        hash_mapping      = self.get_hash_mapping(html_varying)
        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                              ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE  ) as request:

            response = self.text_transformation.transform(request)

            assert response.success is True

            text_to_letter = {}                                                # Extract group letter for each text
            for hash_key, transformed_text in response.transformed_mapping.items():
                alphas = [c for c in transformed_text if c.isalpha()]
                if alphas:
                    text_to_letter[str(hash_key)] = alphas[0]

            unique_letters = set(text_to_letter.values())
            assert len(unique_letters) >= 2                                    # At least 2 different length groups

    # ========================================
    # Cross-Mode Comparison Tests
    # ========================================

    def test__all_modes__same_html__different_transformations(self):            # Verify each mode produces different results for same input
        hash_mapping      = self.get_hash_mapping(self.html_complex)
        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                          ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.XXX) as request_xxx:
            response_xxx = self.text_transformation.transform(request_xxx)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                              ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.HASHES) as request_hashes:
            response_hashes = self.text_transformation.transform(request_hashes)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                              ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE  ) as request_abcde:
            response_abcde = self.text_transformation.transform(request_abcde)

        assert response_xxx.success            is True                         # All should succeed
        assert response_hashes.success         is True
        assert response_abcde.success          is True

        assert response_xxx.total_hashes       == len(hash_mapping)            # All should have same number of hashes
        assert response_hashes.total_hashes    == len(hash_mapping)
        assert response_abcde.total_hashes     == len(hash_mapping)

        assert response_xxx.transformation_mode    == Enum__Text__Transformation__Mode.XXX       # Verify modes
        assert response_hashes.transformation_mode == Enum__Text__Transformation__Mode.HASHES
        assert response_abcde.transformation_mode  == Enum__Text__Transformation__Mode.ABCDE_BY_SIZE

        first_hash = Safe_Str__Hash(list(hash_mapping.keys())[0])             # Compare transformations
        xxx_result    = response_xxx.transformed_mapping[first_hash]
        hashes_result = response_hashes.transformed_mapping[first_hash]
        abcde_result  = response_abcde.transformed_mapping[first_hash]

        unique_results = len({xxx_result, hashes_result, abcde_result})
        assert unique_results >= 2                                             # At least 2 different transformations

    # ========================================
    # Real-World Scenario Tests
    # ========================================

    def test__realistic_workflow__html_to_transformation_pipeline(self):        # Test complete workflow: HTML → hashes → transform → reconstruct
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

        hash_mapping      = self.get_hash_mapping(html_content)               # Step 1: Extract hash mapping (HTML service)
        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                          ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.XXX) as request:

            response = self.text_transformation.transform(request)             # Step 2: Transform hashes (Semantic Text service)

            with response as _:                                                # Step 3: Verify transformation
                assert _.success      is True
                assert _.total_hashes == len(hash_mapping)

                for hash_key in safe_hash_mapping.keys():                     # Step 4: Verify all hashes can be mapped back
                    assert hash_key in _.transformed_mapping

    def test__realistic_workflow__semantic_structure_analysis(self):            # Test analyzing semantic structure without exposing content
        structured_html = """
            <div>
                <h1>Title</h1>
                <p>This is a short intro.</p>
                <p>This is a much longer paragraph that contains significantly more detailed information about the topic being discussed.</p>
                <p>Another short line.</p>
                <p>And here we have another very long paragraph with lots of content that goes into great detail about various aspects of the subject matter at hand.</p>
            </div>
        """

        hash_mapping      = self.get_hash_mapping(structured_html)
        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                              ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE  ) as request:

            response = self.text_transformation.transform(request)

            assert response.success is True

            length_groups = {}                                                 # Analyze structure: count texts by length group
            for hash_key, transformed_text in response.transformed_mapping.items():
                alphas = [c for c in transformed_text if c.isalpha()]
                if alphas:
                    letter = alphas[0]
                    length_groups[letter] = length_groups.get(letter, 0) + 1

            assert len(length_groups) >= 2                                     # Should see different groups for different lengths

    def test__realistic_workflow__article_analysis(self):                       # Test article structure analysis with ABCDE
        hash_mapping      = self.get_hash_mapping(self.html_article)
        safe_hash_mapping = self.convert_to_safe_hash_dict(hash_mapping)

        with Schema__Text__Transformation__Request(hash_mapping        = safe_hash_mapping                              ,
                                                   transformation_mode = Enum__Text__Transformation__Mode.ABCDE_BY_SIZE  ) as request:

            response = self.text_transformation.transform(request)

            with response as _:
                assert _.success             is True
                assert _.transformed_hashes  == len(hash_mapping)              # All transformed

                letters_found = set()
                for transformed_text in _.transformed_mapping.values():
                    alphas = [c for c in transformed_text if c.isalpha()]
                    if alphas:
                        letters_found.add(alphas[0])

                assert len(letters_found) >= 2                                 # Multiple length categories