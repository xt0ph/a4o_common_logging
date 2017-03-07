# -*- coding: utf-8 -*-
# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
{
    'name': 'Common Logging',
    'version': '7.0.0.4',
    'author': 'Adiczion SARL',
    'license': 'AGPL-3',
    'category': 'Extra',
    'depends': [
        'base'],
    'demo': [],
    'website': 'http://adiczion.com',
    'description': """
Logging
=======

This module does nothing of its own. It provides other modules with a 
centralization environment for logging.

The list of logged events can be accessed via the menu 
'Configuration -> Logging'
    """,
    'data': [
        'security/common_logging_security.xml',
        'security/ir.model.access.csv',
        'views/common_logging_view.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
