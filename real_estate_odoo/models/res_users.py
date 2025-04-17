from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    property_ids = fields.One2many(
        'real.estate',  # related model
        'salesperson_id',  # inverse field
        string='Managed Properties',
        domain=[('state', 'in', ['new', 'received', 'accepted'])]  # only show available properties
    )