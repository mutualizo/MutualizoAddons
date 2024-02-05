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
    'name': 'Mutualizo Brazilian Localisation Data Extension for Fiscal',
    'description': """Include data for Mutualizo Soma Brazilian Localisation Data 
                      Extension for Fiscal module""",
    'license': 'AGPL-3',
    'author': 'Mutualizo',
    'version': '17.0.0.1',
    'depends': [
        'mut_br_fiscal',
    ],
    'data': [
        'data/br_account.beneficio.fiscal.csv',
        'data/br_account.cfop.csv',
        'data/br_account.cnae.csv',
        'data/br_account.enquadramento.ipi.csv',
        'data/br_account.fiscal.document.csv',
        'data/br_account.service.type.csv',
        'data/product.fiscal.classification.csv',
        'data/br_account_document_serie.xml',
    ],
    'demo': [],
    'category': 'Localisation',
    'installable': True,
    'auto_install': False,
}
