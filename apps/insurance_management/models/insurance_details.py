# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import api, fields, models, _, Command
from odoo.exceptions import UserError, ValidationError


class InsuranceDetails(models.Model):
    """Essa classe cria um modelo "insurance.details" e adiciona campos """
    _name = 'insurance.details'
    _description = "Detalhes do seguro"

    name = fields.Char(string='Identificador', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'), help="Identificador de seguros criados")
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, 
                                 help="Parceiro relacionado a seguros")
    start_date = fields.Date(string='Data Inicio', default=fields.Date.context_today, required=True,
                             help="Data Inicial da Cobertura")
    close_date = fields.Date(string='Data Final', readonly=True, help="Data Final da Cobertura")
    invoice_ids = fields.One2many('account.move', 'insurance_id', string='Faturas', readonly=True,
                                  help="Faturas relacionadas ao seguro")
    employee_id = fields.Many2one('employee.details', string='Agente', required=True, 
                                  help="Agente relacionado ao seguro")
    commission_rate = fields.Float(string='Porcentagem de comissão', 
                                   help="Fornecer a taxa de comissão do seguro ao agente",)
    policy_id = fields.Many2one('policy.details', string='Apólice de seguro', required=True,
                                help="Select the policy details and the policy preferred")
    payment_type = fields.Selection([('fixed', 'A Vista'), ('installment', 'Parcelado')], required=True, 
                                    default='fixed', help="Selecione o tipo de pagamento da apólice")
    policy_duration = fields.Integer(string='Duração em meses', required=True,
                                     help="Especifique a duração da política para a qual essa política existe")
    currency_id = fields.Many2one('res.currency', string='Moeda', required=True, 
                                  default=lambda self: self.env.user.company_id.currency_id.id, 
                                  help="Informe a Moeda")
    amount = fields.Monetary(related='policy_id.amount', string='Total',
                             help="O valor da apólice com base na apólice selecionada")
    amount_installment = fields.Monetary(string="Valor da parcela", compute="_compute_amount", required=True,
                                         help="Informe o valor da parcela da apólice")
    amount_remaining = fields.Monetary(string='Valor restante', compute='_compute_amount_remaining')
    state = fields.Selection([('draft', 'rascunho'), ('confirmed', 'Confirmada'), ('closed', 'Encerrada')],
                             required=True, default='draft', help="Situação do seguro")
    hide_inv_button = fields.Boolean(copy=False)
    note_field = fields.Html(string='Comentários', help="Forneça as anotações")
    policy_number = fields.Integer(string="Número da apólice", required=True,
                                   help="O número da apólice é um número exclusivo que uma companhia "
                                        "de seguros usa para identificá-lo como segurado")

    @api.depends('amount', 'policy_duration')
    def _compute_amount(self):
        for record in self:
            if record.policy_duration != 0:
                record.amount_installment = (
                        record.amount / record.policy_duration)
            else:
                record.amount_installment = 0.0

    @api.depends('amount', 'amount_installment', 'invoice_ids.amount_total')
    def _compute_amount_remaining(self):
        for record in self:
            total_invoice_amount = sum(
                record.invoice_ids.mapped('amount_total'))
            total_amount = record.amount
            record.amount_remaining = total_amount - total_invoice_amount

    @api.constrains('commission_rate')
    def _check_commission_rate(self):
        """This function defines a constraint that ensures the '
        commission_rate' attribute of objects meets certain criteria.
        If any object violates the constraint by having a 'commission_rate'
         that falls outside the range of 1 to 100, a validation error
          is raised, """
        if self.filtered(
                lambda reward: (
                        reward.commission_rate < 0 or reward.commission_rate >
                        100)):
            raise ValidationError(
                _('A porcentagem da comissão deve estar entre 0.1-100.0'))

    @api.constrains('policy_number')
    def _check_policy_number(self):
        """This function checks if policy number is not added,validation error
        occurs"""
        if not self.policy_number:
            raise ValidationError(
                _('Adicione o número da apólice'))

    def action_confirm_insurance(self):
        """This function creates a validation error if amount not
         greater than zero"""
        if self.amount > 0:
            self.state = 'confirmed'
            self.hide_inv_button = True
        else:
            raise UserError(_("O valor deve ser maior que zero"))

    def action_create_invoice(self):
        """Function to create invoice with corresponding details"""
        if self.payment_type == 'fixed':
            self.hide_inv_button = False

        created_invoice = self.env['account.move'].sudo().create({
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.context_today(self),
            'partner_id': self.partner_id.id,
            'invoice_user_id': self.env.user.id,
            'invoice_origin': self.name,
            'invoice_line_ids': [(fields.Command.create({
                'name': 'Invoice For Insurance',
                'quantity': 1,
                'price_unit': self.amount if self.payment_type == 'fixed' else
                self.amount_installment,
                'account_id': 41, #TODO: Verificar esse código de conta
            }))],
        })
        self.write({'invoice_ids': [Command.link(created_invoice.id)]})

    def action_close_insurance(self):
        """Function on button to close the paid invoices or else raise
        user error"""
        for records in self.invoice_ids:
            if records.state == 'paid':
                raise UserError(_("Todas as faturas devem ser liquidadas"))
        self.state = 'closed'
        self.close_date = fields.Date.context_today(self)
        self.hide_inv_button = False

    @api.model
    def create(self, vals):
        """Function to create sequence"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'insurance.details') or 'New'
        return super(InsuranceDetails, self).create(vals)
