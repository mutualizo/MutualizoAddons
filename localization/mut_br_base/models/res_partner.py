# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

import re
from odoo import models, fields, api, _
from ..tools import fiscal
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "zip.search.mixin"]

    def _default_country(self):
        return self.env['res.country'].search([('ibge_code', '=', '1058')],limit=1).id

    number = fields.Char('Number', size=10)
    cnpj_cpf = fields.Char( size=18, string='CNPJ/CPF', copy=False )
    inscr_est = fields.Char(size=16, string='State Inscription', copy=False)
    rg_fisica = fields.Char('RG', size=16, copy=False)
    inscr_mun = fields.Char(size=18, string='Municipal Inscription')
    rntrc_code = fields.Char(string="RNTRC Code", size=12)
    cei_code = fields.Char(string="CEI Code", size=12)
    union_entity_code = fields.Char(string="Union Entity code")
    suframa = fields.Char(size=18, string='Suframa')
    legal_name = fields.Char(size=128, string='Legal Name', help="Name used in fiscal documents")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', default=_default_country)
    ibge_code = fields.Char(related='country_id.ibge_code')
    city_id = fields.Many2one('res.city', 'City', domain="[('state_id','=?',state_id)]")
    district = fields.Char('District', size=32)
    type = fields.Selection(selection_add=[('branch', 'Branch')])

    pix_key_ids = fields.One2many(string="Pix Keys", comodel_name="res.partner.pix", inverse_name="partner_id", 
                                  help="Keys for Brazilian instant payment (pix)")

    show_l10n_br = fields.Boolean(compute="_compute_show_l10n_br",
                                  help="Indicates if Brazilian localization fields should be displayed.")

    @api.model
    def _address_fields(self):
        """Returns the list of address
        fields that are synced from the parent."""
        return super()._address_fields() + ["number","district",]

    @api.constrains("cnpj_cpf", "inscr_est")
    def _check_cnpj_inscr_est(self):
        for partner in self:
            domain = []

            # permite cnpj vazio
            if not partner.cnpj_cpf:
                return

            if self.env.context.get("disable_allow_cnpj_multi_ie"):
                return

            allow_cnpj_multi_ie = (partner.env["ir.config_parameter"].sudo()
                                   .get_param("mut_br_base.allow_cnpj_multi_ie", default=True))

            if partner.parent_id:
                domain += [
                    ("id", "not in", partner.parent_id.ids),
                    ("parent_id", "not in", partner.parent_id.ids),
                ]

            domain += [("cnpj_cpf", "=", partner.cnpj_cpf), ("id", "!=", partner.id)]

            # se encontrar CNPJ iguais
            if partner.env["res.partner"].search(domain):
                if allow_cnpj_multi_ie == "True":
                    for partner in partner.env["res.partner"].search(domain):
                        if (partner.inscr_est == partner.inscr_est and not partner.inscr_est):
                            raise ValidationError(_(
                                    "There is already a partner partner with this "
                                    "Estadual Inscription !"))
                    else:
                        raise ValidationError(_("There is already a partner partner with this CNPJ !"))
                else:
                    raise ValidationError(_("There is already a partner partner with this CPF/RG!"))

    def write(self, vals):
        val_city_id = vals.get('city_id', None)
        if bool(val_city_id):
            city_id = self.env['res.city'].search([('id','=?',val_city_id)])
            if bool(city_id):
                vals.update({'city': city_id.name, 
                             'state_id': city_id.state_id.id, 
                             'country_id': city_id.country_id.id})
        elif val_city_id == False:
            vals.update({'city': False})
        result = super(ResPartner, self).write(vals)
        return result
    
    @api.onchange('type')
    def onchange_type(self):
        if self.type == 'branch':
            self.company_type = 'company'
            self.is_company = True
            cnpj_cpf = re.sub('[^0-9]', '', self.parent_id.cnpj_cpf or '') 
            self.cnpj_cpf = cnpj_cpf[:8]
            self.legal_name = self.parent_id.legal_name
            self.name = self.parent_id.name
        else:
            self.company_type = 'person'
            self.is_company = False
            self.cnpj_cpf = False

    @api.constrains('cnpj_cpf', 'country_id', 'is_company')
    def _check_cnpj_cpf(self):
        disable_cpf_cnpj_validation = (self.env["ir.config_parameter"].sudo()
                                       .get_param("mut_br_base.disable_cpf_cnpj_validation", default=False))
        
        if disable_cpf_cnpj_validation:
            return

        for partner in self:
            # permite cnpj vazio
            if not partner.cnpj_cpf:
                continue
            country_code = partner.country_id.code or ''
            if self.type == 'contact' and partner.cnpj_cpf and (country_code.upper() == 'BR' or len(country_code) == 0):
                if partner.is_company:
                    if re.sub('[^0-9]', '', partner.cnpj_cpf) != "00000000000000" and not fiscal.validate_cnpj(partner.cnpj_cpf):
                        raise ValidationError('Invalid CNPJ Number!')
                elif re.sub('[^0-9]', '', self.cnpj_cpf) != "00000000000" and not fiscal.validate_cpf(partner.cnpj_cpf):
                    raise ValidationError('Invalid CPF Number!')

    def _is_cnpj_or_cpf(self):
        res = False
        if fiscal.validate_cnpj(self.cnpj_cpf):
            res = 'CNPJ'
        elif fiscal.validate_cpf(self.cnpj_cpf):
            res = 'CPF'
        return res

    def _validate_ie_param(self, uf, inscr_est):
        try:
            mod = __import__('odoo.addons.br_base.tools.fiscal', globals(), locals(), 'fiscal')
            validate = getattr(mod, 'validate_ie_%s' % uf)
            if not validate(inscr_est):
                return False
        except AttributeError:
            if not fiscal.validate_ie_param(uf, inscr_est):
                return False
        return True

    @api.constrains('inscr_est', 'state_id', 'is_company')
    def _check_ie(self):
        """Checks if company register number in field insc_est is valid,
        this method call others methods because this validation is State wise
        :Return: True or False."""
        
        disable_ie_validation = (self.env["ir.config_parameter"].sudo()
                                 .get_param("mut_br_base.disable_ie_validation", default=False))
        
        if disable_ie_validation:
            return
        
        for partner in self:
            if not partner.inscr_est or partner.inscr_est == 'ISENTO' \
                    or not partner.is_company:
                return True
            uf = partner.state_id and partner.state_id.code.lower() or ''
            res = partner._validate_ie_param(uf, partner.inscr_est)
            if not res:
                raise ValidationError(_('Invalid State Inscription!'))

    @api.constrains('inscr_est')
    def _check_ie_duplicated(self):
        """ Check if the field inscr_est has duplicated value
        """
        if not self.inscr_est or self.inscr_est == 'ISENTO':
            return True
        partner_ids = self.search(['&', ('inscr_est', '=?', self.inscr_est), ('id', '!=', self.id)])

        if len(partner_ids) > 0:
            raise ValidationError(
                _('This State Inscription/RG number is already being used by another partner!'))

    @api.onchange('cnpj_cpf')
    def _onchange_cnpj_cpf(self):
        country_code = self.country_id.code or ''
        if self.cnpj_cpf and (country_code.upper() == 'BR' or len(country_code) == 0):
            val = re.sub('[^0-9]', '', self.cnpj_cpf)
            if self.type == 'branch' and len(val) == 8:
                cnpj_cpf = "%s.%s.%s/" % (val[0:2], val[2:5], val[5:8])
                self.cnpj_cpf = cnpj_cpf
            elif self.type == 'contact':
                if len(val) == 14:
                    cnpj_cpf = "%s.%s.%s/%s-%s"\
                        % (val[0:2], val[2:5], val[5:8], val[8:12], val[12:14])
                    self.cnpj_cpf = cnpj_cpf
                elif not self.is_company and len(val) == 11:
                    cnpj_cpf = "%s.%s.%s-%s"\
                        % (val[0:3], val[3:6], val[6:9], val[9:11])
                    self.cnpj_cpf = cnpj_cpf
                else:
                    raise UserError(_('Verify CNPJ/CPF number'))

    @api.onchange('zip')
    def _onchange_zip(self):
        zip_code = re.sub('[^0-9]', '', self.zip or '')
        if len(zip_code) == 8:
            values = self.search_address_by_zip(zip_code)
            if not values:
                return {
                    'warning': {
                        'title': 'Dica',
                        'message': 'Por favor insira um CEP válido'
                    }
                }
            self.update(values)
        elif self.zip:
            return {
                'warning': {
                    'title': 'Dica',
                    'message': 'Por favor use um CEP de 8 dígitos'
                }
            }


    @api.onchange('city_id')
    def _onchange_city_id(self):
        """ Ao alterar o campo city_id copia o nome
        do município para o campo city que é o campo nativo do módulo base
        para manter a compatibilidade entre os demais módulos que usam o
        campo city.
        """
        if self.city_id:
            self.city = self.city_id.name



    def _compute_show_l10n_br(self):
        """
        Defines when Brazilian localization fields should be displayed.
        """
        for rec in self:
            if rec.company_id and rec.company_id.country_id != self.env.ref("base.br"):
                rec.show_l10n_br = False
            else:
                rec.show_l10n_br = True
