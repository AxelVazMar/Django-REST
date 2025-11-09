from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "stock",
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greather than 0"
            )
        return value

# Nesting serializers

class OrderItemSerializer(serializers.ModelSerializer):
    
    # way to obtain a nested serializer
    # product = ProductSerializer() 

    # Way to obtain an specific fields and avoid get all the nested serializers in the response
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='product.price',
        )

    class Meta:
        model = OrderItem
        fields = (
            'product_name', 
            'product_price',
            'quantity',
            'item_subtotal',
        )

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only = True)
    total_price = serializers.SerializerMethodField(method_name='total') # we can use the method_name to call the method with a ShortName

    def total(self, obj):
        # obj is an instance of the model 'Oder'
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items) 

    class Meta:
        model = Order
        fields = (
            'id', 
            'created_at', 
            'user', 
            'status', 
            'items',
            'total_price',
        )

class ProductInfoSerializer(serializers.Serializer):
    """
    Get all products, count of products, max price
    """
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
