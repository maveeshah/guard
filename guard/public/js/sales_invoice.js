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
              reqd: 1,
            },

            {
              fieldtype: "Column Break",
              fieldname: "col_break_1",
            },
            {
              label: __("Price List"),
              fieldname: "price_list",
              fieldtype: "Link",
              options: "Price List",
              default: "Standard Selling",
              reqd: 1,
              hidden: 1,
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
            frm.events.add_roster_data(frm, {
              from_time: data.from_time,
              to_time: data.to_time,
              customer: data.customer,
              price_list: data.price_list,
              company: frm.doc.company,
            });
            d.hide();
          },
          primary_action_label: __("Get Roster"),
        });
        d.show();
      });
    }
  },

  // customer: function (frm) {
  //   if (frm.doc.project) {
  //     frm.events.add_roster_data(frm, {
  //       project: frm.doc.project,
  //     });
  //   }
  // },

  async add_roster_data(frm, kwargs) {
    console.log(kwargs);
    if (kwargs === "Sales Invoice") {
      // called via frm.trigger()
      kwargs = Object();
    }

    if (!kwargs.hasOwnProperty("customer") && frm.doc.customer) {
      kwargs.customer = frm.doc.customer;
    }

    const rosters = await frm.events.get_roster_data(frm, kwargs);
    return frm.events.set_roster_data(frm, rosters);
  },

  async get_roster_data(frm, kwargs) {
    return frappe
      .call({
        method:
          "guard.guard.doctype.roster.roster.get_customerwise_roster_data",
        args: kwargs,
      })
      .then((r) => {
        if (!r.exc && r.message.length > 0) {
          return r.message;
        } else {
          return [];
        }
      });
  },

  set_roster_data: function (frm, rosters) {
    frm.clear_table("items");
    rosters.forEach(async (roster) => {
      frm.events.append_roster_item(frm, roster, 1.0);
    });
    frm.refresh_field("items");
    // frm.trigger("calculate_items_totals");
  },

  append_roster_item: function (frm, time_log, exchange_rate) {
    console.log(time_log);
    const row = frm.add_child("items");
    row.custom_roster = time_log.name;
    row.item_code = time_log.item;
    row.item_name = time_log.item_name;
    row.description = time_log.description;
    row.rate = time_log.rate;
    row.qty = time_log.quantity;
    row.uom = time_log.uom;
    row.amount = time_log.rate * time_log.quantity;
    row.income_account = time_log.income_account;
  },
});
