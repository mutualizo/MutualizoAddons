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

class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    company_id = fields.Many2one("res.company", string='Company', default=lambda self: self.env.user.company_id)
    journal_id = fields.Many2one(
        'account.journal', string="Diário Contábil",
        help="Diário Contábil a ser utilizado na fatura.", copy=True)
    account_id = fields.Many2one(
        'account.account', string="Conta Contábil",
        help="Conta Contábil a ser utilizada na fatura.", copy=True)
    fiscal_observation_ids = fields.Many2many(
        'br_account.fiscal.observation', string="Mensagens Doc. Eletrônico",
        copy=True)
    note = fields.Text('Observações')

    product_serie_id = fields.Many2one(
        'br_account.document.serie', string='Série Produto',
        domain="[('fiscal_document_id', '=', product_document_id)]", copy=True)
    product_document_id = fields.Many2one(
        'br_account.fiscal.document', string='Documento Produto', copy=True)

    service_serie_id = fields.Many2one(
        'br_account.document.serie', string='Série Serviço',
        domain="[('fiscal_document_id', '=', service_document_id)]",
        copy=True)
    service_document_id = fields.Many2one(
        'br_account.fiscal.document', string='Documento Serviço', copy=True)

    icms_tax_rule_ids = fields.One2many(
        'account.fiscal.position.tax.rule', 'fiscal_position_id',
        string="Regras ICMS", domain=[('domain', '=', 'icms')], copy=True)
    ipi_tax_rule_ids = fields.One2many(
        'account.fiscal.position.tax.rule', 'fiscal_position_id',
        string="Regras IPI", domain=[('domain', '=', 'ipi')], copy=True)
    pis_tax_rule_ids = fields.One2many(
        'account.fiscal.position.tax.rule', 'fiscal_position_id',
        string="Regras PIS", domain=[('domain', '=', 'pis')], copy=True)
    cofins_tax_rule_ids = fields.One2many(
        'account.fiscal.position.tax.rule', 'fiscal_position_id',
        string="Regras COFINS", domain=[('domain', '=', 'cofins')],
        copy=True)
    issqn_tax_rule_ids = fields.One2many(
        'account.fiscal.position.tax.rule', 'fiscal_position_id',
        string="Regras ISSQN", domain=[('domain', '=', 'issqn')], copy=True)
    ii_tax_rule_ids = fields.One2many(
        'account.fiscal.position.tax.rule', 'fiscal_position_id',
        string="Regras II", domain=[('domain', '=', 'ii')], copy=True)
    irrf_tax_rule_ids = fields.One2many(
        'account.fiscal.position.tax.rule', 'fiscal_position_id',
        string="Regras IRRF", domain=[('domain', '=', 'irrf')], copy=True)
    csll_tax_rule_ids = fields.One2many(
        'account.fiscal.position.tax.rule', 'fiscal_position_id',
        string="Regras CSLL", domain=[('domain', '=', 'csll')], copy=True)
    inss_tax_rule_ids = fields.One2many(
        'account.fiscal.position.tax.rule', 'fiscal_position_id',
        string="Regras INSS", domain=[('domain', '=', 'inss')], copy=True)
    outros_tax_rule_ids = fields.One2many(
        'account.fiscal.position.tax.rule', 'fiscal_position_id',
        string="Outras Retenções", domain=[('domain', '=', 'outros')])
    fiscal_type = fields.Selection([('saida', 'Saída'),
                                    ('entrada', 'Entrada')],
                                   string="Tipo da posição", copy=True)
    natureza = fields.Char(string='Natureza Operação',oldname='nat_operacao')
    
    auto_gerar_fatura = fields.Boolean(string="Auto Faturar",help="Gerar Automaticamente a fatura.")
    auto_validar_remessa = fields.Boolean(string="Auto Validar Remessas",help="Validar a Remessa do Pedido (se houver).")
    own_issuer = fields.Boolean(string="Emissão Própria", help="Emissão é própria")

    @api.onchange('product_document_id')
    def onchange_product_document_id(self):
        self.product_serie_id = False
        if bool(self.product_document_id):
            serie = self.env['br_account.document.serie'].search([('fiscal_document_id', '=', self.product_document_id.id)],limit=1)
            if bool(serie):
                self.product_serie_id = serie

    @api.onchange('service_document_id')
    def onchange_service_document_id(self):
        self.service_document_id = False
        if bool(self.service_document_id):
            serie = self.env['br_account.document.serie'].search([('fiscal_document_id', '=', self.service_document_id.id)],limit=1)
            if bool(serie):
                self.service_document_id = serie

    @api.model
    def _get_fpos_by_region(self, country_id=False, state_id=False, zipcode=False, vat_required=False):
        type_inv = self.env.context.get('type', False)
        supplier = self.env.context.get('search_default_supplier', False)
        customer = self.env.context.get('search_default_customer', False)

        base_domain = [('auto_apply', '=', True)]
        if bool(vat_required):
            base_domain += [('vat_required', '=', vat_required)]
        if self.env.context.get('force_company'):
            base_domain += [('company_id', 'in', [self.env.context.get('force_company'), False])]
        if type_inv in ('out_invoice','in_refund') or customer:
            base_domain += [('fiscal_type', '=', 'saida')]
        elif type_inv in ('in_invoice','out_refund') or supplier:
            base_domain += [('fiscal_type', '=', 'entrada')]

        zip_domain = []
        local_domain = []

        # null_state_dom = state_domain = [('state_ids', '=', False)]
        # null_zip_dom = zip_domain = [('zip_from', '=', 0), ('zip_to', '=', 0)]
        # null_country_dom = [('country_id', '=', False), ('country_group_id', '=', False)]

        # DO NOT USE zipcode.isdigit() b/c '4020²' would be true, so we try/except
        try:
            zipcode = int(zipcode)
        except (ValueError, TypeError):
            zipcode = 0

        if zipcode != 0:
            zip_domain = [('zip_from', '<=', zipcode), ('zip_to', '>=', zipcode)]

        if bool(country_id):
            local_domain += [('country_id', '=', country_id)]
            # domain_group = base_domain + [('country_group_id.country_ids', '=', country_id)]
            if state_id:
                local_domain += [('state_ids', '=', state_id)]
            # Build domain to search records with exact matching criteria
        fpos = self.search(base_domain + local_domain + zip_domain, limit=1)
        
            # # return records that fit the most the criteria, and fallback on less specific fiscal positions if any can be found
            # if not fpos and state_id:
            #     fpos = self.search(domain_country + null_state_dom + zip_domain, limit=1)
            # if not fpos and zipcode:
            #     fpos = self.search(domain_country + state_domain + null_zip_dom, limit=1)
            # if not fpos and state_id and zipcode:
            #     fpos = self.search(domain_country + null_state_dom + null_zip_dom, limit=1)

        # fallback: country group with no state/zip range
        # if not fpos:
        #     fpos = self.search(domain_group + null_state_dom + null_zip_dom, limit=1)

        if not fpos:
            fpos = self.search(base_domain, limit=1)

        return fpos

    @api.model
    def map_tax_extra_values(self, product, partner, fiscal_classification, service_type, issqn_tipo, analytic):
        taxes = ('icms', 'simples', 'ipi', 'pis', 'cofins', 'issqn', 'ii', 'irrf', 'csll', 'inss', 'outros')
        res = {'mensagem': []}
        for tax in taxes:
            vals = {
                'partner': partner,
                'fiscal_type': product.fiscal_type,
                'fiscal_category': product.fiscal_category_id,
                'origin': product.origin,
                'fiscal_classification': fiscal_classification if bool(fiscal_classification) else product.fiscal_classification_id,
                'to_service_type': service_type if bool(service_type) else product.service_type_id,
                'issqn_tipo': issqn_tipo,
                'analytic': analytic,
            }
            msg,vals = self._filter_rules(self.id, tax, **vals)
            res['mensagem'] += msg
            res.update({k: v for k, v in vals.items() if v})
        return res

    def _filter_rules(self, fpos_id, type_tax, **kwargs):
        rule_obj = self.env['account.fiscal.position.tax.rule']
        domain = [('fiscal_position_id', '=', fpos_id),('domain', '=', type_tax)]
        rules = rule_obj.search(domain)

        if not bool(kwargs.get('issqn_tipo')) and bool(kwargs.get('partner')) and bool(kwargs.get('partner').city_id):
            kwargs['issqn_tipo'] = 'R' if kwargs.get('partner').city_id.id != self.company_id.city_id.id else 'N'

        if rules:
            msgs = []
            rules_points = {}
            for rule in rules:

                # Calcula a pontuacao da regra.
                # Quanto mais alto, mais adequada está a regra em relacao ao
                # faturamento
                rules_points[rule.id] = self._calculate_points(rule, **kwargs)

            # Calcula o maior valor para os resultados obtidos
            greater_rule = max([(v, k) for k, v in rules_points.items()])
            # Se o valor da regra for menor do que 0, a regra é descartada.
            if greater_rule[0] < 0:
                return msgs,{}

            # Procura pela regra associada ao id -> (greater_rule[1])
            rules = [rules.browse(greater_rule[1])]
            
            for rule in rules:
                for msg in rule.fiscal_observation_ids:
                    msgs += [msg.id]

            # Retorna dicionario com o valores dos campos de acordo com a regra
            return msgs,{
                ('%s_rule_id' % type_tax): rules[0],
                'cfop_id': rules[0].cfop_id,
                'icms_benef': rules[0].icms_benef,
                ('tax_%s_id' % type_tax): rules[0].tax_id,
                # ICMS
                'icms_cst_normal': rules[0].cst_icms,
                'icms_aliquota_reducao_base': rules[0].reducao_icms,
                'incluir_ipi_base': rules[0].incluir_ipi_base,
                # ICMS Dif
                'icms_aliquota_diferimento': rules[0].icms_aliquota_diferimento,
                # ICMS ST
                'tax_icms_st_id': rules[0].tax_icms_st_id,
                'icms_st_aliquota_mva': rules[0].aliquota_mva,
                'icms_st_aliquota_reducao_base': rules[0].reducao_icms_st,
                'icms_st_aliquota_deducao': rules[0].icms_st_aliquota_deducao,
                'tax_icms_fcp_st_id': rules[0].tax_icms_fcp_st_id,
                'icms_st_preco_pauta': rules[0].preco_pauta,
                # ICMS Difal
                'tem_difal': rules[0].tem_difal,
                'tax_icms_inter_id': rules[0].tax_icms_inter_id,
                'tax_icms_intra_id': rules[0].tax_icms_intra_id,
                'tax_icms_fcp_id': rules[0].tax_icms_fcp_id,
                # Simples
                'icms_csosn_simples': rules[0].csosn_icms,
                'icms_aliquota_credito': rules[0].icms_aliquota_credito,
                # IPI
                'ipi_cst': rules[0].cst_ipi,
                'ipi_reducao_bc': rules[0].reducao_ipi,
                'ipi_codigo_enquadramento': rules[0].enq_ipi,
                'ipi_classe_enquadramento': rules[0].cla_ipi,
                # PIS
                'pis_cst': rules[0].cst_pis,
                # PIS
                'cofins_cst': rules[0].cst_cofins,
                # ISSQN
                'issqn_tipo': rules[0].issqn_tipo,
                'l10n_br_issqn_deduction': rules[0].l10n_br_issqn_deduction,
            }
        else:
            return [],{}

    def _calculate_points(self, rule, **kwargs):
        """Calcula a pontuação das regras. A pontuação aumenta de acordo
        com os 'matches'. Não havendo match(exceto quando o campo não está
        definido) retorna o valor -1, que posteriormente será tratado como
        uma regra a ser descartada.
        """

        fiscal_type = kwargs.get('fiscal_type')
        partner = kwargs.get('partner')
        rule_points = 0

        # Verifica o tipo do produto. Se sim, avança para calculo da pontuação
        # Se não, retorna o valor -1 (a regra será descartada)
        if bool(fiscal_type) and fiscal_type == rule.tipo_produto:
            fiscal_category = kwargs.get('fiscal_category')
            origin = kwargs.get('origin')
            fiscal_classification = kwargs.get('fiscal_classification')
            
            # Verifica a categoria fiscal. Se contido, adiciona 1 ponto
            # Se não, retorna valor -1 (a regra será descartada)
            if bool(fiscal_category) and fiscal_category in rule.fiscal_category_ids:
                rule_points += 1
            elif len(rule.fiscal_category_ids) > 0:
                return -1

            if fiscal_type == 'product':
                # Verifica origem. Se contido, adiciona 1 ponto
                # Se não, retorna -1
                if bool(origin) and origin == rule.origin:
                    rule_points += 1
                elif bool(rule.origin):
                    return -1
                
                # Verifica produtos. Se contido, adiciona 1 ponto
                # Se não, retorna -1
                if bool(fiscal_classification) and fiscal_classification in rule.product_fiscal_classification_ids:
                    rule_points += 1
                elif len(rule.product_fiscal_classification_ids) > 0:
                    return -1
    
                # Verifica o estado. Se contido, adiciona 1 ponto
                # Se não, retorna -1
                if bool(partner) and partner.state_id in rule.state_ids:
                    rule_points += 1
                elif len(rule.state_ids) > 0:
                    return -1

            elif fiscal_type == 'service':
                service_type = kwargs.get('service_type')
                analytic = kwargs.get('analytic')
                issqn_tipo = kwargs['issqn_tipo']
 
                if bool(issqn_tipo) and issqn_tipo == rule.issqn_tipo:
                    rule_points += 1
                elif bool(rule.issqn_tipo):
                    return -1
                
                if bool(analytic) and analytic in rule.service_analytic_ids:
                    rule_points += 1
                elif len(rule.service_analytic_ids) > 0:
                    return -1
                
                if bool(service_type) and service_type in rule.service_type_ids:
                    rule_points += 1
                elif len(rule.service_type_ids) > 0:
                    return -1
        else:
            return -1

        return rule_points
