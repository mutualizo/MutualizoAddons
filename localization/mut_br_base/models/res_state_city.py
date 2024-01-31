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


class ResStateCity(models.Model):
    """ Este objeto persite todos os municípios relacionado a um estado.
    No Brasil é necessário em alguns documentos fiscais informar o código
    do IBGE dos município envolvidos da transação.
    """
    _name = 'res.state.city'
    _description = 'City of states in the country'

    name = fields.Char(string='Name', size=64, required=True)
    state_id = fields.Many2one(comodel_name='res.country.state', string='State', required=True)
    country_id = fields.Many2one(comodel_name='res.country', string='State', related='state_id.country_id',
                                 store=True, readonly=True)
    region_id = fields.Many2one(comodel_name='res.region', string='Region', related="state_id.region_id", 
                                store=True, readonly=True)
    ibge_code = fields.Char(string='IBGE Code', size=7, copy=False)


