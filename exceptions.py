# -*- coding: utf-8 -*-
# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from functools import wraps
from odoo.exceptions import UserError
from odoo import _
import traceback
import requests
import logging

_logger = logging.getLogger(__name__)


def catch_exception(log_only=False, header=False):
    def wrap(function):
        @wraps(function)
        def wrapped_function(self, *args, **kwargs):
            CommonLogging = self.env['logging']
            try:
                return function(self, *args, **kwargs)
            except requests.exceptions.Timeout as e:
                summary = ' '.join(filter(None, [header, _('Timeout Error:')]))
                CommonLogging.write_log(summary, level='error',
                    model=self._name,
                    description="%s\n\n%s" % (repr(e), traceback.format_exc()))
                _logger.error("%s %s" % (summary, e))
                if not log_only:
                    raise UserError("%s %s" % (summary, e))
            except requests.exceptions.HTTPError as e:
                summary = ' '.join(filter(None, [header, _('Http Error:')]))
                CommonLogging.write_log(summary, level='error',
                    model=self._name,
                    description="%s\n\n%s" % (repr(e), traceback.format_exc()))
                _logger.error("%s %s" % (summary, e))
                if not log_only:
                    raise UserError("%s %s" % (summary, e))
            except requests.exceptions.ConnectionError as e:
                summary = ' '.join(filter(None,
                        [header, _('Error Connecting:')]))
                CommonLogging.write_log(summary, level='error',
                    model=self._name,
                    description="%s\n\n%s" % (repr(e), traceback.format_exc()))
                _logger.error("%s %s" % (summary, e))
                if not log_only:
                    raise UserError("%s %s" % (summary, e))
            except requests.exceptions.RequestException as e:
                summary = ' '.join(filter(None,
                        [header, _('Something Else:')]))
                CommonLogging.write_log(summary, level='error',
                    model=self._name,
                    description="%s\n\n%s" % (repr(e), traceback.format_exc()))
                _logger.error("%s %s" % (summary, e))
                if not log_only:
                    raise UserError("%s %s" % (summary, e))
            except Exception as e:
                summary = ' '.join(filter(None,
                        [header, _('Another exception (see description):')]))
                CommonLogging.write_log(summary, level='error',
                    model=self._name,
                    description="%s\n\n%s" % (repr(e), traceback.format_exc()))
                _logger.error("%s %s" % (summary, e))
                if not log_only:
                    raise UserError("%s %s" % (summary, e))
        return wrapped_function
    return wrap


class Error(Exception):
    """Base class for exceptions in our modules."""
    def __init__(self, *args):
        Exception.__init__(self, *args)


class ValidationError(Error):
    """Raised when the data is inconsistent

    Attributes:
        msg -- Summary of the error occurred
        extention -- Dictionnary for misc informations
    """
    def __init__(self, msg, extension=None):
        super(ValidationError, self).__init__(self, msg)
        if extension:
            self.ext = extension
        self.msg = msg
