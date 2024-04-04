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
        #'views/account_account_view.xml',
        'views/account_fiscal_position_view.xml',
        'views/account_invoice_refund_view.xml',
        'views/account_bank_statement_import_view.xml',
        # 'views/account_journal_view.xml',
        'views/account_beneficio_fiscal_view.xml',
        'views/account_cfop_view.xml',
        'views/account_cnae_view.xml',
        'views/fiscal_document_related_view.xml',
        'views/document_serie_view.xml',
        'views/enquadramento_ipi_view.xml',
        'views/account_fiscal_category_view.xml',
        'views/account_fiscal_document_view.xml',
        'views/account_fiscal_observation_view.xml',
        'views/product_fiscal_classification_view.xml',
        'views/service_type_view.xml',
        'views/menus_view.xml',
        'security/ir.model.access.csv'
    ],
    'external_dependencies': {},
    'images': ['static/description/banner.gif'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
    'module_type': 'official',
}
