from odoo import models, fields, api, _
from odoo.exceptions import UserError


class VisaAppointment(models.Model):
    _name = "visa.appointment"
    # _registry =
    _description = "client appointment"
    _rec_name = "client_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    client_id = fields.Many2one(comodel_name='visa.application', string="client")
    user_id = fields.Many2one('res.users', string='User',tracking=True, readonly=True,
                              states={'draft': [('readonly', False)]}, default=lambda self: self.env.user)#track_visibility='onchange'
    role = fields.Selection(string="role",default="client",related="client_id.role")
    # gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="gender", default='male',
    #                           related='client_id.gender')
    gender = fields.Selection(related='client_id.gender')
    appointment_time = fields.Datetime(string="Appointment time", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
    ref = fields.Char(string="Reference")
    feedback = fields.Html(string="Feedback")
    reason = fields.Char(string= "cancellation reason")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('approved', 'Approved'),
        ('cancelled', 'cancelled')], default='draft', string="Status", required="True")

    @api.onchange('client_id')
    def onchange_client_id(self):
        self.ref = self.client_id.ref
        # raise UserError(_("ref is changed"))

    def action_test(self):
        return{
            'type': 'ir.actions.act_url',
            'url': self.feedback,
            'target':'new' #open in new window 'new','self'
        }

    def action_in_consultation(self):
        for rec in self:
            rec.state = 'in_consultation'

            #search method
            clients = self.env['visa.application'].search([])
            print('clients...',clients)
            female_clients = self.env['visa.application'].search([('gender','=','female'),('age','<=',40)])  #and
            female = self.env['visa.application'].search(['|',('gender','=','female'),('gender','=','male')]) #or
            print('females are...',female_clients)
            print(female)

            #SEARCH_COUNT
            client_count = self.env['visa.application'].search_count([])
            print('clients_counts are',client_count)

            #ref orm
            client = self.env.ref('visa.view_visa_application_tree') # orm method
            print(client)
            browse_result = self.env['visa.application'].browse(200)
            browse_result_search = self.env['visa.application'].search([('id','=',6)])

            browse_result_multi = self.env['visa.application'].browse([1,2]) #bowse multi use list

            print(browse_result)
            print(browse_result_multi)
            print('search ..',browse_result_search)

            # if browse_result.exists():
            #     print("exist")
            # else:
            #     print("not")


    def action_approve(self):
        for rec in self:
            rec.state = 'approved'

        return {
            'effect': {
                'fadeout': 'fast',
                'message': 'click successful',
            }
        }

    def action_cancel(self):
        # action = self.env.ref('visa.action_cancel_appointment').read()[0]  # orm method
        #or
        action =self.env['ir.actions.act_window']._for_xml_id('visa.action_cancel_appointment')
        #or
        # action ={
        #     'type':'ir.actions.act_windows',
        #     'res_model':'cancel.appointment.wizard',
        #     'view_mode':'form',
        #     'target':'new'
        # }
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.model
    def test_cron_job(self):
            print('abc')
