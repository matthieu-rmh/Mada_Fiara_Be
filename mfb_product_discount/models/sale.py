from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """
        Automatically applies the discount from the product when the product is selected.
        """
        for line in self :
            if line.product_id.product_discount:
                discount = line.product_id.product_discount
                line.discount = discount
                    
