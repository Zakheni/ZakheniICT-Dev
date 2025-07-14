from odoo import models, fields

class TransportReport(models.Model):
    _name = 'sql.transport.report'
    _description = 'Transport Report'
    _auto = True
    _order = 'date desc'  # Most recent first

    date = fields.Datetime(string="Date", readonly=True)
    year = fields.Char(string="Year", readonly=True)
    month = fields.Char(string="Month", readonly=True)
    weeks = fields.Integer(string="Week", readonly=True)
    day = fields.Char(string="Day", readonly=True)
    custom_invoice_type = fields.Char(string="Custom Invoice Type", readonly=True)
    contract_order_number = fields.Char(string="Contract Order Number", readonly=True)
    service_offering_type = fields.Char(string="Service Offering Type", readonly=True)
    waste_stream = fields.Char(string="Waste Stream", readonly=True)
    waste_type = fields.Char(string="Waste Type", readonly=True)
    rate_per_bin = fields.Float(string="Rate Per Bin", readonly=True)
    rate_per_km = fields.Float(string="Rate Per Km", readonly=True)
    rate_per_load = fields.Float(string="Rate Per Load", readonly=True)
    fixed_transport_rate = fields.Float(string="Fixed Transport Rate", readonly=True)
    discount_rate = fields.Float(string="Discount Rate", readonly=True)
    escalation_rate = fields.Float(string="Escalation Rate", readonly=True) 