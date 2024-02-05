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
from ..tools.cst import ORIGEM_PROD


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    expense_is = fields.Boolean(string='Despesa')
    
    fiscal_type = fields.Selection([('service', 'Serviço'), ('product', 'Produto')], 'Tipo Fiscal', 
                                   required=True, default='product')
    origin = fields.Selection(ORIGEM_PROD, 'Origem', default='0',company_dependent=True)
    fiscal_classification_id = fields.Many2one('product.fiscal.classification', 
                                               string="Classificação Fiscal (NCM)")
    service_type_id = fields.Many2one('br_account.service.type', 'Tipo de Serviço')
    cest = fields.Char(string="CEST", size=10, help="Código Especificador da Substituição Tributária")
    fiscal_observation_ids = fields.Many2many('br_account.fiscal.observation', 
                                              string="Mensagens Doc. Eletrônico")
    fiscal_category_id = fields.Many2one('br_account.fiscal.category', string='Categoria Fiscal', 
                                         company_dependent=True)
    description_fiscal = fields.Text('Fiscal Description', translate=True, 
                                     help="Descrição do produto a ser inserido nas Faturas. ")
    uom_imposto_id = fields.Many2one('product.uom', 'Medida de Imposto', 
                                     help="Default Unit of Measure used for all stock operation.")
    uom_fator_imposto = fields.Float('Fator de Imposto', digits='Product Unit of Measure',
                                     help="Fator de conversão da unidade de medida do imposto.")
    weight_gross = fields.Float('Gross Weight', digits='Stock Weight', store=True, 
                                help="The weight of the contents in Kg, including any packaging, etc.")
    icms_benef = fields.Many2one('br_account.beneficio.fiscal', string="Benificio Fiscal")

    @api.constrains('cest')
    def _check_cest(self):
        for fiscal in self:
            if bool(fiscal.cest):
                if not bool(str(fiscal.cest).isnumeric()) or len(fiscal.cest) != 7:
                    raise ValidationError(_('Invalid CEST Number!'))
        return True

    @api.onchange('expense_is')
    def _onchange_expense_is(self):
        if self.expense_is:
            self.type = 'service'

    @api.onchange('type')
    def onchange_product_type(self):
        if self.type !='consu' and self.fiscal_type != self.type:
            self.fiscal_type = 'service' if self.type == 'service' else 'product'
        if self.type =='consu' and self.fiscal_type != 'product':
            self.fiscal_type = 'product'
 
    @api.onchange('fiscal_type')
    def onchange_product_fiscal_type(self):
        if self.fiscal_type != self.type:
            self.type = 'service' if self.fiscal_type == 'service' else 'consu'

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.constrains('cest')
    def _check_cest(self):
        for fiscal in self:
            if bool(fiscal.cest):
                if not bool(str(fiscal.cest).isnumeric()) or len(fiscal.cest) != 7:
                    raise ValidationError(_('Invalid CEST Number!'))
        return True
