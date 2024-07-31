import frappe
from frappe.utils.password import check_password


@frappe.whitelist(allow_guest=True)
def get_access_api_token(**kwargs):
    try:
        usr = kwargs.get("usr")
        pwd = kwargs.get("pwd")

        if check_password(usr, pwd):
            is_first_time_login = frappe.db.get_value("User Mapping", usr, "first_time_login")
            
            user_doc = frappe.get_doc("User", usr)
            api_key = user_doc.api_key
            api_secret = user_doc.get_password("api_secret")
            
            if api_key and api_secret:
                api_token = f"token {api_key}:{api_secret}"
                access_api_token = {"access_token": api_token}
                
                return success_response({   
                    "access_token": access_api_token,
                    "first_time_login": is_first_time_login
                })

        return error_response("Invalid credentials")

    except Exception as e:
        frappe.logger("token").exception(e)
        return error_response(str(e))

def success_response(data=None, id=None):
    response = {"msg": "success"}
    if data:
        response["data"] = data
    if id:
        response["data"] = {"id": id, "name": id}
    return response

def error_response(err_msg):
    return {"msg": "error", "error": err_msg}

