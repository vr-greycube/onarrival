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
			transaction_date_time , toal.customer , cu.customer_group,  
			toal.supplier , toal.item_code , toal.item_name , toal.status , 
			toal.supplier_charge , toal.to_bill , toal.billed 
		from `tabOnArrival API Log` toal
		inner join tabCustomer cu on cu.name = toal.customer
				{conditions}
        """.format(conditions=conditions), filters, as_dict=True, )

    return data


def get_columns(filters):
    columns = [
        {
            "label": _("Transaction Date"),
            "fieldtype": "Date",
            "fieldname": "transaction_date_time",
            "width": 180
        },
        {
            "label": _("Customer"),
            "fieldtype": "Link",
            "fieldname": "customer",
            "options": "Customer",
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
            "label": _("Customer Group"),
            "fieldname": "customer_group",
            "width": 220
        },
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "width": 220
        },
        {
            "label": _("Supplier Charge"),
            "fieldname": "supplier_charge",
            "fieldtype": "Currency",
            "width": 140
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "width": 150
        },
        {
            "label": _("To Bill"),
            "fieldname": "to_bill",
            "fieldtype": "Check",
            "width": 90
        },
        {
            "label": _("Billed"),
            "fieldname": "billed",
            "fieldtype": "Check",
            "width": 120
        },
        # {
        #     "label": _("Sales Invoice"),
        #     "fieldtype": "Link",
        #     "fieldname": "invoice",
        #     "options": "Sales Invoice",
        #     "width": 200
        # },
    ]

    return columns


def get_conditions(filters):
    conditions = []

    if filters.from_date:
        conditions.append("toal.transaction_date_time >= %(from_date)s")
    if filters.to_date:
        conditions.append("toal.transaction_date_time <= %(to_date)s")

    if filters.customer:
        conditions.append("toal.customer = %(customer)s")
    if filters.supplier:
        conditions.append("toal.supplier = %(supplier)s")

    return conditions and " where " + " and ".join(conditions) or ""
