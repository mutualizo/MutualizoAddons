# -*- coding: utf-8 -*-
from odoo import http,logging

_logger = logging.getLogger(__name__)


def log_switch(log_type, log):
    if log_type == 'debug':
        _logger.debug(log)
    elif log_type == 'info':
        _logger.info(log)
    elif log_type == 'warning':
        _logger.warning(log)
    elif log_type == 'error':
        _logger.error(log)
    elif log_type == 'critical':
        _logger.critical(log)


class LogController(http.Controller):
    @http.route('/log', auth='public')
    def index(self, **kw):
        log_type = kw.get('log_type') if kw.get('log_type') else 'debug'
        log_message = kw.get('message')
        log_timestamp = kw.get('type_stamp')
        log_values = {
            'type': log_type,
            'message': log_message,
            'timestamp': log_timestamp
        }
        log_switch(log_type, log_message)
        self.env['logger'].create(log_values)
