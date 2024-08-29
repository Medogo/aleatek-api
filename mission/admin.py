from django.contrib import admin

# Register your models here.
from .models import Mission, Article, ArticleSelect, ArticleMission, MissionActive

admin.site.register(Mission)
admin.site.register(Article)
admin.site.register(ArticleSelect)
admin.site.register(ArticleMission)
admin.site.register(MissionActive)


