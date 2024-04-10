from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    sacador_id = fields.Many2one('res.partner', string='Sacador/Avalista')
    
    due_amount_rec = fields.Float(string="Total Receber", help="Valor Total a Receber", compute='_compute_due_amount_rec')
    due_amount_pay = fields.Float(string="Total Pagar", help="Valor Total a Pagar", compute='_compute_due_amount_pay')

    def action_view_due_statements_rec(self):
        """Function for showing the all invoices that not paid completely"""
        due_invoices = self.env['account.move'].search([('partner_id', '=', self.id), ('payment_state', '!=', 'paid'),
                                                        ('move_type', '=', 'out_invoice')]).line_ids.mapped('id')
        return {
            'res_model': 'account.move.line',
            'type': 'ir.actions.act_window',
            'name': 'Due Statements',
            'view_mode': 'tree,form',
            'views':
                [(self.env.ref('mut_br_account_payment.view_pay_and_rec_list').id,'list'),
                 (self.env.ref('account.view_move_line_form').id, 'form')],
            'context': {'create': False, 'edit': False, 'search_default_group_by_invoices': True},
            'domain': [('id', 'in', due_invoices),('account_type', '=', 'asset_receivable'), ('credit', '=', 0)],
        }

    def action_view_due_statements_pay(self):
        """Function for showing the all invoices that not paid completely"""
        due_invoices = self.env['account.move'].search([('partner_id', '=', self.id), ('payment_state', '!=', 'paid'),
                                                        ('move_type', '=', 'in_invoice')]).line_ids.mapped('id')
        return {
            'res_model': 'account.move.line',
            'type': 'ir.actions.act_window',
            'name': 'Due Statements',
            'view_mode': 'tree,form',
            'views':
                [(self.env.ref('mut_br_account_payment.view_pay_and_rec_list').id,'list'),
                 (self.env.ref('account.view_move_line_form').id, 'form')],
            'context': {'create': False, 'edit': False, 'search_default_group_by_invoices': True},
            'domain': [('id', 'in', due_invoices),('account_type', '=', 'liability_payable'), ('debit', '=', 0)],
        }

    def _compute_due_amount_rec(self):
        """Function for computing the total payment due of the customer"""
        self.due_amount_rec = sum(self.env['account.move'].search(
            [('partner_id', '=', self.id), ('payment_state', '!=', 'paid'),
             ('move_type', '=', 'out_invoice')]).mapped('amount_residual'))

    def _compute_due_amount_pay(self):
        """Function for computing the total payment due of the customer"""
        self.due_amount_pay = sum(self.env['account.move'].search(
            [('partner_id', '=', self.id), ('payment_state', '!=', 'paid'),
             ('move_type', '=', 'in_invoice')]).mapped('amount_residual'))
