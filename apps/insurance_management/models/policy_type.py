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


class PolicyType(models.Model):
    """Essa classe cria um modelo "policy.type" e adiciona campos """
    _name = 'policy.type'
    _description = "Tipo da Apólice"

    name = fields.Char(string='Name', help="Descrição do Tipo da Apólice")
