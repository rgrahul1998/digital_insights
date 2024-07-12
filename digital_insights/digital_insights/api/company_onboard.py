import frappe


@frappe.whitelist(allow_guest=True)
def create_company_onboard_api(**kwargs):
    if frappe.db.exists("Company Onboard", {"name": kwargs.get("company")}):
        return {
            "status": "error",
            "message": "Company name already exist"
        }

    company_onboard_doc = frappe.get_doc(
        {
            "doctype": "Company Onboard",
            "company":  kwargs.get("company"),
            "name1": kwargs.get("name"),
            "sector": kwargs.get("sector"),
            "location": kwargs.get("location")
        }
    )
    company_onboard_doc.insert()

    frappe.db.set_value("User Mapping", kwargs.get("user"), "first_time_login", 0)

    return {
        "status": "success",
        "message": "Company onboard successful."
    }