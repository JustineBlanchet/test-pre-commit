from odoo import models, api, _
from datetime import datetime, time
from math import ceil
from odoo.addons.resource.models.utils import HOURS_PER_DAY

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    def _create_patch_calendar_omydoo(self):
            self.env['resource.calendar'].create({ 
                'name': 'patch_calendar_omydoo',
                'attendance_ids': [
                    (0, 0, {'name': 'Monday', 'dayofweek': '0', 'hour_from': 0, 'hour_to': 23.99}),
                    (0, 0, {'name': 'Tuesday', 'dayofweek': '1', 'hour_from': 0, 'hour_to': 23.99}),
                    (0, 0, {'name': 'Wednesday', 'dayofweek': '2', 'hour_from': 0, 'hour_to': 23.99}),
                    (0, 0, {'name': 'Thursday', 'dayofweek': '3', 'hour_from': 0, 'hour_to': 23.99}),
                    (0, 0, {'name': 'Friday', 'dayofweek': '4', 'hour_from': 0, 'hour_to': 23.99}),
                    (0, 0, {'name': 'Saturday', 'dayofweek': '5', 'hour_from': 0, 'hour_to': 23.99}),
                    (0, 0, {'name': 'Sunday', 'dayofweek': '6', 'hour_from': 0, 'hour_to': 23.99}),
                ]
            })
            calendar = self.env['resource.calendar'].search([('name', '=', 'patch_calendar_omydoo')], limit=1)
            return calendar                   
                        
    def _get_duration(self, check_leave_type=True, resource_calendar=None):
        self.ensure_one()
        
        if self.holiday_status_id.time_type == 'other':
            resource_calendar = self.env['resource.calendar'].search([('name', '=', 'patch_calendar_omydoo')], limit=1)
            if not resource_calendar:
                resource_calendar = self._create_patch_calendar_omydoo()
        
        resource_calendar = resource_calendar or self.resource_calendar_id

        if not self.date_from or not self.date_to or not resource_calendar:
            return (0, 0)
        hours, days = (0, 0)
        if self.employee_id:
            # We force the company in the domain as we are more than likely in a compute_sudo
            domain = [('time_type', '=', 'leave'),
                      ('company_id', 'in', self.env.companies.ids + self.env.context.get('allowed_company_ids', [])),
                      # When searching for resource leave intervals, we exclude the one that
                      # is related to the leave we're currently trying to compute for.
                      '|', ('holiday_id', '=', False), ('holiday_id', '!=', self.id)]
            if self.leave_type_request_unit == 'day' and check_leave_type:
                # list of tuples (day, hours)
                work_time_per_day_list = self.employee_id.list_work_time_per_day(self.date_from, self.date_to, calendar=resource_calendar, domain=domain)
                days = len(work_time_per_day_list)
                hours = sum(map(lambda t: t[1], work_time_per_day_list))
            else:
                work_days_data = self.employee_id._get_work_days_data_batch(self.date_from, self.date_to, domain=domain, calendar=resource_calendar)[self.employee_id.id]
                hours, days = work_days_data['hours'], work_days_data['days']
        else:
            today_hours = resource_calendar.get_work_hours_count(
                datetime.combine(self.date_from.date(), time.min),
                datetime.combine(self.date_from.date(), time.max),
                False)
            hours = resource_calendar.get_work_hours_count(self.date_from, self.date_to)
            days = hours / (today_hours or HOURS_PER_DAY)
        if self.leave_type_request_unit == 'day' and check_leave_type:
            days = ceil(days)
        return (days, hours)
