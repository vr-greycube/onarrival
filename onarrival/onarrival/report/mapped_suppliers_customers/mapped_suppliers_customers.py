# Copyright (c) 2022, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    return get_columns(filters), get_data(filters)


def get_data(filters):

    conditions = get_conditions(filters)
    data = frappe.db.sql(
        """
			select 
				tcsim.customer, tc.customer_group, 
				tcsim.supplier, sup.customer_group supplier_group,
                date(tcsim.creation) creation 
			from 
				`tabCustomer Supplier Item Mapping` tcsim 
				inner join tabCustomer tc on tc.name = tcsim.customer
				inner join tabCustomer sup on sup.name = tcsim.supplier
				{conditions}
			group by 
				tcsim.customer, tc.customer_group, tcsim.supplier, sup.customer_group
			order by 
				tcsim.customer, tc.customer_group, tcsim.supplier, sup.customer_group
        """.format(conditions=conditions), filters, as_dict=True, )

    return data


def get_columns(filters):
    columns = [
        {
            "label": _("Customer"),
            "fieldtype": "Link",
            "fieldname": "customer",
            "options": "Customer",
            "width": 220
        },
        {
            "label": _("Customer Group"),
            "fieldname": "customer_group",
            "width": 220
        },
        {
            "label": _("Supplier"),
            "fieldtype": "Link",
            "fieldname": "supplier",
            "options": "Customer",
            "width": 220
        },
        {
            "label": _("Supplier Group"),
            "fieldname": "supplier_group",
            "width": 220
        },
        {
            "label": _("Creation"),
            "fieldtype": "Date",
            "fieldname": "creation",
            "width": 220
        },
    ]

    return columns


def get_conditions(filters):
    conditions = []

    if filters.customer:
        conditions.append("tcsim.customer = %(customer)s")
    if filters.supplier:
        conditions.append("tcsim.supplier = %(supplier)s")

    return conditions and " where " + " and ".join(conditions) or ""
