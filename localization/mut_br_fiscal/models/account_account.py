# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import api, fields, models, _


class AccountAccount(models.Model):
    _inherit = 'account.account'

    account_type = fields.Selection([('tax', 'Imposto'), ('income', 'Receita'), ('expense', 'Despesa')],string="Tipo de conta")
    shortcut = fields.Integer(string="Cod.Curto", index=True)
