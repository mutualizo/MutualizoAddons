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
    'name': "Account Brasil Mutualizo",
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
        'mut_br_base'],
    'data': [
    ],
    'external_dependencies': {},
    'images': ['static/description/banner.gif'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
