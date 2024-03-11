// Copyright (c) 2024, Ameer Muavia Shah and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Time Sheet', {
    // refresh: function(frm) {

    // }
	validate: function (frm) {
		calculateAmountAndHours(frm);
	}
});

frappe.ui.form.on('Employee Timesheet Detail', {
    rate: function (frm, cdt, cdn) {
        updateAmount(frm, cdt, cdn);
    },
    hours: function (frm, cdt, cdn) {
        updateAmount(frm, cdt, cdn);
    },
});

function updateAmount(frm, cdt, cdn) {
    const child_row = locals[cdt][cdn];
    if (child_row.rate && child_row.hours) {
        frappe.model.set_value(cdt, cdn, 'amount', child_row.hours * child_row.rate);
    }
    frm.refresh_field('details');
    calculateAmountAndHours(frm);
}

function calculateAmountAndHours(frm) {
    var totalAmount = 0;
    var totalHours = 0;
    frm.doc.details.forEach((d) => {
        totalAmount += d.amount;
        totalHours += d.hours;
    });
    frm.set_value('total_amount', totalAmount);
    frm.set_value('total_hours', totalHours);
    frm.refresh_field('total_amount');
    frm.refresh_field('total_hours');
}
