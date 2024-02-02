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
from odoo.addons.mut_br_base.tools.fiscal import IND_IE_DEST, FRT_RESP

class ResPartner(models.Model):
    _inherit = 'res.partner'

    indicador_ie_dest = fields.Selection(IND_IE_DEST, string="Indicador IE", 
                                         help="Caso não preencher este campo vai usar a \
                                               regra:\n9 - para pessoa física\n1 - para pessoa jurídica com IE \
                                               cadastrada\n2 - para pessoa jurídica sem IE cadastrada ou 9 \
                                               caso o estado de destino for AM, BA, CE, GO, MG, MS, MT, PE, RN, SP")

    freight_responsibility = fields.Selection(FRT_RESP, 'Modalidade do frete')
    end_cobranca_id = fields.Many2one('res.partner', compute='_compute_enderecos', string="Cobrança", store=True)
    contato_id = fields.Many2one('res.partner', compute='_compute_enderecos', string="Contato", store=True)
    email_nfe = fields.Char(string="E-Mail Doc. Eletr.", help="e-Mail para onde os documentos eletrônicos a receber serão enviados, caso esteja em branco vai para o e-Mail padrão.")

    @api.depends('child_ids')
    def _compute_enderecos(self):
        """ Procura o endereço de Cobrança e Contato e caso não haja devolve o endereço atual """
        # Procura o endereço de cobrança
        for reg in self:
            cobranca = reg.env['res.partner'].search([('parent_id','=',reg.id),('type','=','invoice')],limit=1)
            contato = reg.env['res.partner'].search([('parent_id','=',reg.id),('type','=','contact')],limit=1)
            # Passa o endereco caso tenha
            reg.end_cobranca_id = cobranca if cobranca else False
            reg.contato_id = contato if contato else False

