// Copyright (c) 2022, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Mapped Item Supplier"] = {
	"filters": [
		{
			"fieldname": "customer",
			"fieldtype": "Link",
			"label": __("Customer"),
			"options": "Customer",
			"reqd": 1,
			"get_query": function () {
				return {
					query: "onarrival.onarrival.doctype.onarrival_settings.onarrival_settings.get_customer_supplier",
					filters: {
						'party_type': 'customer'
					}
				};
			}
		},
		{
			"fieldname": "supplier",
			"fieldtype": "Link",
			"label": __("Supplier"),
			"options": "Customer",
			"get_query": function () {
				return {
					query: "onarrival.onarrival.doctype.onarrival_settings.onarrival_settings.get_customer_supplier",
					filters: {
						'party_type': 'supplier'
					}
				};
			}
		},
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (value && data && column.fieldname == "item_name") {
			value = frappe.utils.get_form_link('Item', data.item, true, value)
		}
		return value;
	},
};
