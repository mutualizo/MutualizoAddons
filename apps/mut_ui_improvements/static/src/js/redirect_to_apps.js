odoo.define('mut_ui_improvements.redirect_to_apps', function (require) {
    "use strict";
    
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    
    var RedirectToApps = AbstractAction.extend({
        start: function () {
            var self = this
            return this._super().then(function () {
                setTimeout(function () {
                    self.openMenuApps();
                }, 100)
            });
        },

        openMenuApps: function() {
            let liDropdown = document.querySelector("li.dropdown");
            liDropdown.classList.add("show")
            let aFull = document.querySelector("a.full");
            aFull.setAttribute("aria-expanded", "true")
            let divDropdown = document.querySelector("div.dropdown-menu");
            divDropdown.classList.add("show")
        }
    });
    
    core.action_registry.add('redirect_to_apps', RedirectToApps);
});