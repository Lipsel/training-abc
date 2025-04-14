from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

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
    
    expected_price = fields.Float(
        required=True
    )
    
    selling_price = fields.Float(
        readonly=True
    )
    
    bedrooms = fields.Integer(
        default=2
    )
    
    living_area = fields.Integer(
        string="Living Area (sqm)"
    )
    
    facades = fields.Integer()
    
    garage = fields.Boolean()
    
    garden = fields.Boolean()
    
    garden_area = fields.Integer()
    
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area"
    )
    
    best_offer = fields.Float(
        string="Best Offer Price",
        compute="_compute_best_offer"
    )
    
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
    
    tag_ids = fields.Many2many(
        "real.estate.tag",
        string="Tags"
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
    
    def action_accept(self):
        """
        Accept the current offer and update the property's buyer and selling price.
        Ensure only one offer can be accepted per property.
        """
        for offer in self:
            # Check if there is already an accepted offer for the property
            if offer.property_id.offer_ids.filtered(lambda o: o.status == "accepted"):
                raise UserError(_("Only one offer can be accepted for a property."))

            # Update the property's buyer and selling price
            offer.property_id.write({
                'buyer_id': offer.partner_id.id,
                'selling_price': offer.price,
            })

            # Set the current offer's status to "accepted"
            offer.status = "accepted"

        return True

    def action_refuse(self):
        """
        Refuse the current offer by setting its status to "refused".
        """
        for offer in self:
            offer.status = "refused"
        return True
    
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise models.UserError(_("Una proprietà cancellata non può essere venduta"))
            record.state = 'sold'
        return True
    
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise models.UserError(_("Una proprietà venduta non può essere cancellata"))
            record.state = 'canceled'
        return True
    
    #Fa la somma di living area e garden area per vedere l'area totale
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")  
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price')) if record.offer_ids else 0
    
    
    @api.onchange("garden")
    def _onchange_garden(self):
        for estate in self:
            if not estate.garden:
                estate.garden_area = 0
    
    
    @api.constrains("selling_price")
    def _check_constraint(self):
        for estate in self:
            if estate.selling_price < 5000:
                raise ValidationError(_("La vendita non deve essere minore di 5000"))
    
    @api.constrains('expected_price', 'selling_price')
    def _check_prices(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError(_("Il Valore Expected Price deve essere positivo"))
            if record.selling_price < 0:
                raise ValidationError(_("Il Selling Price deve essere positivo"))
    
    
    
    
    # @api.onchange("date_availability")
    # def _onchange_date_availability(self):
    #     for estate in self:
    #         return {
    #             "warning": {
    #                 "title": _("Warning"),
    #                 "message": ("My message")
    #             }
    #         }
    
    
    
    
    
    
    
    
    
    
    
    