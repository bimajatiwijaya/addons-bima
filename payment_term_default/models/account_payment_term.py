# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    default_for_vendor = fields.Boolean("Set as default vendor payment term")
    default_for_customer = fields.Boolean(
        "Set as default customer payment term")
