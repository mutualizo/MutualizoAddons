{
    'name': 'OAuth2 - AWS Cognito Integration',
    'version': "17.0.0.0",
    'category': 'Extra Tools',
    'summary': """Microsoft Azure OAuth2 SSO Integration is used to login odoo
     with microsoft azure account using the single sign on functionality.""",
    'description': """Basic module for Microsoft Azure connector used to login 
     with azure account in odoo.We can login in odoo using azure portal account 
     and also there is no need to enter the pass word each time.""",
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': '',
    'website': "https://www.cybrosys.com",
    'depends': ['base', 'auth_oauth'],
    'data': [
        'data/auth_oauth_provider_data.xml',
        'views/auth_oauth_provider_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
