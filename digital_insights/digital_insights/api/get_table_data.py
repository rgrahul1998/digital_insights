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

    if 'filters' in kwargs:
        for filter_item in kwargs['filters']:
            operator_value = ""
            if filter_item['operator'] == "equals":
                operator_value = "="
            elif filter_item['operator'] == "not equals":
                operator_value = "!="
            else:
                operator_value = filter_item['operator']

            filter_data = {
                "column": {
                    "aggregation": "",
                    "alias": "",
                    "column": filter_item['column']['column'],
                    "expression": {},
                    "format": {},
                    "granularity": "",
                    "label": filter_item['column']['label'],
                    "meta": None,
                    "order": "",
                    "table": filter_item['column']['table'],
                    "type": filter_item['column']['type']
                },
                "expression": {},
                "operator": {
                    "label": filter_item['operator'],
                    "value": operator_value
                },
                "value": {
                    "label": filter_item['value'],
                    "value": filter_item['value']
                }
            }
            data['filters'].append(filter_data)

    query_json = json.dumps(data, indent=2)
        
    frappe.db.set_value("Insights Query", kwargs.get('query_name'), "data_source", kwargs.get('data_source'))
    frappe.db.set_value("Insights Query", kwargs.get('query_name'), "json", query_json)
    insights_query = frappe.get_doc("Insights Query", kwargs.get('query_name'))
    insights_query.save()

    InsightsQueryClient.run(insights_query)
    
    insights_query_result = frappe.get_doc("Insights Query Result", insights_query.result_name).results
    insights_query_result = json.loads(insights_query_result)
    return insights_query_result
