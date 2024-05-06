import re
import json
import logging
import requests

from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

from datetime import datetime
from erpbrasil.base import misc
from erpbrasil.base.fiscal import cnpj_cpf

from odoo.addons.l10n_br_base.tools import check_cnpj_cpf

from .error_messages import FinanceApiErrorMessages as api_errors

logger = logging.getLogger(__name__)


MAIL_REGEX = re.compile(
    r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
)


class FinancialAPIsController(http.Controller):

    @http.route(
        "/invoice/load",
        type="json",
        auth="public",
    )
    def load_invoices(self, **kw):
        start_time = datetime.now()
        api_user = request.env.ref("mut_financial_apis.api_user")
        data = request.jsonrequest
        if isinstance(data, dict):
            invoices = data.get("invoices_receivables", [])
        callbacks = []
        env = request.env(user=api_user)
        for invoice in invoices:
            installment_uid = invoice.get("installment", {}).get("external_id")
            validation_error = self.validate_invoice_data(env, invoice)
            if validation_error:
                callbacks.append(
                    self._format_callback(
                        installment_uid, "not_created", validation_error
                    )
                )
                continue

            company_id = self.get_company_by_cnpj(invoice.get("cnpj_singular"))
            if not company_id:
                callbacks.append(
                    self._format_callback(
                        installment_uid,
                        "not_created",
                        api_errors.COMPANY_NOT_FOUND,
                    )
                )
                continue

            bradesco_id = request.env.ref("l10n_br_base.res_bank_237")
            payment_mode_id = (
                env["account.payment.mode"]
                .with_company(company_id)
                .search([("fixed_journal_id.bank_id", "=", bradesco_id.id)], limit=1)
            )
            if not payment_mode_id:
                callbacks.append(
                    self._format_callback(
                        installment_uid,
                        "not_created",
                        api_errors.PAYMENT_MODE_NOT_FOUND,
                    )
                )
                continue

            partner_id = self.get_invoice_partner(
                env, company_id.id, invoice.get("payer")
            )
            self.create_account_move(
                env, company_id, payment_mode_id, partner_id, invoice
            )
            callbacks.append(
                self._format_callback(installment_uid, "created")
            )
        interval = (datetime.now() - start_time)
        logger.info(
            f"Invoice Load API Processing Time: {len(invoices)} "
            f"items in {interval.seconds}.{interval.microseconds} seconds")
        self.send_callbacks(data.get("url_callback"), callbacks)

    def _format_callback(self, external_id, status, error={}):
        return {
            "external_id_installment": external_id,
            "installment_state": status,
            "error": error,
        }

    def validate_invoice_data(self, env, invoice):
        """
        Check payer CNPJ/CPF and E-Mail
        """
        payer = invoice.get("payer")
        installment = invoice.get("installment", {})
        due_date = installment.get("due_date")
        external_id = installment.get("external_id")
        if not external_id:
            return api_errors.MISSING_EXTERNAL_ID
        try:
            check_cnpj_cpf(env, payer.get("cpf_cnpj") or "", env.ref("base.br"))
        except ValidationError:
            return api_errors.INVALID_CNPJ_CPF
        if not re.fullmatch(MAIL_REGEX, payer.get("email")):
            return api_errors.INVALID_EMAIL
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            return api_errors.INVALID_DUE_DATE
        try:
            if float(installment.get("amount")) <= 0:
                raise ValueError
        except ValueError:
            return api_errors.INVALID_INSTALLMENT_AMOUNT

    def get_company_by_cnpj(self, cnpj):
        # Search singular company by cnpj
        cnpj_numbers = re.sub("[^0-9]", "", cnpj)
        formatted_cnpj = cnpj_cpf.formata(str(cnpj))
        company_id = (
            request.env["res.company"]
            .sudo()
            .search(
                [
                    "|",
                    ("partner_id.cnpj_cpf", "=", cnpj_numbers),
                    ("partner_id.cnpj_cpf", "=", formatted_cnpj),
                ]
            )
        )
        return company_id

    def get_invoice_partner(self, env, company_id, partner_data):
        # Search partner by cnpn_cpf
        cnpj_cpf_numbers = re.sub("[^0-9]", "", partner_data.get("cpf_cnpj"))
        formatted_cnpj_cpf = cnpj_cpf.formata(str(partner_data.get("cpf_cnpj")))
        partner_id = env["res.partner"].search(
            [
                "|",
                ("cnpj_cpf", "=", cnpj_cpf_numbers),
                ("cnpj_cpf", "=", formatted_cnpj_cpf),
            ],
            limit=1,
        )
        # Create partner if not find one
        if not partner_id:
            partner_data_to_create = {
                "name": partner_data.get("name"),
                "legal_name": partner_data.get("legal_name")
                or partner_data.get("name"),
                "cnpj_cpf": formatted_cnpj_cpf,
                "email": partner_data.get("email"),
            }
            partner_data_to_create.update(
                self.get_partner_adress_data(env, partner_data)
            )
            partner_id = env["res.partner"].create(partner_data_to_create)
        return partner_id

    def get_partner_adress_data(self, env, partner_data):
        # Search Country
        country_name = (partner_data.get("country") or "").strip()
        if country_name == "Brasil":
            country_name = "Brazil"
        country_id = env["res.country"].search([("name", "=ilike", country_name)])
        # Search State
        state_code = (partner_data.get("state") or "").strip()
        state_id = env["res.country.state"].search(
            [("code", "=ilike", state_code), ("country_id", "=", country_id.id)]
        )
        # Search City
        city_name = (partner_data.get("city") or "").strip()
        city_id = env["res.city"].search(
            [
                ("name", "=ilike", city_name),
                ("state_id", "=", state_id.id),
                ("country_id", "=", country_id.id),
            ]
        )
        # Format ZIP
        zip_numbers = re.sub("[^0-9]", "", partner_data.get("zip_code"))
        formatted_zip_code = misc.format_zipcode(zip_numbers, country_id.code)
        # Format District
        formatted_district = (partner_data.get("district") or "").strip().title()
        # Return partner address data
        return {
            "zip": formatted_zip_code,
            "street_name": partner_data.get("address"),
            "street_number": partner_data.get("number"),
            "street2": partner_data.get("complement"),
            "district": formatted_district,
            "city_id": city_id.id,
            "state_id": state_id.id,
            "country_id": country_id.id,
        }

    def create_account_move(
        self, env, company_id, payment_mode_id, partner_id, invoice
    ):
        installment = invoice.get("installment")
        url_callback = invoice.get("url_callback")
        contact_list = invoice.get("contact_list")
        installment["due_date"] = datetime.strptime(installment["due_date"], "%Y-%m-%d")

        default_product = env.ref("mut_financial_apis.api_product_product")

        partner_contact_list = self.get_invoice_followers(env, company_id, contact_list)
        partner_contact_list.append(partner_id)

        invoice_values = {
            "company_id": company_id.id,
            "move_type": "out_invoice",
            "partner_id": partner_id.id,
            "url_callback": url_callback,
            "contract_number": installment.get("contract_number"),
            "total_installments": installment.get("total_installments"),
            "installment_uid": installment.get("external_id"),
            "installment_number": installment.get("number"),
            "invoice_date": installment.get("due_date"),
            "invoice_date_due": installment.get("due_date"),
            "payment_mode_id": payment_mode_id.id,
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "product_id": default_product.id,
                        "name": default_product.name,
                        "price_unit": float(installment.get("amount")),
                        "quantity": 1,
                        "tax_ids": [(6, 0, default_product.taxes_id.ids)],
                    },
                )
            ],
            "message_follower_ids": [
                (0, 0, {"res_model": "account.move", "partner_id": partner_id})
                for partner_id in partner_contact_list
            ],
            "additional_description_installment": installment.get(
                "additional_description_installment"
            ),
        }
        # Check if this installment was already processed by Odoo
        account_move_id = (
            env["account.move"]
            .with_company(company_id.id)
            .search([("installment_uid", "=", installment.get("external_id"))])
        )
        if not account_move_id:
            account_move_id = (
                env["account.move"].with_company(company_id.id).create(invoice_values)
            )
        else:
            # TODO We can edit the existing move here if the state is draft
            pass
        return account_move_id

    def get_invoice_followers(self, env, company_id, contact_list):
        # Get id list from partners to be notified
        partner_contact_list = []
        for contact in contact_list:
            partner_id = (
                env["res.partner"]
                .with_company(company_id.id)
                .search([("email", "=", contact.get("email"))])
            )
            if not partner_id:
                partner_id = (
                    env["res.partner"]
                    .with_company(company_id.id)
                    .create(
                        {"name": contact.get("name"), "email": contact.get("email")}
                    )
                )
            partner_contact_list.append(partner_id.id)
        return partner_contact_list

    def send_callbacks(self, url, callbacks):
        header = {"Content-Type": "application/json"}
        callback_url = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("financial_apis.nifi_callback_url")
        )
        if not callback_url:
            # TODO Send an error message
            return
        res = requests.request(
            "POST",
            callback_url,
            headers=header,
            data=json.dumps({"url_callback": url, "items": callbacks}),
        )
        if not res.ok:
            # TODO raise??
            pass
