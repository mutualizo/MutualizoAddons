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

class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_br_mut_payment_interest_account_id = fields.Many2one('account.account', string="Conta para pagamento de juros/multa")
    l10n_br_mut_payment_discount_account_id = fields.Many2one('account.account', string="Conta para desconto de pagamentos")

    l10n_br_mut_interest_account_id = fields.Many2one('account.account', string="Conta para recebimento de juros/multa")
    l10n_br_mut_discount_account_id = fields.Many2one('account.account', string="Conta para desconto de recebimentos")
    l10n_br_mut_bankfee_account_id = fields.Many2one('account.account', string="Conta para tarifas bancárias")

    l10n_br_mut_multa_tx = fields.Float(string='Tx.Multa %', digits=(16, 4), default=0.0)
    l10n_br_mut_juros_mes_tx = fields.Float(string='Tx.Juros/Mes %', digits=(16, 4), default=0.0)
    l10n_br_mut_desc_ant_tx = fields.Float(string='Tx.Desc.Ant./Mes %', digits=(16, 4), default=0.0)
    