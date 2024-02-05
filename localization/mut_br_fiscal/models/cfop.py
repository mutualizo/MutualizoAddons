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


class BrAccountCFOP(models.Model):
    _name = 'br_account.cfop'
    _description = 'CFOP - Código Fiscal de Operações e Prestações'
    _order = 'code asc'

    code = fields.Char('Código', size=4, required=True)
    name = fields.Char('Nome', size=256, required=True)
    small_name = fields.Char('Nome Reduzido', size=32, required=True)
    description = fields.Text('Descrição')
    type = fields.Selection([('input', 'Entrada'),
                             ('output', 'Saída')],
                            'Tipo', required=True)
    parent_id = fields.Many2one('br_account.cfop', 'CFOP Pai')
    child_ids = fields.One2many('br_account.cfop', 'parent_id', 'CFOP Filhos')
    internal_type = fields.Selection([('view', 'Visualização'), 
                                      ('normal', 'Normal')],
                                      'Tipo Interno', required=True, default='normal')

    _sql_constraints = [
        ('br_account_cfop_code_uniq', 'unique (code)', 'Já existe um CFOP com esse código !')
    ]

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
