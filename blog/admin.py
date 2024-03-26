from django.contrib import admin

from . import models


@admin.action(description="Mark selected stories as published")
def make_published(modeladmin, request, queryset):
    queryset.update(status="pub")


@admin.action(description="Mark selected stories as Draft")
def make_draft(modeladmin, request, queryset):
    queryset.update(status="drf")


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'author', 'datetime_modified')
    actions = [make_published, make_draft]
    list_filter = ['status', 'datetime_modified']
    ordering = ['datetime_modified']


admin.site.register(models.Post, PostAdmin)
