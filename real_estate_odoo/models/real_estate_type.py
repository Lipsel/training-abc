from odoo import fields, models, api
from odoo.exceptions import ValidationError

class EstateType(models.Model):
    _name = "real.estate.type"
    _description = "Real Estate Type"
    _order = "sequence desc"
    
    sequence = fields.Integer(default=1)
    name = fields.Char(string="Name")
    
    property_ids = fields.One2many('real.estate', 'real_estate_type_id', string="Properties")
    
    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            existing = self.search([('name', '=', record.name), ('id', '!=', record.id)])
            if existing:
                raise ValidationError("Il nome del type deve essere unico")
    