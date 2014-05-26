# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  :copyright (c) 2014 Xavier Bruhiere.
  :license: MIT, see LICENSE for more details.
'''

import base64
import requests


def decode_values(fct):
    ''' Decode base64 encoded responses from Consul storage '''
    def inner(*args, **kwargs):
        ''' decorator '''
        data = fct(*args, **kwargs)
        if 'error' not in data:
            for result in data:
                result['Value'] = base64.b64decode(result['Value'])
        return data
    return inner


def safe_request(fct):
    ''' Return json messages instead of raising errors '''
    def inner(*args, **kwargs):
        ''' decorator '''
        try:
            _data = fct(*args, **kwargs)
        except requests.exceptions.ConnectionError as error:
            return {'error': str(error), 'status': 404}

        if _data.ok:
            if _data.content:
                safe_data = _data.json()
            else:
                safe_data = {'success': True}
        else:
            safe_data = {'error': _data.reason, 'status': _data.status_code}

        return safe_data
    return inner
