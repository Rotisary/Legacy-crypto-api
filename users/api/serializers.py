from rest_framework import serializers
from users.models import User, Profile, Wallet, Fund
from itertools import chain 


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['user_id', 'email', 'username', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
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
        fields = ['email', 'name']    



class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    wallet = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='wallet-detail',
        lookup_field='slug'
    )
    class Meta:
        model = Profile
        fields = ['user', 'balance', 'wallet']
        extra_kwargs = {
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
        fields = ['seed_phrase', 'owner', 'external_wallet']
        extra_kwargs = {
            'owner': {
                'view_name': 'profile-detail',
                'read_only': True,
                'lookup_field': 'slug'
            }
        }


    def validate_seed_phrase(self, value):
        if '_' not in value:
            raise serializers.ValidationError({'error': "you need to add '_' to seed phrase to save it"})
        return value
    

class FundSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.SerializerMethodField('get_owner_name')
    class Meta:
        model = Fund
        fields = ['url', 'amount', 'owner', 'created_at']
        extra_kwargs = {
            'created_at': {'read_only': True}
        }


    def get_owner_name(self, fund):
        name = fund.owner.user.name
        return name