from unittest                                                                    import TestCase
from fastapi                                                                     import FastAPI
from mgraph_ai_service_semantic_text.fast_api.routes.Routes__Text_Transformation import Routes__Text_Transformation
from starlette.testclient                                                        import TestClient
from tests.unit.Semantic_Text__Service__Fast_API__Test_Objs                      import get__service__html__client


class test__Routes__Text_Transformation__mode_specific(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.app                 = FastAPI()
        cls.text_transformation = Routes__Text_Transformation(app=cls.app).setup()
        cls.client__html_service = get__service__html__client()

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


