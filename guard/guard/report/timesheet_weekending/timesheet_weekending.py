# Copyright (c) 2023, Ameer Muavia Shah and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters,columns)

    return columns, data

def get_columns():
	return [
		{
			"fieldname": "site",
			"label": "Site Name",
			"fieldtype": "Data",
            "align": "left",
			"width": 300
		},
		{
			"fieldname": "employee_name",
			"label": "Officer Name",
			"fieldtype": "Data",
            "align": "left",
			"width": 200
		},
		{
			"fieldname": "attendance_date",
			"label": "Date",
			"fieldtype": "Date",
            "align": "left",
			"width": 200
		},
		{
			"fieldname": "shift_start_time",
			"label": "Start Time",
			"fieldtype": "Time",
            "align": "left",
			"width": 155
		},
				{
			"fieldname": "shift_end_time",
			"label": "Finish Time",
			"fieldtype": "Time",
            "align": "left",
			"width": 155
		},
		{
			"fieldname": "hours",
			"label": "Hours",
			"fieldtype": "Int",
			"width": 155,
            "align": "left",
		},

	]

docstatus_dict = {
	"Submitted": 1,
	"Cancelled": 2,
	"Draft": 0
}


def get_data(filters, columns):
    Roster = frappe.qb.DocType("Roster")

    sites_query = (
        frappe.qb.from_(Roster)
        .select(
            Roster.site,
            Roster.employee_name,
            Roster.attendance_date,
            Roster.shift_start_time,
            Roster.shift_end_time,
            Roster.hours,
        )
        .where(
            (Roster.docstatus == docstatus_dict.get(filters.docstatus)) &
            (Roster.attendance_date >= filters.from_date) &
            (Roster.attendance_date <= filters.to_date) &
            (Roster.customer == filters.customer)
        )
    )

    sites = sites_query.run(as_dict=1)

    # Calculate the total hours
    total_hours = sum([site['hours'] for site in sites if site['hours']])

    sites.append({
        "site": "Total Hours",
        "employee_name": "",
        "attendance_date": "",
        "shift_start_time": "",
        "shift_end_time": "",
        "hours": total_hours
    })

    return sites

