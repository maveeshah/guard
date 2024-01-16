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
    
    # write a query to fetch data for the given site between specified dates
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
        )
    )
    
    site_data = query.run(as_dict=1)
    
    return site_data

def get_data(filters):
    Roster = frappe.qb.DocType("Roster")
    # write a query to fetch unique site names from roster between those dates
    query = (
        frappe.qb.from_(Roster)
        .select(
            Roster.site
        )
        .where(
            (Roster.docstatus == docstatus_dict.get(filters.docstatus))
            & (Roster.attendance_date >= filters.from_date)
            & (Roster.attendance_date <= filters.to_date)
            & (Roster.customer <= filters.customer)
        ).groupby(Roster.site)
    )
    frappe.log_error(message=query, title="Weekly Report Query")
    # run the query and get the data in a variable
    sites = query.run(as_dict=1)
    frappe.log_error(message=sites, title="Sites Data")
    
    # fetch roster data for each site
    site_data = []
    for site in sites:
        # convert the result of get_site_data to a list of dictionaries
        site_data.append(list(get_site_data(site.site, filters)))
    
    # Flatten the nested lists
    site_data = [item for sublist in site_data for item in sublist]
    
    return site_data