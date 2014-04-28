PyConsul
========

[![Latest Version](https://pypip.in/v/pyconsul/badge.png)](https://pypi.python.org/pypi/pyconsul/)
[![Build Status](https://drone.io/github.com/hackliff/pyconsul/status.png)](https://drone.io/github.com/hackliff/pyconsul/latest)
[![Coverage Status](https://coveralls.io/repos/hackliff/pyconsul/badge.png)](https://coveralls.io/r/hackliff/pyconsul)
[![Requirements Status](https://requires.io/github/hackliff/pyconsul/requirements.png?branch=master)](https://requires.io/github/hackliff/pyconsul/requirements/?branch=master)
[![License](https://pypip.in/license/pyconsul/badge.png)](https://pypi.python.org/pypi/pyconsul/)

> Python client for [Consul][1]


A dummy, one-file implementation on top of the [HTTP API][5] of Consul.

Install
-------

* Install Consul following [the official guide][3], or this one-liner:

```console
$ # Install consul 0.1.0_linux_amd64 under /usr/local/bin
$ wget -qO- https://raw.githubusercontent.com/hackliff/pyconsul/master/install-consul.sh | (sudo) bash
```

* Install pyconsul library

```console
$ (sudo) pip install pyconsul
```


Getting started
---------------

I strongly advise you to go through [the official Consul documentation][4]
before playing around with pyconsul.

First, we need an agent in server mode.

```console
consul agent -server -bootstrap \
  -data-dir /tmp/consul \
  -node=agent-one \
  -client=192.168.0.19 \
  -bind=0.0.0.0
```

Optionally, on different hosts, launch more consul agents in client mode.

```console
$ # Replace with the address provided above to `--client`
$ consul agent --join 192.168.0.19 -data-dir /tmp/consul
```

Then you can interact with them it.

```python
from pyconsul.http import Consul

# `host` meets `-client <host>` arg of consul (default to 127.0.0.1)
consul_ = Consul(host='0.0.0.0', port=8500)
print consul_.status
print consul_.health(node='agent-one')

# Access key / value storage
consul_.set('node/name', 'test')
print consul_.storage.get('node/name')
consul_.storage.delete('node/name')

# Or manage local agent (incomplete)
print consul_.local_agent.members
print consul_.local_agent.services
consul_.local_agent.join('172.17.0.3')
```

... in construction ...



License
-------

Copyright 2014 Xavier Bruhiere.

PyConsul is available under the [MIT Licence][2].


[1]: http://consul.io
[2]: http://opensource.org/licenses/MIT
[3]: http://www.consul.io/intro/getting-started/install.html
[4]: http://www.consul.io/intro/
[5]: http://www.consul.io/docs/agent/http.html
