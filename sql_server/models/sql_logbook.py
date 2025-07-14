from odoo import models, fields

class LogbookEntries(models.Model):
    _name = 'sql.logbook.entries'
    _description = 'Logbook Entries'
    _auto = True

    log_date = fields.Datetime(string="Log Date", readonly=True)
    opening_km = fields.Float(string="Opening KM", readonly=True)
    closing_km = fields.Float(string="Closing KM", readonly=True)
    fuel_amount = fields.Float(string="Fuel Amount", readonly=True)
    fuel_quantity = fields.Float(string="Fuel Quantity", readonly=True)
    driver_first_name = fields.Char(string="Driver Name", readonly=True)
    truck_registration_number = fields.Char(string="Truck Reg. Number", readonly=True)

    # Computed field for distance
    distance = fields.Float(string="Distance (KM)", compute='_compute_distance', store=True, readonly=True)

    def _compute_distance(self):
        for record in self:
            record.distance = record.closing_km - record.opening_km 