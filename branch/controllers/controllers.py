# -*- coding: utf-8 -*-
# from odoo import http


# class Branch(http.Controller):
#     @http.route('/branch/branch/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/branch/branch/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('branch.listing', {
#             'root': '/branch/branch',
#             'objects': http.request.env['branch.branch'].search([]),
#         })

#     @http.route('/branch/branch/objects/<model("branch.branch"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('branch.object', {
#             'object': obj
#         })
