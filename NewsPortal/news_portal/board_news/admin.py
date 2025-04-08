from django.contrib import admin
from .models import Post, Author, Category, Comment


# Функция для повышения рейтинга поста, автора или комментария на 1
@admin.display(description='Поднять рейтинг на 1')
def update_rating(modeladmin, request, queryset):
    for instance in queryset:
        instance.rating += 1
        instance.save()


# Кастомизация отображения модели Post в админ-панели
class PostAdmin(admin.ModelAdmin):
    # Столбцы в таблице
    list_display = ('get_title', 'get_author_username', 'get_date', 'get_rating',)
    # Поля модели, по которым можно фильтровать таблицу
    list_filter = ('date_time_in', 'rating',)
    # Поля модели, по которым можно искать совпадения в строке поиска
    search_fields = ('title', 'author_post__user__username',)
    # Список действий, которые можно применять к выбранным экземплярам модели
    actions = [update_rating]

    # Заменить название столбца "title"
    @admin.display(description='Заголовок')
    def get_title(self, obj):
        return obj.title

    # Заменить название столбца "author_post"
    @admin.display(description='Автор')
    def get_author_username(self, obj):
        return obj.author_post.user.username

    # Заменить название столбца "date_time_in" и определить формат вывода
    @admin.display(description='Дата публикации')
    def get_date(self, obj):
        return obj.date_time_in.strftime('%d.%m.%Y %H:%M')

    # Заменить название столбца "rating"
    @admin.display(description='Рейтинг')
    def get_rating(self, obj):
        return obj.rating


# Кастомизация отображения модели Author в админ-панели
class AuthorAdmin(admin.ModelAdmin):
    # Столбцы в таблице
    list_display = ('get_username', 'get_rating',)
    # Поля модели, по которым можно фильтровать таблицу
    list_filter = ('user', 'rating',)
    # Поля модели, по которым можно искать совпадения в строке поиска
    search_fields = ('user__username',)
    # Список действий, которые можно применять к выбранным экземплярам модели
    actions = [update_rating]

    # Заменить название столбца "user"
    @admin.display(description='Имя пользователя')
    def get_username(self, obj):
        return obj.user.username

    # Заменить название столбца "rating"
    @admin.display(description='Рейтинг')
    def get_rating(self, obj):
        return obj.rating


# Кастомизация отображения модели Category в админ-панели
class CategoryAdmin(admin.ModelAdmin):
    # Столбцы в таблице
    list_display = ('get_category_name', 'get_subscribers',)
    # Поля модели, по которым можно фильтровать таблицу
    list_filter = ('category_name', 'subscribers',)
    # Поля модели, по которым можно искать совпадения в строке поиска
    search_fields = ('category_name', 'subscribers')

    # Заменить название столбца "category_name"
    @admin.display(description='Категория')
    def get_category_name(self, obj):
        return obj.category_name

    # Заменить название столбца "subscribers" и определить формат вывода
    @admin.display(description='Подписчики')
    def get_subscribers(self, obj):
        return ", ".join([user.username for user in obj.subscribers.all()])


# Кастомизация отображения модели Comment в админ-панели
class CommentAdmin(admin.ModelAdmin):
    # Столбцы в таблице
    list_display = ('get_title', 'get_author_username', 'get_comment', 'get_date', 'get_rating',)
    # Поля модели, по которым можно фильтровать таблицу
    list_filter = ('author', 'date_time_in', 'rating',)
    # Поля модели, по которым можно искать совпадения в строке поиска
    search_fields = ('text', 'date_time_in',)
    # Список действий, которые можно применять к выбранным экземплярам модели
    actions = [update_rating]

    # Заменить название столбца "post"
    @admin.display(description='Пост')
    def get_title(self, obj):
        return obj.post.title

    # Заменить название столбца "author"
    @admin.display(description='Автор')
    def get_author_username(self, obj):
        return obj.author.username

    # Заменить название столбца "text"
    @admin.display(description='Комментарий')
    def get_comment(self, obj):
        return obj.text

    # Заменить название столбца "date_time_in"
    @admin.display(description='Дата добавления')
    def get_date(self, obj):
        return obj.date_time_in.strftime('%d.%m.%Y %H:%M')

    # Заменить название столбца "rating"
    @admin.display(description='Рейтинг')
    def get_rating(self, obj):
        return obj.rating


# Регистрация моделей в админ-панели
admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
