from odoo import models, fields

class BinsAnalysis(models.Model):
    _name = 'sql.bins.analysis'
    _description = 'Bins Analysis'
    _auto = True

    bin_number = fields.Char(string="Bin Number", readonly=True)
    bin_type = fields.Char(string="Bin Type", readonly=True)
    bin_condition = fields.Char(string="Bin Condition", readonly=True)
    in_use = fields.Char(string="In Use?", readonly=True)
    mine_name = fields.Char(string="Mine Name", readonly=True)
    bin_current_location = fields.Char(string="Current Location", readonly=True)
    waste_description = fields.Char(string="Waste Description", readonly=True)
    waste_detail = fields.Char(string="Waste Detail", readonly=True) 