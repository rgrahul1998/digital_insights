import frappe

@frappe.whitelist(allow_guest=True)
def set_chart_values(**kwargs):    
    insights_chart = frappe.get_doc("Insights Chart", {"query": kwargs.get("query_name")})
    

    xAxis = [{"column": column} for column in kwargs.get("x_axis", [])]
    yAxis = [{"column": column, "series_options": {"type": kwargs.get("chart_type", "line")}} for column in kwargs.get("y_axis", [])]

    insights_chart_options = {
        "xAxis": xAxis,
        "yAxis": yAxis,
        "rotateLabels": kwargs.get("rotateLabels"),
        "title": kwargs.get("query_name"),
        "colors": [
            "#318AD8", "#F683AE", "#48BB74", "#F56B6B", "#FACF7A", 
            "#44427B", "#5FD8C4", "#F8814F", "#15CCEF", "#A6B1B9"
        ],
        "query": kwargs.get("query_name")
    }
    
    insights_chart.chart_type = kwargs.get("chart_type")
    insights_chart.options = frappe.as_json(insights_chart_options)
    
    insights_chart.save(ignore_permissions=True)

    return {"message": "Chart options updated successfully"}
