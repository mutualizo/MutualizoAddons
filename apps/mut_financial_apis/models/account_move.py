from odoo import models, fields

from datetime import timedelta, date


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

    def _cron_confirm_invoices_generate_boleto_cnab(self):
        company_ids = self.env["res.company"].search([])
        for company_id in company_ids:
            invoices_to_confirm = (
                self.env["account.move"]
                .search(
                    [
                        ("company_id", "=", company_id.id),
                        ("move_type", "=", "out_invoice"),
                        ("state", "=", "draft"),
                        (
                            "payment_mode_id.fixed_journal_id.bank_id",
                            "=",
                            self.env.ref("l10n_br_base.res_bank_237").id,
                        ),
                        ("contract_number", "!=", False),
                        ("invoice_line_ids", "!=", False),
                    ]
                )
                .filtered(
                    lambda x: (
                        (
                            x.invoice_date_due
                            <= (
                                date.today()
                                + timedelta(days=company_id.days_until_bank_slips_due)
                            )
                        )
                        if company_id.days_until_bank_slips_due
                        else x
                    )
                )
            )
            if invoices_to_confirm:
                for invoice in invoices_to_confirm:
                    invoice.action_post()
                    if not invoice.file_boleto_pdf_id:
                        invoice.generate_boleto_pdf()
                action_payment_order = invoices_to_confirm.create_account_payment_line()
                payment_order_id = self.env["account.payment.order"].browse(
                    action_payment_order.get("res_id")
                )
                payment_order_id.draft2open()
                payment_order_id.open2generated()
                if company_id.user_to_notify_cnab:
                    self.env["mail.activity"].create(
                        {
                            "summary": (
                                "Novo Arquivo de Remessa Criado: "
                                + f"{payment_order_id.name}"
                            ),
                            "res_model_id": self.env.ref(
                                "account_payment_order.model_account_payment_order"
                            ).id,
                            "res_id": payment_order_id.id,
                            "date_deadline": date.today() + timedelta(days=5),
                            "user_id": company_id.user_to_notify_cnab.id,
                        }
                    )
            return
