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


class BrAccountServiceType(models.Model):
    _name = 'br_account.service.type'
    _description = 'Cadastro de Operações Fiscais de Serviço'

    code = fields.Char('Código', size=16, required=True)
    name = fields.Char('Descrição', size=256, required=True)
    parent_id = fields.Many2one('br_account.service.type', 'Tipo de Serviço Pai')
    child_ids = fields.One2many('br_account.service.type', 'parent_id', 'Tipo de Serviço Filhos')
    internal_type = fields.Selection([('view', 'Visualização'), ('normal', 'Normal')], 'Tipo Interno', required=True, default='normal')
    federal_nacional = fields.Float('Imposto Fed. Sobre Serviço Nacional',company_dependent=True)
    federal_importado = fields.Float('Imposto Fed. Sobre Serviço Importado',company_dependent=True)
    estadual_imposto = fields.Float('Imposto Estadual',company_dependent=True)
    municipal_imposto = fields.Float('Imposto Municipal',company_dependent=True)
    fonte_dados = fields.Char('Fonte',company_dependent=True)

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
