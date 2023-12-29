# Copyright (c) 2023, Ameer Muavia Shah and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "site",
			"label": "Site Name",
			"fieldtype": "Link",
			"options": "Site",
			"width": 300
		},
		{
			"fieldname": "employee",
			"label": "Officer Name",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 200
		},
		{
			"fieldname": "attendance_date",
			"label": "Date",
			"fieldtype": "Date",
			"width": 200
		},
		{
			"fieldname": "shift_start_time",
			"label": "Start Time",
			"fieldtype": "Time",
			"width": 155
		},
				{
			"fieldname": "shift_end_time",
			"label": "Finish Time",
			"fieldtype": "Time",
			"width": 155
		},
		{
			"fieldname": "hours",
			"label": "Hours",
			"fieldtype": "Float",
			"width": 155
		},

	]

docstatus_dict = {
	"Submitted": 1,
	"Cancelled": 2,
	"Draft": 0
}
def get_data(filters):
	Roster = frappe.qb.DocType("Roster")
	query = (
		frappe.qb.from_(Roster)
		.select(
			Roster.site,
			Roster.employee,
			Roster.attendance_date,
			Roster.shift_start_time,
			Roster.shift_end_time,
			Roster.hours,
		)
		.where(
			(Roster.docstatus == docstatus_dict.get(filters.docstatus))
			& (Roster.site == filters.site)
			& (Roster.attendance_date >= filters.from_date)
			& (Roster.attendance_date <= filters.to_date)
		)
	)

	return query.run(as_dict=1)



# Attendance = frappe.qb.DocType("Attendance")
# query = (
# 	frappe.qb.from_(Attendance)
# 	.select(
# 		Attendance.employee,
# 		Extract("day", Attendance.attendance_date).as_("day_of_month"),
# 		Attendance.status,
# 		Attendance.shift,
# 	)
# 	.where(
# 		(Attendance.docstatus == 1)
# 		& (Attendance.company == filters.company)
# 		& (Extract("month", Attendance.attendance_date) == filters.month)
# 		& (Extract("year", Attendance.attendance_date) == filters.year)
# 	)
# )

# if filters.employee:
# 	query = query.where(Attendance.employee == filters.employee)
# query = query.orderby(Attendance.employee, Attendance.attendance_date)

# return query.run(as_dict=1)