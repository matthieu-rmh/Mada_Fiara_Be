from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_price_modified = fields.Boolean(string="Is Price Modified", default=False)

    @api.onchange('price_unit')
    def _onchange_price_unit_warning(self):

        if self.order_id.pricelist_id.id == 1 and self.price_unit < self.product_id.list_price :
            return {
                'warning': {
                'title': _("Attention pour %s", self.product_id.name),
                'message': _("Le montant saisissé est inférieur au prix  de l'article %s selon le tarif %s.", self.product_id.list_price, self.order_id.pricelist_id.name),
                }
            }
        elif self.order_id.pricelist_id.id == 2 and self.price_unit < self._get_product_price_in_pricelist(self.order_id.pricelist_id.id, self.product_id) : 
            return {
                'warning': {
                'title': _("Attention pour %s", self.product_id.name),
                'message': _("Le montant saisissé est inférieur au prix de l'article %s selon le tarif %s.", price, self.order_id.pricelist_id.name),
                }
            }

    def _get_product_price_in_pricelist(self, pricelist_id, product) :
        self.ensure_one() 
        pricelist = self.env['product.pricelist'].browse(pricelist_id)

        price = pricelist._get_product_price(product, 1, self.env.user.partner_id)

        return price

    
    def _action_sale_price_alert(self) :
        print("hello world")

    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        
        if  res.product_id and res.order_id.pricelist_id.id == 1 and res.price_unit < res.product_id.list_price:
            res.is_price_modified = True
        elif res.product_id and res.order_id.pricelist_id.id == 2 and res.price_unit < self._get_product_price_in_pricelist(res.order_id.pricelist_id.id, res.product_id) : 
            res.is_price_modified = True

        return res

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        
        for line in self:
            if 'price_unit' in vals and line.product_id:
                if line.order_id.pricelist_id.id == 1 and line.price_unit < line.product_id.list_price:
                    line.is_price_modified = True
                elif line.order_id.pricelist_id.id == 2 and line.price_unit < self._get_product_price_in_pricelist(line.order_id.pricelist_id.id, line.product_id) : 
                    line.is_price_modified = True
                else:
                    line.is_price_modified = False

        return res