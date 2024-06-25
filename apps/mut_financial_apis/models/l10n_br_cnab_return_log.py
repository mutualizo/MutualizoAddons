import json
import pytz

from datetime import datetime, date

from datetime import datetime

from odoo import fields, models

from ..helpers import send_callbacks, format_callback

CALLBACK_STATUS = {
    "02-Entrada Confirmada": "bank_slip_registered",
    "03-Entrada Rejeitada": "bank_slip_error",
    "06-Liquidação Normal *": "bank_slip_paid",
    "22-Título Com Pagamento Cancelado": "bank_slip_canceled",
    "09-Baixado Automat. via Arquivo": "bank_slip_canceled",
}

class L10nBrCNABReturnLog(models.Model):
    _inherit = "l10n_br_cnab.return.log"

    financial_log_ids = fields.One2many(
        comodel_name="financial.callback.log",
        inverse_name="cnab_return_id",
        string="Financial Callback Logs",
    )

    def log_and_send_callbacks(self, url_callback, callbacks):
        try:
            res = send_callbacks(self.env, url_callback, callbacks)
            success, error = res.ok, ""
        except Exception as e:
            success, error = False, str(e)
        # Using sudo because sometimes users with no privilage
        # need to read the CNAB Return File and create a log
        self.env["financial.callback.log"].sudo().create({
            "cnab_return_id": self.id,
            "payload": json.dumps({"url_callback": url_callback, "items": callbacks}),
            "success": success,
            "error": error
        })

    def update_bank_slip_status(self):
        for event in self.event_ids.filtered(lambda x: x.invoice_id):
            status = CALLBACK_STATUS.get(event.occurrences)
            if status:
                event.invoice_id.write({"bank_slip_status": status})

    def send_cnab_return_callbacks(self):
        event_ids = self.event_ids.filtered(
            lambda x: x.invoice_id.url_callback and x.invoice_id.installment_uid
        )
        for url_callback in set(event_ids.invoice_id.mapped("url_callback")):
            """
                Get the status for each 'installment_uid'
                If there's two status for the same installment, only
                send the callback for the latest one
            """
            installment_data = {}
            for event in event_ids.filtered(
                lambda x: x.invoice_id.url_callback == url_callback
            ):
                installment_uid = event.invoice_id.installment_uid
                status = CALLBACK_STATUS.get(event.occurrences)
                installment_data[installment_uid] = {
                    "event_date": datetime.combine(
                        event.occurrence_date, datetime.min.time()
                    ).isoformat(),
                    "uid": installment_uid,
                    "status": status,
                    "credit_date": datetime.combine(
                        event.real_payment_date, datetime.min.time()
                    ).isoformat() if event.real_payment_date else False,
                    "payment_value": event.payment_value,
                }
            callbacks = [
                format_callback(
                    installment["event_date"],
                    installment["uid"],
                    installment["status"],
                    {},
                    installment["credit_date"],
                    installment["payment_value"]
                ) for uid, installment in installment_data.items()
            ]
            self.log_and_send_callbacks(url_callback, callbacks)
