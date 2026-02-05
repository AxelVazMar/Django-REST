from django.db import transaction
from .models import Product, Order, OrderItem, User
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name",
            "description",
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

class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = (
                'product',
                'quantity'
            )

    id = serializers.UUIDField(read_only = True)
    items = OrderItemCreateSerializer(many=True)

    def update(self, instance, validated_data):
        orderitem_data = validated_data.pop('items')

        with transaction.atomic():
            instance = super().update(instance, validated_data)
            
            if orderitem_data is not None:
                # Clear existing items (optional, depends on requirements)
                instance.items.all().delete()

                # Recreate items with updated data
                for item in orderitem_data:
                    OrderItem.objects.create(order=instance, **item)
        return instance

    def create(self, validated_data):
        orderitem_data = validated_data.pop('items')

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            for item in orderitem_data:
                OrderItem.objects.create(order=order, **item)
        
        return order

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'status',
            'items',
        )
        # Setting the user automatically
        extra_kwargs = {
            'user': {'read_only': True}
        }

class OrderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only = True) # Making this read only so if we need to create an order, the id would be generated auto
    items = OrderItemSerializer(many=True, read_only=True)
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

class UserItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')

    class Meta:
        model = OrderItem
        fields = (
            'product_name',
        )

class UserOrderSerializer(serializers.ModelSerializer):
    items = UserItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'items',
        )

class UserSerializer(serializers.ModelSerializer):
    orders = UserOrderSerializer(many=True, read_only=True)
    total_orders = serializers.SerializerMethodField(method_name='get_total_orders')

    def get_total_orders(self, obj):
        return obj.orders.count()

    class Meta:
        model = User
        fields = (
            'username', 
            'user_permissions', 
            'is_authenticated', 
            'get_full_name', 
            'orders',
            'total_orders'
        )
        # fields = (
        #     'username',
        #     'email',
        #     'is_staff',
        #     'is_superuser'
        # )