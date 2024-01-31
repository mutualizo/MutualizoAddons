# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import models, fields, api, _


class ResBank(models.Model):
    _inherit = 'res.bank'

    number = fields.Char('Number', size=10)
    street2 = fields.Char('Complement', size=128)
    district = fields.Char('District', size=32)
    city = fields.Many2one(comodel_name='res.state.city', string='City', domain="[('state_id','=?',state_id)]")
    state = fields.Many2one('res.country.state', 'Fed. State', domain="[('country_id', '=?', country)]")
    country = fields.Many2one('res.country')
    acc_number_format = fields.Text(help=_("""You can enter here the format as\
    the bank accounts are referenced in ofx files for the import of bank\
    statements.\nYou can use the python patern string with the entire bank \
    account field.\nValid Fields:\n
          %(bra_number): Bank Branch Number\n
          %(bra_number_dig): Bank Branch Number's Digit\n
          %(acc_number): Bank Account Number\n
          %(acc_number_dig): Bank Account Number's Digit\n
    For example, use '%(acc_number)s' to display the field 'Bank Account \
    Number' plus '%(acc_number_dig)s' to display the field 'Bank Account \
    Number s Digit'."""), default='%(acc_number)s')
    
