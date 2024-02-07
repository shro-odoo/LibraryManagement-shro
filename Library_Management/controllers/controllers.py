from odoo import http
from odoo.http import request

class Library(http.Controller):

    @http.route(['/library','/library/page/<int:page>'], auth='public', website=True)
    def index(self, page=1, date=None, **kw):
        Book = request.env['library.book']
        domain = [('availability_status', 'not in', ['borrowed'])]
        
        page = int(page)
        books_per_page = 6
        total_books = Book.search_count(domain)
        total_pages = (total_books + books_per_page - 1) // books_per_page
        books = Book.search(domain, limit=books_per_page, offset=(page - 1) * books_per_page)

        pager = request.website.pager(
            url='/library',
            total=total_books,
            page=page,
            step=books_per_page,
            scope=total_books,
        )

        return request.render('Library_Management.index', {
            'books': books,
            'pager': pager
        })

    @http.route('/library/<int:book_id>/', auth='public', website=True)
    def book_details(self, book_id):
        book = http.request.env['library.book'].browse(book_id)
        return http.request.render('Library_Management.book_details', {
        'book': book
        })
        

