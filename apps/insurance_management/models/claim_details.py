# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import api, fields, models, _


class ClaimDetails(models.Model):
    """Essa classe cria um modelo "claim.details" (Pedidos de Indenização) e adiciona campos """
    _name = 'claim.details'
    _description = "Detalhes do Pedido de Indenização de Seguro"

    name = fields.Char(string='Identificador', copy=False, readonly=True, index=True, default=lambda self: _('New'), 
                       help="Sequência dos pormenores relativos a pedidos de indenização de seguros")
    insurance_id = fields.Many2one('insurance.details', required=True, domain=[('state', '=', 'confirmed')],
                                   string="Seguro", help="Os pedidos confirmados podem ser selecionados")
    partner_id = fields.Many2one(related='insurance_id.partner_id', string='Reclamante', 
                                 help="Reclamante indicado no seguro")
    policy_id = fields.Many2one(related='insurance_id.policy_id', string='Apólice de seguro',
                                help="Apólice de seguro relacionada a seguros")
    employee_id = fields.Many2one(related='insurance_id.employee_id', string='Agente',
                                  help="Funcionário relacionado a seguro")
    currency_id = fields.Many2one('res.currency', string='Moeda', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id, help="Moeda Default")
    amount = fields.Monetary(related='insurance_id.amount', string='Total', help="Valor relacionado ao seguro")
    date_claimed = fields.Date(string='Data Aplicada', default=fields.Date.context_today, 
                               help="Data de aplicação dos detalhes do pedido de seguro")
    invoice_id = fields.Many2one('account.move', string='Invoiced', readonly=True, copy=False,
                                 help="Fatura relacionada ao sinistro")
    note_field = fields.Html(string='Comentários', help="Notas relacionadas")

    @api.model
    def create(self, vals):
        """Function to create sequence"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'claim.details') or 'New'
        return super(ClaimDetails, self).create(vals)

    def action_create_bill(self):
        """Function to create bill with corresponding details"""
        if not self.invoice_id:
            invoice_val = self.env['account.move'].sudo().create({
                'move_type': 'in_invoice',
                'invoice_date': fields.Date.context_today(self),
                'partner_id': self.partner_id.id,
                'invoice_user_id': self.env.user.id,
                'claim_id': self.id,
                'invoice_origin': self.name,
                'invoice_line_ids': [(fields.Command.create({
                    'name': 'Invoice For Insurance Claim',
                    'quantity': 1,
                    'price_unit': self.amount,
                    'account_id': 41,
                }))],
            })
            self.invoice_id = invoice_val
