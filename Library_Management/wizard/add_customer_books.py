from odoo import fields, models, api


class LibraryBookAddCustomer(models.TransientModel):
    _name = 'library.book.add.customer'
    _description = 'Add customer to books'

    name = fields.Char(required=True)
    phone = fields.Char(string="Phone Number")
    bill_amount = fields.Float()
    amount_paid = fields.Float()
    new_customer = fields.Many2one('library.book')

    def action_add_customer(self):
        active_ids = self._context.get('active_ids')
        books = self.env['library.book'].browse(active_ids)
        customer_data = {
        'name': self.name,
        'phone': self.phone,
        'bill_amount': self.bill_amount,
        'amount_paid': self.amount_paid
        }
        for book in books:
            book.write({'customer_ids': [(0, 0, customer_data)]})



            