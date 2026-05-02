from django.contrib import admin
from django.contrib.auth.models import User
from accounts.models.profile import Profile
from accounts.models.follow import Follow


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['display_name', 'bio', 'birth_date', 'avatar']
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)
    list_display = ['username', 'email', 'is_active', 'date_joined']
    search_fields = ['username', 'email']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    list_filter = ['created_at']
    search_fields = ['follower__username', 'following__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


# Unregister User and register with ProfileInline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
