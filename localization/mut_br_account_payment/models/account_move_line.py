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

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

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
