from odoo import models, fields

class MineContractAnalysis(models.Model):
    _name = 'sql.mine.contract.analysis'
    _description = 'Mine Contract Rate Analysis'
    _auto = True

    customer_name = fields.Char(string="Customer Name", readonly=True)
    mine_name = fields.Char(string="Mine Name", readonly=True)
    contract_order_number = fields.Char(string="Contract Order Number", readonly=True)
    start_date = fields.Date(string="Start Date", readonly=True)
    end_date = fields.Date(string="End Date", readonly=True)
    service_offering_type = fields.Char(string="Service Type", readonly=True)
    waste_description = fields.Char(string="Waste Description", readonly=True)
    waste_detail = fields.Char(string="Waste Detail", readonly=True) 