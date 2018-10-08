# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo import SUPERUSER_ID


class TestPartner(TransactionCase):
    """ Test default_get extension """

    def setUp(self):
        res = super(TestPartner, self).setUp()
        self.res_partner_obj = self.env['res.partner']
        acc_payment_term_obj = self.env['account.payment.term']
        self.acc_payment_term_id = acc_payment_term_obj.create({
            'name': 'Test',
            'default_for_customer': True,
        })
        return res

    def test_create_partner(self):
        fields = ['customer']
        defaults = self.res_partner_obj.default_get(fields)
        self.assertEqual(defaults.get('property_payment_term_id'),
                         self.acc_payment_term_id.id, "Wrong payment term!")
