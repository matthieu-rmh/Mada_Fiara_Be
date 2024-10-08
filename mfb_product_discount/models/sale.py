from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """
        Automatically applies the discount from the product when the product is selected.
        """
        for line in self :
            if line.disable_discount :
                line.discount = 0
            else :
                if line.order_id.partner_id and line.order_id.partner_id.customer_discount > 0 :
                    partner_discount = line.order_id.partner_id.customer_discount
                    product_discount = line.product_id.product_discount

                    if partner_discount > product_discount :
                        line.discount = partner_discount
                    else :
                        line.discount = product_discount       
                elif line.product_id.product_discount > 0 :
                    discount = line.product_id.product_discount
                    line.discount = discount
                        
