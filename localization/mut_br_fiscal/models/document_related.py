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
from odoo.addons.mut_br_base.tools import fiscal
from odoo.exceptions import UserError, ValidationError


class AccountDocumentRelated(models.Model):
    _name = 'br_account.document.related'
    _description = """Documento relacionado"""

    invoice_id = fields.Many2one('account.move', 'Documento Fiscal', ondelete='cascade')
    invoice_related_id = fields.Many2one('account.move', 'Documento Fiscal', ondelete='cascade')
    document_type = fields.Selection([('nf', 'NF'), 
                                      ('nfe', 'NF-e'), 
                                      ('cte', 'CT-e'),
                                      ('nfrural', 'NF Produtor'), 
                                      ('cf', 'Cupom Fiscal')],
                                      'Tipo Documento', required=True)
    access_key = fields.Char('Chave de Acesso', size=44)
    serie = fields.Char('Série', size=12)
    internal_number = fields.Char('Número', size=32)
    state_id = fields.Many2one('res.country.state', 'Estado', domain="[('country_id.code', '=', 'BR')]")
    cnpj_cpf = fields.Char('CNPJ/CPF', size=18)
    cpfcnpj_type = fields.Selection([('cpf', 'CPF'), 
                                     ('cnpj', 'CNPJ')], 
                                     'Tipo Doc.', default='cnpj')
    inscr_est = fields.Char('Inscr. Estadual/RG', size=16)
    date = fields.Date('Data')
    fiscal_document_id = fields.Many2one('br_account.fiscal.document', 'Documento')

    @api.constrains('cnpj_cpf')
    def _check_cnpj_cpf(self):
        for reg in self:
            check_cnpj_cpf = True
            if reg.cnpj_cpf:
                if reg.cpfcnpj_type == 'cnpj':
                    if not fiscal.validate_cnpj(reg.cnpj_cpf):
                        check_cnpj_cpf = False
                elif not fiscal.validate_cpf(reg.cnpj_cpf):
                    check_cnpj_cpf = False
            if not check_cnpj_cpf:
                raise ValidationError(_('CNPJ/CPF do documento relacionado é invalido!'))

    @api.constrains('inscr_est')
    def _check_ie(self):
        for reg in self:
            check_ie = True
            if reg.inscr_est:
                uf = reg.state_id and reg.state_id.code.lower() or ''
                try:
                    mod = __import__('odoo.addons.mut_br_base.tools.fiscal', globals(), locals(), 'fiscal')
    
                    validate = getattr(mod, 'validate_ie_%s' % uf)
                    if not validate(reg.inscr_est):
                        check_ie = False
                except AttributeError:
                    if not fiscal.validate_ie_param(uf, reg.inscr_est):
                        check_ie = False
            if not check_ie:
                raise UserError(_('Inscrição Estadual do documento fiscal inválida!'))

    @api.onchange('invoice_related_id')
    def onchange_invoice_related_id(self):
        if not self.invoice_related_id:
            return
        inv_id = self.invoice_related_id
        if not inv_id.product_document_id:
            return

        self.document_type = self.translate_document_type(inv_id.product_document_id.code)

        if inv_id.product_document_id.code in ('55', '57'):
            self.serie = False
            self.internal_number = False
            self.state_id = False
            self.cnpj_cpf = False
            self.cpfcnpj_type = False
            self.date = False
            self.fiscal_document_id = False
            self.inscr_est = False

    def translate_document_type(self, code):
        if code == '55':
            return 'nfe'
        elif code == '65':
            return 'nfce'
        elif code == '04':
            return 'nfrural'
        elif code == '57':
            return 'cte'
        elif code in ('2B', '2C', '2D'):
            return 'cf'
        else:
            return 'nf'
