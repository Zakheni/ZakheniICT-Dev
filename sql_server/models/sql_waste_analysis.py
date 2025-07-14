from odoo import models, fields

class WasteAnalysis(models.Model):
    _name = 'sql.waste.analysis'
    _description = 'Waste Analysis'
    _auto = True
    _order = 'date_of_service_request desc'  # Most recent first

    customer_name = fields.Char(string="Customer Name", readonly=True)
    mine_name = fields.Char(string="Mine Name", readonly=True)
    date_of_service_request = fields.Datetime(string="Service Request Date", readonly=True)
    waste_description = fields.Char(string="Waste Description", readonly=True)
    service_offering_type = fields.Char(string="Service Type", readonly=True)
    site_name = fields.Char(string="Site Name", readonly=True)
    manifest_number = fields.Char(string="Manifest Number", readonly=True)
    tonnage = fields.Float(string="Tonnage", readonly=True) 