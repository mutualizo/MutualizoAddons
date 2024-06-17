from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    def read(self, fields=None, load="_classic_read"):
        res = super(ResUsers, self).read(fields=fields, load=load)
        # We only want to redirect to app lists if the read is only in the
        # user default action. Then, we redirect to the apps list page
        if fields == ["action_id"] and not res[0].get("action_id"):
            action = self.env.ref("mut_ui_improvements.action_redirect_to_apps")
            res[0]["action_id"] = (action.id, action.name)
        return res
