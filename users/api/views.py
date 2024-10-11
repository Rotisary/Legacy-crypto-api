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


from users.models import User, Profile, Wallet, Fund
from users.api.serializers import (
    UserSerializer, 
    UserUpdateSerializer, 
    ProfileSerializer, 
    ChangePasswordSerializer,
    WalletSerializer,
    FundSerializer,
)

import random
import uuid
import string



@api_view(['POST', ])
@permission_classes([])
@parser_classes([JSONParser, MultiPartParser])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        id_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
        data = {}
        if serializer.is_valid(raise_exception=True):
            newuser = serializer.save(user_id=id_string)
            token = Token.objects.get(user=newuser).key
            data['respone'] = 'successfully registered user'
            data['email'] = newuser.email
            data['username'] = newuser.username
            data['name'] = newuser.name
            data['token'] = token
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

class ObtainAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [JSONParser, MultiPartParser]
    

    def post(self, request):
        data = {}

        email = request.data.get('email')
        password = request.data.get('password')
        account = authenticate(email=email, password=password)

        if account is not None:
            try:
                token = Token.objects.get(user=account).key
            except Token.DoesNotExist:
                create_token = Token.objects.create(user=account)
                token = create_token.key

            data['response'] = 'Successfully Authenticated'
            data['pk'] = account.pk
            data['email'] = account.email
            data['token'] = token
            status_code = status.HTTP_200_OK
        else:
            data['response'] = 'error'
            data['error_message'] = 'Invalid credentials'
            status_code = status.HTTP_400_BAD_REQUEST  
        return Response(data=data, status=status_code)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def user_detail_view(request, username):
    try:
        user = User.objects.get(username=username)

        if request.user != user:
            raise PermissionDenied
        else:
            if request.method == 'GET':
                serializer = UserSerializer(user, context={'request': request})
                data = serializer.data
                return Response(data=data)
    except User.DoesNotExist:
        raise NotFound(detail='this user does not exist')



@api_view(['PUT', ])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser])
def update_user_detail_view(request, username):
    try:
        user = User.objects.get(username=username)
    
        if request.user != user:
             raise PermissionDenied
        else:
            if request.method == 'PUT':
                serializer = UserUpdateSerializer(user, data=request.data, partial=True)
                data = {}
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    data['success'] = 'update successful'
                    return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        raise NotFound(detail='this user does not exist')


@api_view(['DELETE', ])
@permission_classes([IsAuthenticated])
def delete_user_view(request, username):
    try:
        user = User.objects.get(username=username)
   
        if request.user != user:
            raise PermissionDenied
        else:
            data = {}
            if request.method == 'DELETE':
                operation = user.delete()
                if operation:
                    data['success'] = 'delete successful'
                    status_code = status.HTTP_200_OK
                else:
                    data['error'] = 'failed to delete user'
                    status_code = status.HTTP_400_BAD_REQUEST
                
                return Response(data=data, status=status_code)
    except User.DoesNotExist:
        raise NotFound(detail='this user has already been deleted')
    

class ChangePasswordApiView(UpdateAPIView):
    authentication_classes = ([TokenAuthentication, ])
    permission_classes = ([IsAuthenticated, ])
    parser_classes = [JSONParser, MultiPartParser]
    serializer_class = ChangePasswordSerializer
    model = User


    def get_object(self, queryset=None):
        obj = self.request.user
        return obj 
 
    
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)


        if serializer.is_valid(raise_exception=True):
            new_password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['confirm_password']
            if not self.object.check_password(serializer.validated_data['old_password']):
                return Response({
                    'old_password': 'wrong password! please enter correct password'}, 
                    status=status.HTTP_400_BAD_REQUEST
                    )

            if confirm_password != new_password:
                return Response({
                    'confirm password': 'the passwords must match!'}, 
                    status=status.HTTP_400_BAD_REQUEST
                    )
            
            self.object.set_password(new_password)
            self.object.save()
            return Response({
                'password': 'password changed successfully!'}, 
                status=status.HTTP_200_OK
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def profile_view(request, slug):
    try:
        profile = Profile.objects.get(slug=slug)
    
        if request.user != profile.user:
            raise PermissionDenied
        else:
            if request.method == 'GET': 
                    serializer = ProfileSerializer(profile, context={'request': request})
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        raise NotFound(detail='this profile does not exist')


@api_view(['PUT', ])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser])
def update_profile_view(request, slug):
    try:
        profile = Profile.objects.get(slug=slug)

    
        if request.user != profile.user:
            raise PermissionDenied
        else:
            if request.method == 'PUT':
                serializer = ProfileSerializer(profile, data=request.data, partial=True)
                data = {}
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    data['success'] = 'update successful'
                    return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Profile.DoesNotExist:
        raise NotFound(detail='this profile does not exist')
    

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@parser_classes([JSONParser, MultiPartParser])
def add_wallet(request):
    if request.method == 'POST':
        user = request.user.profile
        serializer = WalletSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def wallet_view(request, slug):
    try:
        wallet = Wallet.objects.get(slug=slug) 

        if request.user.profile != wallet.owner:
            raise PermissionDenied
        else:
            if request.method == 'GET':
                serializer = WalletSerializer(wallet, context={'request': request})
                return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Wallet.DoesNotExist:
        raise NotFound(detail="sorry, couldn't find your wallet")
    

@api_view(['DELETE', ])
@permission_classes([IsAuthenticated])
def delete_wallet_view(request, username):
    try:
        wallet = Wallet.objects.get(owner__user__username=username)
   
        if request.user.profile != wallet.owner:
            raise PermissionDenied
        else:
            data = {}
            if request.method == 'DELETE':
                operation = wallet.delete()
                if operation:
                    data['success'] = 'delete successful'
                    status_code = status.HTTP_200_OK
                else:
                    data['error'] = 'failed to delete wallet'
                    status_code = status.HTTP_400_BAD_REQUEST
                
                return Response(data=data, status=status_code)
    except Wallet.DoesNotExist:
        raise NotFound(detail='this wallet has already been deleted')
        

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@parser_classes([JSONParser, MultiPartParser])
def send_fund(request, username):
    if request.method == 'POST':
        if not request.user.is_admin:
            raise PermissionDenied(detail='you are not allowed to perform this action')
        else:
            receiver = Profile.objects.get(user__username=username)
            serializer = FundSerializer(data=request.data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save(owner=receiver)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def fund_detail(request, pk):
    try:
        fund = Fund.objects.get(id=pk) 
        if request.method == 'GET':
            serializer = FundSerializer(fund, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Fund.DoesNotExist:
        raise NotFound(detail="sorry, couldn't find your wallet")
    

class FundHistory(ListAPIView):
    queryset = Fund.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)
    serializer_class = FundSerializer
    filter_backends = ([SearchFilter, OrderingFilter])
    search_fields = ['amount', 'owner__user__name']
    ordering = ['-created_at']