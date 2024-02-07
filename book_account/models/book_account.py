from odoo import api, fields, models, Command
from odoo.exceptions import UserError, ValidationError

class BookAccount(models.Model):
    _inherit = "library.book"

    def action_sold(self):
        for book in self:
            if book.availability_status != 'available':
                raise UserError("This book is not available for sale.")
            if not book.buyer_id:
                raise UserError("A buyer must be specified before selling the book.")
            
            # Create an account move for the sale
            values = {
                'partner_id': book.buyer_id.id,
                'move_type': 'out_invoice',
                'line_ids': [
                    Command.create({
                        'name': book.name,
                        'quantity': 1,
                        'price_unit': book.price
                    })
                ],
            }
            self.env['account.move'].create(values)
        return super().action_sold()
        

