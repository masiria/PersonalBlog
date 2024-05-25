from django.contrib import admin
from .models import Category, Post, Comment, Tag, IPAddress


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    prepopulated_fields = {'slug': ('name',)}


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'category_to_string', 'create_date', 'tag_to_string', 'user')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('user',)

    def category_to_string(self, obj):
        categories = [category.name for category in obj.category.all()]
        return ", ".join(categories)
    category_to_string.short_description = 'category'

    def tag_to_string(self, obj):
        tags = [tag.name for tag in obj.tags.all()]
        return ", ".join(tags)
    tag_to_string.short_description = 'tags'

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'parent', 'approved', 'create_date')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    prepopulated_fields = {'slug': ('name',)}

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class IPAddressAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IPAddress, IPAddressAdmin)

