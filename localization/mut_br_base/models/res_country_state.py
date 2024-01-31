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


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    ibge_code = fields.Char('IBGE Code', size=2)
    region_id = fields.Many2one(comodel_name='res.region', string='Region', domain="[('country_id','=?',country_id)]")
