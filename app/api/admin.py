from django.contrib import admin
from .models import Title, Genre, Category, Review, Comment


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'author', 'score')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'text', 'author')


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
