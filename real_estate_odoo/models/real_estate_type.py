from odoo import fields, models

class EstateType(models.Model):
    _name = "real.estate.type"
    _description = "Real Estate Type"
    
    name = fields.Char(string="Name")
    