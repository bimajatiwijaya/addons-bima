# -*- coding: utf-8 -*-
"""
Model approval settings
"""
from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp.exceptions import UserError


class ResPartnerApproval(osv.osv):
    _name = 'res.partner.approval'

    _columns = {
        'user_id': fields.many2one('res.users', string='User'),
        'approved': fields.boolean(string='Approved'),
        'partner_id': fields.many2one('res.partner'),
    }

    _defaults = {
        'approved': False,
    }


class ResPartner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'active': fields.boolean('Active'),
        'users_approval': fields.one2many('res.partner.approval', 'partner_id', string='Users Approval'),
    }

    _defaults = {
        'active': False,
    }

    def approve(self, cr, uid, ids, context=None):
        model_app_o = self.pool.get('ir.model.approval')
        ir_model_obj = self.pool.get('ir.model')
        partner_model_id = ir_model_obj.search(cr, uid,
                                               [('model', '=', 'res.partner')],
                                               limit=1)
        partner_app_id = model_app_o.search(cr, uid, [
            ('model_id', '=', partner_model_id[0])], context=context)
        if not partner_app_id:
            raise UserError(_("Partner approval not active. Please contact "
                              "administrator."))
        partner_app_o = model_app_o.browse(cr, uid, partner_app_id,
                                           context=context)
        partner_users_approval = [u.user_id.id for u in
                                  partner_app_o.validator_ids]
        set_users_app = set(partner_users_approval)
        len_users_app = len(partner_users_approval)
        if uid in partner_users_approval:
            partner_o_ids = self.browse(cr, uid, ids, context=context)
            for partner in partner_o_ids:
                list_user_partner_app = []
                for app in partner.users_approval:
                    if app.approved:
                        list_user_partner_app.append(app.user_id.id)
                result = list(set_users_app & set(list_user_partner_app))
                if len(result) == len_users_app:
                    self.write(cr, uid, ids, {'active': True}, context=context)
                else:
                    self.write(cr, uid, ids, {
                        'users_approval': [(0, 0, {'user_id': uid,
                                                   'approved': True})]
                    }, context=context)
        else:
            raise UserError(_("You don't have access to approve partner. "
                              "Please contact administrator."))
