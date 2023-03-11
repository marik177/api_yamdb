import secrets
import string
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import exceptions
from rest_framework import generics, filters, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.decorators import action
from .serializers import (EmailAuthSerializer, ObtainEmailSerializer,
                          UserSerializer, CategorySerializer,
                          GenreSerializer, TitleReadSerializer,
                          TitleWriteSerializer,
                          ReviewSerializer, CommentSerializer)
from .models import Category, Genre, Title, Review, Comment
from .utils import Util, PermissionModelViewSet
from .filters import TitleFilters
from .permissions import IsAdmin, IsAdminUserOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

User = get_user_model()


class CommentViewSet(PermissionModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id)


class ReviewViewSet(PermissionModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title__id=title_id)

    def perform_create(self, serializer):
        author = self.request.user
        title = get_object_or_404(Title,
                                  pk=self.kwargs.get('title_id'))
        serializer.save(author=author, title=title)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(Avg('reviews__score'))
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilters

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        else:
            return TitleWriteSerializer

    # def get_serializer_class(self):
    #     if self.action in ('list', 'retrieve'):
    #         return TitleReadSerializer
    #
    #     return TitleWriteSerializer


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminUserOrReadOnly]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminUserOrReadOnly]
    search_fields = ['name']
    lookup_field = 'slug'


class ObtainEmailAPIView(generics.GenericAPIView):
    serializer_class = ObtainEmailSerializer

    def post(self, request):
        serializer = ObtainEmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            confirmation_code = "".join([secrets.choice
                                         (string.ascii_letters + string.digits)
                                         for i in range(6)])
            user.confirmation_code = confirmation_code
            user.save()
            email_body = f'Привет, {user.username}' \
                         f'.\nДля получения token отправьте запрос с ' \
                         f'параметрами email и confirmation_code' \
                         f'  на /auth/token/\nconfirmation_code --> ' \
                         f'{confirmation_code} '
            data = {'email_body': email_body,
                    'email_subject':
                        'Verify your email', 'to_email': (user.email,)}
            """разкоментировать Util.send_email(data) для"""
            """отправки кода на почту"""
            # Util.send_email(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    search_fields = ['username', ]

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=(IsAuthenticated,),
            url_path='me', url_name='me')
    def user_me(self, request, *args, **kwargs):
        user_instance = self.request.user
        serializer = self.get_serializer(user_instance)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(user_instance,
                                             data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailAuthAPIView(generics.GenericAPIView):
    serializer_class = EmailAuthSerializer

    def post(self, request):
        email = request.data.get('email', None)
        confirmation_code = request.data.get('confirmation_code', None)
        try:
            user = User.objects.get(email=email,
                                    confirmation_code=confirmation_code)
            token = user.get_tokens()
            return Response(token)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                ('Неправильно указан email или confirmation_code'))
