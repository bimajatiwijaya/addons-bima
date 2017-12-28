# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime
import requests
import re
import logging
_logger = logging.getLogger(__name__)


class HrAttendance(models.Model):
    _inherit = 'hr.employee'

    x302_s_user_id = fields.Integer('User ID in machine', help="Solution type X302-S User ID.")

    @api.multi
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
        def get_data_from_x302_s(self, date, x302_user_id):
            r = requests.session()
            datas = {
                'sdate': date, 'edate': date, 
                'uid': x302_user_id}
            block = []
            try:
                response = r.post('http://172.16.5.11/form/Download',data=datas, stream=True)
                _logger.debug("XXXXXXXXXXXXXXXXXX")
                _logger.debug(response.text)
                block = response.text.split('\n')
            except:
                # Failed to connect machine 
                pass
            return block
        
        today = fields.date.today()
        emp_obj = self.env['hr.employee']
        attendance_obj = self.env['hr.attendance']
        emp_ids = emp_obj.search([('x302_s_user_id', '!=', 0)])
        today_attendance = attendance_obj.search([('check_in', '>=', str(today) + " 00:00:00")])
        regex = re.compile(r'[\n\r\t]')
        for emp_id in emp_ids:
            emp_attendance = today_attendance.filtered(lambda x: x.employee_id.id == emp_id.id)
            if not emp_attendance:
                block = get_data_from_x302_s(self, date=today, x302_user_id=emp_id.x302_s_user_id)
                if len(block) == 0:
                    continue
                block.pop()
                last_idx = len(block) - 1
                _logger.debug(str(block))
                while(last_idx > -1):
                    row = regex.sub(' ', block[last_idx])
                    row = row.split(' ')
                    _logger.debug(row)
                    if row[5] == '0':
                        _logger.debug("Create check in for "+ emp_id.name)
                        respone = attendance_obj.create({
                            'employee_id': emp_id.id,
                            'check_in': row[2] + " " +row[3],
                        })
                        _logger.info("Succeed with ID : "+ str(respone.id))
                    # How if user create manual and only fill check out for today ?
                    last_idx -= 1
            else:
                _logger.debug(emp_attendance)
                _logger.debug("UPDATE ATTENDANCE")
