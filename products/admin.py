from django.contrib import admin
from .models import Order, Product,Category,OrderProduct,Customer

admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(OrderProduct)
admin.site.register(Customer)

