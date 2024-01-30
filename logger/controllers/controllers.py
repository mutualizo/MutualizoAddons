# -*- coding: utf-8 -*-
from odoo import http, fields
import logging

_logger = logging.getLogger(__name__)


def log(**kw):
    if kw['log_type'] == 'debug':
        _logger.debug(log)
    elif kw['log_type'] == 'info':
        _logger.info(log)
    elif kw['log_type'] == 'warning':
        _logger.warning(log)
    elif kw['log_type'] == 'error':
        _logger.error(log)
    elif kw['log_type'] == 'critical':
        _logger.critical(log)


def log_parser(**kw):
    log_type = kw.get('log_type') if kw.get('log_type') else 'debug'
    log_message = kw.get('message') if kw.get('message') else 'missing "message" on args'
    log_timestamp = kw.get('timestamp') if kw.get('timestamp') else fields.Datetime.now
    log_ip = kw.get('ip') if kw.get('ip') else 'missing "ip" on args'
    return {
        'ip': log_ip,
        'type': log_type,
        'message': log_message,
        'timestamp_message': log_timestamp,
        'timestamp': fields.Datetime.now,
    }


class LogController(http.Controller):
    @http.route('/log', auth='public')
    def index(self, **kw):
        parsed_log = log_parser(**kw)
        log(**parsed_log)
        self.env['logger'].create(parsed_log)
