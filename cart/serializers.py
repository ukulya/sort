from rest_framework import serializers

from shop.services import ProductService
from utils.constants import decimal_kwargs


class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    slug = serializers.SlugField()
    quantity = serializers.IntegerField()
    name = serializers.URLField()
    preview = serializers.SerializerMethodField()
    price = serializers.CharField(source='price_with_applied_modifiers')
    total = serializers.DecimalField(**decimal_kwargs)

    def get_preview(self, value):
        return self.context.get('request').build_absolute_uri(value)


class CartSerializer(serializers.Serializer):
    subtotal = serializers.DecimalField(**decimal_kwargs)
    total = serializers.DecimalField(**decimal_kwargs)
    products = CartItemSerializer(many=True)
    count = serializers.IntegerField()
    total_weight = serializers.SerializerMethodField()
    additional_costs = serializers.SerializerMethodField()

    @staticmethod
    def get_products_total_cost(cart: dict):
        return cart.get('total', 0)

    def get_total(self, cart: dict):
        total = cart.get('total', 0)
        margin = self.context.get('margin')
        return total + (total // 100 * margin)

    def get_additional_costs(self, cart: dict):
        margin = self.context.get('margin')
        return cart.get('total', 0) // 100 * margin

    @staticmethod
    def get_total_weight(cart: dict):
        product_ids = [product['id'] for product in cart['products']]
        return ProductService.get_total_weight_for_products(product_ids)


class CartRemoveSerializer(serializers.Serializer):
    product = serializers.SlugRelatedField(slug_field='slug', queryset=ProductService.all(), required=True)


class CartUpdateSerializer(CartRemoveSerializer):
    quantity = serializers.IntegerField(min_value=1, required=True)
