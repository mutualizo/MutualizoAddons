from odoo import fields, models, api


class L10nBrCNABReturnLog(models.Model):
    _inherit = "l10n_br_cnab.return.log"

    company_id = fields.Many2one(comodel_name="res.company", string="Empresa")

    @api.model
    def create(self, vals):
        if vals.get("bank_account_id"):
            bank_account_id = (
                self.env["res.partner.bank"].sudo().browse(vals.get("bank_account_id"))
            )
            if bank_account_id.company_id == self.env.company:
                vals["company_id"] = self.env.company.id
        return super(L10nBrCNABReturnLog, self).create(vals)
