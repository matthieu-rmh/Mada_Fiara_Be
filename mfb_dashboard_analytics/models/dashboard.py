from odoo import models, fields

class Dashboard(models.Model):
    _name = 'dashboard.analytics'
    _description = 'Dashboard for Expenses and Revenues'

    date = fields.Date(string="Date")
    total_expenses = fields.Float(string="Total Expenses")
    total_revenues = fields.Float(string="Total Revenues")