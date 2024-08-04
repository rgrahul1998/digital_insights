import frappe


@frappe.whitelist(allow_guest=True)
def create_request_demo(**kwargs):
    request_demo_doc = frappe.get_doc(
        {
            "doctype": "Request Demo",
            "work_email":  kwargs.get("work_email"),
            "name1": kwargs.get("name"),
            "company": kwargs.get("company"),
            "contact_no": kwargs.get("contact_no"),
            "country": kwargs.get("country"),
            "description": kwargs.get("description"),
        }
    )
    request_demo_doc.insert(ignore_permissions=True)


    return {
        "status": "success",
        "message": "Request Submitted."
    }