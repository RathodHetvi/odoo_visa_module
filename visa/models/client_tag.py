from odoo import models, fields,api


class ClientTag(models.Model):
    _name = "client.tag"
    _description = "client tag"
    _rec_name = "sequence"

    # name= fields.Char(string="tag")
    # tag_id= fields.Many2one('client.model.lines',string="tag",computed='_compute_tag_name')
    tag_id= fields.Many2many('all.tag',string="tag",compute='_compute_tag_name')
    # country = fields.Many2many('country.name',string='country name',related='client_ids.client_name.country')
    country = fields.Many2many('country.name',string='country name',related='client_ids.client_name.country')
    active = fields.Boolean(string="Active", default=True)
    sequence = fields.Many2one(string='client',related='client_ids.client_name')
    # client_ids = fields.Many2many('visa.application',string="client",computed='_compute_tag')
    client_ids = fields.One2many('client.model.lines','visa_application_client',string="client")#,inverse='_inverse_tag'
    # count_country = fields.Integer(compute='compute_client_code')
    count_country = fields.Integer(string="count",compute="_compute_len_country")
    # color=fields.Integer("color") #have to be integer field for color

    _sql_constraints = [
        ('unique_tag_name','unique (sequence)','no. must be unique. ')

    ]

    # @api.depends('tag_id')
    # def _inverse_tag(self):
    #     for rec in self:
    #
    #         # rec.filtered("visa_type_tag.is_tag_id")
    #         rec.client_ids.visa_type_tag=rec.tag_id.visa_type_tag
    #         # rec.client_ids.name=rec.tag_id.name

    @api.depends('client_ids')
    def _compute_tag_name(self):
        for rec in self:
            rec.tag_id = rec.client_ids.client_name.visa_type_tag
            # rec.tag_id = rec.country.tag_id
    @api.model
    @api.depends('country')
    def _compute_len_country(self):
        for rec in self:
            rec.count_country = len(rec.country)


class ClientModelLines(models.Model):
    _name = "client.model.lines"
    _description = "client model lines"
    _rec_name = "client_name"
    #visa_client_name = fields.Many2one(comodel_name='visa.application', string="client")
    client_name = fields.Many2one(comodel_name='visa.application')
    country=fields.Many2many(related='client_name.country')
    visa_type_tag= fields.Many2many(related='client_name.visa_type_tag')
    ref = fields.Char(compute="_compute_ref",string="Reference")#,compute="_compute_ref,comodel_name ='visa.application',

    visa_application_client = fields.Many2one('client.tag')

    @api.depends("client_name")
    def _compute_ref(self):
        for rec in self:
            rec.ref = rec.client_name.ref


class AllTag(models.Model):
    _name='all.tag'
    _description = "all tag"
    _rec_name = "tag_name"

    tag_name=fields.Char(string='tag_name')
    visa_type_tag = fields.Many2many(comodel_name='visa.application', string="Tags")

    # color=fields.Integer(string='color')





