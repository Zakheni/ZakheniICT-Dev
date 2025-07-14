from odoo import models, fields

class BookingsAnalysis(models.Model):
    _name = 'sql.bookings.analysis'
    _description = 'Bookings Analysis'
    _auto = True
    _order = 'date_received desc'  # Most recent first

    bin_id = fields.Char(string="Bin ID", readonly=True)
    date_received = fields.Datetime(string="Date Received", readonly=True)
    mine_name = fields.Char(string="Mine Name", readonly=True)
    customer_name = fields.Char(string="Customer Name", readonly=True)
    waste_description = fields.Char(string="Waste Description", readonly=True)
    service_offering_type = fields.Char(string="Service Type", readonly=True) 