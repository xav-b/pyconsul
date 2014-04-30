'''
Tests for pyconsul.utils
'''

import unittest
import requests
from nose.tools import eq_, nottest
import pyconsul.utils as utils


@nottest
@utils.safe_request
def _test_request(url):
    return requests.get(url)


# TODO safe_request
class UtilsTestCase(unittest.TestCase):

    @utils.decode_values
    @nottest
    def _fake_base64_value(self, plain_text):
        return [{'Value': utils.base64.b64encode(plain_text)}]

    @utils.decode_values
    @nottest
    def _fake_error_value(self, plain_text):
        return {'error': 'whatever'}

    def test_decode_base64_values(self):
        plain_text = 'plain text'
        result = self._fake_base64_value(plain_text)
        eq_(result[0]['Value'], plain_text)

    def test_call_decode_on_error_message(self):
        plain_text = 'plain text'
        result = self._fake_error_value(plain_text)
        eq_(result, {'error': 'whatever'})

    def test_safe_request_no_connection_error(self):
        data = _test_request('http://randomfake.invalid')
        self.assertIn('error', data)
        eq_(data['status'], 404)
