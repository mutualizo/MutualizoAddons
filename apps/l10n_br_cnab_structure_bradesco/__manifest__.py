# © 2024 Mutualizo
{
    "name": "Bradesco CNAB Structure",
    "summary": """
        This module allows defining the structure for generating the CNAB file.
        Used to exchange information with Brazilian banks.""",
    "version": "14.0.1.2.0",
    "author": "Mutualizo",
    "maintainers": ["mutualizo"],
    "website": "https://www.mutualizo.com.br/",
    "depends": [
        "l10n_br_cnab_structure"
    ],
    "data": [],
    "demo": [],
    "post_init_hook": "post_init_hook",
    "external_dependencies": {"python": ["pyyaml", "unidecode"]},
}
