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


class BrAccountFiscalObservation(models.Model):
    _name = 'br_account.fiscal.observation'
    _description = 'Mensagen Documento Eletrônico'
    _order = 'sequence'

    sequence = fields.Integer('Sequência', default=1, required=True)
    name = fields.Char('Descrição', required=True, size=50)
    message = fields.Text('Mensagem', required=True)
    tipo = fields.Selection([('fiscal', 'Observação Fiscal'),('observacao', 'Observação')], string="Tipo")
    document_id = fields.Many2one('br_account.fiscal.document', string="Documento Fiscal")
