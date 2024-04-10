# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################


import logging

from odoo import fields, models, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class AccountMoveLineChangeDateMaturity(models.TransientModel):
    _name = 'account.move.line.change.date.maturity'
    _description = 'Histórico de Mudança na Data de Vencimento'
    
    user_id = fields.Many2one('res.users', 'Responsável', default=lambda self: self.env.user)
    can_do = fields.Boolean('Pode fazer?', default=True)
    date_maturity_new = fields.Date(string='Para', default=fields.date.today())
    narration = fields.Text('Motivo')
    state = fields.Selection([('draft', 'Aberto'), ('posted', 'Publicado')], string='Status', readonly=True, default='draft')
    move_line_ids = fields.Many2many('account.move.line', string='Duplicatas')

    #TODO: Verificar
    @api.onchange('move_ids')
    def on_change_move_id(self):
        for wizard in self:
            wizard.can_do = False
            for move_line_id in wizard.move_line_ids:
                if move_line_id.account_id.reconcile and not move_line_id.reconciled: 
                    wizard.can_do = True 
            
    def do_new_date_maturity(self):
        for wizard in self:
            if wizard.can_do:
                if len(wizard.narration) < 10:
                    raise UserError('A narrativa tem que ter mais de 10 caracteres')
                for move_line_id in wizard.move_line_ids:
                    if move_line_id.date_maturity == wizard.date_maturity_new:
                        raise UserError('A nova data tem que ser diferente da data atual')
                    var = {
                        'move_line_id': move_line_id.id,
                        'date_maturity_old': move_line_id.date_maturity,
                        'narration': wizard.narration,
                    }
                    move_line_id.write({'date_maturity': wizard.date_maturity_new})
                    self.env['account.move.line.list.change.maturity'].create(var)
                wizard.state = 'posted'
        return True
