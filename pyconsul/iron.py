# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Sugar syntax to discuss with "iron-app" enabled application
  -----------------------------------------------------------

  :copyright (c) 2014 Xavier Bruhiere.
  :license: MIT, see LICENSE for more details.
'''

import os
import datetime as dt
import pandas as pd
from influxdb import InfluxDBClient
from .http import Consul


class Metrics(object):
    _namespace = 'iron-app'

    def __init__(self, app_name, host=None, port=None):
        self.db_name = '.'.join([self._namespace, app_name])
        host = host or os.environ.get('INFLUXDB_HOST', 'localhost')
        port = port or os.environ.get('INFLUXDB_PORT', 8086)
        self._db = self._connect_influxdb(host, port)

    def _connect_influxdb(self, host, port):
        return InfluxDBClient(
            host, port,
            # Current version of iron-consul hardcodes db user informations
            'root', 'root', self.db_name
        )

    @property
    def available(self):
        ''' Check if a related database exists '''
        return self.db_name in map(
            lambda x: x['name'], self._db.get_database_list()
        )

    # TODO Learn influx dsl and add some time controls
    # TODO Review this with a better understanding of influxdb structure
    def _series(self, name):
        raw_data = self._db.query('select * from {}'.format(name))
        t_data = pd.np.array(raw_data[0]['points']).T
        return pd.Series(
            name=raw_data[0]['name'],
            data=t_data[2],
            index=map(lambda x: dt.datetime.fromtimestamp(x), t_data[0])
        )

    def __getitem__(self, key):
        '''
        Add elegant support for attributes related to endpoints.
        For example: agent.members hits GET /v1/agent/members
        '''
        # Default behavior
        if key in self.__dict__:
            return self.__dict__[key]
        # Dynamic attribute based on the property name
        else:
            if key == 'metadatas':
                key = ''
            # Get metadata
            return self._series(key)


class App(object):
    '''
    Iron-app protocol abstraction
    See https://github.com/hivetech/iron-app
    '''
    _namespace = 'iron-app'

    def __init__(self, app_name, **kwargs):
        self._app = app_name
        self._consul = Consul(
            host=kwargs.get('consul_host', None),
            port=kwargs.get('consul_port', None)
        )
        self.metrics = Metrics(
            app_name,
            host=kwargs.get('influxdb_host', None),
            port=kwargs.get('influxdb_port', None)
        )

    # TODO This is raw consul output, make it friendly
    def _metadatas(self, extra=''):
        return self._consul.storage.get(
            '/'.join([self._namespace, self._app, 'metadata', extra]),
            recurse=True
        )

    def __getitem__(self, key):
        '''
        Add elegant support for attributes related to endpoints.
        For example: agent.members hits GET /v1/agent/members
        '''
        # Default behavior
        if key in self.__dict__:
            return self.__dict__[key]
        # Dynamic attribute based on the property name
        else:
            if key == 'metadatas':
                key = ''
            # Get metadata
            return self._metadatas(key)
