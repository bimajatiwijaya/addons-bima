# -*- coding: utf-8 -*-
"""
Model approval settings
"""
from openerp.addons.data_approval.tests.test_setting_users import TestUserSettings


class TestModelApproval(TestUserSettings):
    """
    create model approval res.partner
    first user : don't have permission edit res.parter
    should raise error
    
    second user : have permission edit res.partner
    should not raise error
    """
    def test_setting_partner_approval(self):
        create_error = "user don't have permission edit res.partner model !"
        partner_o = self.env['ir.model'].search(
            [('model', '=', 'res.partner')], limit=1)
        with self.assertRaises(Exception) as context:
            self.app_o.create({
                'model_id': partner_o.id,
                'validator_ids': [
                    (0, 0, {'user_id': self.partner_user.id, 'sequence': 1})
                ]
            })
        self.assertTrue(create_error == context.exception[0])
        # Mean user should not set on res.partner approval
        # Delete existing res.partner approval
        self.app_o.search([('model_id', '=', partner_o.id)]).unlink()
        self.app_o.create({
            'model_id': partner_o.id,
            'validator_ids': [
                (0, 0, {'user_id': self.partner_manager.id, 'sequence': 1})
            ]
        })
