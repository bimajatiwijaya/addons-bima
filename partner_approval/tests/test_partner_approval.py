# -*- coding: utf-8 -*-
"""
Model approval settings
"""
from openerp.addons.data_approval.tests.test_setting_users import \
    TestUserSettings


class TestPartnerApproval(TestUserSettings):
    """
    STORY
    1. create model approval res.partner
    2. set 2 user who have permission write
    3. create new partner
        a. status partner unactive
    4. 2 user login and approve partner
    5. first user approve partner
        a. status partner still unactive
    6. second user approve partner
        a. partner activated
    """

    def test_partner_approval(self):
        partner_app_user = \
            self.env.ref('partner_approval.group_partner_approval')
        groups_id = self.partner_manager.groups_id
        groups_id |= partner_app_user
        self.partner_manager.write({
            'groups_id': [(6, 0, [g.id for g in groups_id])]
        })
        self.partner_manager2.write({
            'groups_id': [(6, 0, [g.id for g in groups_id])]
        })
        partner_o = self.env['res.partner']
        partner_model_o = self.env['ir.model'].search(
            [('model', '=', 'res.partner')], limit=1)
        self.app_o.create({
            'model_id': partner_model_o.id,
            'validator_ids': [
                (0, 0, {'user_id': self.partner_manager.id,
                        'sequence': 1}),
                (0, 0, {'user_id': self.partner_manager2.id,
                        'sequence': 2}),
            ]
        })
        new_partner1 = partner_o.create({
            'name': 'Test Contact',
            'email': 'contact@email.com',
            'company_type': 'company',
        })
        self.assertTrue(not new_partner1.active)
        new_partner2 = partner_o.create({
            'name': 'Test Contact',
            'email': 'contact@email.com',
            'company_type': 'company',
        })
        self.assertTrue(not new_partner2.active)
        new_partners = new_partner1 | new_partner2
        # first approval and all partner not activated yet
        new_partners.sudo(self.partner_manager.id).approve()
        self.assertTrue(not all([p.active for p in new_partners]))
        # final approval and all partner activated
        new_partners.sudo(self.partner_manager2.id).approve()
        self.assertTrue(all([p.active for p in new_partners]))
