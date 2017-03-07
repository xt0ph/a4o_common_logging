# -*- coding: utf-8 -*-
# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from openerp import registry
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, timedelta
import logging
import time

_logger = logging.getLogger(__name__)
_Step = 5000


class CommonLogging(osv.osv):
    _name = "logging"
    _description = "Logging information"
    _rec_name = "technical_model_name"
    _order = "date desc, id desc"

    _columns = {
        'model_id': fields.many2one('ir.model', 'Model', required=True,
            help='Select the model.'),
        'technical_model_name': fields.related('model_id', 'name',
            string="Tech. model name", readonly=True),
        'date': fields.datetime('Date of Event', select=True,
            help="Date and time of the event"),
        'level': fields.selection([
            ('debug', 'Debug'),
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('error', 'Error'),
            ('fatal', 'Fatal')], string='Level', required=True,
            help="Level of the line"),
        'summary': fields.char('Summary'),
        'description': fields.char('Description'),
    }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
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
        with registry(cr.dbname).cursor() as new_cr:
            model_id = self.pool.get('ir.model').search(new_cr,
                uid, [('model', '=', model)])[0]
            self.create(new_cr, uid, {
                'date': date or time.strftime('%Y-%m-%d %H:%M:%S'),
                'level': level,
                'summary': summary,
                'description': description or '',
                'model_id': model_id,
            }, context=context)
            new_cr.commit()
        return True
    
    def cleaning_log(self, cr, uid, oldest_than=100, models=None, context=None):
        """
        :param oldest_than: Number of days.
        """
        domain = []
        if models:
            #models = eval(models)
            if not isinstance(models, list):
                models = [models]
            model_ids = self.pool.get('ir.model').search(cr, uid,
                [('model', 'in', models)], context=context)
            if model_ids:
                domain.append(('model_id', 'in', model_ids))
        dead_line = datetime.now() - timedelta(days=int(oldest_than))
        dead_line = dead_line. strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        domain.append(('date', '<', dead_line))
        while True:
            ids = self.search(cr, uid, domain, limit=_Step, context=context)
            if not ids:
                break
            self.unlink(cr, uid, ids, context=context)
        return True
