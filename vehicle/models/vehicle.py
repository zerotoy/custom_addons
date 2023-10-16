# -*- coding: utf-8 -*-
from odoo import models, fields, api

class VehicleBrand(models.Model):
    _name = 'vehicle.brand'

    name = fields.Char(string='Name',required=True,index=True)

    type_ids = fields.One2many(
        string='Type',
        comodel_name='vehicle.type',
        inverse_name='brand_id',
    )

class VehicleYear(models.Model):
    _name = 'vehicle.year'

    name = fields.Char(string='Year',required=True,index=True)
    
class VehicleType(models.Model):
    _name = 'vehicle.type'

    name = fields.Char(string='Name',required=True,index=True)
    brand_id = fields.Many2one(string='Brand',comodel_name='vehicle.brand',ondelete='restrict',)

class VehicleModel(models.Model):
    _name = 'vehicle.model'

    name = fields.Char(string='Name',required=True,index=True)
    type_id = fields.Many2one(string='Type',comodel_name='vehicle.type',ondelete='restrict',)
    
    pricelist_ids = fields.One2many(
        string='Pricelist',
        comodel_name='vehicle.pricelist',
        inverse_name='model_id',
    )

class VehiclePricelist(models.Model):
    _name = 'vehicle.pricelist'

    name = fields.Char(string='Code',required=True,index=True)
    price = fields.Float(string='Price',digits='account',required=True)
    model_id = fields.Many2one(string='Model',comodel_name='vehicle.model',ondelete='restrict',)
    year_id = fields.Many2one(string='Year',comodel_name='vehicle.year',ondelete='restrict', required=True)
