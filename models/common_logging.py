# -*- coding: utf-8 -*-
# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from openerp import models, fields, api, registry, _
import logging
import time

_logger = logging.getLogger(__name__)


class CommonLogging(models.Model):
    _name = "logging"
    _description = "Logging information"
    _rec_name = "model_id"
    _order = "date desc"

    model_id = fields.Many2one(
        comodel_name='ir.model', string='Model', required=True,
        help='Select the model.')
    technical_model_name = fields.Char(
        string="Tech. model name", readonly=True, related='model_id.model')
    date = fields.Datetime(
        string='Date of Event', index=True, default=fields.datetime.now(),
        help="Date and time of the event")
    level = fields.Selection([
            ('debug', 'Debug'),
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('error', 'Error'),
            ('fatal', 'Fatal'),
        ], string='Level', required=True, help="Level of the line")
    summary = fields.Char(string='Summary')
    description = fields.Char(string='Description')
    
    @api.multi
    def write_log(self, summary, level='info', date=None, description=None,
                  model=None):
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
        with api.Environment.manage():
            with registry(self.env.cr.dbname).cursor() as new_cr:
                new_env = api.Environment(
                    new_cr, self.env.uid, self.env.context)
                new_env = self.with_env(new_env)
                new_env.create({
                    'date': date or time.strftime('%Y-%m-%d %H:%M:%S'),
                    'level': level,
                    'summary': summary,
                    'description': description or '',
                    'model_id': model and new_env.env['ir.model'].search(
                        [('model', '=', model)]).id,
                })
