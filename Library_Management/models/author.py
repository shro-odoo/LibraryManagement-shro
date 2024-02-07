# -*- coding: utf-8 -*-
from odoo import models, fields


class Author(models.Model):
    _name = "library.author"
    _description = "Author"
    _sql_constraints = [
        ('unique_author_name', 'UNIQUE(name)', 'Author name must be unique.')
    ]

    name = fields.Char(required=True)
    books_ids = fields.One2many('library.book', 'author_id', string="Books")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    
