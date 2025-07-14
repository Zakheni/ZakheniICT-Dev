from odoo import models, fields

class DisposalRateAnalysis(models.Model):
    _name = 'sql.disposal.rate.analysis'
    _description = 'Disposal Rate Analysis'
    _auto = True
    _order = 'date desc'  # Most recent first

    date = fields.Datetime(string="Date", readonly=True)
    year = fields.Char(string="Year", readonly=True)
    month = fields.Char(string="Month", readonly=True)
    weeks = fields.Integer(string="Week", readonly=True)
    day = fields.Char(string="Day", readonly=True)
    manifest_number = fields.Char(string="Manifest Number", readonly=True)
    disposal_site = fields.Char(string="Disposal Site", readonly=True)
    waste_stream = fields.Char(string="Waste Stream", readonly=True)
    waste_type = fields.Char(string="Waste Type", readonly=True)
    tonnage = fields.Float(string="Tonnage", readonly=True)
    exclusive_amount = fields.Float(string="Exclusive Amount", readonly=True)
    vat_rate = fields.Float(string="VAT Rate (%)", readonly=True)
    discount_rate = fields.Float(string="Discount Rate (%)", readonly=True)
    escalation_rate = fields.Float(string="Escalation Rate (%)", readonly=True)
    inclusive_amount = fields.Float(string="Inclusive Amount", readonly=True) 