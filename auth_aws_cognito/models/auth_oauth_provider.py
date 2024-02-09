"""AWS Cognito login"""
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


class AuthOauthProvider(models.Model):
    """This class is used to add new fields into the provider"""
    _inherit = 'auth.oauth.provider'

    client_secret_id = fields.Char(string='Client Secret',
                                   help="Client Secret of the AWS Cognito app")
    response_type = fields.Selection([('token', 'Token'), ('code', 'Code')],
                                     default='token',
                                     required=True, String="Response Type",
                                     help="Response type of the AWS Cognito")
