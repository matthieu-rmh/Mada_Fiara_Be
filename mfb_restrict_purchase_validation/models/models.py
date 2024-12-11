from odoo import models, fields, api
from odoo.exceptions import UserError

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_id')
    def _onchange_product_id_update_cost(self):
        """
        Met à jour le coût lorsque le produit est sélectionné.
        """
        # get currency rates of AED currency
        currency_rates = self.env['res.currency.rate'].sudo().search([('currency_id', '=', 
                                                                        self.env['res.currency'].sudo().search([('name', '=', 'AED')], limit=1).id
                                                                        )]) 
        
        # get the latest aed currency rate
        latest_rate = max(currency_rates,  key=lambda x: x.name) 

        for line in self:
            if line.product_id:
                # raise UserError(str(line.product_id.standard_price))
                # Récupère le coût du produit
                line.price_unit = line.product_id.standard_price * latest_rate.inverse_company_rate
            else:
                line.price_unit = 0.0