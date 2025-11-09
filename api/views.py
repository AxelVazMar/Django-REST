from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from api.serializers import ProductSerializer, OrderSerializer, OrderItemSerializer, ProductInfoSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics

# Generics views

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id' # We can use lookup_field to search some object in the url argument e.g: /products/id/ or /products/name/

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer

# API VIEWS

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# View to list 1 product filtering by the id
# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk) # how this is a single object we don't need a many=true
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related('items__product')
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)
