import frappe
from insights.api.queries import create_query
import json
from insights.insights.doctype.insights_query.insights_query_client import InsightsQueryClient


@frappe.whitelist(allow_guest=True)
def get_table_data(**kwargs):
    data = {
        "calculations": [],
        "columns": [],
        "dimensions": [],
        "filters": [],
        "joins": [],
        "limit": 10,
        "measures": [],
        "orders": [],
        "table": {
            "label": None,
            "table": None
        }
    }    
    
    if 'table' in kwargs:
        data['table']['table'] = kwargs['table'][0]
        data['table']['label'] = kwargs['table'][0]
    
    if 'columns' in kwargs:
        for col in kwargs['columns']:
            column_data = {
                "table": col["table"],
                "column": col["column"],
                "label": col["label"],
                "type": col["type"],
                "alias": col["label"],
                "order": "",
                "granularity": "",
                "aggregation": "",
                "format": {},
                "expression": {},
                "meta": None
            }
            data['columns'].append(column_data)
    
    query_json = json.dumps(data, indent=2)
    
    insights_query = create_query(is_assisted_query=1)
    
    frappe.db.set_value("Insights Query", insights_query.name, "data_source", kwargs.get('data_source'))
    frappe.db.set_value("Insights Query", insights_query.name, "json", query_json)
    insights_query = frappe.get_doc("Insights Query", insights_query.name)
    insights_query.save()

    InsightsQueryClient.run(insights_query)
    
    insights_query_result = frappe.get_doc("Insights Query Result", insights_query.result_name).results
    insights_query_result = json.loads(insights_query_result)
    return insights_query_result
