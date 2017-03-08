# -*- coding: utf-8 -*-
# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from osv import osv, fields
from tools.translate import _
import pooler
import logging
import time

_logger = logging.getLogger(__name__)


class CommonLogging(osv.osv):
    _name = "logging"
    _description = "Logging information"
    _rec_name = "model_id"
    _order = "date desc"

    _columns = {
        'model_id': fields.many2one('ir.model', 'Model', required=True,
            help='Select the model.'),
        'technical_model_name': fields.related('model_id', 'model', type='char',
            size=64, relation="ir.model", string="Tech. model name",
            store=False),
        'date': fields.datetime('Date of Event',
            help="Date and time of the event"),
        'level': fields.selection([
                ('debug', 'Debug'),
                ('info', 'Info'),
                ('warning', 'Warning'),
                ('error', 'Error'),
                ('fatal', 'Fatal'),
            ], 'Level', required=True, help="Level of the line"),
        'summary': fields.char('Summary', size=256),
        'description': fields.text('Description'),
    }
    _defaults = {
        'date': lambda *a: time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    def write_log(self, cr, uid, summary, level='info', date=None,
            description=None, model=None, context=None):
        """
        Uses a new cursor to write a log information
        :param summary:
        :param level:
        :param date:
        :param description:
        :param model: Technical name of the model for which the logging
                      information is written.
        :return: Nothing
        """
        context = context or {}
        Model = self.pool.get('ir.model')
        new_cr = pooler.get_db(cr.dbname).cursor()
        data = {
            'date': date or time.strftime('%Y-%m-%d %H:%M:%S'),
            'level': level,
            'summary': summary,
            'description': description or '',
        }
        if model:
            model_id = Model.search(new_cr, uid, [('model', '=', model)])[0]
            data.update({'model_id': model_id})
        result = self.create(new_cr, uid, data, context=context)
        new_cr.commit()
        new_cr.close()
        return result
CommonLogging()
