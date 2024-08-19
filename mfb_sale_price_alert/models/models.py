from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
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
        elif self.product_id and self.order_id.pricelist_id.id == 2 : 
            price = self._get_product_price_in_pricelist(self.order_id.pricelist_id.id, self.product_id) 
            if self.price_unit < price :
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
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

        sale_order_lines = self.env['sale.order.line'].search([
            ('create_date', '>=', start_of_week),
            ('create_date', '<=', today),
            ('is_price_modified', '=', True)  
        ])
        
        content = ""
        for line in sale_order_lines:
            price = line._get_product_price_in_pricelist(line.order_id.pricelist_id.id, line.product_id) if line.order_id.pricelist_id.id == 2 else line.product_id.list_price
            content += "<tr>"
            content += "<td>{}</td>".format(line.product_id.default_code)
            content += "<td>{}</td>".format(line.product_id.name)
            content += "<td>{}</td>".format(line.price_unit)
            content += "<td>{}</td>".format(price)
            content += "<td>{}</td>".format(line.product_uom_qty)
            content += "<td>{}</td>".format(line.order_id.pricelist_id.name)
            content += "</tr>"

        email_body = """
        <div style="box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif,'Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol';background-color:#edf2f7;margin:0;padding-top:50px;padding-bottom:50px;width:100%">
      <table align="center" width="100%" cellpadding="0" cellspacing="0" style="box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif,'Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol';background-color:#edf2f7;border-color:#e8e5ef;border-radius:2px;border-width:1px;margin-top:0;padding:0;width:100%">
        <tbody>
          <tr>
            <td>
            <table align="center" width="570" cellpadding="0" cellspacing="0" style="box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif,'Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol';background-color:#ffffff;border-color:#e8e5ef;border-radius:2px;border-width:1px;margin-top:50px;padding:20px;width:570px">
            <tbody>
             
              <tr>
                <td>
                  <h1 style="font-size:18px"><b>Bonjour,</b></h1>
                  <p style="font-size:16px;">Ci-après les produits dont les prix sont inférieur aux prix du fiche article :</p>
                  <table>
                    <thead>
                        <th>Code article</th>
                        <th>Désignation</th>
                        <th>Prix saisi</th>
                        <th>Prix du fiche article</th>
                        <th>Quantité</th>
                        <th>Catégorie tarifaire</th>
                    <thead>
                    <tbody>
                        {}
                    <tbody>
                  </table>
                </td>
              </tr>
            </tbody>
          </table>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
        """.format(content)
        self.env['mail.mail'].create({
                'subject': 'Résumé des ventes en dessous du prix du fiche article',
                'body_html':email_body,
                'email_from': "notification.madafiarabe@gmail.com",
                'email_to': 'velonirinamihaja@gmail.com',  
            }).send()

    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        
        if  res.product_id and res.order_id.pricelist_id.id == 1 and res.price_unit < res.product_id.list_price:
            res.is_price_modified = True
        elif res.product_id and res.order_id.pricelist_id.id == 2 and res.price_unit < res._get_product_price_in_pricelist(res.order_id.pricelist_id.id, res.product_id) : 
            res.is_price_modified = True

        return res

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        
        for line in self:
            if 'price_unit' in vals and line.product_id:
                if line.order_id.pricelist_id.id == 1 and line.price_unit < line.product_id.list_price:
                    line.is_price_modified = True
                elif line.order_id.pricelist_id.id == 2 and line.price_unit < line._get_product_price_in_pricelist(line.order_id.pricelist_id.id, line.product_id) : 
                    line.is_price_modified = True
                else:
                    line.is_price_modified = False

        return res