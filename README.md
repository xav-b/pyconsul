PyConsul
========

> Python client for [Consul][1]


A dummy, one-file, implementation on top of the [HTTP API][5] of Consul.

Install
-------

* Install Consul following [the official guide][3] or this one-liner:

```console
$ # Install consul 0.1.0_linux_amd64 under /usr/local/bin
$ wget -qO- https://raw.githubusercontent.com/hackliff/pyconsul/master/install-consul.sh | (sudo) bash
```

* Install pyconsul library

```console
$ git clone https://github.com/hackliff/pyconsul
$ cd pyconsul && (sudo) python setup.py install
```


Getting started
---------------

I strongly advise you to go through [the official Consul documentation][4]
before playing around with pyconsul.

Make sure an agent is running, for example with :

```console
consul agent -server -bootstrap \
  -data-dir /tmp/consul \
  -node=agent-one \
  -bind=0.0.0.0
```

Then you can talk to it

```python
from pyconsul import Consul

# On the same server
consul_ = Consul()
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
