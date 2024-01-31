# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    allow_cnpj_multi_ie = fields.Boolean(
        string="Multiple partners with the same CPF/CNPJ",
        config_parameter="mut_br_base.allow_cnpj_multi_ie",
        default=False,
    )

    disable_cpf_cnpj_validation = fields.Boolean(
        "Disable CPF and CNPJ validation",
        config_parameter="mut_br_base.disable_cpf_cnpj_validation",
        default=False,
    )

    disable_ie_validation = fields.Boolean(
        "Disable IE validation",
        config_parameter="mut_br_base.disable_ie_validation",
        default=False,
    )

