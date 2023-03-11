from django.core.mail import EmailMessage
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .permissions import IsAdmin, IsOwner, IsModerator, IsUser


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'],
                             body=data['email_body'], to=data['to_email'])
        email.send()


class PermissionModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    permission_classes_by_action = {'list': [AllowAny],
                                    'create': [IsUser | IsAdmin | IsModerator],
                                    'retrieve': [AllowAny],
                                    'partial_update': [IsOwner],
                                    'destroy': [IsAdmin | IsModerator]}

    def get_permissions(self):
        try:
            return [permission() for permission
                    in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
