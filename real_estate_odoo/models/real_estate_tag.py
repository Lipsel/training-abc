from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EstatePropertyTag(models.Model):
    _name = 'real.estate.tag'
    _description = 'Property Tag'
    _order = "name"
    

    name = fields.Char(required=True)
    color = fields.Integer()
    
    
    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            existing = self.search([('name', '=', record.name), ('id', '!=', record.id)])
            if existing:
                raise ValidationError("Il nome del tag deve essere unico")