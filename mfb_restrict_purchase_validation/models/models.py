from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_id')
    def _onchange_product_id_update_cost(self):
        """
        Met à jour le coût standard lorsque le produit est sélectionné.
        """
        for line in self:
            if line.product_id:
                # Récupère le coût standard du produit
                line.price_unit = line.product_id.standard_price
            else:
                line.price_unit = 0.0