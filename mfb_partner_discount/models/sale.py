from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        """
        Automatically applies the discount from the customer when the partner is selected.
        """
        if self.partner_id and self.partner_id.customer_discount:
            discount = self.partner_id.customer_discount
            for line in self.order_line:
                line.discount = discount


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """
        Automatically applies the discount from the customer when the product is selected.
        """
        for line in self :
            if line.order_id.partner_id and line.order_id.partner_id.customer_discount:
                discount = line.order_id.partner_id.customer_discount
                line.discount = discount
                    
