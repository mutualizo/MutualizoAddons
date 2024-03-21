# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import fields, models


class PaymentType(models.Model):
    _name = 'payment.type'
    _description = 'Tipo de Pagamento'

    name = fields.Char(string="Tipo de Pagamento", help="Descreva o tipo de pagamento da apólice")
