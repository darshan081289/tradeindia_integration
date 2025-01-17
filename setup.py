# setup.py
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="tradeindia_integration",
    version="0.0.1",
    description="TradeIndia Integration for ERPNext",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)

# requirements.txt
frappe
requests

# MANIFEST.in
include MANIFEST.in
include requirements.txt
include *.json
include *.md
include *.py
include *.txt
recursive-include tradeindia_integration *.css
recursive-include tradeindia_integration *.csv
recursive-include tradeindia_integration *.html
recursive-include tradeindia_integration *.ico
recursive-include tradeindia_integration *.js
recursive-include tradeindia_integration *.json
recursive-include tradeindia_integration *.md
recursive-include tradeindia_integration *.png
recursive-include tradeindia_integration *.py
recursive-include tradeindia_integration *.svg
recursive-include tradeindia_integration *.txt
recursive-exclude tradeindia_integration *.pyc

# hooks.py
app_name = "tradeindia_integration"
app_title = "TradeIndia Integration"
app_publisher = "Your Name"
app_description = "TradeIndia Integration for ERPNext"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "your.email@example.com"
app_license = "MIT"

# Document Events
doc_events = {
    "Lead": {
        "after_insert": "tradeindia_integration.tradeindia_integration.utils.handle_lead_after_insert",
    }
}

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "tradeindia_integration.tradeindia_integration.utils.daily_sync"
    ]
}

# fixtures
fixtures = [
    {
        "doctype": "Custom Field",
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
