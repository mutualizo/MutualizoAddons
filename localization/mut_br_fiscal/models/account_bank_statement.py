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

from odoo import fields, models, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    def _default_name(self):
        journal_id = self.journal_id.id or self.env.context.get('default_journal_id',False)
        if bool(journal_id):
            journal = self.env['account.journal'].browse(journal_id)
            if self.__can_manual_create(journal):
                return journal.statement_sequence_id.next_by_id()

    name = fields.Char(string='Reference', compute=False, readonly=False, copy=False, default=_default_name)
    date = fields.Date(index=True, compute=False, default=fields.Datetime.now)
    journal_id = fields.Many2one(comodel_name='account.journal', compute=False, store=True,
                                 check_company=True)

    manual_create = fields.Boolean(compute='_compute_manual_create')

    def __can_manual_create(self, journal_id):
        if (journal_id.type == 'cash' and bool(journal_id.statement_sequence_id)) or (journal_id.type == 'bank' and \
                                         journal_id.bank_statements_source in ['manual', 'file_import'] and \
                                         bool(journal_id.statement_sequence_id)):
            return True
        else:
            return False
        
            
    def _compute_manual_create(self):
        for reg in self:
            reg.manual_create = self.__can_manual_create(reg.journal_id)
    
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            journal_id = val.get('journal_id',False) or self.env.context['default_journal_id']
            if bool(journal_id):
                journal = self.env['account.journal'].browse(journal_id)
                if self.__can_manual_create(journal):
                    if not bool(val.get('journal_id', False)):
                        val['journal_id'] = journal_id
                    if not bool(val.get('date', False)):
                        val['date'] = fields.Datetime.now()
                    if not bool(val.get('name',False)) and journal.statement_sequence_id:
                        val['name'] = journal.statement_sequence_id.next_by_id()
        return super().create(vals_list)
    
    def write(self, vals):
        if vals.get('date',None) != None and vals['date'] == False:
            del vals['date']
        for reg in self:
            journal_id = reg.journal_id or vals.get('journal_id',False)
            if bool(journal_id) and reg.__can_manual_create(journal_id):
                if not bool(reg.date):
                    vals['date'] = fields.Datetime.now()
                if not bool(reg.name) and journal_id.statement_sequence_id:
                    vals['name'] = journal_id.statement_sequence_id.next_by_id()
        return super().write(vals)
                                    
                       
                
    
    