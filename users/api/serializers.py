from rest_framework import serializers
from users.models import User, Profile, Wallet, Fund
from itertools import chain 


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['url', 'user_id', 'email', 'username', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'url': {'lookup_field': 'username'},
            'user_id': {'read_only': True}
        }

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({'password': "second password does not match the first!"})
        return data


    def create(self, validated_data):
        password_two = validated_data.pop('password2', None)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'name']    



class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    wallet = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='wallet-detail',
        lookup_url_kwarg='username'
    )
    class Meta:
        model = Profile
        fields = ['url', 'user', 'balance', 'wallet']
        extra_kwargs = {
            'url': {'lookup_url_kwarg': 'username'},
            'user': {
                'lookup_field': 'username',
                'read_only': True
            },
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wallet
        fields = [ 'url', 'seed_phrase', 'owner', 'external_wallet']
        extra_kwargs = {
	    'url': {'lookup_url_kwarg': 'username'},
            'owner': {
                'view_name': 'profile-detail',
                'read_only': True,
                'lookup_url_kwarg': 'username'
            }
        }


    def validate_seed_phrase(self, value):
        if '_' not in value:
            raise serializers.ValidationError({'error': "you need to add '_' to seed phrase to save it"})
        return value
    

class FundSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Fund
        fields = ['url', 'amount', 'owner', 'created_at']
        extra_kwargs = {
            'owner': {
                'read_only': True,
                'view_name': 'profile-detail',
                'lookup_url_kwarg': 'username'
            },
            'created_at': {'read_only': True}
        }
