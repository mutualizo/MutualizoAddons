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
from .cst import CST_ICMS

class BrAccountBeneficioFiscal(models.Model):
    _name = 'br_account.beneficio.fiscal'
    _description = 'Código de Benefício Fiscal'

    code = fields.Char('Código',size=10)
    name = fields.Char('Descrição', required=True)
    state_id = fields.Many2one('res.country.state', 'Estado', domain="[('country_id.code', '=', 'BR')]", 
                               required=True)
    dt_start = fields.Date('Data Inicial')
    dt_end = fields.Date('Data Final')
    cst_line_ids = fields.One2many('br_account.beneficio.fiscal.cst', 'beneficio_id', string="CSTs", copy=True)
    memo = fields.Text('Observação')

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = "[%s] %s" % (rec.code or '', rec.name or '')

class BrAccountBeneficioFiscalCST(models.Model):
    _name = 'br_account.beneficio.fiscal.cst'
    _description = 'CST - Código de Benefício Fiscal'
    
    name = fields.Selection(CST_ICMS, string="CST ICMS")
    beneficio_id = fields.Many2one('br_account.beneficio.fiscal',string='CST - Código de Benefício Fiscal')
    code = fields.Char(related='beneficio_id.code',store=True)
    #name = fields.Char(related='beneficio_id.code')
    state_id = fields.Many2one(related='beneficio_id.state_id',store=True)
    dt_start = fields.Date(related='beneficio_id.dt_start',store=True)
    dt_end = fields.Date(related='beneficio_id.dt_end',store=True)