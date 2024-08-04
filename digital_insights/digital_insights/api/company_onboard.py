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
    company_list_doc = frappe.get_doc(
        {
            "doctype": "Company List",
            "parent": kwargs.get("user"),
            "parentfield": "company_list",
            "parenttype": "User Mapping",
            "company_name":  kwargs.get("company")
        }
    )
    company_list_doc.insert(ignore_permissions=True)

    frappe.db.set_value("User Mapping", kwargs.get("user"), "first_time_login", 0)

    return {
        "status": "success",
        "message": "Company onboard successful."
    }