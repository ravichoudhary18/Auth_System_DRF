from rest_framework import serializers
from authentication.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.models import update_last_login


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for Register User endpoint.
    """
    username = serializers.CharField(
        required=True,
        error_messages={'blank': 'username field cannot be blank.'},
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='User with this username already exists.'
                )
            ],
    )
    email = serializers.EmailField(
        required=True,
        error_messages={'blank': 'Email field cannot be blank.'},
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='User with this email already exists.'
            )
        ]
        )
    password = serializers.CharField(
        required=True, 
        style={"input_type": "password"}, 
        write_only=True
    )
    conform_password = serializers.CharField(
        style={"input_type": "password"}, 
        write_only=True
    )
    phone = serializers.IntegerField(
        required=False,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='User with this Phone Number already exists.'
                )
            ],    
    )
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'conform_password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        username = self.validated_data['username']
        user = User(
            email=self.normalize_email(self.validated_data['email']), 
            username=username, 
            phone=self.validated_data['phone'] if 'phone' in self.validated_data else None
        )
        password = self.validated_data['password']
        conform_password = self.validated_data['conform_password']
        if password != conform_password:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for Login User endpoint.
    """

    username = serializers.CharField(
        max_length=255, 
        required=True,
        error_messages={'blank': 'Username field cannot be blank.'},
        write_only=True
    )
    password = serializers.CharField(
        max_length=255, 
        required=True,
        style={"input_type": "password"},
        error_messages={'blank': 'Password field cannot be blank.'},    
        write_only=True,
    )
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self, data):
        print(data)
        username = data.get('username', None)
        password = data['password']

        if password is None:
            print('password is None')
            raise serializers.ValidationError(
                'A password is required to login.'
            )

        if '@' in username:
            try:
                queryset = User.objects.get(email=username)
                if queryset.check_password(password):
                    user = queryset
                else:
                    user = None
            except User.DoesNotExist:
                user = None
                return user
        else:
            user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email or username and password was not found.'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                'This user not found.'
            )

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            print(refresh, type(refresh), refresh.access_token, type(refresh.access_token))

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'username': user.username,
                'role': user.role,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for Logout change endpoint.
    """
    refresh_token = serializers.CharField(max_length=255)

    class Meta:
        fields = ['refresh_token']
        

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(
        max_length=255, 
        required=True,
        style={"input_type": "password"},
        error_messages={'blank': 'Old Password field cannot be blank.'},
    )
    new_password = serializers.CharField(
        max_length=255, 
        required=True,
        style={"input_type": "password"},
        error_messages={'blank': 'New Password field cannot be blank.'},
    )
    conform_password = serializers.CharField(
        max_length=255, 
        required=True,
        style={"input_type": "password"},
        error_messages={'blank': 'Conform Password field cannot be blank.'},
    )

    def validate(self, data):
        old_password = data('old_password', None)
        new_password = data.get('new_password', None)
        conform_password = data.get('conform_password', None)
        if new_password != conform_password:
            raise serializers.ValidationError({'password': 'New Password and Conform Password not match.'})

        if old_password == new_password:
            raise serializers.ValidationError({'password': 'Old Password and New Password can not same.'})
        
        return data
        
