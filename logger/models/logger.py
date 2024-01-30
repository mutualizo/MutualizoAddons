from odoo import models, fields, api


class Logger(models.Model):
    _name = 'logger'
    _description = 'Logger'

    message = fields.Char(string='Log Message', required=True)
    ip = fields.Char(string='Sender IP')
    timestamp_message = fields.Datetime(string='Timestamp Message', readonly=True)
    timestamp = fields.Datetime(string='Timestamp', default=fields.Datetime.now, readonly=True)
    log_type = fields.Char(string='Log Type', default='debug')
