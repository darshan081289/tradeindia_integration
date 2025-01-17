from . import __version__ as app_version

# tradeindia_integration/tradeindia_integration/hooks.py

app_name = "tradeindia_integration"
app_title = "TradeIndia Integration"
app_publisher = "Your Name"
app_description = "Integration between TradeIndia and ERPNext"
app_email = "your@email.com"
app_license = "MIT"

# Includes in <head>
app_include_js = "/assets/tradeindia_integration/js/tradeindia_integration.min.js"

# Auto-created on install
fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "TradeIndia Integration"]]},
]

# Document Events
# --------------
doc_events = {
    "Lead": {
        "after_insert": "tradeindia_integration.tradeindia_integration.doctype.tradeindia_settings.tradeindia_settings.process_new_lead",
        "on_update": "tradeindia_integration.tradeindia_integration.doctype.tradeindia_settings.tradeindia_settings.update_lead"
    }
}

# Scheduled Tasks
# --------------
scheduler_events = {
    "daily": [
        "tradeindia_integration.tradeindia_integration.doctype.tradeindia_settings.tradeindia_settings.sync_tradeindia_leads"
    ],
    "hourly": [
        "tradeindia_integration.tradeindia_integration.doctype.tradeindia_settings.tradeindia_settings.check_api_status"
    ]
}

# Custom DocTypes
# --------------
doctype_js = {
    "Lead": "public/js/lead.js"
}

# Website Settings
# --------------
website_route_rules = [
    {"from_route": "/tradeindia", "to_route": "tradeindia_settings"}
]

# DocType Class
# ------------
doc_events = {
    "Lead": {
        "validate": "tradeindia_integration.tradeindia_integration.doctype.tradeindia_settings.tradeindia_settings.validate_lead",
        "on_update": "tradeindia_integration.tradeindia_integration.doctype.tradeindia_settings.tradeindia_settings.handle_lead_update",
        "after_insert": "tradeindia_integration.tradeindia_integration.doctype.tradeindia_settings.tradeindia_settings.handle_new_lead"
    }
}

# Permission Rules
# --------------
has_permission = {
    "Lead": "tradeindia_integration.tradeindia_integration.doctype.tradeindia_settings.tradeindia_settings.has_lead_permission"
}

# Override Standard Methods
# -----------------------
override_whitelisted_methods = {
    "frappe.desk.form.assign_to.add": "tradeindia_integration.tradeindia_integration.doctype.tradeindia_settings.tradeindia_settings.custom_assign_to"
}

# API Endpoints
# ------------
api_version = 1

# Custom Fields
# ------------
required_apps = ["erpnext"]

# Boot Info
# --------
boot_session = "tradeindia_integration.tradeindia_integration.doctype.tradeindia_settings.tradeindia_settings.boot_session"

# Error Handlers
# -------------
after_migrate = ["tradeindia_integration.tradeindia_integration.setup.after_migrate"]
