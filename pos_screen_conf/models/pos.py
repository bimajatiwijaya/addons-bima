# -*- coding: utf-8 -*-
from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    price_display = fields.Boolean(
        string='Price Display', help="Display price setting on POS screen.",
        default=True)
    payment_display = fields.Boolean(
        string='Payment Numpad Display', help="Display button payment "
                                              "setting.", default=True)
    numpad_display = fields.Boolean(
        string='Numpad Display', help="Display numpad setting.", default=True)
    price_numpad_display = fields.Boolean(
        string='Price Numpad Display', help="Display price numpad setting.",
        default=True)
    disc_numpad_display = fields.Boolean(
        string='Discount Numpad Display', help="Display discount numpad "
                                               "setting.", default=True)
