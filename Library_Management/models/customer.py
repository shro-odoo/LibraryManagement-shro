from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class Customer(models.Model):
    _name = "library.customer"
    _description = "Customer"
    _sql_constraints = [
        ('positive_amount_paid', 'CHECK(amount_paid >= 0)', 'Amount paid must be positive.')
    ]

    name = fields.Char(required=True)
    phone = fields.Char(string="Phone Number")
    bill_amount = fields.Float()
    payment_method = fields.Selection([
        ('cash', 'Cash'), ('credit_card', 'Credit Card'), ('bank_transfer', 'Bank Transfer')],
        string='Payment Method')
    amount_paid = fields.Float()
    borrowed_book_ids = fields.Many2many('library.book', string="Borrowed Books")
    is_bill_paid = fields.Boolean(string="Bill Paid", compute="_compute_is_bill_paid", store=True)

    @api.depends('amount_paid', 'bill_amount')
    def _compute_is_bill_paid(self):
        for customer in self:
            if customer.amount_paid == customer.bill_amount:
                customer.is_bill_paid = True
            else:
                customer.is_bill_paid = False

    @api.constrains('bill_amount', 'amount_paid')
    def _check_bill_amount(self):
        for customer in self:
            if customer.amount_paid > customer.bill_amount:
                raise ValidationError("Amount paid cannot be greater than bill amount.")