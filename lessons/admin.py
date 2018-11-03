from django.contrib import admin

from .models import Lesson

class LessonAdmin(admin.ModelAdmin):
    class Meta:
          model=Lesson

admin.site.register(Lesson,LessonAdmin)