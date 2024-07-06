import frappe
from frappe.utils.password import check_password


@frappe.whitelist(allow_guest=True)
def get_access_api_token(**kwargs):
    try:
        usr = kwargs.get("usr")
        pwd = kwargs.get("pwd")
        a= check_password(usr, pwd)
        if check_password(usr, pwd):
            is_first_time_login = frappe.db.get_value("User Mapping", usr, "first_time_login")
            return {"msg": "success",
                    "first_time_login": is_first_time_login}

    except Exception as e:
        frappe.logger("token").exception(e)
        return error_response(e)


def success_response(data=None, id=None):
	response = {"msg": "success"}
	response["data"] = data
	if id:
		response["data"] = {"id": id, "name": id}
	return response


def error_response(err_msg):
	return {"msg": "error", "error": err_msg}