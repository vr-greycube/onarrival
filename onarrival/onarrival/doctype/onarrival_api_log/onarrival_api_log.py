# Copyright (c) 2022, GreyCube Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from onarrival.onarrival.controllers.billing import get_item_price


class OnArrivalAPILog(Document):
    def on_update(self):
        pass
        # make error log if item_price is missing
        if not get_item_price(self.item_code, self.customer):
            frappe.log_error("Item Price missing for %s: %s " %
                             (self.customer, self.item_name), "Item Price Missing")

        # maybe notify user notification ?
