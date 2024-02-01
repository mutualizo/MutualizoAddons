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
    'name': "Base Brasil Mutualizo",
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
        'base', 
        'base_setup', 
        'base_address_extended',
        'contacts',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_region_view.xml',
        'views/res_state_city_view.xml',
        'views/res_country_view.xml',
        'views/res_country_state_view.xml',
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
        'views/res_config_settings_view.xml',
        'views/menus_view.xml',
    ],
    'external_dependencies': {},
    'images': ['static/description/banner.gif'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
