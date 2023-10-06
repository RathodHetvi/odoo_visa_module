from odoo.tests.common import TransactionCase

class TestCommonCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context,tracking_disable = True))

