# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import requests


class HrAttendance(models.Model):
    _inherit = 'hr.employee'

    x302_s_user_id = fields.Integer('User ID in machine', help="Solution type X302-S User ID.")

    def sync_attendance(self):
        """
        0 -> pulang
        1 -> masuk
        data_today <- get all data from machine
        # data type <- {user_id_machine: {'check_in': x, 'check_out': y}, ..., 
        # {}}
        employees <- all_active_employee()
        for emp in employees:
            
        """
        r = requests.session()
        datas = {'sdate': '2017-12-27','edate': '2017-12-27', 'uid': 3}
        # datas = {}
        response = r.post('http://172.16.5.11/form/Download',data=datas, stream=True)
        block = response.text.split('\n')
        print(block[0].split('\t')[0])
        for elmt in range(len(block)):
            print(elmt+1, block[elmt])
