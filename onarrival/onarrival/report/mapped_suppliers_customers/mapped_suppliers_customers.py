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
				toal.customer, tc.customer_group, 
				toal.supplier, sup.customer_group supplier_group
			from 
				`tabOnArrival API Log` toal 
				inner join tabCustomer tc on tc.name = toal.customer
				inner join tabCustomer sup on sup.name = toal.supplier
				{conditions}
			group by 
				toal.customer, tc.customer_group, toal.supplier, sup.customer_group
			order by 
				toal.customer, tc.customer_group, toal.supplier, sup.customer_group
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
    ]

    return columns


def get_conditions(filters):
    conditions = []

    if filters.customer:
        conditions.append("toal.customer = %(customer)s")
    if filters.supplier:
        conditions.append("toal.supplier = %(supplier)s")

    return conditions and " where " + " and ".join(conditions) or ""
