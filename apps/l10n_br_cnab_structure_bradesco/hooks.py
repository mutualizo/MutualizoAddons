import logging

from odoo import _, tools

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """Import XML data to change core data"""

    files = [
        "data/l10n_br_cnab.structure.csv",
        "data/l10n_br_cnab.batch.csv",
        "data/cnab.payment.way.csv",
        "data/l10n_br_cnab.line.csv",
        "data/cnab.line.field.group.csv",
        "data/l10n_br_cnab.line.field.csv",
        "data/cnab.line.group.field.condition.csv",
        "data/cnab.occurrence.csv",
        "data/cnab.pix.key.type.csv",
        "data/cnab.pix.transfer.type.csv",
    ]

    _logger.info(_("Loading l10n_br_cnab_structure_bradesco data files."))

    for file in files:
        tools.convert_file(
            cr,
            "l10n_br_cnab_structure_bradesco",
            file,
            None,
            mode="init",
            noupdate=True,
            kind="init",
        )
