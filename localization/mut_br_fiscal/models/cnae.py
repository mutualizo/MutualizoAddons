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


class BrAccountCNAE(models.Model):
    _name = 'br_account.cnae'
    _description = 'Cadastro de CNAE'

    code = fields.Char('Código', size=16, required=True)
    name = fields.Char('Descrição', size=64, required=True)
    version = fields.Char('Versão', size=16, required=True)
    parent_id = fields.Many2one('br_account.cnae', 'CNAE Pai')
    child_ids = fields.One2many('br_account.cnae', 'parent_id', 'CNAEs Filhos')
    internal_type = fields.Selection([('view', 'Visualização'), 
                                      ('normal', 'Normal')],
                                      'Tipo Interno', required=True, default='normal')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('code', operator, name)] + args, limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = "%s - %s" % (rec.code, rec.name or '')
