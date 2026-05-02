from django.contrib import admin

from posts.models.post import Post
from posts.models.comment import Comment
from posts.models.like import Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'content_preview', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['author__username', 'content']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Conteúdo', {'fields': ('author', 'content', 'media')}),
        ('Status', {'fields': ('is_active',)}),
        ('Datas', {'fields': ('created_at', 'updated_at')}),
    )

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Conteúdo'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'post', 'content_preview', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['author__username', 'post__id', 'content']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Comentário', {'fields': ('post', 'author', 'content')}),
        ('Status', {'fields': ('is_active',)}),
        ('Datas', {'fields': ('created_at', 'updated_at')}),
    )

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Conteúdo'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__id']
    readonly_fields = ['created_at']
