from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    user_to_notify_cnab = fields.Many2one(
        comodel_name="res.users", string="Usuário para Notificar CNAB"
    )
    days_until_bank_slips_due = fields.Integer(
        string="Dias até o vencimento dos boletos",
    )

    @api.onchange("state_id")
    def _onchange_state_id(self):
        if self.city_id.state_id != self.state_id:
            self.city_id = None

    @api.onchange("zip")
    def _onchange_zip(self):
        super(ResCompany, self)._onchange_zip()
        if self.zip:
            zip_vals = self.env["l10n_br.zip"]._consultar_cep(self.zip)
            if zip_vals:
                zip_vals['zip'] = zip_vals.pop('zip_code')
                zip_vals['street2'] = zip_vals.pop('zip_complement')
                self.update(zip_vals)
                # Update in city_id because the onchange in
                # state_id erases the current city
                self.update({"city_id": zip_vals["city_id"]})