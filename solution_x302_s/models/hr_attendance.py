# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime
import requests
import re
import logging
_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    """ Add user id machine in employee """
    _inherit = 'hr.employee'

    x302_s_user_id = fields.Integer('User ID in machine', help="Solution type X302-S User ID.")


class HrAttendance(models.Model):
    """ Cron to read and update attendance in odoo """
    _inherit = 'hr.attendance'

    @api.model
    def sync_attendance(self):
        """ sync 1 direction machine to odoo """
        def get_data_from_x302_s(self, date, x302_user_id):
            r = requests.session()
            datas = {
                'sdate': date, 'edate': date, 
                'uid': x302_user_id}
            block = []
            try:
                response = r.post('http://172.16.5.14/form/Download',data=datas, stream=True)
                block = response.text.split('\n')
            except:
                # Failed to connect machine 
                pass
            return block
        
        today = fields.date.today()
        emp_obj = self.env['hr.employee']
        attendance_obj = self.env['hr.attendance']
        # search employee who registered on machine
        emp_ids = emp_obj.search([('x302_s_user_id', '!=', 0)])
        print(emp_ids)
        today_attendance = attendance_obj.search([('check_in', '>=', str(today) + " 00:00:00")])
        regex = re.compile(r'[\n\r\t]') # remove 3 character
        for emp_id in emp_ids:
            emp_attendance = today_attendance.filtered(lambda x: x.employee_id.id == emp_id.id)
            if not emp_attendance:
                block = get_data_from_x302_s(self, date=today, x302_user_id=emp_id.x302_s_user_id)
                if len(block) == 0:
                    continue
                block.pop()
                last_idx = len(block) - 1
                _logger.debug("Check block => "+str(block))
                idx = 0
                while(idx <= last_idx):
                    row = regex.sub(' ', block[idx])
                    row = row.split(' ')
                    _logger.debug(row)
                    if row[5] == '0':
                        _logger.debug("Create check in for "+ emp_id.name)
                        respone = attendance_obj.create({
                            'employee_id': emp_id.id,
                            'check_in': row[2] + " " +row[3],
                        })
                        _logger.info("Succeed with ID : "+ str(respone.id))
                        break
                    # How if user create manual and only fill check out for today ?
            else:
                _logger.debug("UPDATE EXISTING ATTENDANCE")
                block = get_data_from_x302_s(self, date=today, x302_user_id=emp_id.x302_s_user_id)
                if len(block) == 0:
                    continue
                block.pop()
                last_idx = len(block) - 1
                while(last_idx > -1):
                    row = regex.sub(' ', block[last_idx])
                    row = row.split(' ')
                    _logger.debug(row)
                    if row[5] == '1':
                        respone = emp_attendance[0].write({
                            'check_out': row[2] + " " +row[3],
                        })
                        break
                    last_idx -= 1