# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import fields, models, api

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    acc_number_dig = fields.Char(related='bank_account_id.acc_number_dig')
    bank_agency_number = fields.Char(related='bank_account_id.bra_number')
    bank_agency_dig = fields.Char(related='bank_account_id.bra_number_dig')
    acc_partner_id = fields.Many2one('res.partner',related='bank_account_id.partner_id')
    can_collection = fields.Boolean(string='Disponível na cobrança', default=True)
