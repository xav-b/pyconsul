'''
Tests for pyconsul.factory
'''

import unittest
from nose.tools import eq_
import json
import responses
import pyconsul.factory as factory


# TODO test payload parameter
class FactoryTestCase(unittest.TestCase):

    def setUp(self):
        self.default_api_url = 'http://localhost:8500/v1'
        self.consultant_ = factory.Consultant()

    def tearDown(self):
        responses.reset()

    def test_default_initialize(self):
        eq_(self.consultant_.master, 'http://localhost:8500')
        eq_(self.consultant_._endpoint, '')

    def test_custom_initialize(self):
        custom_consultant_ = factory.Consultant(host='172.17.0.3', port=8000)
        eq_(custom_consultant_.master, 'http://172.17.0.3:8000')

    @responses.activate
    def test_get_wrapper(self):
        nodes_body = '[{"Address": "192.168.0.19", "Node": "agent-one"}]'
        responses.add(
            responses.GET,
            '{}/catalog/nodes'.format(self.default_api_url),
            body=nodes_body, status=200,
            content_type='text/plain; charset=utf-8')
        nodes = self.consultant_._get('catalog/nodes')
        eq_(nodes, json.loads(nodes_body))

    @responses.activate
    def test_get_wrapper_invalid_route(self):
        not_found_body = '{"error": "Not Found", "status": 404}'
        responses.add(
            responses.GET,
            '{}/invalid/endpoint'.format(self.default_api_url),
            body=not_found_body, status=200
        )
        result = self.consultant_._get('invalid/endpoint')
        eq_(result, json.loads(not_found_body))

    @responses.activate
    def test_custom_builtin_getattr(self):
        nodes_body = '[{"Address": "192.168.0.19", "Node": "agent-one"}]'
        responses.add(
            responses.GET,
            '{}//nodes'.format(self.default_api_url),
            body=nodes_body, status=200)
        eq_(self.consultant_.nodes, json.loads(nodes_body))

    @responses.activate
    def test_custom_builtin_getattr_invalid_attribute(self):
        not_found_body = '{"error": "Not Found", "status": 404}'
        responses.add(
            responses.GET,
            '{}//invalid'.format(self.default_api_url),
            body=not_found_body, status=200)
        eq_(self.consultant_.invalid, json.loads(not_found_body))

    def test_default_getattr(self):
        eq_(self.consultant_._endpoint, '')
