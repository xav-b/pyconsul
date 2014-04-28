# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Python client for Consul (http://www.consul.io)
  -----------------------------------------------

  :copyright (c) 2014 Xavier Bruhiere.
  :license: MIT, see LICENSE for more details.
'''

import abc
import sys
import base64
import requests

__project__ = 'pyconsul'
__author__ = 'Xavier Bruhiere'
__copyright__ = 'Xavier Bruhiere'
__licence__ = 'MIT'
__version__ = '0.0.1'

__consul_api_version__ = 'v1'


def decode_values(fct):
    def inner(*args, **kwargs):
        data = fct(*args, **kwargs)
        if 'error' not in data:
            for result in data:
                result['Value'] = base64.b64decode(result['Value'])
        return data
    return inner


def safe_request(fct):
    def inner(*args, **kwargs):
        try:
            _data = fct(*args, **kwargs)
        except requests.exceptions.ConnectionError as error:
            # TODO Raise a custom error
            sys.exit(error.message)

        if _data.ok:
            if _data.content:
                safe_data = _data.json()
            else:
                safe_data = {'deleted': True}
        else:
            safe_data = {'error': _data.reason, 'status': _data.status_code}

        return safe_data
    return inner


class FactoryConsultant(object):
    '''
    Abstract class to talk to Consul. It takes responsability of:
      - consul api knowledge
      - safe requests with error handers
      - short attributes access
    '''

    __metaclass__ = abc.ABCMeta

    # Useless but safe default value
    _endpoint = ''

    def __init__(self, host='localhost', port=8300):
        self.master = 'http://{}:{}'.format(host, port)

    @safe_request
    def _get(self, resource, payload=None):
        ''' Wrapper around requests.get that shorten caller url and takes care
        of errors '''
        # Avoid dangerous default function argument `{}`
        payload = payload or {}
        # Build the request and return json response
        return requests.get(
            '{}/{}/{}'.format(self.master, __consul_api_version__, resource),
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


# TODO Some way to disable value decoding ?
class KVStorage(FactoryConsultant):
    '''
    Leverage Consul key / value storage
    See http://www.consul.io/intro/getting-started/kv.html
    '''
    _endpoint = 'kv'

    @decode_values
    def get(self, key, **kwargs):
        '''
        Fetch value at the given key
        kwargs can hold `recurse`, `wait` and `index` params
        '''
        return self._get('/'.join([self._endpoint, key]), payload=kwargs)

    @safe_request
    def set(self, key, value, **kwargs):
        '''
        Store a new value at the given key
        kwargs can hold `cas` and `flags` params
        '''
        return requests.put(
            '{}/{}/kv/{}'.format(self.master, __consul_api_version__, key),
            data=value,
            params=kwargs
        )

    @safe_request
    def delete(self, key, recurse=False):
        return requests.delete(
            '{}/{}/kv/{}'.format(self.master, __consul_api_version__, key),
            params={'recurse': recurse}
        )


# TODO All of the agent/check/* and agent/services/* endpoints
class Agent(FactoryConsultant):
    '''
    Local agent HTTP access
    In addition to methods below, it provides the following attributes:
        - checks
        - services
        - members
    '''
    _endpoint = 'agent'

    def join(self, address, wan=0):
        return self._get('agent/join/{}?wan={}'.format(address, wan))

    def force_leave(self, node):
        return self._get('agent/force-leave/{}'.format(node))


# TODO Use the `dc` parameter
# TODO Expose blocking queries feature
class Consul(FactoryConsultant):
    '''
    Client main entry point
    In addition to methods below, it provides the following attributes:
        - datacenters
        - nodes
        - services
    '''
    _endpoint = 'catalog'

    def __init__(self, host='localhost', port=8500):
        FactoryConsultant.__init__(self, host=host, port=port)
        self.local_agent = Agent(host=host, port=port)
        self.storage = KVStorage(host=host, port=port)

    @property
    def status(self):
        return {
            'leader': self._get('status/leader'),
            'peers': self._get('status/peers')
        }

    def node(self, name):
        return self._get('catalog/node/' + name)

    def service(self, name):
        return self._get('catalog/service/' + name)

    def health(self, **kwargs):
        '''
        Support `node`, `service`, `check`, `state`
        '''
        for resource, name in kwargs.iteritems():
            endpoint = 'health/{}/{}'.format(resource, name)
        return self._get(endpoint)
