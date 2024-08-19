from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_price_modified = fields.Boolean(string="Is Price Modified", default=False)

    @api.onchange('price_unit')
    def _onchange_price_unit_warning(self):

        if self.order_id.pricelist_id.id === 2 : #and self.price_unit < self.product_id.list_price :
            return {
                'warning': {
                'title': _("Attention pour %s", self.product_id.name),#
                'message': _("Le montant saisissé est inférieur au prix de l'article selon le tarif %s.", self._get_product_price_in_pricelist(self.order_id.pricelist_id.id, self.product_id)),#self.self.order_id.pricelist_id.name,
                }
            }
        #else if self.order_id.pricelist_id.id === 2 and self.price_unit < _get_product_price_in_pricelist()

    def _get_product_price_in_pricelist(self, pricelist_id, product) :
        self.ensure_one() 
        pricelist = self.env['product.pricelist'].browse(pricelist_id)

        price = pricelist.get_product_price(product, 1, self.env.user.partner_id)

        return price

    
    def _action_sale_price_alert(self) :
        print("hello world")

    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        
        if  res.product_id and res.price_unit < res.product_id.list_price:
            res.is_price_modified = True

        return res

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        
        for line in self:
            if 'price_unit' in vals and line.product_id:
                if line.price_unit < line.product_id.list_price:
                    line.is_price_modified = True
                else:
                    line.is_price_modified = False

        return res