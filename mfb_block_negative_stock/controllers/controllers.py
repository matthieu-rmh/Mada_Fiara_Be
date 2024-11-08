# -*- coding: utf-8 -*-
# from odoo import http


# class RnkSaleConfirm(http.Controller):
#     @http.route('/rnk_sale_confirm/rnk_sale_confirm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rnk_sale_confirm/rnk_sale_confirm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rnk_sale_confirm.listing', {
#             'root': '/rnk_sale_confirm/rnk_sale_confirm',
#             'objects': http.request.env['rnk_sale_confirm.rnk_sale_confirm'].search([]),
#         })

#     @http.route('/rnk_sale_confirm/rnk_sale_confirm/objects/<model("rnk_sale_confirm.rnk_sale_confirm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rnk_sale_confirm.object', {
#             'object': obj
#         })
