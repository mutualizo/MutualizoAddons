from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = "account.journal"

    counterpart_pending_account = fields.Boolean(
        string="Criar Contrapartida em Conta Pendente",
        help=(
            "Criar a contrapartida do movimento em conta "
            "pendente de Recebimentos/Pagamentos"
        ),
    )

    def _prepare_counterpart_line(self, move, amount, date):
        res = super(AccountJournal, self)._prepare_counterpart_line(move, amount, date)
        if self.counterpart_pending_account:
            account_id = (
                self.payment_debit_account_id.id
                if amount > 0.0
                else self.payment_credit_account_id.id
            )
            if account_id:
                res.update({"account_id": account_id})
        return res
