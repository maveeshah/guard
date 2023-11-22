# Copyright (c) 2023, Ameer Muavia Shah and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class Roster(Document):
	pass


@frappe.whitelist()
def get_customerwise_roster_data(customer=None, 
								 from_time=None, to_time=None,
								  price_list=None, company=None):
	condition = ""
	if customer:
		condition += "AND r.customer = %(customer)s "
	if from_time and to_time:
		condition += "AND r.attendance_date BETWEEN %(from_time)s AND %(to_time)s"

	query = f"""
		SELECT
			r.name as name,
			r.item as item,
			r.hours as quantity,
			i.item_name as item_name,
			i.description as description,
			i.stock_uom as uom,
			c.default_income_account as income_account,
			(
				SELECT ip.price_list_rate
				FROM `tabItem Price` ip
				WHERE ip.item_code = r.item
				AND ip.price_list = %(price_list)s
				ORDER BY ip.creation DESC
				LIMIT 1
			) as rate
		FROM `tabRoster` r
		INNER JOIN `tabItem` as i ON r.item = i.name
		LEFT JOIN `tabCompany` as c ON c.name = %(company)s
		WHERE r.docstatus = 1
			{condition}
		ORDER BY r.attendance_date ASC
	"""

	filters = {
		"customer": customer, 
		"from_time": from_time, 
		"to_time": to_time, 
		"price_list": price_list,
		"company": company  # replace with the actual company name
	}


	# filters = {"customer": customer}
	# AND is_billable = 1
	# AND sales_invoice is NULL
	return frappe.db.sql(query, filters, as_dict=1)
