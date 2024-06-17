from odoo import http
from odoo.addons.website_slides.controllers.main import WebsiteSlides


class WebsiteSlidesInherit(WebsiteSlides):
    @http.route("/slides", type="http", auth="user", website=True, sitemap=True)
    def slides_channel_home(self, **post):
        return super(WebsiteSlidesInherit, self).slides_channel_home(**post)
