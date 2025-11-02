from django.http import JsonResponse
from api.serializers import ProductSerializer
from api.models import Product

def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse({
        'data': serializer.data # .data is the representation of the data of the content serializer variable
    })