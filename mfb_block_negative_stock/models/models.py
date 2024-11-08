# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """
        Check product stock avalaible
        """
        for line in self.order_line:
            location = self.warehouse_id.lot_stock_id
            stock = sum(self.env['stock.quant'].search([('product_id','=',line.product_id.id),('location_id','=',location.id)]).mapped('quantity'))
            reserved = sum(self.env['stock.quant'].search([('product_id','=',line.product_id.id),('location_id','=',location.id)]).mapped('reserved_quantity'))
            available = stock - reserved
            if available < line.product_uom_qty:
                raise UserError(_('Impossible de confirmer car l\'article : "'+ str(line.product_id.product_tmpl_id.name)) + ' " est  en rupture de stock')
        res = super(SaleOrder,self).action_confirm()
