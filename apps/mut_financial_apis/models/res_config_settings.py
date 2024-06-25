from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    nifi_callback_url = fields.Char(
        string="Nifi Callback URL",
        config_parameter="mut_financial_apis.nifi_callback_url",
    )
    financial_api_key = fields.Char(
        string="Financial API Key", config_parameter="mut_financial_apis.load_api_key"
    )
    user_to_notify_cnab = fields.Many2one(
        comodel_name="res.users",
        related="company_id.user_to_notify_cnab",
        string="Usuário",
        readonly=False,
    )
    days_until_bank_slips_due = fields.Integer(
        related="company_id.days_until_bank_slips_due",
        string="Número de Dias",
        readonly=False,
    )
    cnab_start_time = fields.Float(
        string="Horário de Início",
        related="company_id.cnab_start_time",
        readonly=False,
    )
    cnab_end_time = fields.Float(
        string="Horário Final",
        related="company_id.cnab_end_time",
        readonly=False,
    )
