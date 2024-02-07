from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

class Book(models.Model):
    _name = "library.book"
    _description = "Book"
  
    name = fields.Char(string="Name")
    description = fields.Text()
    price = fields.Float(required=True)
    edition = fields.Char(string="Edition", size=100)
    language = fields.Selection([
        ('english', 'English'),
        ('french', 'French'),
        ('german', 'German'),
        ('spanish', 'Spanish'),
        ('italian', 'Italian'),
        ('japanese','Japanese'),
        ('other', 'Other'),
    ], string="Language", help="The language in which the book is written.")
    types = fields.Selection(
        [('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('sci-fi', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('mystery', 'Mystery'),
        ('horror', 'Horror'),
        ('romance', 'Romance'),
        ('thriller', 'Thriller'),
        ('biography', 'Biography'),
        ('self-help', 'Self-Help'),
        ('poetry', 'Poetry'),
        ('drama', 'Drama'),
        ('history', 'History'),
        ('children', 'Children'),
        ('manga', 'Manga'),
        ('comic', 'Comic')]
    )
    total_books = fields.Integer()
    image = fields.Image('Image', max_height=100, max_width=100, copy=False)
    author_name = fields.Char(related='author_id.name', string='Author Name')
    customer_ids = fields.Many2many('library.customer', string="Customer")
    author_id = fields.Many2one('library.author', string="Author")
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    publisher_id = fields.Many2one('library.publisher', string="Publisher")
    end_date = fields.Datetime(string='End Date', compute='_compute_end_date', store=True)
    total_price = fields.Float(string="Total Price", compute="_compute_total_price")
    availability_status = fields.Selection(
        selection=[('available', 'Available'), ('borrowed', 'Borrowed'), ('sold','Sold'), ('notfound', 'Not Found')],
        string="Availability Status",
        default='available'
    )
    
    _sql_constraints = [
        ('positive_price', 'CHECK(price >= 0)', 'Price must be positive.'),
        ('positive_total_books', 'CHECK(total_books >= 0)', 'Total books must be positive.')
    ]
    
    @api.depends('create_date')
    def _compute_end_date(self):
        for record in self:
            record.end_date = record.create_date + relativedelta(days=6)

    @api.depends('price', 'total_books')
    def _compute_total_price(self):
        for book in self:
            book.total_price = book.price * book.total_books

    def _inverse_total_price(self):
        for book in self:
            if book.total_books != 0:
                book.price = book.total_price / book.total_books
            else:
                book.price = 0.0

    @api.constrains('price')
    def _check_positive_price(self):
        for book in self:
            if book.price <= 0:
                raise ValidationError("Price must be a positive value.")
    
    def action_borrow(self):
        for book in self:
            if book.availability_status != 'available':
                raise UserError("This book is not available for borrowing.")
            book.availability_status = 'borrowed'

    def action_return(self):
        for book in self:
            if book.availability_status != 'borrowed':
                raise UserError("This book is not borrowed.")
            book.availability_status = 'available'
    
    def action_sold(self):
        for book in self:
            if book.availability_status != 'available':
                raise UserError("This book is not available for sale.")
            book.availability_status = 'sold'

            

                