# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################
import re
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

ACCOUNT_SHORTCODE_REGEX = re.compile(r'^[0-9]+$')


class AccountAccount(models.Model):
    _inherit = 'account.account'

    flow_account_type = fields.Selection([('tax', 'Imposto'), ('income', 'Receita'), ('expense', 'Despesa')],
                                    string="Tipo de conta")
    shortcode = fields.Char(string="Código Curto", size=10, index=True)

    @api.constrains('shortcode')
    def _check_account_shortcode(self):
        for account in self:
            if not re.match(ACCOUNT_SHORTCODE_REGEX, account.shortcode):
                raise ValidationError(_("The account Shortcode can only contain numeric characters."))

    @api.constrains('company_id', 'shortcode')
    def _constrains_shortcode(self):
        # check for duplicates in each root company
        by_root_company = self.grouped(lambda record: record.company_id.root_id)
        for root_company, records in by_root_company.items():
            by_shortcode = records.grouped('shortcode')
            if len(by_shortcode) < len(records):
                # retrieve duplicates within self
                duplicates = next(recs for recs in by_shortcode.values() if len(recs) > 1)
            else:
                # search for duplicates of self in database
                duplicates = self.search([
                    ('company_id', 'child_of', root_company.id),
                    ('shortcode', 'in', list(by_shortcode)),
                    ('id', 'not in', records.ids),
                ])
            if duplicates:
                raise ValidationError(
                    _("The shortcode of the account must be unique per company!")
                    + "\n" + "\n".join(f"- {duplicate.shortcode} in {duplicate.company_id.name}" for duplicate in duplicates)
                )
