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
    'name': 'Mutualizo Brazilian Localisation Data Extension for Base',
    'description': """Include data for Mutualizo Soma Brazilian Localisation Data Extension for Base""",
    'license': 'AGPL-3',
    'author': 'Mutualizo',
    'version': '17.0.0.1',
    'depends': [
        'mut_br_base',
    ],
    'data': [
        'data/res.bank.csv',
        'data/res.country.csv',
        'data/res.city.csv',
        'data/res.country.state.csv',
        'data/br_base_data.xml',
    ],
    'demo': [],
    'category': 'Localisation',
    'installable': True,
    'auto_install': False,
}
