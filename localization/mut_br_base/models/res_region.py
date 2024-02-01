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


class ResRegion(models.Model):
    _name = 'res.region'
    _description = 'Region of Country'

    name = fields.Char(string="Name", size=100)
    country_id = fields.Many2one('res.country', string="Country", required=True)
    city_ids = fields.One2many('res.city', 'region_id', string="Cities")
    state_ids = fields.One2many('res.country.state', 'region_id', string="States")
