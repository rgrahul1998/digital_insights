import frappe


@frappe.whitelist(allow_guest=True)
def create_user_api(**kwargs):

    if frappe.db.exists("User", {"email": kwargs.get("email")}):
        return {
            "status": "error",
            "message": "User with same email already exist"
        }
    elif frappe.db.exists("User", {"mobile_no": kwargs.get("mobile_no")}):
        return {
            "status": "error",
            "message": "User with same mobile no. already exist"
        }


    user_doc = frappe.get_doc(
        {
            "doctype": "User",
            "email":  kwargs.get("email"),
            "send_welcome_email": False,
            "new_password": kwargs.get("password"),
            "first_name": kwargs.get("name"),
            "mobile_no": kwargs.get("mobile_no"),
        }
    )
    try:
        user_doc.insert(ignore_permissions=True)
    except Exception as e:
        frappe.log_error("User", str(e))
        return {
            "status": "error",
            "message": "Something went wrong. Please contact admin"
        }

    user_map_doc = frappe.get_doc(
        {
            "doctype": "User Mapping",
            "user":  kwargs.get("email"),
            "first_time_login": 1
        }
    )
    try:
        user_map_doc.insert(ignore_permissions=True)
    except Exception as e:
        frappe.log_error("User Mapping", str(e))
        return {
            "status": "error",
            "message": "Something went wrong. Please contact admin"
        }

    return {
        "status": "success",
        "message": "User Created successfully.",
        "email": user_doc.email,
    }