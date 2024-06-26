from odoo import models


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"

    def open2generated(self):
        action = super(AccountPaymentOrder, self).open2generated()
        attach_id = self.env['ir.attachment'].browse(action.get('res_id'))
        if attach_id.exists():
            self.write({'description': attach_id[0].name})
        return action
