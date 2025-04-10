from odoo import models, fields

class RealEstate(models.Model):
    _name = "real.estate"
    _description = "Real Estate Module"
    
    
    name = fields.Char(
        required=True
    )
    
    description = fields.Text()
    
    postcode = fields.Char()
    
    def _default_date(self):
        return fields.Date.today()
    
    date_availability = fields.Date(
        default=_default_date
    )
    
    active = fields.Boolean(
        default=True,
        invisible=True
    )
    
    
    expected_price = fields.Float(required=True)
    
    selling_price = fields.Float(readonly=True)
    
    bedrooms = fields.Integer(default=2)
    
    living_area = fields.Integer(string="Living Area (sqm)")
    
    facades = fields.Integer()
    
    garage = fields.Boolean()
    
    garden = fields.Boolean()
    
    garden_area = fields.Integer()
    
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    
    state = fields.Selection(
        [
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="new"
    )
    
    real_estate_type_id = fields.Many2one(
        "real.estate.type"
    )
    
    offer_ids = fields.One2many(
        "real.estate.offer",
        "property_id"
    )
    
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
        index=True
    )
    
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False,
        index=True
    )
    
    
    
    
    
    
    
    
    
    
    
    
    