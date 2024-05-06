from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    nifi_callback_url = fields.Char(
        string="Nifi Callback URL", config_parameter="financial_apis.nifi_callback_url"
    )
    financial_api_key = fields.Char(
        string="Financial API Key", config_parameter="financial_apis.api_key"
    )
