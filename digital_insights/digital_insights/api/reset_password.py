import frappe


@frappe.whitelist()
def reset_password(**kwargs):
	try:
		email = kwargs.get("email")
		if not frappe.db.exists("User", email):
			return {
                "status": "error",
                "error": "User with this email does not exist"
                }
		user = frappe.get_doc("User", email)
		user.new_password = kwargs.get("new_password")
		user.save(ignore_permissions=True)
        return {
                "status": "success",
                "message": "Password Changed"
                }
	except Exception as e:
		frappe.log("reset_password", str(e))
		return {
                "status": "error",
                "error": "Internal Server Error"
                }