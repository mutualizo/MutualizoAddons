"""AWS Cognito login"""
# -*- coding: utf-8 -*-
###################################################
#  __  __       _               _ _               #
# |  \/  |_   _| |_ _   _  __ _| (_)_______       #
# | |\/| | | | | __| | | |/ _` | | |_  / _ \      #
# | |  | | |_| | |_| |_| | (_| | | |/ / (_) |     #
# |_|  |_|\__,_|\__|\__,_|\__,_|_|_/___\___/      #
#                                                 #
###################################################
import json
import werkzeug.urls
import werkzeug.utils
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome as Home


class OAuthLogin(Home):
    """This class is used for oauth login"""

    def list_providers(self):
        """Which provides the oauth provider to login to the odoo"""
        super().list_providers()
        try:
            auth_providers = request.env[
                'auth.oauth.provider'].sudo().search_read(
                [('enabled', '=', True)])
        except Exception:
            auth_providers = []
        for rec in auth_providers:
            return_url = request.httprequest.url_root + 'auth_oauth/signin'
            state = self.get_state(rec)
            params = dict(
                client_id=rec['client_id'],
                response_type=rec['response_type'],
                scope=rec['scope'],
                redirect_uri=return_url,
            )
            rec['auth_link'] = "%s?%s" % (
                rec['auth_endpoint'], werkzeug.urls.url_encode(params))
        return auth_providers
