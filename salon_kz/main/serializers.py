from rest_framework import serializers
from main import models
from django.db import models as dbmodels
import datetime


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('id', 'username', 'password', 'user_type',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('username', 'password','telephone', 'first_name', 'last_name', 'email',)
        extra_kwargs = {
            'username': {'validators': []},
            'telephone': {'validators': []},
        }
        validators = []

    def update(self, instance, validated_data):
        # instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password', instance.password))
        # instance.telephone = validated_data.get('telephone', instance.username)
        instance.first_name = validated_data.get('first_name', instance.username)
        instance.last_name = validated_data.get('last_name', instance.username)
        instance.email = validated_data.get('email', instance.username)
        instance.save()
        return instance

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = models.City
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.Client
        fields = '__all__'
    

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        instance.user = UserSerializer.update(self, instance=instance.user, validated_data=user_data)
        instance.user.save()
        instance.save()
        return instance

class ClientSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = ('mean', )

class PartnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = models.Partner
        fields = '__all__'

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        instance.user = UserSerializer.update(self, instance=instance.user, validated_data=user_data)
        instance.save()
        return instance


class SalonSerializer(serializers.ModelSerializer):
    partner = PartnerSerializer(read_only=True)
    class Meta:
        model = models.Salon
        fields = '__all__'

class SalonSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.Salon
        fields = ('mean', )

class ServiceSerializer(serializers.ModelSerializer):
    salon = SalonSerializer(read_only=True)
    class Meta:
        model = models.Service
        fields = '__all__'
    
    def create(self, validated_data):
        service = models.Service(**validated_data)
        service.save
        return service


class  MasterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    salon = SalonSerializer(read_only=True)
    class Meta:
        model = models.Master
        fields = '__all__'

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        instance.user = UserSerializer.update(self, instance=instance.user, validated_data=user_data)
        is_aproved = bool(validated_data.get('is_aproved'))
        instance.is_aproved = is_aproved
        instance.save()
        return instance

class MasterSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.Master
        fields = ('mean', )


class MasterServiceSerializer(serializers.ModelSerializer):
    master = MasterSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    salon = SalonSerializer(read_only=True)
    class Meta:
        model = models.MasterService
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    master_service = MasterServiceSerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    partner = PartnerSerializer(read_only=True)
    class Meta:
        model = models.Order
        fields = '__all__'
 
class CommentSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)
    salon = SalonSerializer(read_only=True)
    class Meta:
        model = models.Comment
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)
    class Meta:
        model = models.Rating
        fields = '__all__'

class ClientRatingSerializer(RatingSerializer):
    client = ClientSerializer(read_only=True)
    class Meta:
        model = models.ClientRating
        fields = '__all__'

class SalonRatingSerializer(RatingSerializer):
    salon = SalonSerializer(read_only=True)
    class Meta:
        model = models.SalonRating
        fields = '__all__'

class MasterRatingSerializer(RatingSerializer):
    master = MasterSerializer(read_only=True)
    class Meta:
        model = models.MasterRating
        fields = '__all__'



