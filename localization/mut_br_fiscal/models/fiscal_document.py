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


class BrAccountFiscalDocument(models.Model):
    _name = 'br_account.fiscal.document'
    _description = 'Tipo de Documento Fiscal'

    code = fields.Char('Codigo', size=8, required=True)
    name = fields.Char('Descrição', size=64)
    electronic = fields.Boolean('Eletrônico')
    nfse_eletronic = fields.Boolean('Emite NFS-e?')

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
