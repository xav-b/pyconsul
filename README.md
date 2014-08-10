PyConsul
========

[![Latest Version](https://pypip.in/v/pyconsul/badge.png)](https://pypi.python.org/pypi/pyconsul/)
[![Build Status](https://api.shippable.com/projects/535e1b4d456b81c100ad365c/badge/master)](https://www.shippable.com/projects/535e1b4d456b81c100ad365c/builds/4)
[![Coverage Status](https://coveralls.io/repos/hackliff/pyconsul/badge.png?branch=master)](https://coveralls.io/r/hackliff/pyconsul?branch=master)
[![Code Health](https://landscape.io/github/hackliff/pyconsul/master/landscape.png)](https://landscape.io/github/hackliff/pyconsul/master)
[![Requirements Status](https://requires.io/github/hackliff/pyconsul/requirements.png?branch=master)](https://requires.io/github/hackliff/pyconsul/requirements/?branch=master)
[![License](https://pypip.in/license/pyconsul/badge.png)](https://pypi.python.org/pypi/pyconsul/)

> Python client for [Consul][1]


A dummy, one-file implementation on top of the [HTTP API][5] of Consul.

This is also a convenient interface for [iron-app][8] enabled applications.


Teaser
------

```
# Dpending on your setup, sudo might be required
pip install pyconsul
```

```python
# Assuming you have a running server of consul locally
# Consul cluster visibility
c = http.Consul()
print c.nodes, c.services
Out[20]: 
[{u'Node': u'master', u'Address': u'192.168.0.21'}] {u'consul': []}

print c.health(node='master')
Out[21]: 
[{u'CheckID': u'serfHealth',
  u'Name': u'Serf Health Status',
  u'Node': u'master',
  u'Notes': u'',
  u'Output': u'Agent alive and reachable',
  u'ServiceID': u'',
  u'ServiceName': u'',
  u'Status': u'passing'}]

# Consul kv storage interface
print c.storage.get('my/config', recurse=True)
Out[22]: 
[{u'CreateIndex': 26,
  u'Flags': 0,
  u'Key': u'my/config',
  u'LockIndex': 0,
  u'ModifyIndex': 26,
  u'Value': 'nothing set yet'}]

# App on steroids, powered by iron-app
app = iron.App('my-app')
# Get my-app os, platform, command ...
print app['metadatas']
if app.metrics.available:
  io_data = app.metrics['io.read.count']
  print io_data.head()
Out[28]:
2014-08-10 10:43:01    12590538
2014-08-10 10:42:51    12590538
2014-08-10 10:42:41    12590538
2014-08-10 10:42:31    12590538
2014-08-10 10:42:26    12590538
Name: io.read.count, dtype: int64
```

Pyconsul is developed as a submodule of the [unide][7] project. Check out [the
documentation to learn more][6].


License
-------

Copyright 2014 Xavier Bruhiere.

PyConsul is available under the [MIT Licence][2].


[1]: http://consul.io
[2]: http://opensource.org/licenses/MIT
[3]: http://www.consul.io/intro/getting-started/install.html
[4]: http://www.consul.io/intro/
[5]: http://www.consul.io/docs/agent/http.html
[6]: http://doc.unide.co/articles/pyconsul/
[7]: http://unide.co
[8]: https://github.com/hivetech/iron-app
