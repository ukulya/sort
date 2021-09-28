from django.conf import settings

CART_SESSION_KEY = getattr(settings, 'CART_SESSION_KEY', 'CART')
