# -*- coding: utf-8 -*-
"""
Model approval settings
"""
from openerp import fields, models


class IrModel(models.Model):
    _inherit = 'ir.model'

    need_approval = fields.Boolean('Model need approval', default=False)
