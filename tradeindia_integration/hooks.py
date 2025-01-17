app_name = "tradeindia_integration"
app_title = "TradeIndia Integration"
app_publisher = "Your Name"
app_description = "Integration between TradeIndia and ERPNext"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "your@email.com"
app_license = "MIT"

fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Lead-tradeindia_lead_id"
                ]
            ]
        ]
    }
]
