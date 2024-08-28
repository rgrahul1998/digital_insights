import frappe
from frappe.utils.password import check_password

@frappe.whitelist(allow_guest=True)
def user_associated_company(**kwargs):
    try:
        user = kwargs.get("user")

        company_list = frappe.db.get_all("Company List", {"parent":user}, pluck = "company_name")
        sidebar_component_list = frappe.db.get_all("User Sidebar Component", {"parent":user}, pluck = "sidebar_component")
        return success_response(data={"company_list": company_list, "sidebar_component_list": sidebar_component_list})
    except Exception as e:
        frappe.logger("token").exception(e)
        return error_response(str(e))

def success_response(data=None):
    response = {"msg": "success"}
    if data:
        response["data"] = data
    return response

def error_response(err_msg):
    return {"msg": "error", "error": err_msg}
