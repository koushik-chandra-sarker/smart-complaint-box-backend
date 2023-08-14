import json

from django.core import serializers
from django.shortcuts import render

from rest_framework import status, mixins, viewsets
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from author.models import User
from author.models.user_model import EmailConfirmed, Designation
from author.serializers import ChangePasswordSerializer, DesignationSerializer


class GetDesignationViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['type'] = "Bearer"
        user = json.loads(serializers.serialize('json', User.objects.filter(email=self.user)))
        try:
            data["author"] = user[0]['fields']
        except:
            data['author'] = {}
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # # if using drf authtoken, create a new token
        # if hasattr(author, 'auth_token'):
        #     author.auth_token.delete()
        # token, created = Token.objects.get_or_create(author=author)
        # # return new token
        # return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'message': "Password update successful"}, status=status.HTTP_200_OK)


def varify_mail_address(request):
    activation_key = request.GET.get('token')
    data = EmailConfirmed.objects.get(activation_key=activation_key)
    if data:
        if data.email_confirm:
            return render(request, template_name='email_confirmed.html',
                          context={'messageType': 1, 'message': 'Email already confirmed'})
        else:
            data.email_confirm = True
            data.save()
            return render(request, template_name='email_confirmed.html',
                          context={'messageType': 0, 'message': 'Email Verified Successfully'})
    else:
        return render(request, template_name='email_confirmed.html',
                      context={'messageType': -1, 'message': 'Email Verification Failed'})
