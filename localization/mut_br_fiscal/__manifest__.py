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
    'name': "Fiscal Brasil Mutualizo",
    'version': '17.0.0.1',
    'category': 'localization',
    'summary': 'Base Contábil para os módulos da localização do Brasil pela Mutualizo',
    'description': 'Este módulo adiciona os campos brasileiros de identificação '
                   'de pessoas físicas e jurídicas.',
    'author': "Mutualizo Solutions",
    'maintainer': 'Mutualizo Solutions',
    'company': 'Mutualizo Solutions',
    'website': "https://www.mutualizo.com",
    'depends': [
        'account',
        'product',
        'base_accounting_kit', #Include in Cyber Addons
        'mut_br_base'],
    'data': [
        'views/account.xml',
        'views/account_fiscal_position_view.xml',
        'views/account_invoice_refund.xml',
        'views/account_bank_statement_import_view.xml',
        'views/account_journal_views.xml',
       # 'views/account_invoice_view.xml',
       # 'views/account_tax.xml',
    ],
    'external_dependencies': {},
    'images': ['static/description/banner.gif'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
    'module_type': 'official',
}
