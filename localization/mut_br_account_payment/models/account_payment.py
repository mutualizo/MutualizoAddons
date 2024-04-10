# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from datetime import datetime
from odoo import fields, models, api
from odoo.tools import float_is_zero, float_compare, float_round
from dns.rdataclass import NONE


class AccountPayment(models.Model):
    _inherit = "account.payment"

    discount = fields.Monetary(string='Desconto', default=0.0, currency_field='currency_id')
    interest = fields.Monetary(string='Juros', default=0.0, currency_field='currency_id')
    fee = fields.Monetary(string='Multa', default=0.0, currency_field='currency_id')

    pay_sub = fields.Monetary(compute="_pay_amount", string='Valor Pago', currency_field='currency_id', readonly=True, store=True)
    pay_amount = fields.Monetary(compute="_pay_amount", string='Total Pago', currency_field='currency_id', readonly=True, store=True)

    @api.depends('fee', 'interest', 'amount', 'discount')
    def _pay_amount(self):
        self.pay_sub = (self.amount + self.discount)
        self.pay_amount = self.amount + self.fee + self.interest


class AccountRegisterPayments(models.TransientModel):
    """Inherits the account.payment.register model to add the new
     fields and functions"""
    _inherit = "account.payment.register"

    amount = fields.Monetary(currency_field='currency_id', store=True, readonly=True, compute='_compute_amount')
    vl_principal = fields.Monetary(string='Principal', compute='_compute_amount', store=True, readonly=False, currency_field='currency_id')
    
    vl_discount = fields.Monetary(string='Desconto', default=0.0, currency_field='currency_id')
    vl_interest = fields.Monetary(string='Juros', default=0.0, currency_field='currency_id', store=True, readonly=False)
    vl_fee = fields.Monetary(string='Multa', default=0.0, currency_field='currency_id', store=True, readonly=False)

    pr_discount = fields.Float(string='Desconto %', digits=(16, 4), default=0.0, store=True, readonly=False)
    pr_interest = fields.Float(string='Juros %', digits=(16, 4), default=0.0, store=True, readonly=False)
    pr_fee      = fields.Float(string='Multa %', digits=(16, 4), default=0.0, store=True, readonly=False)

    pay_sub = fields.Monetary(compute="_pay_amount", string='Vl. Titulo', currency_field='currency_id', readonly=True, store=True)
    pay_amount = fields.Monetary(compute="_pay_amount", string='Vl. Pago', currency_field='currency_id', readonly=True, store=True)
    
    def _get_total_amount_using_same_currency(self, batch_result, early_payment_discount=True):
        self.ensure_one()
        amount = 0.0
        fee = 0.0
        interest = 0.0
        mode = False
        moves = batch_result['lines'].mapped('move_id')
        for move in moves:
            if early_payment_discount and move._is_eligible_for_early_payment_discount(move.currency_id, self.payment_date):
                discount = move.invoice_payment_term_id._get_amount_due_after_discount(move.amount_total, move.amount_tax)#todo currencies
                amount + discount
                mode = 'early_payment'
            else:
                for aml in batch_result['lines'].filtered(lambda l: l.move_id.id == move.id):
                    amount += aml.amount_residual_currency
                    # d1 = datetime.strptime(aml.date_maturity, "%Y-%m-%d")
                    # d2 = datetime.strptime(self.payment_date, "%Y-%m-%d")
                    late_payment = (self.payment_date - aml.date_maturity).days
                    if late_payment > 0:
                        fee += amount * (self.company_id.l10n_br_mut_multa_tx/100)
                        interest += amount * (((self.company_id.l10n_br_mut_juros_mes_tx/30) * late_payment) / 100)
        return abs(amount), abs(interest), abs(fee), mode
    
    
    @api.depends('can_edit_wizard', 'payment_date', 'currency_id', 'amount')
    def _compute_early_payment_discount_mode(self):
        for wizard in self:
            if not wizard.journal_id or not wizard.currency_id or not wizard.payment_date:
                wizard.early_payment_discount_mode = wizard.early_payment_discount_mode
            elif wizard.can_edit_wizard:
                batch_result = wizard._get_batches()[0]
                total_amount_residual_in_wizard_currency, interest, fee, mode = wizard._get_total_amount_in_wizard_currency_to_full_reconcile(batch_result)
                wizard.early_payment_discount_mode = \
                    wizard.currency_id.compare_amounts(wizard.amount, total_amount_residual_in_wizard_currency) == 0 \
                    and mode == 'early_payment'
            else:
                wizard.early_payment_discount_mode = False

    @api.depends('vl_principal', 'pr_discount', 'vl_discount', 'pr_interest', 'vl_interest', 'pr_fee', 'vl_fee')
    def _pay_amount(self):
        for wizard in self:
            wizard.pay_sub = (wizard.vl_principal + wizard.vl_discount)
            wizard.pay_amount = wizard.pay_sub + wizard.vl_fee + wizard.vl_interest
 
    @api.depends('can_edit_wizard', 'source_amount', 'source_amount_currency', 'source_currency_id', 'company_id',
                  'currency_id', 'payment_date')
    def _compute_amount(self):
        for wizard in self:
            if not wizard.journal_id or not wizard.currency_id or not wizard.payment_date:
                wizard.amount = wizard.amount
            elif wizard.source_currency_id and wizard.can_edit_wizard:
                batch_result = wizard._get_batches()[0]
                wizard.amount, wizard.vl_interest, wizard.vl_fee = wizard._get_total_amount_in_wizard_currency_to_full_reconcile(batch_result)[0:3]
                # wizard.amount = wizard._get_total_amount_in_wizard_currency_to_full_reconcile(batch_result)[0]
            else:
                # The wizard is not editable so no partial payment allowed and then, 'amount' is not used.
                wizard.amount = 0.0
                wizard.vl_interest = 0.0
                wizard.vl_fee = 0.0
            wizard.vl_principal = wizard.amount - wizard.vl_discount
            wizard.pr_interest = float_round((wizard.vl_interest / wizard.vl_principal) * 100, precision_digits=4)
            
                    
    @api.onchange("vl_principal")
    def _set_principal_vl(self):
        if self.env.context.get("disable_autocal_discount"):
            return
        for wizard in self.with_context({'disable_autocal_discount': True}):
            if wizard.amount > 0.0:
                vl_discount = wizard.amount - wizard.vl_principal
            if float_compare(wizard.vl_discount, vl_discount, 2):
                wizard.vl_discount = vl_discount

########################################################################

    @api.onchange('pr_discount','vl_principal')
    def _set_discount_vl(self):
        if self.env.context.get("disable_autocal_discount"):
            return
        for wizard in self.with_context({'disable_autocal_discount': True}):
            vl_discount = float_round((wizard.amount * (wizard.pr_discount / 100)), 2)
            if float_compare(vl_discount, wizard.vl_discount, 2):
                wizard.vl_discount = vl_discount

    @api.onchange('vl_discount')
    def _set_discount_pr(self):
        if self.env.context.get("disable_autocal_discount"):
            return
        for wizard in self.with_context({'disable_autocal_discount': True}):
            wizard.vl_principal = wizard.amount - wizard.vl_discount
            if wizard.amount > 0.0:
                pr_discount = float_round((wizard.vl_discount / wizard.amount) * 100, precision_digits=4)
            else:
                pr_discount = 0.0
            if float_compare(pr_discount, wizard.pr_discount, 4):
                wizard.pr_discount = pr_discount

########################################################################

    @api.onchange('vl_interest','vl_principal')
    def _set_interest_vl(self):
        if self.env.context.get("disable_autocal_interest"):
            return
        for wizard in self.with_context({'disable_autocal_interest': True}):
            if wizard.amount > 0.0:
                pr_interest = float_round((wizard.vl_interest / wizard.vl_principal) * 100, precision_digits=4)
            else:
                pr_interest = 0.0
            if float_compare(pr_interest, wizard.pr_interest, 4):
                wizard.pr_interest = pr_interest

    @api.onchange('pr_interest')
    def _get_interest_vl(self):
        if self.env.context.get("disable_autocal_interest"):
            return
        for wizard in self.with_context({'disable_autocal_interest': True}):
            vl_interest = (wizard.vl_principal * (wizard.pr_interest / 100))
            if float_compare(vl_interest, wizard.vl_interest, 2):
                wizard.vl_interest = vl_interest 

########################################################################

    @api.onchange('vl_fee','vl_principal')
    def _set_fee_vl(self):
        if self.env.context.get("disable_autocal_fee"):
            return
        for wizard in self.with_context({'disable_autocal_fee': True}):
            if wizard.amount > 0.0:
                pr_fee = float_round((wizard.vl_fee / wizard.vl_principal) * 100, precision_digits=4)
            else:
                pr_fee = 0.0
            if float_compare(pr_fee, wizard.pr_fee, 4):
                wizard.pr_fee = pr_fee

    @api.onchange('pr_fee')
    def _get_fee_vl(self):
        if self.env.context.get("disable_autocal_fee"):
            return
        for wizard in self.with_context({'disable_autocal_fee': True}):
            vl_fee = (wizard.vl_principal * (wizard.pr_fee / 100))
            if float_compare(vl_fee, wizard.vl_fee, 2):
                wizard.vl_fee = vl_fee 

