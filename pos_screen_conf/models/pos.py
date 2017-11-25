# -*- coding: utf-8 -*-
from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    price_display = fields.Boolean(
        string='Price Display', help="Display price setting on POS screen.",
        default=True)
