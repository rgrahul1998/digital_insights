import frappe
from insights.api.queries import create_query


@frappe.whitelist(allow_guest=True)
def create_new_query(**kwargs):    
    insights_query = create_query(is_assisted_query=1)
    return insights_query
