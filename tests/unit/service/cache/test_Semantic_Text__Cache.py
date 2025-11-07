from unittest                                                                           import TestCase
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client           import Service__Fast_API__Client
from mgraph_ai_service_cache_client.client_contract.Service__Fast_API__Client__Config   import Service__Fast_API__Client__Config
from mgraph_ai_service_cache_client.schemas.consts.consts__Cache_Client                 import ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE, ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME, ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE
from mgraph_ai_service_semantic_text.service.cache.Semantic_Text__Cache                 import Semantic_Text__Cache
from mgraph_ai_service_semantic_text.utils.Version                                      import version__mgraph_ai_service_semantic_text
from osbot_utils.helpers.duration.decorators.capture_duration                           import capture_duration
from osbot_utils.testing.Temp_Env_Vars                                                  import Temp_Env_Vars
from osbot_utils.testing.__                                                             import __
from osbot_utils.utils.Env                                                              import get_env
from osbot_utils.utils.Http                                                             import GET_json
from tests.unit.Semantic_Text__Service__Fast_API__Test_Objs                             import get__cache_service__fast_api_server

class test_Semantic_Text__Cache(TestCase):

    @classmethod
    def setUpClass(cls):                                                        # ONE-TIME setup: start Cache service
        #with capture_duration() as setup_duration:
            with get__cache_service__fast_api_server() as _:
                cls.cache_service_server   = _.fast_api_server
                cls.cache_service_base_url = _.server_url

            cls.cache_service_server.start()

            env_vars = { ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE             : cls.cache_service_base_url ,
                         ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_NAME  : ''                        ,
                         ENV_VAR__AUTH__TARGET_SERVER__CACHE_SERVICE__KEY_VALUE : ''                        }

            cls.temp_env_vars = Temp_Env_Vars(env_vars=env_vars).set_vars()
            cls.semantic_text_cache = Semantic_Text__Cache().setup()
        # if in_github_action():
        #     assert setup_duration.seconds < 1.5                             # full setup and start servers in GitHub should be less than 1.5 seconds (usually it is about 0.5 )
        # else:
        #     assert setup_duration.seconds < 0.5                             # full setup and start servers should be less than 0.5 seconds (on laptop battery it is about 0.3 ms :) )

    @classmethod
    def tearDownClass(cls):                                                     # Stop both servers
        cls.cache_service_server.stop()
        cls.temp_env_vars.restore_vars()

    def test__setUpClass(self):
        assert self.cache_service_server.running is True
        with self.semantic_text_cache as _:
            assert type(_                    ) is Semantic_Text__Cache
            assert type(_.cache_client       ) is Service__Fast_API__Client
            assert type(_.cache_client.config) is Service__Fast_API__Client__Config
            assert _.cache_client.config.obj() == __(base_url        = self.cache_service_base_url             ,
                                                     api_key         = ''                                      ,
                                                     api_key_header  = ''                                      ,
                                                     timeout         = 30                                      ,
                                                     verify_ssl      = True                                    ,
                                                     service_name    = 'Service__Fast_API'                     ,
                                                     service_version = version__mgraph_ai_service_semantic_text)

            assert get_env(ENV_VAR__URL__TARGET_SERVER__CACHE_SERVICE) == self.cache_service_base_url

    def test__check_cache_server(self):
        assert GET_json(self.cache_service_base_url + '/info/health') == {'status': 'ok'}
        assert self.semantic_text_cache.cache_client.info().health()  == {'status': 'ok'}

    def test_admin__storage_folders(self):
        with self.semantic_text_cache as _:
            storage_folders = _.admin__storage_folders()
            assert type(storage_folders) is list
            assert storage_folders       == []

    def test_server__storage_info(self):
        with self.semantic_text_cache as _:
            storage_info = _.server__storage_info()
            assert type(storage_info) is dict
            assert storage_info       == { 'storage_mode': 'memory',
                                           'ttl_hours'   : 24      }

    def test_namespaces(self):
        with self.semantic_text_cache as _:
            assert _.namespaces() == []