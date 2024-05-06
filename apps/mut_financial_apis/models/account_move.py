from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    contract_number = fields.Char(string="Contract Number", tracking=True)
    total_installments = fields.Integer(string="Total Installments")
    installment_uid = fields.Char(string="Installment External Identifier")
    installment_number = fields.Integer(string="Installment Number")
    url_callback = fields.Char(string="URL Callback")
    additional_description_installment = fields.Text(
        string="Additional Description Installment"
    )
