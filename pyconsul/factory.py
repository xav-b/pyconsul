# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Factory for HTTP implementations
  --------------------------------

  :copyright (c) 2014 Xavier Bruhiere.
  :license: MIT, see LICENSE for more details.
'''

import abc
import requests
import pyconsul.utils


class Consultant(object):
    '''
    Abstract class to talk to Consul. It takes responsability of:
      - consul api knowledge
      - safe requests with error handers
      - short attributes access
    '''

    __metaclass__ = abc.ABCMeta

    # Useless but safe default value
    _endpoint = ''

    def __init__(self, host='localhost', port=8500):
        self.master = 'http://{}:{}'.format(host, port)

    @pyconsul.utils.safe_request
    def _get(self, resource, payload=None):
        ''' Wrapper around requests.get that shorten caller url and takes care
        of errors '''
        # Avoid dangerous default function argument `{}`
        payload = payload or {}
        # Build the request and return json response
        return requests.get(
            '{}/{}/{}'.format(
                self.master, pyconsul.__consul_api_version__, resource),
            params=payload
        )

    @pyconsul.utils.safe_request
    def _put(self, resource, payload=None):
        ''' Wrapper around requests.put that shorten caller url and takes care
        of errors '''
        # Avoid dangerous default function argument `{}`
        payload = payload or {}
        # Build the request and return json response
        return requests.put(
            '{}/{}/{}'.format(
                self.master, pyconsul.__consul_api_version__, resource),
            params=payload
        )

    def __getattr__(self, name):
        '''
        Add elegant support for attributes related to endpoints.
        For example: agent.members hits GET /v1/agent/members
        '''
        # Default behavior
        if name in self.__dict__:
            return self.__dict__[name]
        # Dynamic attribute based on the property name
        else:
            # We don't check anything because _get check for unknown resources
            return self._get('/'.join([self._endpoint, name]))
