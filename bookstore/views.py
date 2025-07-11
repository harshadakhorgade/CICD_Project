from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Author, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .models import Book, Order, OrderItem, Customer

# 📚 List all books
def book_list(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'bookstore/book_list.html', {'books': books})

# 📖 Book detail
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookstore/book_detail.html', {'book': book})

# 🛒 Create order (demo purpose)
@login_required
def create_order(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    quantity = 1

    customer, created = Customer.objects.get_or_create(user=request.user)

    order = Order.objects.create(customer=customer)
    OrderItem.objects.create(order=order, book=book, quantity=quantity)

    return redirect('order_detail', order_id=order.id)

# 💳 View single order details
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
    items = order.items.select_related('book')
    total_price = sum(item.total_price for item in items)

    return render(request, 'bookstore/order_detail.html', {
        'order': order,
        'items': items,
        'total_price': total_price,
    })

# 🧾 List all orders for current user
@login_required
def order_list(request):
    orders = Order.objects.filter(customer=request.user.customer).order_by('-created_at')
    return render(request, 'bookstore/order_list.html', {'orders': orders})

# 📊 Stats example view
def stats_view(request):
    total_books = Book.objects.aggregate(Sum('stock'))['stock__sum'] or 0
    total_authors = Author.objects.count()

    return render(request, 'bookstore/stats.html', {
        'total_books': total_books,
        'total_authors': total_authors,
    })
