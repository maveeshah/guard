// Copyright (c) 2023, Ameer Muavia Shah and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Weekly Report"] = {
	"filters": [
		{
			fieldname: "site",
			label: __("Site Name"),
			fieldtype: "Link",
			options: "Site",
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			reqd: 1,
			default: frappe.datetime.add_days(frappe.datetime.nowdate(), -6),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.nowdate(),
			reqd: 1,
		},
		{
			fieldname: "docstatus",
			label: __("Document Status"),
			fieldtype: "Select",
			options: ["Submitted","Cancelled","Draft"],
			default: "Submitted",
			reqd: 1,
		},
	]
};
