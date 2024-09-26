import frappe
from insights.insights.doctype.insights_query.insights_query_client import get_matching_columns_from, get_related_table_names

@frappe.whitelist(allow_guest=True)
def fetch_related_tables_columns(table_names, data_source, search_txt=None):
    print(table_names, type(table_names))

    related_table_names = get_related_table_names(table_names, data_source)
    selected_table_cols = get_matching_columns_from(table_names, data_source, search_txt)
    related_table_cols = get_matching_columns_from(
        related_table_names, data_source, search_txt
    )

    columns = []
    for col in selected_table_cols + related_table_cols:
        col_added = any(
            col["column"] == column["column"] and col["table"] == column["table"]
            for column in columns
        )
        if col_added:
            continue
        columns.append(
            {
                "column": col.column,
                "label": col.label,
                "type": col.type,
                "table": col.table,
                "table_label": col.table_label,
                "data_source": col.data_source,
            }
        )

    result = {}
    for column in columns:
        table_label = column['table_label']
        if table_label not in result:
            result[table_label] = []
        result[table_label].append(column)

    
    # Print columns and child table for debugging
    print("Columns:", columns)
    print("Child Table:", result)
    return columns