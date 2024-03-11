// Copyright (c) 2024, Ameer Muavia Shah and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Time Sheet', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Employee Timesheet Detail', {
	rate: function (frm, cdt, cdn) {
		const child_row = locals[cdt][cdn];
		if (child_row.rate && child_row.hours) {
			frappe.model.set_value(cdt, cdn, 'amount', child_row.hours * child_row.rate);
		}
		frm.refresh_field('details');
	},
	hours: function (frm, cdt, cdn) {
		const child_row = locals[cdt][cdn];
		if (child_row.rate && child_row.hours) {
			frappe.model.set_value(cdt, cdn, 'amount', child_row.hours * child_row.rate);
		}
		frm.refresh_field('details');
	},
});
