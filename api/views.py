from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from api.serializers import ProductSerializer
from api.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# View to list 1 product filtering by the id
@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk) # how this is a single object we don't need a many=true
    serializer = ProductSerializer(product)
    return Response(serializer.data)