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


class City(models.Model):
    """ Este objeto persite todos os municípios relacionado a um estado.
    No Brasil é necessário em alguns documentos fiscais informar o código
    do IBGE dos município envolvidos da transação.
    """
    _inherit = "res.city"

    region_id = fields.Many2one(comodel_name='res.region', string='Region', related="state_id.region_id", 
                                store=True, readonly=True)
    ibge_code = fields.Char(string='IBGE Code', size=7, copy=False)


