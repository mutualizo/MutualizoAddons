# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import models, fields, api


class Company(models.Model):
    _inherit = "res.company"

    cnpj_cpf = fields.Char(compute='_compute_address', inverse='_inverse_cnpj_cpf', size=18, string='CNPJ')
    inscr_est = fields.Char(compute='_compute_address', inverse='inverse_inscr_est', size=16, 
                            string='State Inscription')
    inscr_mun = fields.Char(compute='_compute_address', inverse='inverse_inscr_mun', size=18, 
                            string='Municipal Inscription')
    suframa = fields.Char(compute='_compute_address', inverse='inverse_suframa', size=18, string='Suframa')
    legal_name = fields.Char(compute='_compute_address', inverse='inverse_legal_name', size=128, 
                             string='Legal Name')
    city_id = fields.Many2one(compute='_compute_address', inverse='inverse_city_id', comodel_name='res.state.city', 
                              string="City")
    district = fields.Char(compute='_compute_address', inverse='inverse_district', size=32, string="District")
    number = fields.Char(compute='_compute_address', inverse='inverse_number', size=10, string="Number")

    def _inverse_cnpj_cpf(self):
        for company in self:
            company.partner_id.cnpj_cpf = company.cnpj_cpf
    
    def inverse_inscr_est(self):
        for company in self:
            company.partner_id.inscr_est = company.inscr_est
            
    def inverse_inscr_mun(self):
        for company in self:
            company.partner_id.inscr_mun = company.inscr_mun
    
    def inverse_suframa(self):
        for company in self:
            company.partner_id.suframa = company.suframa

    def inverse_legal_name(self):
        for company in self:
            company.partner_id.legal_name = company.legal_name
            
    def inverse_city_id(self):
        for company in self:
            company.partner_id.city_id = company.city_id 

    def inverse_district(self):
        for company in self:
            company.partner_id.district = company.district
            
    def inverse_number(self):
        for company in self:
            company.partner_id.number = company.number       
            
    @api.onchange('cnpj_cpf')
    def onchange_mask_cnpj_cpf(self):
        if self.cnpj_cpf:
            val = re.sub('[^0-9]', '', self.cnpj_cpf)
            if len(val) == 14:
                cnpj_cpf = "%s.%s.%s/%s-%s" % (val[0:2], val[2:5], val[5:8], val[8:12], val[12:14])
                self.cnpj_cpf = cnpj_cpf

    @api.onchange('city_id')
    def onchange_city_id(self):
        """ Ao alterar o campo city_id copia o nome
        do município para o campo city que é o campo nativo do módulo base
        para manter a compatibilidade entre os demais módulos que usam o
        campo city.
        """
        if self.city_id:
            self.city = self.city_id.name

    @api.onchange('zip')
    def onchange_mask_zip(self):
        if self.zip:
            val = re.sub('[^0-9]', '', self.zip)
            if len(val) == 8:
                zip = "%s-%s" % (val[0:5], val[5:8])
                self.zip = zip





















                            