# -*- coding: utf-8 -*-
# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
{
    'name': 'Common Logging',
    'version': '12.0.0.6',
    'author': 'Adiczion SARL',
    'license': 'AGPL-3',
    'category': 'Extra',
    'depends': [
        'base',
        'mail',
        ],
    'demo': [],
    'website': 'http://adiczion.com',
    'description': """
Logging
=======

This module does nothing by itself. It provides to the other modules a
centralization environment for logging.

The list of logged events can be accessed via the menu
'Configuration -> Logging'
    """,
    'data': [
        'security/common_logging_security.xml',
        'security/ir.model.access.csv',
        'data/common_logging_data.xml',
        'views/common_logging_view.xml',
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
