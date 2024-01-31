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


class ResCountry(models.Model):
    _inherit = 'res.country'

    bc_code = fields.Char('BC Code', size=5)
    ibge_code = fields.Char('IBGE Code', size=5)
    siscomex_code = fields.Char('Siscomex Code', size=4)
