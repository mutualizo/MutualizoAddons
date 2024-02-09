# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import fields, models, tools, api, _
from odoo.addons.base.models.res_bank import sanitize_account_number
from odoo.exceptions import UserError, RedirectWarning


class AccountJournal(models.Model):
    _inherit = "account.journal"

    statement_sequence_id = fields.Many2one('ir.sequence', 'Statement Sequence',
        copy=False, check_company=True)
    
    def _create_statement_seq(self, code: str, name: str):
        vals = {
            'active': True,
            'code': self._name,
            'company_id': self.company_id.id,
            'implementation': 'standard',
            'name': name,
            'number_increment': 1,
            'padding': 5,
            'prefix': f"{code}/ST/%(day)s/%(month)s/%(year)s/"
        }
        return self.env['ir.sequence'].sudo().create(vals).id

    @api.model_create_multi
    def create(self, vals_list):
        regs = super().create(vals_list)
        for reg in regs:
            if bool(reg.statement_sequence_id) == False:
                if reg.type == 'cash' or (reg.type == 'bank' and reg.bank_statements_source == 'manual'):
                    reg.write({'statement_sequence_id': reg._create_statement_seq(reg.code,reg.name)})
        return regs
    
    def write(self, vals):
        for reg in self:
            if bool(reg.statement_sequence_id) == False and vals.get('statement_sequence_id',None) == None:
                if reg.type == 'cash' or (reg.type == 'bank' and reg.bank_statements_source == 'manual'):
                    reg.write({'statement_sequence_id': reg._create_statement_seq(reg.code,reg.name)})
        return super().write(vals)
        
    def __get_bank_statements_available_sources(self):
        rslt = super(AccountJournal, self).__get_bank_statements_available_sources()
        rslt += [('manual', _('Só Manual'))]
        return rslt

