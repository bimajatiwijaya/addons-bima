# -*- coding: utf-8 -*-
from openerp import api, fields, models, _


class IrModelValidation(models.Model):
    _name = "ir.model.approval"
    _description = "Model Validation"
    _inherit = ['mail.thread']
    _order = "id desc"

    name = fields.Char('Name')
    model_id = fields.Many2one('ir.model', string="Model")
    validator_ids = fields.One2many('res.users.approval', 'model_validation_id',
                                    string="Approval",
                                    help="List user who should validate model")

    @api.model
    def create(self, vals):
        if vals.get('model_id'):
            model_id = self.env['ir.model'].browse([vals.get('model_id')])
            vals['name'] = model_id.name
        return super(IrModelValidation, self).create(vals)


class ResUsersApproval(models.Model):
    _name = "res.users.approval"

    user_id = fields.Many2one('res.users', string="User", required=True)
    sequence = fields.Integer('Sequence', default=0)
    model_validation_id = fields.Many2one('ir.model.approval')
