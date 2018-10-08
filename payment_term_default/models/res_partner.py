# -*- coding: utf-8 -*-

from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def default_get(self, values):
        res = super(ResPartner, self).default_get(values)
        # For vendor
        if not res.get('property_supplier_payment_term_id') and \
                res.get('supplier'):
            payment_term_obj = self.env['account.payment.term']
            payment_term_id = payment_term_obj.search([
                ('default_for_vendor', '=', True)], limit=1)
            res['property_supplier_payment_term_id'] = payment_term_id.id
        # For customer
        if not res.get('property_payment_term_id') and res.get('customer'):
            payment_term_obj = self.env['account.payment.term']
            payment_term_id = payment_term_obj.search([
                ('default_for_customer', '=', True)], limit=1)
            res['property_payment_term_id'] = payment_term_id.id
        return res
