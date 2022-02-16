// Copyright (c) 2022, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('OnArrival Settings', {
	refresh: function (frm) {
		frm.set_query("only_for_customer", function () {
			return {
				query: "onarrival.onarrival.doctype.onarrival_settings.onarrival_settings.get_customer_supplier",
				filters: {
					'party_type': 'customer'
				}
			};
		});

		frm.set_query("only_for_supplier", function () {
			return {
				query: "onarrival.onarrival.doctype.onarrival_settings.onarrival_settings.get_customer_supplier",
				filters: {
					'party_type': 'supplier'
				}
			};
		});

	},

	generate_sales_invoice: function (frm) {
		return frappe.call({
			method: 'make_invoice',
			doc: frm.doc,
			freeze: true,
			callback: (r) => {
				frm.reload_doc()
			},
			error: (r) => {
				frappe.show_alert("Something went wrong please try again");
			}
		});
	}
});
