from django.urls import reverse
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])

            token = RefreshToken.for_user(user).access_token

            current_site = get_current_site(request).domain
            relativeLink = reverse('verify-email')

            absurl = 'http://' + current_site + \
                     relativeLink + '?token=' + str(token)
            email_body = 'Привет,  ' + user.username + \
                         "\n Перейди по ссылке для " \
                         "подтверждения email \n" + absurl
            data = {'email_body': email_body,
                    'email_subject': 'Verify your email',
                    'to_email': (user.email,)}
            Util.send_email(data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
