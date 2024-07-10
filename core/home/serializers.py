from rest_framework import serializers
from .models import Person , Color
from django.contrib.auth.models import User



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    # def validate(self , data):
    #     if data.get("username") and data.get('password'):
    #         if User.objects.filter(username=data.get('username')).exists():
    #             if User.objects.filter(username=data.get('username') , password=data.get('password')).exists():
    #                 return data
    #             raise serializers.ValidationError("Incorrect password")
    #         raise serializers.ValidationError('User does not exists')
    #     raise serializers.ValidationError("Provide proper details")



class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        if attrs.get('username') and attrs.get("email") and attrs.get('password'):
            if User.objects.filter(username=attrs['username']).exists():
                raise serializers.ValidationError("User already exists")

            if User.objects.filter(email=attrs['email']).exists():
                raise serializers.ValidationError("User already exists")
            
            if len(attrs.get('password'))<7:
                raise serializers.ValidationError("Password must be greater than 6 characters")
            
            return attrs
        raise serializers.ValidationError("Provide all the user details properly")

    def create(self, validated_data):
        user = User(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=30)
#     email = serializers.EmailField()
#     password = serializers.CharField(min_length=6)


class ColorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ["color_name"]

class PeopleSerializer(serializers.ModelSerializer):
    # color = ColorsSerializer()
    color_info = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = "__all__"
        depth = 1

    def get_color_info(self, data):
        color = Color.objects.get(id=data.color.id)
        return {"color_name": data.color.color_name, "hex_code": "#000"}

    def validate(self, data):
        print("Person validation function called")
        if data['age']<18:
            return serializers.ValidationError("Age should be greater than or equal to 18")
        return data