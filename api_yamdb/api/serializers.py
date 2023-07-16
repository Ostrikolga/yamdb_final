from api.validators import UsernameValidator, validate_username
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field="id",
        many=False,
        read_only=True
    )

    class Meta:
        fields = "__all__"
        model = Review

    def validate(self, data):
        if self.context["request"].method != "POST":
            return data
        title = get_object_or_404(
            Title,
            pk=self.context["view"].kwargs.get("title_id")
        )
        author = self.context["request"].user
        if Review.objects.filter(title_id=title, author=author).exists():
            raise serializers.ValidationError(
                "Вы уже оставляли обзор на данное произведение"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    review = serializers.ReadOnlyField(
        source='review.id'
    )

    class Meta:
        fields = "__all__"
        model = Comment


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username, UsernameValidator(), ],
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate(self, data):
        user_username = User.objects.filter(username=data['username']).exists()
        user_email = User.objects.filter(email=data['email']).exists()
        if (
            ((user_username) and (not user_email))
            or ((user_email) and (not user_username))
        ):
            raise ValidationError(
                "Поле 'username' или 'email' заполнены неправильно!"
            )
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio', 'role'
        )
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров"""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title для записи данных."""
    
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title для чтения данных."""
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


