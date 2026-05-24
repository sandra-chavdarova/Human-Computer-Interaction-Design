from django.contrib import admin

from .models import *


# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']

    # exclude = ('user',)

    # def save_model(self, request, obj, form, change):
    #     obj.user = request.user
    #     return super().save_model(request, obj, form, change)

    # Автори може да бидат додадени само од супер-корисници
    def has_add_permission(self, request):
        return request.user.is_superuser


class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',)
    # search_fields = ('description',)
    inlines = [BookAuthorInline, ]

    # -------
    # Книги можат да бидат додадени само од автори и авторот по автоматизам се додава како автор на книгата
    def has_add_permission(self, request):
        return Author.objects.filter(user=request.user).exists()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        author = Author.objects.filter(user=request.user).first()
        if author and not change:
            BookAuthor.objects.create(book=obj, author=author)

    # -------

    # Книги можат да бидат менувани само од нивите автори
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return BookAuthor.objects.filter(book=obj, author__user=request.user).exists()

    # Авторите може да ги листаат сите книги за кои имаат опис
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        book_ids = BookAuthor.objects.filter(author__user=request.user).values_list('book_id', flat=True)
        return qs.filter(id__in=book_ids, description__gt='')

    # Супер-корисници може да пребаруваат книги според зборови во опис
    def get_search_fields(self, request):
        if request.user.is_superuser:
            return ('description',)
        return ()


admin.site.register(Author, AuthorAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Book, BookAdmin)
