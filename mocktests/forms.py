from django import forms
from django.utils import timezone

from mocktests.models import MockTest,MockTestSection,MockTestSubSection
from questions.models import Question,MockTestSentence
from tinymce.widgets import TinyMCE

FORMAT = '%Y/%m/%d %H:%M'

class MockTestForm(forms.ModelForm):

    title = forms.CharField(label="Title", max_length=200)
    subtitle = forms.CharField(label="Subtitle", max_length=200)
    overview = forms.CharField(widget=TinyMCE(attrs={'height':500}))
    description = forms.CharField(widget=TinyMCE(attrs={'height':500}))
    guidelines = forms.CharField(widget=TinyMCE(attrs={'height':500}))

    active_from = forms.DateTimeField(widget=forms.DateTimeInput(format=FORMAT),
        input_formats=[FORMAT])
    active_to = forms.DateTimeField(widget=forms.DateTimeInput(format=FORMAT),
        input_formats=[FORMAT])

    ACTIVE = 1
    INACTIVE = 0
    STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = MockTest
        fields = ['title','subtitle','overview' ,'description', 'guidelines',
            'active_from', 'active_to','status']

    def clean(self):
        cleaned_data = super(MockTestForm, self).clean()
        if ('active_from' in self.cleaned_data and
            'active_to' in self.cleaned_data):
            if (self.cleaned_data['active_from'] >=
                self.cleaned_data['active_to'] and
                self.cleaned_data['active_to'] > timezone.now()):
                raise forms.ValidationError("Please enter a valid active \
                    time frame")
        return self.cleaned_data

    def __init__(self, instance=None, reviewprogram=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance:
            self.instance.exam = instance
            self.initial['title'] = instance.title
            self.initial['subtitle'] = instance.subtitle
            self.initial['overview'] = instance.overview
            self.initial['description'] = instance.description
            self.initial['guidelines'] = instance.guidelines
            self.initial['active_from'] = instance.active_from
            self.initial['active_to'] = instance.active_to
            self.initial['status'] = instance.status
            # question_course = instance.reviewprogram
        # elif course:
        #     question_course = course
        # self.fields['category'].choices = [(x, x) for x in
        #     Question.objects.filter(course=question_course)
        #     .values_list('category',flat=True).distinct()]




class SectionForm(forms.ModelForm):

    title = forms.CharField(label="Title", max_length=200)
    subtitle = forms.CharField(label="Subtitle", max_length=200)
    description = forms.CharField(widget=TinyMCE(attrs={'height':500}))
    guidelines = forms.CharField(widget=TinyMCE(attrs={'height':500}))
    test_time_minutes = forms.TimeField(widget=forms.TimeInput(format='%H:%M'),  help_text=("Hours:Minutes"))
    max_no_of_attempts =  forms.IntegerField(label="Test Attempts")
    passing_mark =  forms.IntegerField(label="Passing Mark")
    password = forms.CharField(label="Password (optional)",
        widget=forms.PasswordInput(render_value=True), required=False)

    ACTIVE = 1
    INACTIVE = 0
    STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = MockTestSection
        fields = ['title','subtitle' ,'description', 'guidelines',  'test_time_minutes',
            'max_no_of_attempts','passing_mark', 'password',   'status']

    def clean(self):
        cleaned_data = super(SectionForm, self).clean()
        return self.cleaned_data

    def __init__(self, instance=None, mocktest=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance:
            self.instance.exam = instance
            self.initial['title'] = instance.title
            self.initial['subtitle'] = instance.subtitle
            self.initial['description'] = instance.description
            self.initial['guidelines'] = instance.guidelines
            self.initial['test_time_minutes'] = instance.test_time_minutes
            self.initial['max_no_of_attempts'] = instance.max_no_of_attempts
            self.initial['passing_mark'] = instance.passing_mark
            self.initial['password'] = instance.password
            self.initial['status'] = instance.status
            # question_course = instance.reviewprogram
        # elif course:
        #     question_course = course
        # self.fields['category'].choices = [(x, x) for x in
        #     Question.objects.filter(course=question_course)
        #     .values_list('category',flat=True).distinct()]


class SubSectionForm(forms.ModelForm):

    title = forms.CharField(label="Title", max_length=30)
    subtitle = forms.CharField(label="Subtitle", max_length=200)
    description = forms.CharField(widget=TinyMCE(attrs={'height':500}))
    guidelines = forms.CharField(widget=TinyMCE(attrs={'height':500}))
    ACTIVE = 1
    INACTIVE = 0
    STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = MockTestSubSection
        fields = ['title','subtitle' ,'description', 'guidelines', 'status']

    def clean(self):
        cleaned_data = super(SubSectionForm, self).clean()
        return self.cleaned_data

    def __init__(self, instance=None, mocktestsection=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance:
            self.instance.exam = instance
            self.initial['title'] = instance.title
            self.initial['subtitle'] = instance.subtitle
            self.initial['description'] = instance.description
            self.initial['guidelines'] = instance.guidelines
            self.initial['status'] = instance.status
            # question_course = instance.reviewprogram
        # elif course:
        #     question_course = course
        # self.fields['category'].choices = [(x, x) for x in
        #     Question.objects.filter(course=question_course)
        #     .values_list('category',flat=True).distinct()]



class SentenceForm(forms.ModelForm):

    sentence_no = forms.IntegerField(label="Sentence No.: ",help_text="")
    sentence_text = forms.CharField(widget=TinyMCE(attrs={'height':500}),label="Sentence: ")
     
    # questions = Question.objects.all()
    # question =forms.ChoiceField()


    class Meta:
        model = MockTestSentence
        fields = ['sentence_no', 'sentence_text','image']

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        if instance:
            self.instance.mocktestsentence = instance
            self.initial['sentence_no'] = instance.sentence_no
            self.initial['sentence_text'] = instance.sentence_text
             
            self.initial['image'] = instance.image

