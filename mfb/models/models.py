from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'

    subname = fields.Char(string="Subname")

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    @api.onchange("product_id")
    def _onchange_employee_id(self):
        if self.product_id and self.product_id.is_jirama_type:
            self.is_jirama_type = True
            self.is_insurance_type = False
            self.is_fuel_type = False
            self.is_autopart_purchase_type = False
        if self.product_id and self.product_id.is_insurance_type:
            self.is_jirama_type = False
            self.is_insurance_type = True
            self.is_fuel_type = False
            self.is_autopart_purchase_type = False
        if self.product_id and self.product_id.is_fuel_type:
            self.is_jirama_type = False
            self.is_insurance_type = False
            self.is_fuel_type = True
            self.is_autopart_purchase_type = False
        if self.product_id and self.product_id.is_autopart_purchase_type:
            self.is_jirama_type = False
            self.is_insurance_type = False
            self.is_fuel_type = False
            self.is_autopart_purchase_type = True
        elif self.product_id and not self.product_id.is_jirama_type and not self.product_id.is_insurance_type and not self.product_id.is_fuel_type and not self.product_id.is_autopart_purchase_type:
            self.is_jirama_type = False
            self.is_insurance_type = False
            self.is_fuel_type = False
            self.is_autopart_purchase_type = False

    is_jirama_type = fields.Boolean(compute="_compute_is_jirama_type")
    is_insurance_type = fields.Boolean(compute="_compute_is_insurance_type")
    is_fuel_type = fields.Boolean(compute="_compute_is_fuel_type")
    is_autopart_purchase_type = fields.Boolean(compute="_compute_is_autopart_purchase_type")

    # Jirama type fields
    jirama_new_index = fields.Char(string="Jirama new index")
    jirama_old_index = fields.Char(string="Jirama old index")
    new_index_date  = fields.Date(string="New index date")
    old_index_date  = fields.Date(string="Old index date")
    jirama_consumption = fields.Float(string="Jirama consumption (kWh)")

    # Insurance type fields
    insurance_start_date = fields.Date(string="Insurance start date")
    insurance_end_date = fields.Date(string="Insurance end date")
    insured_vehicle  = fields.Many2one("mfb.vehicle", string="Insured Vehicle")
    insurance_agency  = fields.Many2one("mfb.agency", string="Insurance agency")

    # Fuel type field
    fueled_vehicle = fields.Many2one("mfb.vehicle", string="Fueled vehicle")
    fuel_type = fields.Selection([('gasoil', 'Gasoil'),
                              ('essence', 'Essence')], string="Fuel type")
    fuel_qty = fields.Float(string="Fueled quantity (L)")


    # Autopart purchase type
    auto_part = fields.Many2one("product.template", string="Auto part")


    def _compute_is_jirama_type(self):
        for record in self:
            is_jirama = False
            if record.product_id:
                if record.product_id.is_jirama_type:
                    is_jirama = True
            record.is_jirama_type = is_jirama

    def _compute_is_insurance_type(self):
        for record in self:
            is_insurance = False
            if record.product_id:
                if record.product_id.is_insurance_type:
                    is_insurance = True
            record.is_insurance_type = is_insurance

    def _compute_is_fuel_type(self):
        for record in self:
            is_fuel = False
            if record.product_id:
                if record.product_id.is_fuel_type:
                    is_fuel = True
            record.is_fuel_type = is_fuel

    def _compute_is_autopart_purchase_type(self):
        for record in self:
            is_autopart_purchase = False
            if record.product_id:
                if record.product_id.is_autopart_purchase_type:
                    is_autopart_purchase = True
            record.is_autopart_purchase_type = is_autopart_purchase

    


class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_jirama_type = fields.Boolean(string="Is Jirama type", default=False)
    is_insurance_type = fields.Boolean(string="Is Insurance type", default=False)
    is_fuel_type = fields.Boolean(string="Is Fuel type", default=False)
    is_autopart_purchase_type = fields.Boolean(string="Is Autopart Purchase type", default=False)

class MfbVehicle(models.Model):
    _name = 'mfb.vehicle'

    name = fields.Char(string="Vehicle Name", required=True)
    number = fields.Char(string="Vehicle Number", required=True)

class MfbAgency(models.Model):
    _name = 'mfb.agency'

    name = fields.Char(string="Agency Name", required=True)

class PaymentMethod(models.Model):
    _inherit = 'payment.method'

    image = fields.Image(
        required=False,
    )

class AccountTax(models.Model):
    _inherit = 'account.tax'

    def _action_deactivate_all_unrelevant_taxes(self):
        """
        Deactivate taxes having the next conditions : 
        type_tax_use = 'sale' and tax_scope = 'consu' and not (tax_group_id = 2 and price_include is true)
        """

        domain = [
            ('type_tax_use', '=', 'sale'),
            ('tax_scope', '=', 'consu'),
            '!', '&', ('tax_group_id', '=', 2),
                    ('price_include', '=', True)
                ]

        taxes = self.env['account.tax'].sudo().search(domain)

        if taxes:
            for tax in taxes:
                tax.write({'active': False})