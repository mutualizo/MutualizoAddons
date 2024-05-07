{
    'name': 'Financial APIs',
    'version': "14.0.0.0",
    'category': 'Extra Tools',
    'description': """Financial APIs by Mutualizo""",
    'author': 'Mutualizo',
    'company': 'Mutualizo',
    'maintainer': 'Mutualizo',
    'website': "https://www.mutualizo.com.br",
    'depends': ['l10n_br_account_payment_brcobranca'],
    'data': [
        # Data
        "data/data.xml",
        # Views
        "views/account_move.xml",
        "views/res_config_settings.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
