hpOneView
=========

This library provides a pure Python interface to the HP OneView REST APIs.

HP OneView is a fresh approach to converged infrastructure management, inspired
by the way you expect to work, with a single integrated view of your IT
infrastructure.

The HP OneView Python library depends on the
[Python-Future](http://python-future.org/index.htm)  library to provide Python
2/3 compatibility.  This will be installed automatically if you use the installation
methods described below.

Installation
------------

### From source

Either:

```bash
$ git clone https://github.com/HewlettPackard/python-hpOneView.git
$ cd python-hpOneView
$ python setup.py install --user  # to install in the user directory (~/.local)
$ sudo python setup.py install    # to install globally
```

Or if using PIP:

```bash
$ git clone https://github.com/HewlettPackard/python-hpOneView.git
$ cd python-hpOneView
$ pip install .
```

Both of these installation methods work if you are using virtualenv, which you should be!

### From Pypi

Coming soon


API Implementation
------------------

Status listing of the HP OneView REST interfaces that have been implemented in the Python library so far is hosted in the [Wiki section](https://github.com/HewlettPackard/python-hpOneView/wiki/API-Implementation) 
