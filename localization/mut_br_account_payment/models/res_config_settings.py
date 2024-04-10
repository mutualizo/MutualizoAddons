# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import api, fields, models

from odoo.addons.account.models.company import PEPPOL_LIST


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_br_mut_payment_interest_account_id = fields.Many2one(
        comodel_name="account.account",
        related='company_id.l10n_br_mut_payment_interest_account_id',
        help='Conta onde será debitado o montante de tarifas pagas',
        string="Conta para pagamento de juros/multa",
        readonly=False,
        check_company=True,
        domain="[('deprecated', '=', False)]") 

    l10n_br_mut_payment_discount_account_id = fields.Many2one(
        comodel_name='account.account',
        related='company_id.l10n_br_mut_payment_discount_account_id',
        string="Conta para desconto de pagamentos",readonly=False,
        check_company=True,
        domain="[('deprecated', '=', False)]") 
    
    l10n_br_mut_discount_account_id = fields.Many2one(
        comodel_name='account.account',
        related='company_id.l10n_br_mut_discount_account_id',
        string="Conta para desconto de recebimentos",
        readonly=False,
        check_company=True,
        domain="[('deprecated', '=', False)]") 

    l10n_br_mut_interest_account_id = fields.Many2one(
        comodel_name='account.account',
        related='company_id.l10n_br_mut_interest_account_id',
        string="Conta para recebimento de juros",
        readonly=False,
        check_company=True,
        domain="[('deprecated', '=', False)]")
     
    l10n_br_mut_bankfee_account_id = fields.Many2one(
        comodel_name='account.account',
        related='company_id.l10n_br_mut_bankfee_account_id',
        string="Conta para tarifas bancárias",
        readonly=False,
        check_company=True,
        domain="[('deprecated', '=', False)]")

#######################################################################

    l10n_br_mut_multa_tx = fields.Float(
        related='company_id.l10n_br_mut_multa_tx',
        string="Taxa de Multa por Atraso",
        readonly=False,
        help='Taxa Padrão da Multa para Recebimentos em Atraso'
    )
    l10n_br_mut_juros_mes_tx = fields.Float(
        related='company_id.l10n_br_mut_juros_mes_tx',
        readonly=False,
        string="Taxa de Juros Mensal por Recebimentos em Atraso",
        help='Taxa Padrão de Juros de Mora por mês em documentos recebíveis em atraso'
    )
    l10n_br_mut_desc_ant_tx = fields.Float(
        related='company_id.l10n_br_mut_desc_ant_tx',
        readonly=False,
        string="Taxa para descontos de documentos recebidos antecipadamente",
        help='Taxa para documentos recebidos antecipadamente'
    )
