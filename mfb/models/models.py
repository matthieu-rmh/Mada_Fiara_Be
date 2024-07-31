from odoo import models, fields
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class PaymentMethod(models.Model):
    _inherit = 'payment.method'

    image = fields.Image(
        required=False,
    )