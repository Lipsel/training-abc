from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class EstateType(models.Model):
    _name = "real.estate.type"
    _description = "Real Estate Type"
    _order = 'sequence, name'
    
    sequence = fields.Integer(default=1)
    name = fields.Char(string="Name")
    
    property_ids = fields.One2many('real.estate', 'real_estate_type_id', string="Properties")
    property_count = fields.Integer(compute="_compute_property_count")
    
    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for vals in vals_list:
            self.env["real.estate.tag"].create(
                {
                    "name": vals.get("name")
                }
            )
        return res
    
    def unlink(self):
        self.property_ids.state = "cancelled"
        return super().unlink()
    
    @api.depends("property_ids")
    def _compute_property_count(self):
        for rec in self:
            rec.property_count = len(rec.property_ids)
    
    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            existing = self.search([('name', '=', record.name), ('id', '!=', record.id)])
            if existing:
                raise ValidationError("Il nome del type deve essere unico")
    
    
    def action_open_property_ids(self):
        return {
            "name": _("Related Properties"),
            "type": "ir.actions.act.window",
            "view_mode": "list,form",
            "res_model": "real.estate",
            "target": "current",
            "domain": [("real_estate_type_id", "=", self.id)],
            "context": {"default_real_estate_type_id": self.id}
        }
    