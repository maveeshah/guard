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

#
def get_data(filters,columns):
    Roster = frappe.qb.DocType("Roster")
    
    # Fetch unique site names from the Roster between the specified dates
    sites_query = (
        frappe.qb.from_(Roster)
        .select(Roster.site)
        .where(
            (Roster.docstatus == docstatus_dict.get(filters.docstatus)) &
            (Roster.attendance_date >= filters.from_date) &
            (Roster.attendance_date <= filters.to_date) &
            (Roster.customer <= filters.customer)
        )
        .groupby(Roster.site)
    )
    sites = sites_query.run(as_dict=1)
    
    # Initialize an empty list to hold all the data
    report_data = []
    
    # Loop through each site and fetch the detailed data
    for site in sites:
        # Insert a header row for the new site
        # report_data.append({
        #     "site": "Timesheet for " + site['site'],
        #     "is_header": True,  # This is used to indicate a header row for the frontend
        #     "colspan": len(columns)  # Assuming 'columns' is the list of all columns
        # })
        # report_data.append({
        #     "site": "Timesheet for " + site['site'],
        #     "employee_name": "",
        #     "attendance_date": "",
        #     "shift_start_time": "",
        #     "shift_end_time": "",
        #     "hours": ""
        # })
        
        # Fetch data for the current site
        site_data = get_site_data(site['site'], filters)
        report_data.extend(site_data)  # Add the site's data to the report
        
        # Calculate the total hours for the site
        total_hours = sum(entry.get('hours', 0) for entry in site_data)
        # Insert a totals row after the site's data
        # report_data.append({
        #     "site": "Total for " + site['site'],
        #     "employee_name": "",
        #     "attendance_date": "",
        #     "shift_start_time": "",
        #     "shift_end_time": "",
        #     "hours": total_hours
        # })
        report_data.append({
            "site":site['site'],
            "employee_name": "Total hours",
            "is_total": True,  # This is used to indicate a totals row for the frontend
            "colspan": len(columns),  # Same here for the number of columns to span
            "hours": total_hours
        })

    return report_data


#  def get_data(filters):
#     Roster = frappe.qb.DocType("Roster")
#     # write a query to fetch unique site names from roster between those dates
#     query = (
#         frappe.qb.from_(Roster)
#         .select(
#             Roster.site
#         )
#         .where(
#             (Roster.docstatus == docstatus_dict.get(filters.docstatus))
#             & (Roster.attendance_date >= filters.from_date)
#             & (Roster.attendance_date <= filters.to_date)
#             & (Roster.customer <= filters.customer)
#         ).groupby(Roster.site)
#     )
#     # run the query and get the data in a variable
#     sites = query.run(as_dict=1)
#     previous_site = None    
#     # fetch roster data for each site
#     site_data = []
#     for site in sites:
#         # convert the result of get_site_data to a list of dictionaries
#         site_data.append(list(get_site_data(site.site, filters)))
    
#     # Flatten the nested lists
#     site_data = [item for sublist in site_data for item in sublist]
    
#     return site_data