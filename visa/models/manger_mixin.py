from odoo import models,fields,api,_

class ManagerMixin(models.AbstractModel):
    _name="manager.mixin"
    _description="visa manager"

    active=fields.Boolean(string="active")
    s_no =fields.Char(string="s.no")
    joined_date=fields.Date(string="joined Date")

    def archive_this(self):
        self.active = False


class ManagerAgent(models.Model):
    _name = "manager.agent"
    _inherit= ["manager.mixin"]
    _description = "all agents"

    name = fields.Char(string="name")
    valid_till = fields.Date(string="licence valid")



class MangerConformer(models.Model):
    _name = "visa.conformer"
    _description = "visa conformer"

    name = fields.Char(string="name of conformer")

