import re
import pytz

from odoo import models, fields

from werkzeug.urls import url_join
from datetime import timedelta, date, datetime, time

from ..helpers import send_callbacks, format_callback

MAIL_REGEX = re.compile(
    r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
)


def time_from_float(value):
    """Odoo saves time values as float (ex 1:30 as 1.5)
    this method extracts hours and minutes from the float value"""
    result = time(0, 0)
    if isinstance(value, float):
        try:
            hour = int(value)
            minute = int(60 * (value - hour))
            result = time(hour, minute)
        except ValueError:
            result = time(0, 0)
    return result


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
    notification_status = fields.Selection(
        [("not_sent", "Not Sent"), ("in_queue", "In Queue"), ("sent", "Sent")],
        string="Notification Status",
        default="not_sent",
    )
    bank_slip_status = fields.Selection(
        [
            ("bank_slip_not_issued", "Não Registrado"),
            ("bank_slip_issued", "Enviado"),
            ("bank_slip_error", "Rejeitado"),
            ("bank_slip_registered", "Registrado"),
            ("bank_slip_paid", "Pago com registro"),
            ("bank_slip_canceled", "Cancelado"),
        ],
        string="Status do Boleto",
        default="bank_slip_not_issued",
        tracking=True,
    )

    def _cron_confirm_invoices_generate_cnab(self):
        now = datetime.now(pytz.timezone("America/Sao_Paulo"))
        if now.weekday() >= 5:
            return
        company_ids = self.env["res.company"].search(
            [
                ("user_ids", "in", self.env.user.id),
                ("days_until_bank_slips_due", "!=", False),
            ]
        )
        for company_id in company_ids:
            start_time = time_from_float(company_id.cnab_start_time)
            end_time = time_from_float(company_id.cnab_end_time)

            if (
                not self.env.context.get("skip_time_verification")
                and now.time() < start_time
                or now.time() > end_time
            ):
                continue

            invoices_to_confirm = self.env["account.move"].search(
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
                    (
                        "invoice_date_due",
                        "<=",
                        date.today()
                        + timedelta(days=company_id.days_until_bank_slips_due),
                    ),
                ],
                limit=2000,
                order="id asc",
            )
            for invoice in invoices_to_confirm:
                invoice.action_post()
                invoice.generate_boleto_pdf()
            if invoices_to_confirm:
                invoices_to_confirm.create_account_payment_line()
            payment_orders = self.env["account.payment.order"].search(
                [
                    ("state", "=", "draft"),
                    ("payment_type", "=", "inbound"),
                    ("company_id", "=", company_id.id),
                ]
            )
            for payment_order_id in payment_orders:
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
                            "date_deadline": date.today(),
                            "user_id": company_id.user_to_notify_cnab.id,
                        }
                    )

    def get_bank_slip_url(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        bank_slip = self.file_boleto_pdf_id
        if bank_slip:
            bank_slip.generate_access_token()
            return url_join(
                base_url,
                f"/web/content/{bank_slip.id}"
                + f"?download=true&access_token={bank_slip.access_token}",
            )
        return ""

    def send_bank_slip_to_invoice_followers(self):
        mail_template = self.env.ref("mut_financial_apis.email_template_send_bank_slip")
        context = {
            "invoice_date_due": self.invoice_date_due.strftime("%d/%m/%Y"),
            "contract_number": self.contract_number,
            "installment_number": self.installment_number,
            "company_email": self.company_id.email,
            "company_name": self.company_id.name,
            "payer_name": self.partner_id.name,
            "total_installments": self.total_installments,
        }
        api_user = self.env.ref("mut_financial_apis.api_user")
        for partner_id in self.message_follower_ids.mapped("partner_id"):
            # The id=2 is OdooBot and id=3 is the Admin User
            # The admin user is automatically added as an invoice follower
            # and we do not want to send all invoices to him by email
            if (
                partner_id == self.partner_id
                and self.company_id.user_to_notify_cnab
                and not re.fullmatch(MAIL_REGEX, partner_id.email or "")
            ):
                self.env["mail.activity"].create(
                    {
                        "summary": (
                            f"O e-mail do pagador da fatura {self.name} "
                            + "é invalido!"
                        ),
                        "note": (
                            f"<p>O email do pagador <a href='#' data-oe-model='res.partner' data-oe-id='{self.partner_id.id}'>{self.partner_id.name}</a> "
                            + f"da fatura <a href='#' data-oe-model='account.move' data-oe-id='{self.id}'>{self.name}</a> é inválido</p>"
                        ),
                        "res_model_id": self.env.ref("account.model_account_move").id,
                        "res_id": self.id,
                        "date_deadline": date.today(),
                        "user_id": self.company_id.user_to_notify_cnab.id,
                    }
                )
                continue
            elif partner_id.id in [2, 3, api_user.partner_id.id] or not re.fullmatch(
                MAIL_REGEX, partner_id.email or ""
            ):
                continue
            mail_template.write(
                {
                    "email_to": partner_id.email,
                }
            )
            mail_template.with_context(context).send_mail(self.id, force_send=True)

    def _get_brcobranca_boleto(self, boletos):
        for boleto in boletos:
            cedente = boleto["cedente"] or ""
            cedente = cedente if len(cedente) < 68 else cedente[:68].strip() + "[...]"
            description = self.additional_description_installment or ""
            boleto["demonstrativo"] = (
                boleto.get("cedente", "")
                + "\n"
                + boleto.get("instrucao1", "")
                + "\n"
                + description[:1000]
            )
            boleto["cedente"] = cedente
            boleto["instrucoes"] = boleto.pop("instrucao1")
        return super(AccountMove, self)._get_brcobranca_boleto(boletos)

    def generate_boleto_pdf(self):
        super(AccountMove, self).generate_boleto_pdf()
        if self.file_boleto_pdf_id and self.contract_number and self.installment_number:
            self.file_boleto_pdf_id.write(
                {"name": f"Boleto-{self.contract_number}-{self.installment_number}.pdf"}
            )
        self.write({"bank_slip_status": "bank_slip_issued"})

    def _cron_send_bank_slip_to_invoice_followers(self):
        now = datetime.now(pytz.timezone("America/Sao_Paulo"))
        if now.weekday() < 5:
            account_move_ids = self.env["account.move"].search(
                [("notification_status", "=", "in_queue"), ("state", "=", "posted")],
                limit=500,
                order="id asc",
            )
            for account_move in account_move_ids:
                if not account_move.file_boleto_pdf_id:
                    account_move.generate_boleto_pdf()
                account_move.send_bank_slip_to_invoice_followers()
            account_move_ids.write({"notification_status": "sent"})
            api_user = self.env.ref("mut_financial_apis.api_user")
            env = self.env(user=api_user)
            callbacks = []
            for url_callback in set(account_move_ids.mapped("url_callback")):
                event_date = datetime.now(pytz.timezone("America/Sao_Paulo")).isoformat(
                    sep="T"
                )
                callbacks = [
                    format_callback(
                        event_date, invoice.installment_uid, "bank_slip_issued"
                    )
                    for invoice in account_move_ids.filtered(
                        lambda x: x.url_callback == url_callback
                    )
                ]
                send_callbacks(env, url_callback, callbacks)
