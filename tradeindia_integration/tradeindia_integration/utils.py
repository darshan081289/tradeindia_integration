import frappe
import requests
import json
from datetime import datetime
from frappe import _
from frappe.utils import get_site_name

class TradeIndiaIntegration:
    def __init__(self, api_key=None, user_id=None):
        self.api_key = api_key or frappe.get_value('TradeIndia Settings', None, 'api_key')
        self.user_id = user_id or frappe.get_value('TradeIndia Settings', None, 'user_id')
        self.base_url = "https://api.tradeindia.com/v1/"
        
    def setup_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def fetch_leads(self, date_from=None, date_to=None):
        """Fetch leads from TradeIndia API"""
        endpoint = f"{self.base_url}leads"
        params = {
            'user_id': self.user_id,
            'from_date': date_from,
            'to_date': date_to
        }
        
        try:
            response = requests.get(endpoint, headers=self.setup_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            frappe.log_error(f"TradeIndia API Error: {str(e)}", "TradeIndia Integration")
            return None

    def create_lead_in_erpnext(self, lead_data):
        """Create a new lead in ERPNext from TradeIndia data"""
        try:
            lead = frappe.get_doc({
                'doctype': 'Lead',
                'lead_name': lead_data.get('name'),
                'company_name': lead_data.get('company_name'),
                'email_id': lead_data.get('email'),
                'mobile_no': lead_data.get('mobile'),
                'source': 'TradeIndia',
                'notes': lead_data.get('requirement_details'),
                'territory': lead_data.get('location', 'India'),
                'tradeindia_lead_id': lead_data.get('lead_id')
            })
            
            lead.insert(ignore_permissions=True)
            frappe.db.commit()
            return lead.name
            
        except Exception as e:
            frappe.log_error(f"ERPNext Lead Creation Error: {str(e)}", "TradeIndia Integration")
            return None

    def sync_leads(self):
        """Sync leads from TradeIndia to ERPNext"""
        leads = self.fetch_leads()
        if not leads:
            return
            
        for lead in leads.get('data', []):
            # Check if lead already exists
            existing_lead = frappe.get_all(
                'Lead',
                filters={'tradeindia_lead_id': lead.get('lead_id')},
                fields=['name']
            )
            
            if not existing_lead:
                self.create_lead_in_erpnext(lead)

# Custom DocType for TradeIndia Settings
def create_tradeindia_settings():
    """Create custom DocType for TradeIndia settings"""
    if not frappe.db.exists('DocType', 'TradeIndia Settings'):
        doc = frappe.new_doc('DocType')
        doc.name = 'TradeIndia Settings'
        doc.module = 'CRM'
        doc.custom = 1
        doc.fields = [
            {
                'fieldname': 'api_key',
                'label': 'API Key',
                'fieldtype': 'Data',
                'reqd': 1
            },
            {
                'fieldname': 'user_id',
                'label': 'User ID',
                'fieldtype': 'Data',
                'reqd': 1
            },
            {
                'fieldname': 'sync_frequency',
                'label': 'Sync Frequency (Minutes)',
                'fieldtype': 'Int',
                'default': 60
            }
        ]
        doc.insert()

# Scheduler job for automatic syncing
def setup_scheduler():
    """Setup scheduler for periodic lead syncing"""
    if not frappe.db.exists('Scheduled Job Type', 'tradeindia_lead_sync'):
        job = frappe.get_doc({
            'doctype': 'Scheduled Job Type',
            'method': 'custom_integrations.tradeindia_integration.sync_leads',
            'frequency': 'Daily',
            'docstatus': 0
        })
        job.insert()

@frappe.whitelist()
def sync_leads():
    """Manual trigger for lead syncing"""
    integration = TradeIndiaIntegration()
    integration.sync_leads()
    frappe.msgprint(_("TradeIndia leads sync completed"))

def install():
    """Installation hook"""
    create_tradeindia_settings()
    setup_scheduler()
    # Add custom field to Lead DocType for TradeIndia lead ID
    if not frappe.db.exists('Custom Field', 'Lead-tradeindia_lead_id'):
        custom_field = frappe.get_doc({
            'doctype': 'Custom Field',
            'dt': 'Lead',
            'fieldname': 'tradeindia_lead_id',
            'label': 'TradeIndia Lead ID',
            'fieldtype': 'Data',
            'insert_after': 'source',
            'unique': 1
        })
        custom_field.insert()
