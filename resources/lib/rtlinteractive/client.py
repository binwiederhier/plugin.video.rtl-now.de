import hashlib
import uuid
import time

import requests
# Verify is disabled and to avoid warnings we disable the warnings. Behind a proxy request isn't working correctly all
# the time and if so can't validate the hosts correctly resulting in a exception and the addon won't work properly.
try:
    from requests.packages import urllib3

    urllib3.disable_warnings()
except:
    # do nothing
    pass


class Client(object):
    CONFIG_RTL_NOW = {'salt_phone': 'ba647945-6989-477b-9767-870790fcf552',
                      'salt_tablet': 'ba647945-6989-477b-9767-870790fcf552',
                      'key_phone': '46f63897-89aa-44f9-8f70-f0052050fe59',
                      'key_tablet': '56f63897-89aa-44f9-8f70-f0052050fe59',
                      'url': 'https://rtl-now.rtl.de/',
                      'id': '9',
                      'episode-thumbnail-url': 'http://autoimg.rtl.de/rtlnow/%PIC_ID%/660x660/formatimage.jpg',
                      'http-header': {'X-App-Name': 'RTL NOW App',
                                      'X-Device-Type': 'rtlnow_android',
                                      'X-App-Version': '1.3.1',
                                      # 'X-Device-Checksum': 'ed0226e4e613e4cd81c6257bced1cb1b',
                                      'Host': 'rtl-now.rtl.de',
                                      'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; GT-I9505 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36'}}

    CONFIG_RTL2_NOW = {'salt_phone': '9be405a6-2d5c-4e62-8ba0-ba2b5f11072d',
                       'salt_tablet': '4bfab4aa-705a-4e8c-b1a7-b551b1b2613f',
                       'key_phone': '26c0d1ac-e6a0-4df9-9f79-e07727f33380',
                       'key_tablet': '83bbc955-c96e-4b50-b263-bc7bcbcdf8c8',
                       'url': 'https://rtl2now.rtl2.de/',
                       'id': '37',
                       'episode-thumbnail-url': 'http://autoimg.rtl.de/rtl2now/%PIC_ID%/660x660/formatimage.jpg',
                       'http-header': {'X-App-Name': 'RTL II NOW App',
                                       'X-Device-Type': 'rtl2now_android',
                                       'X-App-Version': '1.3.1',
                                       # 'X-Device-Checksum': 'ed0226e4e613e4cd81c6257bced1cb1b',
                                       'Host': 'rtl2now.rtl2.de',
                                       'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; GT-I9505 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36'}}

    CONFIG_VOX_NOW = {'salt_phone': '9fb130b5-447e-4bbc-a44a-406f2d10d963',
                      'salt_tablet': '0df2738e-6fce-4c44-adaf-9981902de81b',
                      'key_phone': 'b11f23ac-10f1-4335-acb8-ebaaabdb8cde',
                      'key_tablet': '2e99d88e-088e-4108-a319-c94ba825fe29',
                      'url': 'https://www.voxnow.de/',
                      'id': '41',
                      'episode-thumbnail-url': 'http://autoimg.rtl.de/voxnow/%PIC_ID%/660x660/formatimage.jpg',
                      'http-header': {'X-App-Name': 'VOX NOW App',
                                      'X-Device-Type': 'voxnow_android',
                                      'X-App-Version': '1.3.1',
                                      # 'X-Device-Checksum': 'a5fabf8ef3f4425c0b8ff716562dd1a3',
                                      'Host': 'www.voxnow.de',
                                      'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; GT-I9505 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36'}}

    def __init__(self, config, amount=25):
        self._config = config
        self._amount = amount
        pass

    def get_config(self):
        return self._config

    def get_films(self, format_id, page=1):
        params = {'userid': '0',
                  'formatid': str(format_id),
                  'amount': str(self._amount),
                  'page': str(page)}
        return self._perform_request(path='/api/query/json/content.list_films', params=params)

    def get_formats(self):
        return self._perform_request(path='/api/query/json/content.list_formats')

    def search(self, q):
        params = {'word': q,
                  'extend': '1'}
        return self._perform_request(path='/api/query/json/content.format_search', params=params)

    def get_newest(self):
        return self._perform_request(path='/api/query/json/content.toplist_newest')

    def get_tips(self):
        return self._perform_request(path='/api/query/json/content_redaktion.tipplist')

    def get_top_10(self):
        return self._perform_request(path='/api/query/json/content.toplist_views')

    def get_live_streams(self):
        params = {'sessionid': self._create_session_id()}
        return self._perform_request(path='/api/query/json/livestream.available', params=params)

    def _create_session_id(self):
        session_id = str(uuid.uuid4())
        session_id = session_id.replace('-', '')
        return session_id

    def _calculate_token(self, timestamp, params):
        token = ""

        hash_map = {}
        hash_map.update(params)

        string_builder = ''
        string_builder += self._config['key_tablet']
        string_builder += ';'
        string_builder += self._config['salt_tablet']
        string_builder += ';'
        string_builder += timestamp

        params = sorted(hash_map.items())

        for param in params:
            string_builder += ';'
            string_builder += param[1]
            pass

        if len(hash_map) == 0:
            string_builder += ';'
            pass

        try:
            message_digest = hashlib.md5()
            message_digest.update(string_builder)
            abyte0 = message_digest.digest()
            length = len(abyte0)

            for b in bytearray(abyte0):
                val = b
                val = 0x100 | 0xFF & val
                hval = hex(val).lower()
                token += hval[3:]
        except:
            token = ''

        return token

    def _perform_request(self, method='GET', headers=None, path=None, post_data=None, params=None,
                         allow_redirects=True):
        # params
        _params = {}
        if not params:
            params = {}
            pass
        # always set the id
        params['id'] = self._config['id']

        _params.update(params)
        _params['_key'] = self._config['key_tablet']
        timestamp = str(int(time.time()))
        _params['_ts'] = timestamp
        _params['_tk'] = self._calculate_token(timestamp, params)
        _params['_auth'] = 'integrity'

        # headers
        if not headers:
            headers = {}
            pass
        _headers = self._config['http-header']
        _headers.update(headers)

        # url
        _url = self._config['url']
        if path:
            _url = _url + path.strip('/')
            pass

        result = None
        if method == 'GET':
            result = requests.get(_url, params=_params, headers=_headers, verify=False, allow_redirects=allow_redirects)
            pass

        if result is None:
            return {}

        return result.json()


    pass