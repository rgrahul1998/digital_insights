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
    
    insights_chart_doc = frappe.get_doc("Insights Chart", {"query": query_name})
    axis_json = json.loads(insights_chart_doc.options)
    x_axis_column = [item['column'] for item in axis_json['xAxis']]
    y_axis_column = [item['column'] for item in axis_json['yAxis']]
    
    insights_query_data.update({
        "columns": parsed_json.get("columns"),
        "table": tables,
        "data_source": insights_query_doc.data_source,
        "data_source_type": frappe.db.get_value("Insights Data Source", insights_query_doc.data_source, "database_type"),
        "x_axis_column": x_axis_column,
        "y_axis_column": y_axis_column,
        "chart_type": insights_chart_doc.chart_type,
        "filter": [
                    {
                        'column': filter_item['column'],
                        'operator': filter_item['operator']['label'],
                        'value': filter_item['value']['value'],
                    } for filter_item in parsed_json.get("filters")
                ]

    })    
    return insights_query_data
