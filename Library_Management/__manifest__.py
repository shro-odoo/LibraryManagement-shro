# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Library Management',
    'description': 'A Library Management System is used to organize, track and manage library resources and services.',
    'summary': 'Library management system',
    'installable': True,
    'depends': ['base','website'],
    'application': True,
    'license': 'OEEL-1',
    'version': '1.0',
    'data': [
        'security/ir.model.access.csv',
        'report/library_book_report.xml',
        'views/library_book_template_views.xml',
        'report/library_book_template.xml',
        'wizard/add_customer_books_views.xml',
        'views/library_customer_views.xml',
        'views/library_author_views.xml',
        'views/library_books_views.xml',
        'views/library_menus.xml'
    ],
}



