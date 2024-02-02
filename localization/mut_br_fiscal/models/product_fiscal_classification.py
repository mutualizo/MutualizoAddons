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
from odoo.exceptions import UserError, ValidationError
from ..tools.cst import CST_IPI

class ProductFiscalClassification(models.Model):
    _name = 'product.fiscal.classification'
    _description = 'Classificações Fiscais (NCM)'

    code = fields.Char(string="Código", size=14)
    category = fields.Char(string="Categoria", size=14)
    name = fields.Char(string="Nome", size=300)
    company_id = fields.Many2one('res.company', string="Empresa")
    unidade_tributacao = fields.Char(string="Unidade Tributável", size=4)
    descricao_unidade = fields.Char(string="Descrição Unidade", size=20)
    cest = fields.Char(string="CEST", size=10,help="Código Especificador da Substituição Tributária")
    federal_nacional = fields.Float('Imposto Fed. Sobre Produto Nacional',company_dependent=True)
    federal_importado = fields.Float('Imposto Fed. Sobre Produto Importado',company_dependent=True)
    estadual_imposto = fields.Float('Imposto Estadual',company_dependent=True)
    municipal_imposto = fields.Float('Imposto Municipal',company_dependent=True)
    fonte_dados = fields.Char('Fonte',company_dependent=True)

    # IPI
    classe_enquadramento = fields.Char(string="Classe Enquadr.", size=5)
    codigo_enquadramento = fields.Char(string="Cód. Enquadramento", size=3, default='999')
    tax_ipi_id = fields.Many2one('account.tax', string="Alíquota IPI", domain=[('domain', '=', 'ipi')])
    ipi_tipo = fields.Selection( [('percent', 'Percentual')], 'Tipo do IPI', required=True, default='percent')
    ipi_reducao_bc = fields.Float('% Redução Base', required=True, digits=(12,6),default=0.00)
    ipi_cst = fields.Selection(CST_IPI, string='CST IPI')

    # ICMS ST
    tax_icms_st_id = fields.Many2one('account.tax', string="Alíquota ICMS ST", domain=[('domain', '=', 'icmsst')])
    icms_st_aliquota_reducao_base = fields.Float('% Red. Base ST',digits='Discount')
    icms_st_aliquota_mva = fields.Float('MVA Ajustado ST',digits='Discount', default=0.00)

    active = fields.Boolean(default=True, string='Ativo')

    @api.constrains('cest')
    def _check_cest(self):
        for fiscal in self:
            if bool(fiscal.cest):
                if not bool(str(fiscal.cest).isnumeric()) or len(fiscal.cest) != 7:
                    raise ValidationError(_('Invalid CEST Number!'))
        return True

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
