import json

import frappe
import requests


@frappe.whitelist(allow_guest=True)
def login_via_google(**kwargs):
	credential = kwargs.get("credential")
	print(credential)
	url = f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={credential}"

	response = requests.request("GET", url)

	if response.status_code == 200:
		resp = json.loads(response.text)

		print(response.text)
		social_login = frappe.get_value(
			"Social Login Key", filters={"client_id": resp.get("aud"), "name": "google"}
		)
		if social_login:
			email = resp.get("email")
			user_exists = frappe.db.exists("User", email)
			if user_exists:
				return success_response()
			else:
				return error_response("WRONG")

		else:
			return error_response("Invalid social login key")
	else:
		return error_response("Invalid credential or Google token")


def success_response(data=None):
	response = {"status": "success", "data": data}
	return response


def error_response(err_msg):
	return {"status": "error", "data": {"message": err_msg}}