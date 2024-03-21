# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

from odoo import fields, models


class PolicyDetails(models.Model):
    """Essa classe cria um modelo "policy.details" e adiciona campos """
    _name = 'policy.details'
    _description = "Detalhes da apólice"

    name = fields.Char(string='Sequencia', required=True, help="Dê o nome da apólice")
    policy_type_id = fields.Many2one('policy.type', string='Tipo da apólice', required=True, 
                                     help="Selecione o tipo de apólice")
    payment_type_ids = fields.Many2many('payment.type', help="Selecione os tipos de pagamento da apólice")
    currency_id = fields.Many2one('res.currency', string='Moeda', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id, help="Selecione a Moeda")
    amount = fields.Monetary(string='Total', required=True, help="Informe o valor da apólice")
    note_field = fields.Html(string='Comentário', help="Comentários")
