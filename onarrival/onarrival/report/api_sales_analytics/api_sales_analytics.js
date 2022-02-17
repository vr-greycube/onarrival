// Copyright (c) 2022, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["API Sales Analytics"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname": "supplier",
			"fieldtype": "Link",
			"label": __("Supplier"),
			"options": "Customer",
			"reqd": 1,
			"get_query": function () {
				return {
					query: "onarrival.onarrival.doctype.onarrival_settings.onarrival_settings.get_customer_supplier",
					filters: {
						'party_type': 'supplier'
					}
				};
			}
		},
		{
			"fieldname": "customer",
			"fieldtype": "Link",
			"label": __("Customer"),
			"options": "Customer",
			"get_query": function () {
				return {
					query: "onarrival.onarrival.doctype.onarrival_settings.onarrival_settings.get_customer_supplier",
					filters: {
						'party_type': 'customer'
					}
				};
			}
		},

	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (data && column.fieldname == "item_name") {
			value = frappe.utils.get_form_link('Item', data.item_code, true, value)
		}
		return value;
	},
};
