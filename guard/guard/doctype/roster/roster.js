// Copyright (c) 2023, Ameer Muavia Shah and contributors
// For license information, please see license.txt

frappe.ui.form.on('Roster', {
	refresh: function(frm) {
		frm.set_query('site', () => {
			if (frm.doc.customer) {
				return {
					filters: {
						customer: frm.doc.customer
					}
				}				
			}
		});

	},
	staff: function (frm) {
		if (frm.doc.staff) {
			if (frm.doc.staff == "Employee"){
					frm.doc.subcontractor == ''
			}
			else if (frm.doc.staff == "Subcontractor"){
				frm.doc.employee == ''
		}
		}
	}

});
