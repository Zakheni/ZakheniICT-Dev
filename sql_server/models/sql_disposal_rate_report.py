from odoo import models, fields

class DisposalRateReport(models.Model):
    _name = 'sql.disposal.rate.report'
    _description = 'Disposal Rate Report'
    _auto = True
    _order = 'date desc'  # Most recent first

    date = fields.Datetime(string="Date", readonly=True)
    year = fields.Char(string="Year", readonly=True)
    month = fields.Char(string="Month", readonly=True)
    weeks = fields.Integer(string="Week", readonly=True)
    day = fields.Char(string="Day", readonly=True)
    contract_order_number = fields.Char(string="Contract Order Number", readonly=True)
    disposal_site = fields.Char(string="Disposal Site", readonly=True)
    waste_stream = fields.Char(string="Waste Stream", readonly=True)
    waste_type = fields.Char(string="Waste Type", readonly=True)
    disposal_rate_per_ton = fields.Float(string="Disposal Rate Per Ton", readonly=True)
    discount_rate = fields.Float(string="Discount Rate", readonly=True)
    escalation_rate = fields.Float(string="Escalation Rate", readonly=True) 