from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ast
import logging

from future import standard_library

standard_library.install_aliases()

from hpOneView.exceptions import HPOneViewException

logger = logging.getLogger(__name__)


def handle_exceptions(exception_type, exception_value, traceback, logger=logger):
    message = get_message(exception_value, exception_type)
    logger.error("Uncaught Exception: %s with message: %s" % (exception_type.__name__, message),
                 exc_info=(exception_type, exception_value, traceback))


def get_message(exception_value, exception_type):
    # Used to get the Exception message.
    # It is necessary special treatment to HPOneViewException because:
    # Sometimes, the exception caught from Rest API is passed as message argument to HPOneViewException
    # (E.g. connection.put). So is necessary get the key 'message' inside the message that  actually is a dictionary.
    # Other times the exceptions are caught, then joined with the status code and passed as message argument to
    # HPOneViewException (E.g. connection.post). So to get the real message is necessary remove the status code and
    # transform the string into a dictionary. Finally it would be possible to get the Key 'message'.

    message = ""

    if len(exception_value.args) > 0:

        message = exception_value.args[0]

        if issubclass(exception_type, HPOneViewException):
            try:
                if message.__class__.__name__ == 'dict':
                    message = message['message']
                else:
                    message = ast.literal_eval(exception_value.args[0].splitlines()[1])['message']
            except:
                pass
    return message
