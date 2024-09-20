from odoo import models, fields

class SaleReport(models.Model):
    _inherit = 'sale.report'

    date_entry = fields.Datetime(string="Date de saisie", readonly=True)

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['date_entry'] = "s.date_entry"
        return res
