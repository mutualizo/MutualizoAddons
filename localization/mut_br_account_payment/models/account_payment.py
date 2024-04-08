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

class AccountPayment(models.Model):
    _inherit = "account.payment"

    discount    = fields.Monetary(string='Desconto', default=0.0, currency_field='currency_id')
    interest    = fields.Monetary(string='Juros', default=0.0, currency_field='currency_id')
    fee         = fields.Monetary(string='Multa', default=0.0, currency_field='currency_id')

    pay_sub     = fields.Monetary(compute="_pay_amount",string='Valor Pago', currency_field='currency_id', readonly=True, store=True)
    pay_amount  = fields.Monetary(compute="_pay_amount",string='Total Pago', currency_field='currency_id', readonly=True, store=True)

    @api.depends('fee','interest','amount','discount')
    def _pay_amount(self):
        self.pay_sub = (self.amount + self.discount)
        self.pay_amount = self.amount + self.fee + self.interest

