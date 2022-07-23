from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from authentication.serializers import RegistrationSerializer, LoginSerializer, LogoutSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework import status
from authentication.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken



class RegistrationView(APIView):

    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.created_by = request.user.username
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    """ 
    to login the user which takes the jwt access token checks its validity and
    and authenticity and according to that give access to the user
    """

    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )


    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):

            response = {
                "UserToken": {
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                },
                'UserInfo': {
                    'username': serializer.validated_data['username'],
                    'role': serializer.validated_data['role'],
                }
            }

            return Response(response)


class LogoutView(APIView):
    
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            valid = serializer.is_valid(raise_exception=True)
            
            if valid:
                token = RefreshToken(serializer.data["refresh_token"])
                token.blacklist()
                print(serializer)

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = User.objects.get(username='admin')
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response(status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)