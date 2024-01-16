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
			"fieldname": "employee",
			"label": "Officer Name",
			"fieldtype": "Link",
			"options": "Employee",
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
            Roster.employee,
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
























































# def get_data(filters):

# 	Roster = frappe.qb.DocType("Roster")
# 	# write a query to fetch unique site names from roster between those dates
# 	query = (
# 	    frappe.qb.from_(Roster)
# 	    .select(
# 	        Roster.site
# 	    )
# 	    .where(
# 	        (Roster.docstatus == docstatus_dict.get(filters.docstatus))
# 	        & (Roster.attendance_date >= filters.from_date)
# 	        & (Roster.attendance_date <= filters.to_date)
# 	    ).groupby(Roster.site)
# 	)
# 	# run the query and get the data in a variable
# 	sites = query.run(as_dict=1)
# 	# fetch roster data as before but site be site and let's say if there are two sites then we should have first site data and second site data
# 	# return that data to the report
# 	# Fetch roster data for each site
# 	frappe.log_error(message=str(sites),title="sites")
# 	site_data = []
# 	for site in sites:
# 		site_data.append(get_site_data(site.site, filters))
# 		# complete the function get_site_data
# 	# return site_data
# 	frappe.log_error(message=str(site_data),title="sites data")
# 	return site_data

# def get_site_data(site, filters):
#     Roster = frappe.qb.DocType("Roster")
    
#     # write a query to fetch data for the given site between specified dates
#     query = (
#         frappe.qb.from_(Roster)
#         .select(
# 			Roster.site,
# 			Roster.employee,
# 			Roster.attendance_date,
# 			Roster.shift_start_time,
# 			Roster.shift_end_time,
# 			Roster.hours,
#         )
#         .where(
#             (Roster.docstatus == docstatus_dict.get(filters.docstatus))
#             & (Roster.attendance_date >= filters.from_date)
#             & (Roster.attendance_date <= filters.to_date)
#             & (Roster.site == site)
#         )
#     )
    
#     # run the query and get the data in a variable
#     site_data = query.run(as_dict=1)
#     frappe.log_error(message=str(site_data),title="site data_func")
	
#     return site_data

# 	# query = (
# 	# 	frappe.qb.from_(Roster)
# 	# 	.select(
# 	# 		Roster.site,
# 	# 		Roster.employee,
# 	# 		Roster.attendance_date,
# 	# 		Roster.shift_start_time,
# 	# 		Roster.shift_end_time,
# 	# 		Roster.hours,
# 	# 	)
# 	# 	.where(
# 	# 		(Roster.docstatus == docstatus_dict.get(filters.docstatus))
# 	# 		& (Roster.site == filters.site)
# 	# 		& (Roster.attendance_date >= filters.from_date)
# 	# 		& (Roster.attendance_date <= filters.to_date)
# 	# 	)
# 	# )

# 	# return query.run(as_dict=1)



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