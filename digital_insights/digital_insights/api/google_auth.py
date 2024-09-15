import frappe

@frappe.whitelist(allow_guest=True)
def save_google_user_data(email, name):
    try:        
        if frappe.db.exists("User", {"email": email}):
            user_mapping_info = frappe.db.get_value("User Mapping", email, ["first_time_login", "subscription"], as_dict=1)
            
            user_doc = frappe.get_doc("User", email)

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

            return {
                "msg": "success",  
                "access_token": access_api_token,
                "user": email,
                "first_time_login": user_mapping_info["first_time_login"],
                "subscription": user_mapping_info["subscription"]
            }
        else:
            return {"msg": "error", "error": "User does not exist. Please signup first"}
    
    except Exception as e:
        print(8999999, e)
        frappe.logger("token").exception(e)
        return {"msg": "error", "error": str(e)}

    # # Create new user in Frappe
    # user = frappe.get_doc({
    #     "doctype": "User",
    #     "email": email,
    #     "first_name": name,
    #     "enabled": 1,
    #     # "google_id": google_id
    # })
    # user.insert(ignore_permissions=True)

    # return {"status": "success", "message": "User saved successfully"}
