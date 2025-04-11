from datetime import timedelta
from odoo import fields, models, api

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
        required=True
    )
    
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