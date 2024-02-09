{
    'name': 'OAuth2 - AWS Cognito Integration',
    'version': "17.0.0.0",
    'category': 'Extra Tools',
    'summary': """Integração com o AWS Cognito a partir de Autenticação OAuth2.""",
    'description': """Basic module for AWS Cognito connector used to login 
     with azure account in odoo.We can login in odoo using cognito portal account 
     and also there is no need to enter the pass word each time.""",
    'author': 'Mutualizo',
    'company': 'Mutualizo',
    'maintainer': 'Mutualizo',
    'website': "https://www.mutualizo.com.br",
    'depends': ['base', 'auth_oauth'],
    'data': [
        'data/auth_oauth_provider_data.xml',
        'views/auth_oauth_provider_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
