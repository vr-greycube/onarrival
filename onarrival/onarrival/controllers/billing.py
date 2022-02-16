# Copyright (c) 2022, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import cint, get_link_to_form, unique, nowdate

from frappe.model.document import Document
import itertools
from erpnext import get_default_company
from erpnext.accounts.party import get_party_details
from erpnext.stock.get_item_details import get_price_list_rate_for


def make_invoice(from_date, to_date, only_for_customer=None, only_for_supplier=None):
    '''
    create invoice for date range, customer, supplier
    '''

    filters = []
    if only_for_customer:
        filters.append("oal.customer = %(customer)s")
    if only_for_supplier:
        filters.append("oal.customer = %(supplier)s")

    filters = filters and " and " + " and ".join(filters) or ""

    args = {
        "from_date": from_date,
        "to_date": to_date,
        "customer": only_for_customer,
        "supplier": only_for_supplier
    }

    billing = frappe.db.sql("""
        select 
            item_code, item_name, customer, supplier, count(name) qty
        from 
            `tabOnArrival API Log` oal
        where 
            oal.is_billed = 0
            and oal.transaction_date_time between %(from_date)s and %(to_date)s 
            {}
        group by 
             oal.customer, oal.supplier, oal.item_code, oal.item_name
    """.format(filters), args, as_dict=True)

    if not billing:
        frappe.msgprint(
            "No transactions found to generate invoice within dates {from_date} and {to_date}.".format(**args))

    invoices = []
    for customer, group in itertools.groupby(billing, key=lambda x: (x['customer'])):
        si_doc = frappe.get_doc({
            "doctype": "Sales Invoice",
            "due_date": nowdate(),
            "customer": customer,
            "company": get_default_company(),
        })
        item_rates = get_items_rate(billing, customer)
        for d in group:
            item = si_doc.append("items", {
                "item_code": d["item_code"],
                "warehouse": "",
                "qty": d["qty"],
                "rate": item_rates.get(d["item_code"]),
                "income_account": None,
                "expense_account": None,
                "cost_center": None,
            })
        si_doc.set_missing_values()
        si_doc.insert()
        invoices.append(get_link_to_form("Sales Invoice", si_doc.name))

    if invoices:
        frappe.msgprint("Invoices have been generated: %s" %
                        (", ".join(invoices)))


def get_customer_details(customer):
    customer_details = get_party_details(party=customer, party_type="Customer")
    customer_details.update({
        "company": get_default_company(),
        "price_list": customer_details.get("selling_price_list")
    })

    return customer_details


def get_item_price(item_code, customer=None):
    customer_details = get_customer_details(customer)
    return get_price_list_rate_for(customer_details, item_code) or 0.0


def get_items_rate(items, customer):
    customer_details = get_customer_details(customer)
    out = dict()

    missing = []
    for d in items:
        rate = get_price_list_rate_for(
            customer_details, d["item_code"]) or 0.0
        if not cint(rate):
            missing.append(
                "{} - ({})".format(get_link_to_form("Item", d["item_code"], d["item_name"]), d["supplier"]))
        else:
            out[d.get("item_code")] = rate

    if missing:
        missing = "<ul>" + "".join(["<li>%s</li>" %
                                   d for d in unique(missing)]) + "</ul>"
        frappe.throw("Please set the pricing for %s for these items to generate invoice: <br> %s" % (
            frappe.bold(get_link_to_form("Customer", customer)), missing))
    return out
