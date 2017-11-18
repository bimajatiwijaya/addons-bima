# -*- coding: utf-8 -*-
"""
Model approval settings
"""
from openerp.tests.common import TransactionCase


class TestUserSettings(TransactionCase):

    def setUp(self):
        super(TestUserSettings, self).setUp()
        self.res_user_model = self.env['res.users']
        self.main_company = self.env.ref('base.main_company')
        partner_manager = self.env.ref('base.group_partner_manager')
        partner_user = self.env.ref('base.group_user')
        self.app_o = self.env['ir.model.approval']
        self.user_app_o = self.env['res.users.approval']

        self.partner_manager = self.res_user_model.with_context(
            {'no_reset_password': True}).create(dict(
            name="partner manager",
            company_id=self.main_company.id,
            login="acc",
            email="partner_manager@yourcompany.com",
            groups_id=[
                (6, 0, [partner_manager.id, partner_user.id])]
        ))
        self.partner_user = self.res_user_model.with_context(
            {'no_reset_password': True}).create(dict(
            name="user",
            company_id=self.main_company.id,
            login="fm",
            email="user@yourcompany.com",
            groups_id=[
                (6, 0, [partner_user.id])]
        ))
