from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Category, Genre, Title, Review, Comment

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(source='reviews__score__avg')

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        genre_data = validated_data.pop('genre')
        title = Title.objects.create(category=category_data, **validated_data)
        title.genre.set(genre_data)
        return title


class EmailAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=50)


class ObtainEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'bio', 'email', 'role')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        author = self.context['request'].user
        title = self.context['request'].parser_context['kwargs']['title_id']
        if Review.objects.filter(author=author, title__id=title).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

    def create(self, validated_data):
        author = self.context.get('request').user
        text = validated_data.pop('text')
        review_id = \
            self.context.get('request').parser_context['kwargs']['review_id']
        review = get_object_or_404(Review, pk=review_id)
        comment = Comment.objects.create(author=author,
                                         text=text, review=review)
        return comment
