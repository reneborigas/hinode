from django.contrib import admin

# Register your models here.

from .models import Question,Choice,MockTestSentence

class QuestionAdmin(admin.ModelAdmin):
    class Meta:
          model=Question
          odering=["question_no"]

class ChoiceAdmin(admin.ModelAdmin):
    class Meta:
          model=Choice
          
class MockTestSentenceAdmin(admin.ModelAdmin):
    class Meta:
          model=MockTestSentence



admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice,ChoiceAdmin)
admin.site.register(MockTestSentence,MockTestSentenceAdmin)