# -*- coding: utf-8 -*-
from odoo import models, fields


class Publisher(models.Model):
    _name = "library.publisher"
    _description = "Publisher"
    _sql_constraints = [
        ('unique_publisher_name', 'UNIQUE(name)', 'Publisher name must be unique.')
    ]

    name = fields.Char(required=True)
    books_ids = fields.One2many('library.book', 'publisher_id', string="Books")
