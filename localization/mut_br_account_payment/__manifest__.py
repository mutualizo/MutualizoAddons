# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################

{
    'name': "Account Payment Brasil Mutualizo",
    'version': '17.0.0.1',
    'category': 'localization',
    'summary': 'Base para os módulos da localização do Brasil pela Mutualizo',
    'description': 'Este módulo adiciona os campos brasileiros de identificação '
                   'de pessoas físicas e jurídicas.',
    'author': "Mutualizo Solutions",
    'maintainer': 'Mutualizo Solutions',
    'company': 'Mutualizo Solutions',
    'website': "https://www.mutualizo.com",
    'depends': [
        'account',
        'account_payment',
        'base_accounting_kit',
        'mut_br_account'
    ],
    'data': [
        'views/account_journal_view.xml',
        'views/payment_receivable_view.xml',
        'views/res_partner_view.xml',
        'views/account_payment_view.xml',
        'views/account_move_line_view.xml',
        'views/res_config_settings_views.xml',
        'views/menu_view.xml',
        'wizard/change_date_maturity_view.xml',
        'security/ir.model.access.csv',
    ],
    "external_dependencies": {
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
