import frappe
from frappe.utils.password import check_password


@frappe.whitelist(allow_guest=True)
def get_access_api_token(**kwargs):
    try:
        usr = kwargs.get("usr")
        pwd = kwargs.get("pwd")

        # Check if the user exists
        if not frappe.db.exists("User", usr):
            return error_response("User does not exist. Please signup first")

        # Validate the password
        if check_password(usr, pwd):
            # Get user mapping info
            user_mapping_info = frappe.db.get_value("User Mapping", usr, ["first_time_login", "subscription"], as_dict=1)
            user_doc = frappe.get_doc("User", usr)

            # Check if API key and secret already exist, otherwise generate new ones
            if not user_doc.api_key or not user_doc.get_password("api_secret"):
                user_doc.api_key = frappe.generate_hash(length=15)  # Generate API key
                user_doc.api_secret = frappe.generate_hash(length=15)  # Generate API secret
                user_doc.save(ignore_permissions=True)  # Save the user with new keys

            # Retrieve the API key and secret
            api_key = user_doc.api_key
            api_secret = user_doc.get_password("api_secret")
            
            # Create the API token (for example by concatenating the key and secret)
            api_token = f"{api_key}:{api_secret}"

            access_api_token = {"access_token": api_token}
            print(success_response({
                "access_token": access_api_token,
                "user": usr,
                "first_time_login": user_mapping_info["first_time_login"],
                "subscription": user_mapping_info["subscription"]
            }))
            return success_response({
                "access_token": access_api_token,
                "user": usr,
                "first_time_login": user_mapping_info["first_time_login"],
                "subscription": user_mapping_info["subscription"]
            })

        return error_response("Invalid credentials")

    except Exception as e:
        frappe.log_error("Signin", str(e))
        frappe.logger("token").exception(e)
        return error_response("There was some issue validating user. Please contact admin.")

def success_response(data=None, id=None):
    response = {"msg": "success"}
    if data:
        response["data"] = data
    if id:
        response["data"] = {"id": id, "name": id}
    return response

def error_response(err_msg):
    return {"msg": "error", "error": err_msg}

