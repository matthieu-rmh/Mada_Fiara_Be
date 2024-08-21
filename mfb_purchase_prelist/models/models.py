from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    @api.model
    def default_get(self, fields_list):
        res = super(PurchaseOrder, self).default_get(fields_list)
        product_obj = self.env['product.product']
        low_stock_products = product_obj.search([('qty_available', '<', 10)])

        order_lines = []
        for product in low_stock_products:
            line_values = {
                'product_id': product.id,
                'name': product.name,
                'product_qty': 1, 
                'price_unit': product.standard_price,
                'date_planned': fields.Date.today(),
            }
            order_lines.append((0, 0, line_values))

        if 'order_line' in fields_list:
            res.update({'order_line': order_lines})

        return res
