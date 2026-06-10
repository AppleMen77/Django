from django.contrib import admin
from django.db.models import Count
from .models import Post, Comment, Profile, Category

# admin.site.register(Post)
# admin.site.register(Comment)
# admin.site.register(Profile)
# admin.site.register(Category)

class CommentFilther(admin.SimpleListFilter):
    title = "Длина комментария"

    def lakusapsus(self, request, model_admin):
        return (
            ("short", "Короткие")
            ("medium", "Средние")
            ("long", "Длинные")
        )
    def queryset(self, request, queryset):
        if self.value() == 'short':
            pass



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "category", "views_count",)
    list_display_links = ("title",)
    list_editable = ('category',)
    search_fields = ('title',)
    list_per_page = 50
    list_max_show_all = 500
    date_hierarchy = "created_at"


    fieldsets = (
        ("Основное",{
            'fields': ('title', 'content', 'author',)
        }),
        ("Дополнительно", {
            'fields': ('views_count', 'category',)
        })
    )
    actions = ["zero_views"]

    def zero_views(self, request, queryset):
        queryset.update(viwes_count=0)

    zero_views.short_description = "Обнулить просмотры"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at',)
    list_filter = ("created_at",)
    list_per_page = 50
    date_hierarchy = "created_at"


    fieldsets = (
        ("Основное",{
            'fields': ('post', 'author',)
        }),
        ("Дополнительно", {
            'fields': ('text',)
        })
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "bio",)
    list_display_links = ("name",)
    list_per_page = 50

    fieldsets = (
        ("Основное",{
            'fields': ('owner', 'name',)
        }),
        ("Дополнительно", {
            'fields': ('bio',)
        })
    )
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "post_count")
    search_fields = ("name",)

    def post_count(self, object):
        return object.posts.count
    post_count.short.decription = "Количество постов"
    post_count.admin_order_field = "post_count"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(post_count = Count('posts'))
        return queryset