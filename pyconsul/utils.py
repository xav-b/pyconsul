#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  :copyright (c) 2014 Xavier Bruhiere.
  :license: %LICENCE%, see LICENSE for more details.
'''

import sys
import base64
import requests


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
