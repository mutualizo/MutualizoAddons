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


class BrAccountDocumentSerie(models.Model):
    _name = 'br_account.document.serie'
    _description = 'Série de documentos fiscais'

    code = fields.Char('Código', size=3, required=True)
    name = fields.Char('Descrição', required=True)
    active = fields.Boolean('Ativo')
    fiscal_type = fields.Selection([('service', 'Serviço'),
                                    ('product', 'Produto')], 'Tipo Fiscal',
                                   default='service')
    fiscal_document_id = fields.Many2one('br_account.fiscal.document',
                                         'Documento Fiscal', required=True)
    company_id = fields.Many2one('res.company', 'Empresa', required=True)
    internal_sequence_id = fields.Many2one('ir.sequence', 'Sequência Interna')

    lot_sequence_id = fields.Many2one('ir.sequence', 'Sequência Lote')

    @api.model
    def _create_sequence(self, vals, lote=False):
        """ Create new no_gap entry sequence for every new document serie """
        seq = {
            'name': 'lote_'+vals['name'] if lote else vals['name'],
            'implementation': 'no_gap',
            'padding': 1,
            'number_increment': 1
        }
        if 'company_id' in vals:
            seq['company_id'] = vals['company_id']
        return self.env['ir.sequence'].create(seq).id

    @api.model_create_multi
    def create(self, vals_list):
        """ Overwrite method to create a new ir.sequence if this field is null """
        for vals in vals_list: 
            if not vals.get('internal_sequence_id'):
                vals.update({'internal_sequence_id': self._create_sequence(vals)})
        return super().create(vals_list)

