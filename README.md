[![PyPI version](https://badge.fury.io/py/hpOneView.svg)](https://badge.fury.io/py/hpOneView)
[![Build Status](https://travis-ci.org/HewlettPackard/python-hpOneView.svg?branch=master)](https://travis-ci.org/HewlettPackard/python-hpOneView)

# HPE OneView SDK for Python

This library provides a pure Python interface to the HPE OneView REST APIs.

HPE OneView is a fresh approach to converged infrastructure management, inspired
by the way you expect to work, with a single integrated view of your IT
infrastructure.

The HPE OneView Python library depends on the
[Python-Future](http://python-future.org/index.htm) library to provide Python
2/3 compatibility. This will be installed automatically if you use the installation
methods described below.

## Installation

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

```bash
$ pip install hpOneView
```


## API Implementation

A status of the HPE OneView REST interfaces that have been implemented in this Python library can be found in the [Wiki section](https://github.com/HewlettPackard/python-hpOneView/wiki/HPE-OneView-API-Version-200-Implementation-Status).


## SDK Documentation

The latest version of the SDK documentation can be found in the [SDK Documentation section] (https://hewlettpackard.github.io/python-hpOneView/index.html).

## Logging

This module uses Python’s Standard Library logging module. An example of how to configure logging is provided on [```/examples/logger.py```](/examples/logger.py).

More information about the logging configuration can be found in the Python Documentation.

## Configuration

### JSON

Connection properties for accessing the OneView appliance can be set in a JSON file.

Before running the samples or your own scrips, you must create the JSON file.
An example can be found at: [OneView configuration sample](examples/config-rename.json).

Once you have created the JSON file, you can initialize the OneViewClient:

```python
oneview_client = OneViewClient.from_json_file('/path/config.json')
```

:lock: Tip: Check the file permissions because the password is stored in clear-text.

### Environment Variables

Configuration can also be store in environment variables.

```bash
# Required
export ONEVIEWSDK_IP='172.16.102.82'
export ONEVIEWSDK_USERNAME='Administrator'
export ONEVIEWSDK_PASSWORD='secret123'

# Optional
export ONEVIEWSDK_API_VERSION='200'
export ONEVIEWSDK_AUTH_LOGIN_DOMAIN='authdomain'
export ONEVIEWSDK_PROXY='<proxy_host>:<proxy_port>'
```

:lock: Tip: Make sure no unauthorised person has access to the environment variables, since the password is stored in clear-text.

Once you have defined the environment variables, you can initialize the OneViewClient:

```python
oneview_client = OneViewClient.from_environment_variables()
```

### Dictionary

You can also set the configuration using a dictionary:

```python
config = {
    "ip": "172.16.102.82",
    "credentials": {
        "userName": "Administrator",
        "password": "secret123"
    }
}

oneview_client = OneViewClient(config)
```

:lock: Tip: Check the file permissions because the password is stored in clear-text.

### Proxy

If your environment requires a proxy, define the proxy properties in the JSON file using the following syntax:

```json
  "proxy": "<proxy_host>:<proxy_port>"
```

## Exception handling

All the exceptions raised by the OneView Python SDK inherit from HPOneViewException.

**HPOneViewException** has the following properties:
- **msg** a string containing the error message sent by the OneView REST API;
- **oneview_response** has the entire JSON data (as dict) returned by the OneView, describing the error details. It can be ```None```.

##### Exception handling example:

```python
try:
    fc_network = oneview_client.fc_networks.get(id)
except HPOneViewException as e:
    print(e.msg)
    if e.oneview_response:
    	pprint(e.oneview_response)   
```

For compatibility purposes, the Exception args property is defined with the error arguments. For example:

```python
except Exception as e:
	print(arg[0]) # e.msg equivalent
    print(arg[1]) # e.oneview_reponse equivalent
```

:warning: The Exception Handling was modified on 2016-09-12. So, <u>before</u> this [commit](https://github.com/HewlettPackard/python-hpOneView/commit/37bd76894f8975fa3f78834b61e1eff10dc592e6), the behavior was:

```python
except HPOneViewException as e:
    print(e.msg) # has the entire JSON result from OneView, or the error message.
```

## Contributing

You know the drill. Fork it, branch it, change it, commit it, and pull-request it.
We are passionate about improving this project, and glad to accept help to make it better. However, keep the following in mind:

 - We reserve the right to reject changes that we feel do not fit the scope of this project, so for feature additions, please open an issue to discuss your ideas before doing the work.

#### Naming convention for OneView resources

The following is a summary of the code structure and naming convention for the OneView resources.

- **Packages:** The package is named according to the **HPE OneView API Reference** group, with all characters in lowercase, replacing spaces by underscores.
- **Modules:** The module is named according to the **HPE OneView API Reference** endpoint title, with all characters in lowercase, replacing spaces by underscores.
    For example: In the documentation we have: **FC Networks** so the module name will be **fc_networks**
- **Classes:** We are using camel case to define the class name, for example: **FcNetworks**
- **OneViewClient properties:** In the **oneview_client**, the property name follows exactly the module name, for example: **fc_networks**
- **Examples:** The example is named with the same name of the resource module: **fc_networks**
- **Tests:**  The unit test folders follow the same structure of the resources. The name of the test modules should start with "test_", for example: **test_fc_networks**

## Feature Requests

If you have a need that is not met by the current implementation, please let us know (via a new issue).
This feedback is crucial for us to deliver a useful product. Do not assume that we have already thought of everything, because we assure you that is not the case.

## Testing

We've already packaged everything you need to do to check if the code is passing the tests.
The tox script wraps the unit tests execution against Python 2 and 3, flake8 validation, and the test coverage report generation.

Run the following command:

```
$ tox
```
