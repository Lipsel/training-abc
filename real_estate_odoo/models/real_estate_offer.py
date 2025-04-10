from odoo import fields, models

class RealEstateOffer(models.Model):
    _name = "real.estate.offer"
    _description = "Offers made for real estates"
    _offer = 'price desc'
    
    price = fields.Float()
    
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    
    
    partner_id = fields.Many2one(
        "res.partner",
        required=True
    )
    
    property_id = fields.Many2one(
        "real.estate",
        required=True
    )