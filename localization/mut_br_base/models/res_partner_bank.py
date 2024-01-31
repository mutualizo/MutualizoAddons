# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import models, fields, api


class ResPartnerBank(models.Model):
    """ Adiciona campos necessários para o cadastramentos de contas
    bancárias no Brasil."""
    _inherit = 'res.partner.bank'

    acc_number = fields.Char('Account Number', size=64, required=False)
    acc_number_dig = fields.Char('Account Number Digit', size=8)
    bra_number = fields.Char('Agency', size=8)
    bra_number_dig = fields.Char('Account Agency Digit', size=8)

    @api.depends('acc_number', 'acc_number_dig', 'bra_number', 'bra_number_dig', 'bank_id')
    def _compute_display_name(self):
        for acc in self:
            acc.display_name = "cc: %s-%s - %s - %s" % (rec.acc_number,
                                                         rec.acc_number_dig or '',
                                                         rec.partner_id.name or '',
                                                         rec.bank_id.name or '')

    @api.depends('bank_id', 'acc_number', 'acc_number_dig', 'bra_number', 'bra_number_dig')
    def _compute_sanitized_acc_number(self):
        for acc in self:
            if acc.bank_id:
                acc_number_format = acc.bank_id.acc_number_format or '%(acc_number)s'
                args = {
                    'bra_number': acc.bra_number or '',
                    'bra_number_dig': acc.bra_number_dig or '',
                    'acc_number': acc.acc_number or '',
                    'acc_number_dig': acc.acc_number_dig or ''
                }
                self.sanitized_acc_number = sanitize_account_number(acc_number_format % args)
            else:
                self.sanitized_acc_number = sanitize_account_number(acc.acc_number)
