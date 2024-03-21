# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import models, fields


class AccountMove(models.Model):
    """Esta classe herda "account.move" e adicionou os campos insurance_id e claim_id"""
    
    _inherit = 'account.move'

    insurance_id = fields.Many2one('insurance.details', string='Apolice Seguro', help="Indicar os dados do seguro na fatura")
    claim_id = fields.Many2one('claim.details', string='Pedido Indenização', help="Fornecer os dados da indenização")
