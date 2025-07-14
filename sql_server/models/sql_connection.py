from odoo import models, fields, api, _
from odoo.exceptions import UserError
import pymssql

class SQLServerConnection(models.Model):
    _name = 'sql.server.connection'
    _description = 'SQL Server Connection'

    name = fields.Char('Connection Name', required=True)
    server = fields.Char('Server Address', required=True)
    database = fields.Char('Database Name', required=True)
    username = fields.Char('Username', required=True)
    password = fields.Char('Password', required=True, copy=False)
    is_active = fields.Boolean('Active', default=True)
    last_refresh = fields.Datetime('Last Refresh', readonly=True)
    record_count = fields.Integer('Record Count', readonly=True)

    @api.model
    def default_get(self, fields_list):
        # Check if connection already exists
        existing = self.search([('is_active', '=', True)], limit=1)
        if existing:
            raise UserError(_("Connection already exists. Please edit the existing connection."))
        return super().default_get(fields_list)

    def write(self, vals):
        if 'is_active' in vals and vals['is_active']:
            self.search([('id', '!=', self.id)]).write({'is_active': False})
        return super().write(vals)

    @api.model
    def create(self, vals):
        if vals.get('is_active'):
            self.search([]).write({'is_active': False})
        return super().create(vals)

    @api.model
    def get_connection_status(self):
        conn = self.search([('is_active', '=', True)], limit=1)
        if conn:
            return {
                'type': 'ir.actions.act_window',
                'res_model': self._name,
                'res_id': conn.id,
                'view_mode': 'form',
                'target': 'main',
            }
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'target': 'main',
            'context': {'create': True},
        }

    def _load_all_views(self):
        """Load data from all SQL views"""
        try:
            conn = pymssql.connect(
                server=self.server,
                database=self.database,
                user=self.username,
                password=self.password,
                timeout=10,
                as_dict=True
            )
            
            cursor = conn.cursor()
            
            # Load all views
            self._load_bins_analysis(cursor)
            self._load_revenue_analysis(cursor)
            self._load_mine_contract_analysis(cursor)
            self._load_logbook_entries(cursor)
            self._load_vehicle_inspection(cursor)
            self._load_waste_analysis(cursor)
            self._load_bookings_analysis(cursor)
            self._load_disposal_rate_analysis(cursor)
            self._load_disposal_rate_report(cursor)
            self._load_rental_rate_report(cursor)
            self._load_transport_rate_analysis(cursor)
            self._load_transport_report(cursor)
            
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            raise UserError(str(e))

    def _load_bins_analysis(self, cursor):
        """Load Bins Analysis data"""
        try:
            self.env['sql.bins.analysis'].search([]).unlink()
            cursor.execute('''
                SELECT 
                    CAST(BinNumber as VARCHAR(50)) as bin_number,
                    CAST([Bin Type] as VARCHAR(100)) as bin_type,
                    CAST([Bin Condition] as VARCHAR(100)) as bin_condition,
                    CAST([In Use?] as VARCHAR(10)) as in_use,
                    CAST([Mine Name] as VARCHAR(100)) as mine_name,
                    CAST([Bin Current Location] as VARCHAR(200)) as bin_current_location,
                    CAST([Waste Description] as VARCHAR(200)) as waste_description,
                    CAST([Waste Detail] as VARCHAR(200)) as waste_detail
                FROM [OdooIntegrationDB].[dbo].[vw_Bins_Analysis_report]
            ''')
            records = cursor.fetchall()
            for row in records:
                self.env['sql.bins.analysis'].create(row)
        except Exception as e:
            raise UserError(_("Error loading Bins Analysis: %s" % str(e)))

    def _load_revenue_analysis(self, cursor):
        """Load Revenue Analysis data"""
        try:
            self.env['sql.revenue.analysis'].search([]).unlink()
            cursor.execute('''
                SELECT 
                    CAST(CustomerName as VARCHAR(100)) as customer_name,
                    CAST(MineName as VARCHAR(100)) as mine_name,
                    CAST(InvoiceNumber as VARCHAR(50)) as invoice_number,
                    CAST(ExclusiveTotalAmount as DECIMAL(18,2)) as exclusive_total_amount,
                    CAST(InclusiveTotalAmount as DECIMAL(18,2)) as inclusive_total_amount,
                    CASE 
                        WHEN InvoiceCreatedDate > '9999-12-31' THEN '9999-12-31'
                        WHEN InvoiceCreatedDate < '1753-01-01' THEN '1753-01-01'
                        ELSE InvoiceCreatedDate 
                    END as invoice_created_date,
                    CAST(InvoiceYear as INT) as invoice_year,
                    CAST(InvoiceMonth as INT) as invoice_month,
                    CAST(InvoiceDay as INT) as invoice_day,
                    CAST(WasteDescription as VARCHAR(200)) as waste_description,
                    CAST(ServiceOfferingType as VARCHAR(100)) as service_offering_type
                FROM [OdooIntegrationDB].[dbo].[vw_Revenue_Analysis]
            ''')
            records = cursor.fetchall()
            for row in records:
                self.env['sql.revenue.analysis'].create(row)
        except Exception as e:
            raise UserError(_("Error loading Revenue Analysis: %s" % str(e)))

    def _load_mine_contract_analysis(self, cursor):
        """Load Mine Contract Analysis data"""
        try:
            self.env['sql.mine.contract.analysis'].search([]).unlink()
            cursor.execute('''
                SELECT 
                    CAST(CustomerName as VARCHAR(100)) as customer_name,
                    CAST(MineName as VARCHAR(100)) as mine_name,
                    CAST(ContractOrderNumber as VARCHAR(50)) as contract_order_number,
                    CASE 
                        WHEN StartDate > '9999-12-31' THEN '9999-12-31'
                        WHEN StartDate < '1753-01-01' THEN '1753-01-01'
                        ELSE StartDate 
                    END as start_date,
                    CASE 
                        WHEN EndDate > '9999-12-31' THEN '9999-12-31'
                        WHEN EndDate < '1753-01-01' THEN '1753-01-01'
                        ELSE EndDate 
                    END as end_date,
                    CAST(ServiceOfferingType as VARCHAR(100)) as service_offering_type,
                    CAST(WasteDescription as VARCHAR(200)) as waste_description,
                    CAST(WasteDetail as VARCHAR(200)) as waste_detail
                FROM [OdooIntegrationDB].[dbo].[vw_Mine_Contract_Rate_Analysis]
            ''')
            records = cursor.fetchall()
            for row in records:
                self.env['sql.mine.contract.analysis'].create(row)
        except Exception as e:
            raise UserError(_("Error loading Mine Contract Analysis: %s" % str(e)))

    def _load_logbook_entries(self, cursor):
        """Load Logbook Entries data"""
        try:
            self.env['sql.logbook.entries'].search([]).unlink()
            cursor.execute('''
                SELECT 
                    CASE 
                        WHEN LogDate > '9999-12-31' THEN '9999-12-31'
                        WHEN LogDate < '1753-01-01' THEN '1753-01-01'
                        ELSE LogDate 
                    END as log_date,
                    CAST(OpeningKm as DECIMAL(18,2)) as opening_km,
                    CAST(ClosingKm as DECIMAL(18,2)) as closing_km,
                    CAST(FuelAmount as DECIMAL(18,2)) as fuel_amount,
                    CAST(FuelQuantity as DECIMAL(18,2)) as fuel_quantity,
                    CAST(DriverFirstName as VARCHAR(100)) as driver_first_name,
                    CAST(TruckRegistrationNumber as VARCHAR(50)) as truck_registration_number
                FROM [OdooIntegrationDB].[dbo].[vw_Logbook_Entries]
            ''')
            records = cursor.fetchall()
            for row in records:
                self.env['sql.logbook.entries'].create(row)
        except Exception as e:
            raise UserError(_("Error loading Logbook Entries: %s" % str(e)))

    def _load_vehicle_inspection(self, cursor):
        """Load Vehicle Inspection data"""
        try:
            self.env['sql.vehicle.inspection'].search([]).unlink()
            cursor.execute('''
                SELECT 
                    CAST(InspectionId as VARCHAR(36)) as inspection_id,
                    CASE 
                        WHEN InspectionDate > '9999-12-31' THEN '9999-12-31'
                        WHEN InspectionDate < '1753-01-01' THEN '1753-01-01'
                        ELSE InspectionDate 
                    END as inspection_date,
                    CAST(RegistrationNumber as VARCHAR(50)) as registration_number,
                    CAST(InspectionComment as VARCHAR(MAX)) as inspection_comment,
                    CAST(InspectionStatus as VARCHAR(50)) as inspection_status
                FROM [OdooIntegrationDB].[dbo].[vw_Vehicle_Inspection]
            ''')
            records = cursor.fetchall()
            for row in records:
                self.env['sql.vehicle.inspection'].create(row)
        except Exception as e:
            raise UserError(_("Error loading Vehicle Inspection: %s" % str(e)))

    def _load_waste_analysis(self, cursor):
        """Load Waste Analysis data"""
        try:
            self.env['sql.waste.analysis'].search([]).unlink()
            cursor.execute('''
                SELECT 
                    CAST(CustomerName as VARCHAR(100)) as customer_name,
                    CAST(MineName as VARCHAR(100)) as mine_name,
                    CASE 
                        WHEN DateOfServiceRequest > '9999-12-31' THEN '9999-12-31'
                        WHEN DateOfServiceRequest < '1753-01-01' THEN '1753-01-01'
                        ELSE DateOfServiceRequest 
                    END as date_of_service_request,
                    CAST(WasteDescription as VARCHAR(200)) as waste_description,
                    CAST(ServiceOfferingType as VARCHAR(100)) as service_offering_type,
                    CAST(SiteName as VARCHAR(100)) as site_name,
                    CAST(ManifestNumber as VARCHAR(50)) as manifest_number,
                    CAST(Tonnage as DECIMAL(18,2)) as tonnage
                FROM [OdooIntegrationDB].[dbo].[vw_Waste_Analysis]
            ''')
            records = cursor.fetchall()
            for row in records:
                self.env['sql.waste.analysis'].create(row)
        except Exception as e:
            raise UserError(_("Error loading Waste Analysis: %s" % str(e)))

    def _load_bookings_analysis(self, cursor):
        """Load Bookings Analysis data"""
        try:
            self.env['sql.bookings.analysis'].search([]).unlink()
            cursor.execute('''
                SELECT 
                    CAST([Bin Id] as VARCHAR(36)) as bin_id,
                    CASE 
                        WHEN DateReceived > '9999-12-31' THEN '9999-12-31'
                        WHEN DateReceived < '1753-01-01' THEN '1753-01-01'
                        ELSE DateReceived 
                    END as date_received,
                    CAST(MineName as VARCHAR(100)) as mine_name,
                    CAST(CustomerName as VARCHAR(100)) as customer_name,
                    CAST(WasteDescription as VARCHAR(200)) as waste_description,
                    CAST(ServiceOfferingType as VARCHAR(100)) as service_offering_type
                FROM [OdooIntegrationDB].[dbo].[vw_Bookings_Analysis]
            ''')
            records = cursor.fetchall()
            for row in records:
                self.env['sql.bookings.analysis'].create(row)
        except Exception as e:
            raise UserError(_("Error loading Bookings Analysis: %s" % str(e)))

    def _load_disposal_rate_analysis(self, cursor):
        """Load Disposal Rate Analysis data"""
        try:
            self.env['sql.disposal.rate.analysis'].search([]).unlink()
            cursor.execute('''
                SELECT 
                    CASE 
                        WHEN Date > '9999-12-31' THEN '9999-12-31'
                        WHEN Date < '1753-01-01' THEN '1753-01-01'
                        ELSE Date 
                    END as date,
                    CAST(Year as VARCHAR(4)) as year,
                    CAST(Month as VARCHAR(20)) as month,
                    CAST(weekss as INT) as weeks,
                    CAST(Day as VARCHAR(20)) as day,
                    CAST([Manifest Number] as VARCHAR(50)) as manifest_number,
                    CAST([Disposal Site] as VARCHAR(100)) as disposal_site,
                    CAST([Waste Stream] as VARCHAR(100)) as waste_stream,
                    CAST([Waste Type] as VARCHAR(100)) as waste_type,
                    CAST(Tonnage as DECIMAL(18,2)) as tonnage,
                    CAST([Exclusive Amount] as DECIMAL(18,2)) as exclusive_amount,
                    CAST([VAT Rate (%)] as DECIMAL(5,2)) as vat_rate,
                    CAST([Discount Rate (%)] as DECIMAL(5,2)) as discount_rate,
                    CAST([Escalation Rate (%)] as DECIMAL(5,2)) as escalation_rate,
                    CAST([Inclusive Amount] as DECIMAL(18,2)) as inclusive_amount
                FROM [OdooIntegrationDB].[dbo].[vw_Disposal_Rate_Analysis_Report]
            ''')
            records = cursor.fetchall()
            for row in records:
                self.env['sql.disposal.rate.analysis'].create(row)
        except Exception as e:
            raise UserError(_("Error loading Disposal Rate Analysis: %s" % str(e)))

    def _load_disposal_rate_report(self, cursor):
        """Load Disposal Rate Report data"""
        try:
            self.env['sql.disposal.rate.report'].search([]).unlink()
            cursor.execute('''
                SELECT 
                    CASE 
                        WHEN Date > '9999-12-31' THEN '9999-12-31'
                        WHEN Date < '1753-01-01' THEN '1753-01-01'
                        ELSE Date 
                    END as date,
                    CAST(Year as VARCHAR(4)) as year,
                    CAST(Month as VARCHAR(20)) as month,
                    CAST(Weeks as INT) as weeks,
                    CAST(Day as VARCHAR(20)) as day,
                    CAST(ContractOrderNumber as VARCHAR(50)) as contract_order_number,
                    CAST([Disposal Site] as VARCHAR(100)) as disposal_site,
                    CAST([Waste Stream] as VARCHAR(100)) as waste_stream,
                    CAST([Waste Type] as VARCHAR(100)) as waste_type,
                    CAST([Disposal Rate Per Ton] as DECIMAL(18,2)) as disposal_rate_per_ton,
                    CAST([Discount Rate] as DECIMAL(5,2)) as discount_rate,
                    CAST([Escalation Rate] as DECIMAL(5,2)) as escalation_rate
                FROM [OdooIntegrationDB].[dbo].[vw_Disposal_Rate_Report]
            ''')
            records = cursor.fetchall()
            for row in records:
                self.env['sql.disposal.rate.report'].create(row)
        except Exception as e:
            raise UserError(_("Error loading Disposal Rate Report: %s" % str(e)))

    def _load_rental_rate_report(self, cursor):
        """Load Rental Rate Report data"""
        try:
            self.env['sql.rental.rate.report'].search([]).unlink()
            cursor.execute('''
                SELECT 
                    CASE 
                        WHEN Date > '9999-12-31' THEN '9999-12-31'
                        WHEN Date < '1753-01-01' THEN '1753-01-01'
                        ELSE Date 
                    END as date,
                    CAST(Year as VARCHAR(4)) as year,
                    CAST(Month as VARCHAR(20)) as month,
                    CAST(Weeks as INT) as weeks,
                    CAST(Day as VARCHAR(20)) as day,
                    CAST(ContractOrderNumber as VARCHAR(50)) as contract_order_number,
                    CAST([Bin Volume Type] as VARCHAR(50)) as bin_volume_type,
                    CAST([Rental Rate] as DECIMAL(18,2)) as rental_rate,
                    CAST([Discount Rate] as DECIMAL(5,2)) as discount_rate,
                    CAST([Escalation Rate] as DECIMAL(5,2)) as escalation_rate
                FROM [OdooIntegrationDB].[dbo].[vw_Rental_Rate_Report]
            ''')
            records = cursor.fetchall()
            for row in records:
                self.env['sql.rental.rate.report'].create(row)
        except Exception as e:
            raise UserError(_("Error loading Rental Rate Report: %s" % str(e)))

    def _load_transport_rate_analysis(self, cursor):
        """Load Transport Rate Analysis data"""
        try:
            self.env['sql.transport.rate.analysis'].search([]).unlink()
            cursor.execute('''
                SELECT 
                    CASE 
                        WHEN Date > '9999-12-31' THEN '9999-12-31'
                        WHEN Date < '1753-01-01' THEN '1753-01-01'
                        ELSE Date 
                    END as date,
                    CAST(Year as VARCHAR(4)) as year,
                    CAST(Month as VARCHAR(20)) as month,
                    CAST(Weeks as INT) as weeks,
                    CAST(Day as VARCHAR(20)) as day,
                    CAST([Manifest Number] as VARCHAR(50)) as manifest_number,
                    CAST([Service Offering Type] as VARCHAR(100)) as service_offering_type,
                    CAST([Waste Stream] as VARCHAR(100)) as waste_stream,
                    CAST([Waste Type] as VARCHAR(100)) as waste_type,
                    CAST([Transport Rate Type] as VARCHAR(50)) as transport_rate_type,
                    CAST([Exclusive Amount] as DECIMAL(18,2)) as exclusive_amount,
                    CAST([VAT Rate (%)] as DECIMAL(5,2)) as vat_rate,
                    CAST([Escalation Rate] as DECIMAL(5,2)) as escalation_rate,
                    CAST([Inclusive Amount] as DECIMAL(18,2)) as inclusive_amount
                FROM [OdooIntegrationDB].[dbo].[vw_Transport_Rate_Analysis_Report]
            ''')
            records = cursor.fetchall()
            for row in records:
                self.env['sql.transport.rate.analysis'].create(row)
        except Exception as e:
            raise UserError(_("Error loading Transport Rate Analysis: %s" % str(e)))

    def _load_transport_report(self, cursor):
        """Load Transport Report data"""
        try:
            self.env['sql.transport.report'].search([]).unlink()
            cursor.execute('''
                SELECT 
                    CASE 
                        WHEN Date > '9999-12-31' THEN '9999-12-31'
                        WHEN Date < '1753-01-01' THEN '1753-01-01'
                        ELSE Date 
                    END as date,
                    CAST(Year as VARCHAR(4)) as year,
                    CAST(Month as VARCHAR(20)) as month,
                    CAST(Weeks as INT) as weeks,
                    CAST(Day as VARCHAR(20)) as day,
                    CAST([Custom Invoice Type] as VARCHAR(50)) as custom_invoice_type,
                    CAST(ContractOrderNumber as VARCHAR(50)) as contract_order_number,
                    CAST([Service Offering Type] as VARCHAR(100)) as service_offering_type,
                    CAST([Waste Stream] as VARCHAR(100)) as waste_stream,
                    CAST([Waste Type] as VARCHAR(100)) as waste_type,
                    CAST([Rate Per Bin] as DECIMAL(18,2)) as rate_per_bin,
                    CAST([Rate Per Km] as DECIMAL(18,2)) as rate_per_km,
                    CAST([Rate Per Load] as DECIMAL(18,2)) as rate_per_load,
                    CAST([Fixed Transport Rate] as DECIMAL(18,2)) as fixed_transport_rate,
                    CAST([Discount Rate] as DECIMAL(5,2)) as discount_rate,
                    CAST([Escalation Rate] as DECIMAL(5,2)) as escalation_rate
                FROM [OdooIntegrationDB].[dbo].[vw_Transport_Report]
            ''')
            records = cursor.fetchall()
            for row in records:
                self.env['sql.transport.report'].create(row)
        except Exception as e:
            raise UserError(_("Error loading Transport Report: %s" % str(e)))

    def test_and_load_data(self):
        """Test connection and load all data"""
        try:
            self._load_all_views()
            
            # Update connection info with total records across all views
            total_records = (
                self.env['sql.bins.analysis'].search_count([]) +
                self.env['sql.revenue.analysis'].search_count([]) +
                self.env['sql.mine.contract.analysis'].search_count([]) +
                self.env['sql.logbook.entries'].search_count([]) +
                self.env['sql.vehicle.inspection'].search_count([]) +
                self.env['sql.waste.analysis'].search_count([]) +
                self.env['sql.bookings.analysis'].search_count([]) +
                self.env['sql.disposal.rate.analysis'].search_count([]) +
                self.env['sql.disposal.rate.report'].search_count([]) +
                self.env['sql.rental.rate.report'].search_count([]) +
                self.env['sql.transport.rate.analysis'].search_count([]) +
                self.env['sql.transport.report'].search_count([])
            )
            
            self.write({
                'last_refresh': fields.Datetime.now(),
                'record_count': total_records
            })
            
            return {
                'type': 'ir.actions.act_window',
                'name': _('Connection Status'),
                'res_model': self._name,
                'view_mode': 'tree,form',
                'target': 'main',
            }
            
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Connection Failed'),
                    'message': str(e),
                    'type': 'danger',
                    'sticky': True,
                }
            }

    def unlink(self):
        """Override unlink to prevent deleting active connection"""
        for connection in self:
            if connection.is_active:
                raise UserError(_("Cannot delete active connection. Please deactivate it first."))
        return super().unlink() 