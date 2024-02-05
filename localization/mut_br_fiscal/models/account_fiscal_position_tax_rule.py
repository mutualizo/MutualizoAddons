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
from ..tools.cst import CST_ICMS
from ..tools.cst import CSOSN_SIMPLES
from ..tools.cst import CST_IPI
from ..tools.cst import CST_PIS_COFINS
from ..tools.cst import ORIGEM_PROD


class AccountFiscalPositionTaxRule(models.Model):
    _name = 'account.fiscal.position.tax.rule'
    _description = """Regra de Taxas da Posição Fiscal"""
    _order = 'sequence'

    def _compute_cst(self):
        for rule in self:
            if rule.domain == 'icms':
                rule.cst_vl = rule.cst_icms
            elif rule.domain == 'pis':
                rule.cst_vl = rule.cst_pis
            elif rule.domain == 'cofins':
                rule.cst_vl = rule.cst_cofins
            elif rule.domain == 'ipi':
                rule.cst_vl = rule.cst_ipi
            else:
                rule.cst_vl = False
            
    sequence = fields.Integer(string="Sequência")
    name = fields.Char(string="Descrição", size=100)
    domain = fields.Selection([('icms', 'ICMS'),
                               ('pis', 'PIS'),
                               ('cofins', 'COFINS'),
                               ('ipi', 'IPI'),
                               ('issqn', 'ISSQN'),
                               ('ii', 'II'),
                               ('csll', 'CSLL'),
                               ('irrf', 'IRRF'),
                               ('inss', 'INSS'),
                               ('outros', 'Outros')], string="Tipo")
    fiscal_position_id = fields.Many2one('account.fiscal.position', string="Posição Fiscal")
    fiscal_observation_ids = fields.Many2many('br_account.fiscal.observation', 
                                              relation='account_fiscal_position_tax_rule_observation', 
                                              string="Mensagens Doc. Eletrônico", copy=True)
    company_id = fields.Many2one('res.company', related='fiscal_position_id.company_id', 
                                 string='Company', store=True, readonly=True)

    state_ids = fields.Many2many('res.country.state', string="Estado Destino", 
                                 domain=[('country_id.code', '=', 'BR')])
    fiscal_category_ids = fields.Many2many('br_account.fiscal.category', string="Categorias Fiscais")
    tipo_produto = fields.Selection([('product', 'Produto'), ('service', 'Serviço')], 
                                    string="Tipo produto", default="product")

    service_analytic_ids = fields.Many2many('account.analytic.account', string="Conta", 
                                            relation="account_analytic_account_ret_tax_rule_service_relation")
    
    service_type_ids = fields.Many2many('br_account.service.type', string="Tipos Serviço", 
                                        relation="br_account_service_type_ret_tax_rule_service_relation")

    product_fiscal_classification_ids = fields.Many2many('product.fiscal.classification', 
                                                         string="Classificação Fiscal",
                                                         relation="account_fiscal_position_tax_rule_prod_fiscal_clas_relation")

    cst_vl = fields.Char(string="CST",compute="_compute_cst",store=False)
    cst_icms = fields.Selection(CST_ICMS, string="CST ICMS")
    csosn_icms = fields.Selection(CSOSN_SIMPLES, string="CSOSN ICMS")
    origin = fields.Selection(ORIGEM_PROD, 'Origem')
    icms_benef = fields.Many2one('br_account.beneficio.fiscal', string="Benficio Fiscal")
    cst_pis = fields.Selection(CST_PIS_COFINS, string="CST PIS")
    cst_cofins = fields.Selection(CST_PIS_COFINS, string="CST COFINS")
    cst_ipi = fields.Selection(CST_IPI, string="CST IPI")
    enq_ipi = fields.Many2one('br_account.enquadramento.ipi', string="Enquadramento IPI")
    cla_ipi = fields.Char(string="Clas.Enquadram.", size=5)
    cfop_id = fields.Many2one('br_account.cfop', string="CFOP")
    tax_id = fields.Many2one('account.tax', string="Imposto")
    tax_icms_st_id = fields.Many2one('account.tax', string="ICMS ST", domain=[('domain', '=', 'icmsst')])
    icms_aliquota_credito = fields.Float(string="% Crédito de ICMS",digits=(12,4))
    icms_aliquota_diferimento = fields.Float("% Diferimento",digits=(12,4))
    incluir_ipi_base = fields.Boolean(string="Incl. IPI na base ICMS")
    reducao_icms = fields.Float(string="Redução de base")
    reducao_aliquota_icms = fields.Float(string="% Redução aliquota",digits=(12,4))
    reducao_icms_st = fields.Float(string="Redução de base ST")
    reducao_ipi = fields.Float(string="Redução de base IPI")
    icms_aliquota_reducao_base = fields.Float(string="Aliquota Redução base",digits=(12,4))
    l10n_br_issqn_deduction = fields.Float(string="% Dedução de base ISSQN")
    aliquota_mva = fields.Float(string="Alíquota MVA",digits=(12,4))
    icms_st_aliquota_deducao = fields.Float(string="% ICMS Próprio", digits=(12,4), 
                                            help="Alíquota interna ou interestadual aplicada \
                                                  sobre o valor da operação para deduzir do ICMS ST - Para empresas \
                                                  do Simples Nacional ou usado em casos onde existe apenas ST sem ICMS")
    tem_difal = fields.Boolean(string="Aplicar Difal?")
    tax_icms_inter_id = fields.Many2one('account.tax', help="Alíquota utilizada na operação Interestadual", 
                                        string="ICMS Inter", domain=[('domain', '=', 'icms_inter')])
    tax_icms_intra_id = fields.Many2one('account.tax', help="Alíquota interna do produto no estado destino", 
                                        string="ICMS Intra", domain=[('domain', '=', 'icms_intra')])
    tax_icms_fcp_id = fields.Many2one('account.tax', string="% FCP", domain=[('domain', '=', 'fcp')])
    tax_icms_fcp_st_id = fields.Many2one('account.tax', string=u"% FCP ST", domain=[('domain', '=', 'fcpst')])
    preco_pauta = fields.Float(string="Preço de Pauta")
    issqn_tipo = fields.Selection([('N', 'Normal'),('R', 'Retida'),('S', 'Substituta'),('I', 'Isenta')],
                                  string='Tipo do ISSQN', default='N')

