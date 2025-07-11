from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Author, Book, Customer, Order, OrderItem

# Inline for OrderItem inside Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'price', 'stock')
    list_filter = ('author',)
    search_fields = ('title', 'author__name')
    list_editable = ('price', 'stock')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone')
    search_fields = ('user__username', 'phone')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('customer__user__username',)
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'book', 'quantity')
    list_filter = ('order', 'book')
