# -*- coding: utf-8 -*-
# from odoo import http


# class Corso-odoo-abc(http.Controller):
#     @http.route('/corso-odoo-abc/corso-odoo-abc', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/corso-odoo-abc/corso-odoo-abc/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('corso-odoo-abc.listing', {
#             'root': '/corso-odoo-abc/corso-odoo-abc',
#             'objects': http.request.env['corso-odoo-abc.corso-odoo-abc'].search([]),
#         })

#     @http.route('/corso-odoo-abc/corso-odoo-abc/objects/<model("corso-odoo-abc.corso-odoo-abc"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('corso-odoo-abc.object', {
#             'object': obj
#         })

