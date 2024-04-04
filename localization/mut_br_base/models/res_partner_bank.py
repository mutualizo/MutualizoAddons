# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import models, fields, api, _
from odoo.addons.base.models.res_bank import sanitize_account_number
from odoo.exceptions import UserError

BANK_ACCOUNT_TYPE = [
    ("01", _("Conta corrente individual")),
    ("02", _("Conta poupança individual")),
    ("03", _("Conta depósito judicial/Depósito em consignação individual")),
    ("11", _("Conta corrente conjunta")),
    ("12", _("Conta poupança conjunta")),
    ("13", _("Conta depósito judicial/Depósito em consignação conjunta")),
]

TRANSACTIONAL_ACCOUNT_TYPE = [
    ("checking", _("Checking Account (Conta Corrente)")),
    ("saving", _("Saving Account (Conta Poupança)")),
    ("payment", _("Prepaid Payment Account (Conta Pagamento)")),
]



class ResPartnerBank(models.Model):
    """ Adiciona campos necessários para o cadastramentos de contas
    bancárias no Brasil."""
    _inherit = 'res.partner.bank'

    acc_number = fields.Char('Account Number', size=64, required=False)
    acc_number_dig = fields.Char('Account Number Digit', size=8)
    bra_number = fields.Char('Agency', size=8)
    bra_number_dig = fields.Char('Account Agency Digit', size=8)

    bank_account_type = fields.Selection(selection=BANK_ACCOUNT_TYPE, default="01")

    transactional_acc_type = fields.Selection(selection=TRANSACTIONAL_ACCOUNT_TYPE, string="Account Type",
                                              help="""Type of transactional account, classification used in 
                                              the Brazilian instant payment system (PIX)""")

    partner_pix_ids = fields.One2many(comodel_name="res.partner.pix", inverse_name="partner_bank_id", 
                                      string="Pix Keys")

    bra_bank_bic = fields.Char(string="BIC/Swift Final Code.", size=3, help="Last part of BIC/Swift Code.")

    company_country_id = fields.Many2one(comodel_name="res.country", string="Company Country", 
                                         related="company_id.country_id")

    @api.depends('acc_number', 'acc_number_dig', 'bra_number', 'bra_number_dig', 'bank_id')
    def _compute_display_name(self):
        for acc in self:
            acc.display_name = "cc: %s-%s - %s - %s" % (acc.acc_number,
                                                         acc.acc_number_dig or '',
                                                         acc.partner_id.name or '',
                                                         acc.bank_id.name or '')

    @api.depends('bank_id', 'acc_number', 'acc_number_dig', 'bra_number', 'bra_number_dig')
    def _compute_sanitized_acc_number(self):
        for acc in self:
            if acc.bank_id:
                acc_number_format = acc.bank_id.acc_number_format or '%(acc_number)s'
                args = {
                    'bra_number': acc.bra_number or '',
                    'bra_number_dig': acc.bra_number_dig or '',
                    'acc_number': acc.acc_number or '',
                    'acc_number_dig': acc.acc_number_dig or ''
                }
                self.sanitized_acc_number = sanitize_account_number(acc_number_format % args)
            else:
                self.sanitized_acc_number = sanitize_account_number(acc.acc_number)

    @api.constrains("bra_number")
    def _check_bra_number(self):
        for b in self:
            if b.bank_id.code_bc:
                if len(b.bra_number) > 4:
                    raise UserError(_("Bank branch code must be four caracteres."))

    @api.constrains(
        "transactional_acc_type",
        "bank_id",
        "acc_number",
        "bra_number",
        "acc_number_dig",
    )
    def _check_transc_acc_type(self):
        for rec in self:
            if rec.transactional_acc_type:
                if not rec.bank_id or not rec.bank_id.code_bc or not rec.acc_number:
                    raise UserError(
                        _(
                            "a transactional account must contain the bank "
                            "information (code_bc) and the account number"
                        )
                    )
            if rec.transactional_acc_type in ["checking", "saving"]:
                if not rec.bra_number or not rec.acc_number_dig:
                    raise UserError(
                        _(
                            "A Checking Account or Saving Account transactional account "
                            "must contain the branch number and the account verification "
                            "digit."
                        )
                    )
