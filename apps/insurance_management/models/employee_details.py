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
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class EmployeeDetails(models.Model):
    """Essa classe cria um modelo "employee.details" (Consultor de Seguro) e adiciona campos """
    _name = 'employee.details'
    _description = "Detalhes do Consultor"

    name = fields.Char(string='Nome', required=True, help="Nome do Consultor")
    user_id = fields.Many2one('res.users', string='Related User', copy=False, help="Usuário Relacionado")
    sex = fields.Selection([('male', 'Homem'), ('female', 'Mulher'), ('others', 'Outros')], 
                           help="Selecione o sexo do Consultor")
    phone = fields.Char(string='Número de telefone', help="Número de telefone do Consultor", required=True)
    salary_type = fields.Selection([('fixed', 'Fixo'), ('commission', 'Percentual'), ('both', 'Ambos')],
                                   default='fixed', required=True, help="Selecione o tipo de Comissão")
    currency_id = fields.Many2one('res.currency', string='Moeda', required=True, 
                                  default=lambda self: self.env.user.company_id.currency_id.id, 
                                  help="Selecione a Moeda")
    base_salary = fields.Monetary(string='Valor Fixo', help="Fornecer o Valor Fixo por Venda do Consultor")
    last_salary_date = fields.Date(string='Último pagamento em', copy=False, help="Data da última comissão pago")
    insurance_ids = fields.One2many('insurance.details', 'employee_id', string='Carteira de Seguros', readonly=True,
                                    help="Carteira de seguros criados pelo consultor")
    note_field = fields.Html(string='Comentários', help="Faça anotações, se houver")
    invoice_id = fields.Many2one('account.move', string='Último pagamento', copy=False, readonly=True,
                                 help="Fatura do último pagamento")

    def action_salary_payment(self):
        """This function raises a user error if state is draft and
        user error when base salary is less
        and creates invoice with corresponding details given"""
        if self.invoice_id:
            if self.invoice_id.state == 'draft':
                raise UserError(_("Você deve validar o último pagamento feito para criar um novo pagamento"))
        amount = 0.0
        if self.salary_type == 'fixed':
            amount = self.base_salary
            if self.base_salary == 0.0:
                raise UserError(_("O valor fixo deve ser maior que zero"))
        elif self.salary_type == 'commission':
            for ins in self.insurance_ids:
                if self.last_salary_date:
                    if ins.start_date > self.last_salary_date:
                        amount += (ins.commission_rate * ins.amount) / 100
        else:
            for ins in self.insurance_ids:
                if self.last_salary_date:
                    if ins.start_date > self.last_salary_date:
                        amount += ((ins.commission_rate * ins.amount) / 100 + self.base_salary)
        invoice_date = self.env['account.move'].sudo().create({
            'move_type': 'in_invoice',
            'invoice_date': fields.Date.context_today(self),
            'partner_id': self.user_id.partner_id.id,
            'invoice_user_id': self.env.user.id,
            'invoice_origin': self.name,
            'invoice_line_ids': [(fields.Command.create({
                'name': 'Invoice For Salary Payment',
                'quantity': 1,
                'price_unit': amount,
                'account_id': 41,  #TODO: Criar uma maneira de selecionar as contas
            }))],
        })
        self.sudo().write({
            'invoice_id': invoice_date.id,
            'last_salary_date': fields.Date.context_today(self),
        })

    @api.constrains('phone')
    def check_phone(self):
        """ Make sure phone contains only 10 digits """
        for rec in self:
            if not re.match('^[0-9]{10}$', rec.phone):
                raise ValidationError(
                    _('O número de telefone deve conter exatamente 10 dígitos e somente números são permitidos'))
