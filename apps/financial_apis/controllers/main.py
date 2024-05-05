import re

from odoo import http
from odoo.http import request

from datetime import datetime
from erpbrasil.base import misc
from erpbrasil.base.fiscal import cnpj_cpf


class FinancialAPIsController(http.Controller):

    @http.route(
        "/invoice/load",
        type="json",
        auth="public",
    )
    def load_invoices(self, **kw):
        api_user = request.env.ref("financial_apis.api_user")
        data = request.jsonrequest
        if isinstance(data, dict):
            data = [data]

        for invoice in data:
            company_id = self.get_company_by_cnpj(invoice.get("cnpj_singular"))
            env = request.env(user=api_user)
            if not company_id:
                pass

            partner_id = self.get_invoice_partner(
                env, company_id.id, invoice.get("payer")
            )
            account_move_id = self.create_account_move(
                env=env,
                company_id=company_id.id,
                partner_id=partner_id.id,
                installment_data=invoice.get("installment"),
                url_callback=invoice.get("url_callback"),
                contact_list=invoice.get("contact_list"),
            )
        return

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
            ]
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
        self, env, company_id, partner_id, installment_data, url_callback, contact_list
    ):
        if installment_data.get("due_date"):
            installment_data["due_date"] = (
                datetime.strptime(installment_data.get("due_date"), "%Y-%m-%d") or False
            )
        default_product = env.ref("financial_apis.api_product_product")
        bradesco_id = request.env.ref("l10n_br_base.res_bank_237")
        payment_mode_id = (
            env["account.payment.mode"]
            .with_company(company_id)
            .search([("fixed_journal_id.bank_id", "=", bradesco_id.id)], limit=1)
        )
        partner_contact_list = self.get_invoice_followers(env, company_id, contact_list)
        partner_contact_list.append(partner_id)
        installment_data_to_create = {
            "company_id": company_id,
            "move_type": "out_invoice",
            "partner_id": partner_id,
            "url_callback": url_callback,
            "contract_number": installment_data.get("contract_number"),
            "total_installments": installment_data.get("total_installments"),
            "installment_uid": installment_data.get("external_id"),
            "installment_number": installment_data.get("number"),
            "invoice_date": installment_data.get("due_date"),
            "invoice_date_due": installment_data.get("due_date"),
            "payment_mode_id": payment_mode_id.id,
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "product_id": default_product.id,
                        "name": default_product.name,
                        "price_unit": installment_data.get("amount"),
                        "quantity": 1,
                        "tax_ids": [(6, 0, default_product.taxes_id.ids)],
                    },
                )
            ],
            "message_follower_ids": [
                (0, 0, {"res_model": "account.move", "partner_id": partner_id})
                for partner_id in partner_contact_list
            ],
            "additional_description_installment": installment_data.get(
                "additional_description_installment"
            ),
        }
        account_move_id = (
            env["account.move"]
            .with_company(company_id)
            .create(installment_data_to_create)
        )
        return account_move_id

    def get_invoice_followers(self, env, company_id, contact_list):
        # Get id list from partners to be notified
        partner_contact_list = []
        for contact in contact_list:
            partner_id = (
                env["res.partner"]
                .with_company(company_id)
                .search([("email", "=", contact.get("email"))])
            )
            if not partner_id:
                partner_id = (
                    env["res.partner"]
                    .with_company(company_id)
                    .create(
                        {"name": contact.get("name"), "email": contact.get("email")}
                    )
                )
            partner_contact_list.append(partner_id.id)
        return partner_contact_list
