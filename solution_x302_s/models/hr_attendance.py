# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import requests


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    x302_s_user_id = fields.Integer('User ID in machine', help="Solution type X302 S ID User")

    def sync_attendance(self):
        """
        data_today <- get all data from machine
        # data type <- {user_id_machine: {'check_in': x, 'check_out': y}, ..., 
        # {}}
        employees <- all_active_employee()
        for emp in employees:
            
        """
