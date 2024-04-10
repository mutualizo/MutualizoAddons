# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import fields, models, api

class AccountMoveLineListChangeMaturity(models.Model):
    _name = "account.move.line.list.change.maturity"
    _description = 'Lista de Histórico de Alterações das Datas de Vencimento'

    move_line_id = fields.Many2one('account.move.line', string="Movimento Contábil", index=True)
    user_id = fields.Many2one('res.users', 'Responsável', default=lambda self: self.env.user)
    date_maturity_old = fields.Date(string='De', default=fields.date.today())
    date_maturity_new = fields.Date(string='Para', default=fields.date.today())
    narration = fields.Text('Motivo')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    change_maturity_ids = fields.One2many(string="Others State Tax Number", 
                                          comodel_name="account.move.line.list.change.maturity",
                                          inverse_name="move_line_id")

    def action_change_date_maturity(self):
        """ Open a wizard for changing date of maturity."""
        return {
            'name': "Change Date Maturity",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move.line.change.date.maturity',
            'view_id': self.env.ref('mut_br_account_payment.view_account_move_line_change_date_maturity_form').id,
            'target': 'new',
            'context': {'default_move_line_ids': self.env.context.get('active_ids')},
        }

    def action_register_payment(self):
        """ Open the account.payment.register wizard to pay the selected
         journal entries.
        :return: An action opening the account.payment.register wizard.
        """
        return {
            'name': 'Registrar Pagamento',
            'res_model': 'account.payment.register',
            'view_mode': 'form',
            'context': {
                'active_model': 'account.move.line',
                'active_ids': self.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
