{
    'name': 'Financial APIs',
    'version': "14.0.0.0",
    'category': 'Extra Tools',
    'description':  """
                    Financial APIs by Mutualizo
                    Before run, define the following config settings:
                        - mut_financial_apis.callback_url: where to send the callback_urls
                        - mut_financial_apis.callback_api_key: api_key from the callback lambda
                        - mut_financial_apis.load_api_key: intern api_key to load invoices
                    """,
    'author': 'Mutualizo',
    'company': 'Mutualizo',
    'maintainer': 'Mutualizo',
    'website': "https://www.mutualizo.com.br",
    'depends': ['l10n_br_account_payment_brcobranca'],
    'data': [
        # Data
        "data/data.xml",
        "data/mail_template_data.xml",
        # Views
        "views/account_move.xml",
        "views/res_config_settings.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
