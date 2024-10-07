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

