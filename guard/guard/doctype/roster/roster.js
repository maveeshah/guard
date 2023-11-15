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
		})	
	}
});
