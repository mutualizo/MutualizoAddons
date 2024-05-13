# Copyright 2020 Akretion
# @author Magno Costa <magno.costa@akretion.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models

from ..helpers import send_callbacks, format_callback


class CreditPartnerStatementImporter(models.TransientModel):
    _inherit = "credit.statement.import"

    def import_statement(self):
        res = super(CreditPartnerStatementImporter, self).import_statement()
        account_move_ids = self.env["account.move"].search(res.get("domain"))
        event_ids = account_move_ids.cnab_return_log_id.event_ids
        # TODO: Get the status of the bank slip in a more dynamic way.
        # The return statuses are in the data xml file of the
        # l10n_br_account_payment_order module, the external ids
        # start with bradesco_400_return_
        callback_status = {
            "02-Entrada Confirmada": "bank_slip_registered",
            "03-Entrada Rejeitada": "bank_slip_error",
            "06-Liquidação Normal *": "bank_slip_paid",
            "22-Título Com Pagamento Cancelado": "bank_slip_canceled",
        }
        processed_callbacks = {}
        for url_callback in set(event_ids.invoice_id.mapped("url_callback")):
            callbacks = []
            for event in event_ids.filtered(
                lambda x: x.invoice_id.url_callback == url_callback
            ):
                installment_uid = event.invoice_id.installment_uid
                status = callback_status.get(event.occurrences)
                if installment_uid in processed_callbacks:
                    existing_index = processed_callbacks[installment_uid]
                    callbacks[existing_index] = format_callback(installment_uid, status)
                else:
                    callbacks.append(format_callback(installment_uid, status))
                    processed_callbacks[installment_uid] = len(callbacks) - 1
            send_callbacks(url_callback, callbacks)
        return res
