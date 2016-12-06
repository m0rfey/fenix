from .models import User

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'avatar',
        )

# class UserSer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(required=True, allow_blank=True, max_length=13)
#     first_name = serializers.CharField(max_length=50)
#     last_name = serializers.CharField(max_length=50)
#     email = serializers.EmailField(required=True)
#     password1 = serializers.CharField(required=True)
#     password2 = serializers.CharField(required=True)
#     avatar = serializers.ImageField(required=False)
#
#     def create(self, validated_data):
#         return User.objects.create(**validated_data)
#
#     def update(self, instanse, validated_data):
#         instanse.first_nanme = validated_data.get('first_name', instanse.first_nanme)
#         instanse.last_name = validated_data.get('last_name', instanse.last_name)
#         instanse.email = validated_data.get('email', instanse.email)
#         instanse.password1 = validated_data.get('password1', instanse.password1)
#         instanse.password2 = validated_data.get('password2', instanse.password2)
#         instanse.avatar = validated_data.get('avatar', instanse.avatar)
#         instanse.save()
#         return instanse
