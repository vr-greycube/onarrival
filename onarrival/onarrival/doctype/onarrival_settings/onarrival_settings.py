# Copyright (c) 2022, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import cint
from frappe.model.document import Document
import itertools
from onarrival.onarrival.controllers.billing import make_invoice


class OnArrivalSettings(Document):
    @frappe.whitelist()
    def make_invoice(self):
        return make_invoice(self.from_date, self.to_date,
                            self.only_for_customer, self.only_for_supplier)


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_customer_supplier(doctype, txt, searchfield, start, page_len, filters):
    supplier_customer_group = frappe.db.get_single_value(
        "OnArrival Settings", "supplier_customer_group")

    supplier_filter = filters.get(
        'party_type') == 'supplier' and ' in ' or ' not in '

    return frappe.db.sql("""
    select name, concat(customer_group, ', ', territory)
    from `tabCustomer`
    where disabled = 0 and customer_group {supplier_filter}
    (
        select child.name
        from `tabCustomer Group` cg
        inner join `tabCustomer Group` child on child.lft >= cg.lft and child.rgt <= cg.rgt
        where cg.name = %(supplier_customer_group)s
    )
    and `{key}` LIKE %(txt)s
    order by name limit %(start)s, %(page_len)s""".format(key=searchfield, supplier_filter=supplier_filter), {
        'txt': '%' + txt + '%',
        'start': start, 'page_len': page_len,
        'supplier_customer_group': supplier_customer_group
    })
