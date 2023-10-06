from odoo import models, fields,api


class CountryName(models.Model):
    _name = "country.name"
    _description = "country name"
    _rec_name="country2"

    # name = fields.Char(string="client_name")
    country_code = fields.Integer(string='code')
    country2=fields.Char(string="country")
    client=fields.Many2many('visa.application')
    count_client=fields.Integer(string="count",compute="_compute_count_client")

    # tag_id= fields.Many2one('all.tag',related="country2.tag_id")

    # tag_related = fields.Many2many(comodel_name='client.tag',string="tag",related='country.tag_related')

    #IF NO REC_NAME IN MODEL
    # @api.model
    # def name_create(self,name):
    #     return self.create({'country':name}).name_get()[0]
    @api.model
    @api.depends('client')
    def _compute_count_client(self):
        for rec in self:
            rec.count_client = len(rec.client)