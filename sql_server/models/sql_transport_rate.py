from odoo import models, fields

class TransportRateAnalysis(models.Model):
    _name = 'sql.transport.rate.analysis'
    _description = 'Transport Rate Analysis'
    _auto = True
    _order = 'date desc'  # Most recent first

    date = fields.Datetime(string="Date", readonly=True)
    year = fields.Char(string="Year", readonly=True)
    month = fields.Char(string="Month", readonly=True)
    weeks = fields.Integer(string="Week", readonly=True)
    day = fields.Char(string="Day", readonly=True)
    manifest_number = fields.Char(string="Manifest Number", readonly=True)
    service_offering_type = fields.Char(string="Service Offering Type", readonly=True)
    waste_stream = fields.Char(string="Waste Stream", readonly=True)
    waste_type = fields.Char(string="Waste Type", readonly=True)
    transport_rate_type = fields.Char(string="Transport Rate Type", readonly=True)
    exclusive_amount = fields.Float(string="Exclusive Amount", readonly=True)
    vat_rate = fields.Float(string="VAT Rate (%)", readonly=True)
    escalation_rate = fields.Float(string="Escalation Rate", readonly=True)
    inclusive_amount = fields.Float(string="Inclusive Amount", readonly=True) 