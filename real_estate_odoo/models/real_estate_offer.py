from datetime import timedelta
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class RealEstateOffer(models.Model):
    _name = "real.estate.offer"
    _description = "Offers made for real estates"
    _offer = 'price desc'
    _sql_constraints = [
    ('check_offer_price_positive', 'CHECK(price > 0)', 'Offer price must be strictly positive.'),
]
    
    price = fields.Float()
    
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )
    
    validity = fields.Integer(string="Validity (Days)", default=7)
    
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    
    
    partner_id = fields.Many2one(
        "res.partner",
        required=True
    )
    
    property_id = fields.Many2one(
        "real.estate",
        # required=True,
    )
    
    def action_accept(self):
        self.ensure_one()
        if "accepted" in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("Text error"))
        self.status = "accepted"
        self.property_id.selling_price = self.price
    
    
    def action_refuse(self):
        self.ensure_one()
        self.status = "refused"
        return True
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                create_date = fields.Datetime.from_string(offer.create_date)
                offer.date_deadline = create_date + timedelta(days=offer.validity)
            else:
                # Fallback for new records not yet saved
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)
    
    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                create_date = fields.Datetime.from_string(offer.create_date)
                deadline = fields.Date.from_string(offer.date_deadline)
                offer.validity = (deadline - create_date.date()).days
    
    
    @api.constrains('price')
    def _check_offer_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("Il prezzo offerto deve essere positivo")
    
    
                
        
        
    