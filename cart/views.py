from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.serializers import CartSerializer, CartUpdateSerializer
from shop.models import SortdMargin
from shop.services import CartService, ProductService


class CartView(APIView):
    def get(self, request, *args, **kwargs):
        cart = CartService.get_cart(request)
        margin = SortdMargin.objects.first()
        margin = getattr(margin, 'value', 0)
        serializer = CartSerializer(
            data=cart.serialized, context={'margin': margin, 'request': request}
        )
        serializer.is_valid()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@method_decorator([csrf_exempt, ], 'dispatch')
class CartUpdateView(APIView):
    def validate_serializer(self, serializer_class):
        serializer = serializer_class(data=self.request.data)
        if not serializer.is_valid():
            return serializer, Response(
                data={'message': 'Ошибка обновления корзины', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        return serializer, None

    def put(self, request):
        serializer, error = self.validate_serializer(CartUpdateSerializer)
        if error:
            return error

        product, quantity = (
            serializer.validated_data['product'],
            serializer.validated_data['quantity']
        )
        cart = CartService.update_cart(
            product=product, quantity=quantity, request=request
        )
        return Response(data=cart.serialized, status=status.HTTP_200_OK)


@method_decorator([csrf_exempt, ], 'dispatch')
class RemoveItemFromCartAPIView(APIView):
    def get_object(self):
        return ProductService.get(slug=self.kwargs['slug'])

    def delete(self, request, slug):
        product = self.get_object()
        cart = CartService.remove(request=request, product=product)

        return Response(data=cart.serialized)
