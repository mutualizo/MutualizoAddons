# -*- coding: utf-8 -*-
# from odoo import http


# class ModuleExemple(http.Controller):
#     @http.route('/module_exemple/module_exemple', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/module_exemple/module_exemple/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('module_exemple.listing', {
#             'root': '/module_exemple/module_exemple',
#             'objects': http.request.env['module_exemple.module_exemple'].search([]),
#         })

#     @http.route('/module_exemple/module_exemple/objects/<model("module_exemple.module_exemple"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('module_exemple.object', {
#             'object': obj
#         })

