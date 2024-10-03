from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view,  permission_classes, renderer_classes, parser_classes
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.exceptions import PermissionDenied, NotFound
from crypto.api.custom_functions import get_currency_price

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def get_price(request):
    if request.method == 'GET':
        currency_symbol = request.query_params.get('symbol')
        data = {}
        data['name'], data['symbol'], data['price'] = get_currency_price(currency_symbol)
        return Response(data=data, status=status.HTTP_200_OK)