
from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError


class ReportVehicleWizard(models.TransientModel):
    _name = "report.vehicle.wizard"
    _description = "Create Report Vehicle"

    type_id = fields.Many2one(string='Type',comodel_name='vehicle.type',ondelete='restrict',readonly=False)
    brand_id = fields.Many2one(string='Brand',comodel_name='vehicle.brand',ondelete='restrict',readonly=False)
    year_id = fields.Many2one(string='Year',comodel_name='vehicle.year',ondelete='restrict',readonly=False)
    range_min = fields.Float(string='Price Minimum',)
    range_max = fields.Float(string='Price Max',)
    
    @api.onchange('type_id')
    def _onchange_type(self):
        if not self.type_id:
            self.update({'brand_id':False})
            return{
                'domain': {
                    'brand_id': [('id', '!=', False)]
                }
            }
        self.update({'brand_id':self.type_id.brand_id.id})
        return {
            'domain': {
                'brand_id': [('id', '=', self.type_id.brand_id.id)]
            }
        }
    
    @api.onchange('brand_id')
    def _onchange_brand(self):
        if not self.brand_id:
            return{
                'domain': {
                    'type_id': [('id', '!=', False)]
                }
            }
        return {
            'domain': {
                'type_id': [('brand_id.id', '=', self.brand_id.id)]
            }
        }

    def run_report(self):
        Pricelist = self.env['vehicle.pricelist']
        domain = [('id','!=',False)]
        if self.brand_id:
            domain += [('model_id.type_id.brand_id.id','=',self.brand_id.id)]
        if self.type_id:
            domain += [('model_id.type_id.id','=',self.type_id.id)]
            self.update({'brand_id':self.type_id.brand_id.id})
            domain += [('model_id.type_id.brand_id.id','=',self.type_id.brand_id.id)]
        if self.year_id:
            domain += [('year_id.name','=',self.year_id.name)]
        if self.range_min>0:
            domain += [('price','>',self.range_min)]
        if self.range_max>0:
            domain += [('price','<',self.range_max)]
        prices = Pricelist.search(domain)
        if not prices:
            raise ValidationError(_("Cannot find any Model suited for that filter. Please make it less sophisticated filter!"))
        line_ids = []
        for price in prices:
            line={'price_list_id':price.id}
            line_ids.append([0,0,line])

        data = {
            'type':self.type_id.name or "All Type",
            'brand':self.brand_id.name or "All Brand",
            'range_min':self.range_min,
            'range_max':self.range_max,
            'line_ids':line_ids
        }
        wiz_res = self.env['report.vehicle.result'].create(data)
        # raise ValidationError(_("Dunno"))
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref("vehicle.report_vehicle_result_form").id,
            'res_model': 'report.vehicle.result',
            'res_id': wiz_res.id,
            'type': 'ir.actions.act_window'
        }

class ReportVehicleResult(models.TransientModel):
    _name = "report.vehicle.result"
    _description = "Report Vehicle Result"
    
    
    type = fields.Char(string='Type',)
    brand = fields.Char(string='Brand',)
    range_min = fields.Float(string='Price Minimum',)
    range_max = fields.Float(string='Price Max',)
    line_ids = fields.One2many(string='Report Line',comodel_name='report.vehicle.result.line',inverse_name='report_vehicle_result_id', readonly=True)

class ReportVehicleResult(models.TransientModel):
    _name = "report.vehicle.result.line"
    _description = "Create Report Vehicle"
    _order = "brand_id,type_id,model_id"

    report_vehicle_result_id = fields.Many2one(string='Result',comodel_name='report.vehicle.result',ondelete='restrict',readonly=False)
    price_list_id = fields.Many2one(string='Price',comodel_name='vehicle.pricelist',ondelete='restrict',readonly=False)
    model_id = fields.Char(string='Model',related='price_list_id.model_id.name')
    type_id = fields.Char(string='Model',related='price_list_id.model_id.type_id.name')
    brand_id = fields.Char(string='Model',related='price_list_id.model_id.type_id.brand_id.name')
    year = fields.Char(string='Year',related='price_list_id.year_id.name')
    price = fields.Float(string='Price',related='price_list_id.price')
