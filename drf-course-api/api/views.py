from django.db.models import Max
# from django.shortcuts import get_object_or_404
from api.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem

# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)
from rest_framework import generics
from rest_framework.views import APIView

class ProductListCreateAPIView(generics.ListCreateAPIView):
    # queryset = Product.objects.filter(stock__gt=0) // check stock greater than 0
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ProductDetailAPIView(generics.RetrieveAPIView): # default is pk
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

class OrderListAPIView(generics.ListAPIView):
    # queryset = Product.objects.filter(stock__gt=0) // check stock greater than 0
    queryset =Order.objects.prefetch_related('items__product').all()
    serializer_class =  OrderSerializer

class UserOrderListAPIView(generics.ListAPIView):
    # queryset = Product.objects.filter(stock__gt=0) // check stock greater than 0
    queryset =Order.objects.prefetch_related('items__product').all()
    serializer_class =  OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=user)

class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)