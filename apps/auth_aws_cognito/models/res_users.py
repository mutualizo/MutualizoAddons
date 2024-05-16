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
import json, logging, requests
from odoo.http import request
from odoo import api, models
from odoo import exceptions
from odoo.addons import base
from odoo.addons.auth_signup.models.res_users import SignupError

base.models.res_users.USER_PRIVATE_FIELDS.append('oauth_access_token')
_logger = logging.getLogger(__name__)

try:
    import jwt
except ImportError:
    _logger.warning(
        "Login with AWS Cognito account won't be available.Please install PyJWT "
        "python library, ")
    jwt = None


class ResUsers(models.Model):
    """This class is used to inheriting the res.users and provides the oauth
    access"""
    _inherit = 'res.users'

    @api.model
    def _auth_oauth_rpc(self, endpoint, access_token):
        """This is used to pass the response of sign in."""
        if endpoint:
            headers = {'Authorization': 'Bearer %s' % access_token}
            return requests.get(endpoint, headers=headers).json()

    @api.model
    def _auth_oauth_code_validate(self, provider, code):
        """ Return the validation data corresponding to the access token """
        auth_oauth_provider = self.env['auth.oauth.provider'].browse(provider)
        req_params = dict(
            client_id=auth_oauth_provider.client_id,
            client_secret=auth_oauth_provider.client_secret_id,
            grant_type='authorization_code',
            code=code,
            redirect_uri=request.httprequest.url_root + 'auth_oauth/signin',
        )
        headers = {'Accept': 'application/json'}
        token_info = requests.post(auth_oauth_provider.validation_endpoint,
                                   headers=headers, data=req_params).json()
        if token_info.get("error"):
            raise Exception(token_info['error'])
        access_token = token_info.get('access_token')
        validation = {
            'access_token': access_token
        }
        if token_info.get('id_token'):
            if not jwt:
                raise exceptions.AccessDenied()
            data = jwt.decode(token_info['id_token'], verify=False)
        else:
            data = self._auth_oauth_rpc(auth_oauth_provider.data_endpoint,
                                        access_token)
        validation.update(data)
        return validation

    @api.model
    def _auth_oauth_signin(self, provider, validation, params):
        """ Retrieve and sign in the user corresponding to provider and validated access token
                    :param provider: oauth provider id (int)
                    :param validation: result of validation of access token (dict)
                    :param params: oauth parameters (dict)
                    :return: user login (str)
                    :raise: AccessDenied if signin failed

                    This method can be overridden to add alternative signin methods.
                """
        user = self.search([('login', '=', str(validation.get('email')))])
        if not user:
            user = self.create({
                'login': str(validation.get('email')),
                'name': str(validation.get('email')),
                'oauth_provider_id': provider
            })
            provider_id = self.env['auth.oauth.provider'].sudo().browse(
                provider)
            if provider_id.template_user_id:
                user.is_contractor = provider_id.template_user_id.is_contractor
                user.contractor = provider_id.template_user_id.contractor
                user.groups_id = [
                    (6, 0, provider_id.template_user_id.groups_id.ids)]
        user.write({
            'oauth_provider_id': provider,
            'oauth_uid': validation['user_id'],
            'oauth_access_token': params['access_token'],
        })
        oauth_uid = validation['user_id']
        try:
            oauth_user = self.search([("oauth_uid", "=", oauth_uid),
                                      ('oauth_provider_id', '=', provider)])
            if not oauth_user:
                raise exceptions.AccessDenied()
            assert len(oauth_user) == 1
            oauth_user.write({'oauth_access_token': params['access_token']})
            return oauth_user.login
        except (exceptions.AccessDenied, exceptions.access_denied_exception):
            if self.env.context.get('no_user_creation'):
                return None
            state = json.loads(params['state'])
            token = state.get('t')
            values = self._generate_signup_values(provider, validation, params)
            try:
                _, login, _ = self.signup(values, token)
                return login
            except SignupError:
                raise exceptions.access_denied_exception
        return super()._auth_oauth_signin(provider, validation,
                                                        params)

    @api.model
    def _auth_oauth_validate(self, provider, access_token):
        """ return the validation data corresponding to the access token """
        oauth_provider = self.env['auth.oauth.provider'].search([('name', '=', provider)])
        validation = self._auth_oauth_rpc(oauth_provider.validation_endpoint, access_token)
        if validation.get("error") and validation.get("error") is not None:
            raise Exception(validation['error'])
        if oauth_provider.data_endpoint:
            data = self._auth_oauth_rpc(oauth_provider.data_endpoint, access_token)
            validation.update(data)
        # unify subject key, pop all possible and get most sensible. When this
        # is reworked, BC should be dropped and only the `sub` key should be
        # used (here, in _generate_signup_values, and in _auth_oauth_signin)
        subject = next(filter(None, [
            validation.pop(key, None)
            for key in [
                'sub',  # standard
                'id',  # google v1 userinfo, facebook opengraph
                'user_id',  # google tokeninfo, odoo (tokeninfo)
            ]
        ]), None)
        if not subject:
            raise exceptions.AccessDenied('Missing subject identity')
        validation['user_id'] = subject

        return validation

    @api.model
    def auth_oauth(self, provider, params):
        """This is used to take the access token to sign in with the user account."""
        if params.get('code'):
            validation = self._auth_oauth_code_validate(provider,
                                                        params['code'])
            access_token = validation.pop('access_token')
            params['access_token'] = access_token
        else:
            access_token = params.get('access_token')
            validation = self._auth_oauth_validate(provider, access_token)
        if not validation.get('user_id'):
            if validation.get('id'):
                validation['user_id'] = validation['id']
            elif validation.get('oid'):
                validation['user_id'] = validation['oid']
            else:
                raise exceptions.AccessDenied()
        provider_id = self.env['auth.oauth.provider'].search([('name', '=', provider)]).id
        login = self._auth_oauth_signin(provider_id, validation, params)
        if not login:
            raise exceptions.AccessDenied()
        if provider and params:
            return (self.env.cr.dbname, login, access_token)
        return super(ResUsers, self).auth_oauth(provider, params)

    @classmethod
    def authenticate(cls, db, login, password, user_agent_env):

        record = super(ResUsers, cls).authenticate(db, login, password, user_agent_env)
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if "http://" in base_url and "http://localhost" not in base_url:
            base_url = base_url.replace("http://", "https://")
            request.env['ir.config_parameter'].sudo().set_param('web.base.url', base_url)
        return record
