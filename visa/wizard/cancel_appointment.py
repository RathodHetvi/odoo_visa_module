from odoo import models, fields,api
from odoo.tests import Form
import datetime

class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"


    @api.model
    def default_get(self,fields):
        d = super(CancelAppointmentWizard,self).default_get(fields)
        d['date_cancel'] = datetime.date.today()
        return d



    appointment_id = fields.Many2one('visa.appointment',string="Appointment",domain=[('state','=','draft')])
    reason= fields.Char(string="Reason")
    date_cancel= fields.Date(string="Cancellation Date")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('approved', 'Approved'),
        ('cancelled', 'cancelled')], default='draft', string="Status", required="True")

    def action_cancel(self):
        # for rec in self:
        #     rec.state='cancel'
        for rec in self:
            self.appointment_id.state = 'cancelled'
            # e =self.env.context.get('active_ids')
            # f=self.env['visa.appointment'].browse(e)
            # f.reason=self.reason
            # print(f.reason)
            e=self.env['visa.appointment'].browse(self._context.get('active_ids'))
            print(self._context)
            e.reason = self.reason

            # visa_appointment_form = Form(
            #     self.env['cancel.appointment.wizard'].with_context(active_id=rec.reason, active_model='visa.appointment'))
            # reason = visa_appointment_form.reason
            # print(reason)
            # h=self.env['visa.appointment'].browse(rec.reason).write({'reason':rec.reason})
            # # h.reason=self.reason/
            # print(h)

            #return super(CancelAppointmentWizard, self).write(self.reason)









