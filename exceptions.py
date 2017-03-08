# -*- coding: utf-8 -*-
# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.


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
