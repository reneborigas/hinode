from django import forms
from django.utils import timezone

from lessons.models import Lesson
from questions.models import Question
from tinymce.widgets import TinyMCE

FORMAT = '%Y/%m/%d %H:%M'

class LessonForm(forms.ModelForm):

    title = forms.CharField(label="Title", max_length=30)
    subtitle = forms.CharField(label="Subtitle", max_length=200)
    overview = forms.CharField(widget=TinyMCE(attrs={'height':500}))  
    description = forms.CharField(widget=TinyMCE(attrs={'height':500}))  
     
    ACTIVE = 1
    INACTIVE = 0
    STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'), 
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)  

    class Meta:
        model = Lesson
        fields = ['title','subtitle','overview' ,'description' ,'status']

    def clean(self):
        cleaned_data = super(LessonForm, self).clean()
        return self.cleaned_data

    def __init__(self, instance=None, reviewprogram=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance:
            self.instance.exam = instance
            self.initial['title'] = instance.title
            self.initial['subtitle'] = instance.subtitle
            self.initial['overview'] = instance.overview
            self.initial['description'] = instance.description 
            self.initial['status'] = instance.status  
            # question_course = instance.reviewprogram
        # elif course:
        #     question_course = course
        # self.fields['category'].choices = [(x, x) for x in 
        #     Question.objects.filter(course=question_course)
        #     .values_list('category',flat=True).distinct()]


