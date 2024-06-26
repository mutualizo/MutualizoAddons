odoo.define('mut_financial_apis.cnab', function (require) {
    "use strict";
    
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var viewRegistry = require('web.view_registry');
    
    var CnabListController = ListController.extend({
        buttons_template: 'CnabListView.buttons',
        events: _.extend({}, ListController.prototype.events, {
            'click .o_button_create_cnab': '_onCreateCnab',
        }),
    
        _onCreateCnab: function () {
            var self = this;
            this._rpc({
                model: 'account.move',
                method: 'confirm_invoices_generate_cnab',
                args: [],
                context: {
                    skip_time_verification: true,
                }
            }).then(res => {
                if(res.name) self.do_action(res);
            });
        }
    });

    var CnabListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: CnabListController,
        }),
    });
    
    viewRegistry.add('cnab_account_tree', CnabListView);
});
