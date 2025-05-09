from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import Blog, Tag, Category, LikeDislike, Comment

@admin.register(Blog)
class BlogAdmin(GuardedModelAdmin, SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register([Category, Tag, LikeDislike, Comment])