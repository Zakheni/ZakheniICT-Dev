from odoo import models, fields

class VehicleInspection(models.Model):
    _name = 'sql.vehicle.inspection'
    _description = 'Vehicle Inspection'
    _auto = True
    _order = 'inspection_date desc'  # Most recent first

    inspection_id = fields.Char(string="Inspection ID", readonly=True)
    inspection_date = fields.Datetime(string="Inspection Date", readonly=True)
    registration_number = fields.Char(string="Registration Number", readonly=True)
    inspection_comment = fields.Text(string="Comment", readonly=True)
    inspection_status = fields.Char(string="Status", readonly=True) 