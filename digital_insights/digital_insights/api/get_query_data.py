import frappe
import json  # Import the json module
from insights.api.queries import create_query

@frappe.whitelist(allow_guest=True)
def get_query_data(query_name):    
    insights_query_doc = frappe.get_doc("Insights Query", query_name)
    insights_query_data = {}

    json_string = insights_query_doc.json
    
    parsed_json = json.loads(json_string)
    tables = []
    tables.append(parsed_json.get("table")["table"])
    
    insights_query_data.update({
        "columns": parsed_json.get("columns"),
        "table": tables,
        "data_source": insights_query_doc.data_source,
        "data_source_type": frappe.db.get_value("Insights Data Source", insights_query_doc.data_source, "database_type")
    })    
    
    return insights_query_data
