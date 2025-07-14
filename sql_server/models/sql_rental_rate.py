from odoo import models, fields

class RentalRateReport(models.Model):
    _name = 'sql.rental.rate.report'
    _description = 'Rental Rate Report'
    _auto = True
    _order = 'date desc'  # Most recent first

    date = fields.Datetime(string="Date", readonly=True)
    year = fields.Char(string="Year", readonly=True)
    month = fields.Char(string="Month", readonly=True)
    weeks = fields.Integer(string="Week", readonly=True)
    day = fields.Char(string="Day", readonly=True)
    contract_order_number = fields.Char(string="Contract Order Number", readonly=True)
    bin_volume_type = fields.Char(string="Bin Volume Type", readonly=True)
    rental_rate = fields.Float(string="Rental Rate", readonly=True)
    discount_rate = fields.Float(string="Discount Rate", readonly=True)
    escalation_rate = fields.Float(string="Escalation Rate", readonly=True) 