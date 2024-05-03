# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

import werkzeug.urls
import werkzeug.utils
from werkzeug.exceptions import BadRequest

from odoo import http, SUPERUSER_ID
from odoo.http import request
from odoo.exceptions import AccessDenied

from odoo.addons.web.controllers.main import ensure_db, _get_login_redirect_url
from odoo.addons.auth_oauth.controllers.main import fragment_to_query_string


_logger = logging.getLogger(__name__)


class OAuthController(http.Controller):

    @http.route("/auth_oauth/signin", type="http", auth="none")
    @fragment_to_query_string
    def signin(self, **kw):
        # make sure request.session.db and state['d'] are the same,
        # update the session and retry the request otherwise
        dbname = request.env.cr.dbname
        if not http.db_filter([dbname]):
            return BadRequest()
        ensure_db()
        provider = "AWS Cognito"
        try:
            # auth_oauth may create a new user, the commit makes it
            # visible to authenticate()'s own transaction below
            _, login, key = (
                request.env["res.users"]
                .with_user(SUPERUSER_ID)
                .auth_oauth(provider, kw)
            )
            request.env.cr.commit()
            url = "/web"
            pre_uid = request.session.authenticate(dbname, login, key)
            resp = werkzeug.utils.redirect(
                _get_login_redirect_url(pre_uid, url), code=303
            )
            resp.autocorrect_location_header = False

            # Since /web is hardcoded, verify user has right to land on it
            if werkzeug.urls.url_parse(
                resp.location
            ).path == "/web" and not request.env.user.has_group("base.group_user"):
                resp.location = "/"
            return resp
        except AttributeError:  # TODO juc master: useless since ensure_db()
            # auth_signup is not installed
            _logger.error(
                "auth_signup not installed on database %s: oauth sign up cancelled.",
                dbname,
            )
            url = "/web/login?oauth_error=1"
        except AccessDenied:
            # oauth credentials not valid, user could be on a temporary session
            _logger.info(
                "OAuth2: access denied, redirect to main page in case a valid session exists, without setting cookies"
            )
            url = "/web/login?oauth_error=3"
        except Exception:
            # signup error
            _logger.exception("Exception during request handling")
            url = "/web/login?oauth_error=2"

        redirect = werkzeug.utils.redirect(url, code=303)
        redirect.autocorrect_location_header = False
        return redirect
