from odoo import models, fields, api
from datetime import date
from odoo import _
from odoo.exceptions import ValidationError
from dateutil import relativedelta
import logging


_logger = logging.getLogger(__name__)


class VisaApplication(models.Model):
    _name = "visa.application"
    _description = "client information"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string="name", required=True,tracking=True)
    ref = fields.Char(string="Reference")
    date_of_birth = fields.Date(string="date of birth",store=True)
    age = fields.Integer(string="Age", compute='_compute_age', inverse='_inverse_compute_age',store=True)
    adult = fields.Boolean(string="is_adult",compute='_compute_adult',default=True,store=True) #only compute function is readonly by default
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="gender", default='male')
    role = fields.Selection([('client', 'Client'), ('manager', 'Manager')],string="role",default="client")
    appointment_count = fields.Integer(compute='_compute_appointment_count',string="appointment_count",tracking=True)
    phone = fields.Char(string="Phone",size=10)  # many to many tag will not add coulmn in table made a separate table in datbase
    image = fields.Image(string='')

    # country= fields.Char(string='country')

    visa_type_tag = fields.Many2many(comodel_name='all.tag', string="Tags",tracking=True)
    # visa_type_tag = fields.Many2many(comodel_name='all.tag', string="Tags")
    country = fields.Many2many('country.name',string="country_name")










    # tag_ids = fields.Many2many(relation="relation2",comodel_name='client.tag', string="Tags")
    # country = fields.Many2many('country.name',string="country_name", compute="_compute_country_name")#related='tag_ids.country'
    # print('error')
    # tag_ids2 = fields.Many2many(relation="relation1",comodel_name='client.tag',string='tag2')
    #
    # visa_country_ids = fields.One2many('visa.country','visa_application_id',string="visa country")


    def action_report(self):
        return self.env.ref('visa.visa_report_client_detail').report_action(self) #report_idv

    @api.depends("tag_ids")
    def _compute_country_name(self):
        for record in self:
            record.country = record.tag_ids.country

    @api.depends('ref')
    def _compute_appointment_count(self):
        for rec in self:
            # appointment_count = self.env['visa.appointment'].search_count([('client_id','=',rec.id)])
            appointment_group = self.env['visa.appointment'].read_group(domain=[],fields=['client_id'],groupby=['client_id'])
            for appointment in appointment_group:
                client_id = appointment.get('client_id')[0]
                client_rec = self.browse(client_id)
                client_rec.appointment_count = appointment['client_id_count']
                self -= client_rec # for no appointmnets
        self.appointment_count = 0


    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("Entered date of Birth date is not acceptable"))

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1


    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    @api.depends('age')
    def _compute_adult(self):
        for rec in self:
            if rec.age < 18:
                rec.adult = False
                # print('no')

            else:
                rec.adult = True
                # print('yes')


    def action_open_appointments(self):
        return {
            'type':'ir.actions.act_window',
            'name':'Appointments',
            'res_model':'visa.appointment',
            'domain':[('client_id','=',self.id)],
            'view_mode':'tree,form',
            'target':'current',

        }



    #button action

    @api.model
    def create(self,vals):
        print("create triggered")
        return super(VisaApplication,self).create(vals)
        # for rec in self:
        #     vals={
        #         'name':'created',
        #         'age':18,
        #     }
        #     created=self.env['visa.application'].create(vals)
        #     print('created record',created,created.id)

    # #no decorator for write
    def write(self,vals):
        print("write triggered",vals)
        return super(VisaApplication,self).write(vals)

    def action_update(self):
        _logger.info("IT IS info ")
        _logger.warning("IT IS warning ")
        for rec in self:
            record_update = self.env['visa.application'].browse(13)
            if record_update.exists():
                vals = {
                    'name': 'created2',
                    'age': 18,
                    'ref': '013',

                }
                record_update.write(vals)

    def action_copy(self):
        for rec in self:

            record_copy = self.env['visa.application'].browse(self.id)
            vals = {
                'name': 'd'+self.name,
                'age': 17
            }
            record_copy.copy(vals)


    def action_unlink(self):
        for rec in self:
            record_unlink = self.env['visa.application'].browse(rec.id)
            record_unlink.unlink()

    def name_get(self):
        return [(rec.id,"%s:%s" % (rec.ref,rec.name)) for rec in self]

    #SHOW IN REC_NAME




class VisaCountry(models.Model):
    _name = "visa.country"
    _description = "country information"
    _rec_name="country"

    country = fields.Many2one('country.name', string="country name")
    country_code = fields.Integer(string='code', compute="_compute_country_code")
    visa_type_tag = fields.Many2many(comodel_name='all.tag',string="Tags")

    _order = "id desc"
    _sql_constraints = [
        ('unique_country_name', 'unique (country)', 'country must be unique. ')
    ]
    visa_application_id = fields.Many2one('visa.application')

    @api.depends("country")
    def _compute_country_code(self):
        for record in self:
            record.country_code = record.country.country_code

