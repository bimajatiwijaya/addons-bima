# -*- coding: utf-8 -*-
"""
Model approval settings
"""
from openerp import api, fields, models, _
from openerp.exceptions import UserError


class IrModelValidation(models.Model):
    _name = "ir.model.approval"
    _description = "Model Validation"
    _inherit = ['mail.thread']
    _order = "id desc"

    name = fields.Char('Name')
    model_id = fields.Many2one('ir.model', string="Model")
    validator_ids = fields.One2many('res.users.approval',
                                    'model_validation_id',
                                    string="Approval",
                                    help="List user who should validate model")

    _sql_constraints = [
        ('model_id_uniq', 'unique (model_id)', 'The model already exist on '
                                               'setting approval !')
    ]

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

    _sql_constraints = [
        ('user_model_uniq', 'unique (user_id, model_validation_id)',
         'The user already exist for this model approval !')
    ]

    @api.multi
    def _have_access(self):
        """
        This method guarantine user minimum have perm_write access on model
        :return: boolean
        """
        access_o = self.env['ir.model.access']
        access_ok = False
        for user_app in self:
            match_access = access_o.search([
                ('model_id', '=', user_app.model_validation_id.model_id.id),
                ('perm_write', '=', True)])
            groups_id = self.env['res.groups']
            for access in match_access:
                groups_id |= access.group_id

            groups_id = [g.id for g in groups_id]
            user_groups = [g.id for g in user_app.user_id.groups_id]
            is_intersection = list(set(groups_id) & set(user_groups))
            if is_intersection:
                access_ok = True
        return access_ok

    @api.model
    def create(self, values):
        res = super(ResUsersApproval, self).create(values)
        if not res._have_access():
            raise UserError(_(
                "%s don't have permission edit %s model !" %
                (res.user_id.name, res.model_validation_id.model_id.model)))
        return res

    @api.multi
    def write(self, values):
        res = super(ResUsersApproval, self).write(values)
        if not self._have_access():
            raise UserError(_("Some users don't have permission edit on "
                              "model approval !"))
        return res
