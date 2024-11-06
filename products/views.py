# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Product, Customer, Order, Cart, CartItem
from .serializers import CategorySerializer, ProductSerializer, CustomerSerializer, OrderSerializer, CartSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem, Customer, Product
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_cart(self, request):
        # Mavjud customer ni olish
        customer = Customer.objects.get(phone_number=request.user.username)  # yoki request.user.id
        cart, created = Cart.objects.get_or_create(customer=customer)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        customer = Customer.objects.get(phone_number=request.user.username)  # yoki request.user.id
        cart, created = Cart.objects.get_or_create(customer=customer)

        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # CartItem ni yaratish yoki yangilash
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity  # Agar allaqachon mavjud bo'lsa, miqdorni yangilaymiz
        cart_item.save()

        # Savatchani qaytaramiz
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def remove_from_cart(self, request):
        customer = Customer.objects.get(phone_number=request.user.username)  # yoki request.user.id
        cart = Cart.objects.get(customer=customer)

        product_id = request.data.get('product_id')

        try:
            cart_item = CartItem.objects.get(cart=cart, product__id=product_id)
            cart_item.delete()  # CartItem ni o'chirish
            return Response({'status': 'item removed from cart'}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
