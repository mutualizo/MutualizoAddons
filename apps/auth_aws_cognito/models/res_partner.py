
from odoo import api, fields, models


class Partner(models.Model):
    _description = 'Contact'
    _inherit = ['format.address.mixin', 'image.mixin']
    _name = "res.partner"

    email_verified = fields.Boolean(string='Email Verified', default=False)
