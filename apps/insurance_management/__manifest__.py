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
    'name': 'Mutualizo Insurance Management',
    'version': '17.0.1.0.0',
    'category': 'Accounting',
    'summary': """Insurance Management & Operations of the customers and manage
     the insurance claims and the salary of agents with or without the 
     commission.""",
    'description': """Insurance Management and claims based on policies allows
     the user to create insurance policies """,
    'author': 'Mutualizo Team',
    'company': 'Mutualizo',
    'maintainer': 'Mutualizo',
    'website': 'https://www.mutualizo.com.br',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'data/payment_type_data.xml',
        'data/insurance_details_data.xml',
        'data/claim_details_data.xml',
        'views/claim_details_views.xml',
        'views/employee_details_views.xml',
        'views/insurance_details_views.xml',
        'views/policy_details_views.xml',
        'views/insurance_management_menus.xml',
        'views/policy_type_views.xml',
        'views/payment_type_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'account/static/src/components/**/*',
        ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
