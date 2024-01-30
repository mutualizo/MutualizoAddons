from odoo import models, fields, api


class Logger(models.Model):
    _name = 'logger'
    _description = 'Logger'

    message = fields.Char(string='Log Message', required=True)
    timestamp = fields.Datetime(string='Timestamp', default=fields.Datetime.now, readonly=True)
    log_type = fields.Char(string='Log Type', default='debug')
