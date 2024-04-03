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

def get_site_data(site, filters):
    Roster = frappe.qb.DocType("Roster")
    
    query = (
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
            (Roster.docstatus == docstatus_dict.get(filters.docstatus))
            & (Roster.attendance_date >= filters.from_date)
            & (Roster.attendance_date <= filters.to_date)
            & (Roster.site == site)
            & (Roster.customer == filters.customer)
        )
    )
    
    site_data = query.run(as_dict=1)
    
    return site_data

def get_data(filters,columns):
    Roster = frappe.qb.DocType("Roster")
    
    sites_query = (
        frappe.qb.from_(Roster)
        .select(Roster.site)
        .where(
            (Roster.docstatus == docstatus_dict.get(filters.docstatus)) &
            (Roster.attendance_date >= filters.from_date) &
            (Roster.attendance_date <= filters.to_date) &
            (Roster.customer == filters.customer)
        )
        .groupby(Roster.site)
    )
    sites = sites_query.run(as_dict=1)
    
    report_data = []
    
    for site in sites:
        site_data = get_site_data(site['site'], filters)
        report_data.extend(site_data)
        
        total_hours = sum(entry.get('hours', 0) for entry in site_data)
        report_data.append({
            "site":site['site'],
            "employee_name": "Total hours",
            "is_total": True,
            "colspan": len(columns),
            "hours": total_hours
        })

    return report_data