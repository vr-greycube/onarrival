// Copyright (c) 2022, GreyCube Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Mapped Suppliers Customers"] = {
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
	]
};
