from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    user_to_notify_cnab = fields.Many2one(
        comodel_name="res.users",
        related="company_id.user_to_notify_cnab",
        string="Usuário",
        readonly=False,
    )
    days_until_bank_slips_due = fields.Integer(
        related="company_id.days_until_bank_slips_due",
        string="Número de Dias",
        readonly=False
    )
