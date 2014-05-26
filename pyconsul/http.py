# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Consul HTTP API client
  ----------------------

  :copyright (c) 2014 Xavier Bruhiere.
  :license: MIT, see LICENSE for more details.
'''

import requests
import pyconsul.utils
import pyconsul.factory as factory


# TODO Some way to disable value decoding ?
class KVStorage(factory.Consultant):
    '''
    Leverage Consul key / value storage
    See http://www.consul.io/intro/getting-started/kv.html
    '''
    _endpoint = 'kv'

    @pyconsul.utils.decode_values
    def get(self, key, **kwargs):
        '''
        Fetch value at the given key
        kwargs can hold `recurse`, `wait` and `index` params
        '''
        return self._get('/'.join([self._endpoint, key]), payload=kwargs)

    @pyconsul.utils.safe_request
    def set(self, key, value, **kwargs):
        '''
        Store a new value at the given key
        kwargs can hold `cas` and `flags` params
        '''
        return requests.put(
            '{}/{}/kv/{}'.format(
                self.master, pyconsul.__consul_api_version__, key),
            data=value,
            params=kwargs
        )

    @pyconsul.utils.safe_request
    def delete(self, key, recurse=False):
        return requests.delete(
            '{}/{}/kv/{}'.format(
                self.master, pyconsul.__consul_api_version__, key),
            params={'recurse': recurse}
        )


# TODO All of the agent/check/* and agent/services/* endpoints (as objects ?)
class Agent(factory.Consultant):
    '''
    Local agent HTTP access
    In addition to methods below, it provides the following attributes:
        - checks
        - services
        - members
    '''
    _endpoint = 'agent'

    def join(self, address, wan=None):
        endpoint = 'agent/join/{}'.format(address)
        if wan is not None:
            endpoint += '?wan=1'
        return self._get(endpoint)

    def force_leave(self, node):
        return self._get('agent/force-leave/{}'.format(node))


# TODO Use the `dc` parameter
# TODO Expose blocking queries feature
class Consul(factory.Consultant):
    '''
    Client main entry point
    In addition to methods below, it provides the following attributes:
        - datacenters
        - nodes
        - services
    '''
    _endpoint = 'catalog'

    def __init__(self, host='localhost', port=8500):
        factory.Consultant.__init__(self, host=host, port=port)
        self.local_agent = Agent(host=host, port=port)
        self.storage = KVStorage(host=host, port=port)

    @property
    def status(self):
        return {
            'leader': self._get('status/leader'),
            'peers': self._get('status/peers')
        }

    @property
    def leader(self):
        return self.status['leader']

    @property
    def peers(self):
        return self.status['peers']

    def node(self, name):
        return self._get('catalog/node/' + name)

    def service(self, name):
        return self._get('catalog/service/' + name)

    def health(self, **kwargs):
        '''
        Support `node`, `service`, `check`, `state`
        '''
        if not len(kwargs):
            raise ValueError('no resource provided')
        for resource, name in kwargs.iteritems():
            endpoint = 'health/{}/{}'.format(resource, name)
        return self._get(endpoint)
