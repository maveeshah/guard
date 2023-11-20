frappe.ui.form.on("Sales Invoice", {
  refresh(frm) {
    if (frm.doc.docstatus === 0 && !frm.doc.is_return) {
      frm.add_custom_button(__("Fetch Rooster"), function () {
        let d = new frappe.ui.Dialog({
          title: __("Fetch Rooster"),
          fields: [
            {
              label: __("Customer"),
              fieldname: "customer",
              fieldtype: "Link",
              options: "Customer",
              default: frm.doc.customer,
            },
            {
              fieldtype: "Column Break",
              fieldname: "col_break_1",
            },
            {
              label: __("Project"),
              fieldname: "project",
              fieldtype: "Link",
              options: "Project",
              default: frm.doc.project,
            },
            {
                fieldtype: "Section Break",
                fieldname: "sec_break_1",
              },
            {
              label: __("From"),
              fieldname: "from_time",
              fieldtype: "Date",
              reqd: 1,
            },
            {
              fieldtype: "Column Break",
              fieldname: "col_break_1",
            },
            {
              label: __("To"),
              fieldname: "to_time",
              fieldtype: "Date",
              reqd: 1,
            },
          ],
          primary_action: function () {
            const data = d.get_values();
            frm.events.add_timesheet_data(frm, {
              from_time: data.from_time,
              to_time: data.to_time,
              project: data.project,
            });
            d.hide();
          },
          primary_action_label: __("Get Roster"),
        });
        d.show();
      });
    }
  },
});
