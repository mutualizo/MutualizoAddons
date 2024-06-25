from odoo import models, fields, api
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = "res.company"

    user_to_notify_cnab = fields.Many2one(
        comodel_name="res.users", string="Usuário para Notificar CNAB"
    )
    days_until_bank_slips_due = fields.Integer(
        string="Dias até o vencimento dos boletos"
    )

    cnab_start_time = fields.Float(string="Horário de Início", default=7.5)
    cnab_end_time = fields.Float(string="Horário Final", default=19.5)

    @api.constrains("cnab_start_time", "cnab_end_time")
    def _check_start_end_time(self):
        for company in self:
            if (company.cnab_start_time < 0 or company.cnab_start_time >= 24) or (
                company.cnab_end_time < 0 or company.cnab_end_time >= 24
            ):
                raise UserError("Os horários devem estar entre 0 e 23:59 horas")
            if company.cnab_start_time > company.cnab_end_time:
                raise UserError(
                    "O horário de início não pode ser maior que o horário final"
                )
