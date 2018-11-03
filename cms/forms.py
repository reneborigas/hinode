from django import forms

from programs.models import ReviewProgram, Enrollment
from django.contrib.auth.models import AbstractUser, UserManager,User

from tinymce.widgets import TinyMCE
class ReviewProgramForm(forms.ModelForm):

    title = forms.CharField(label="Review Program", max_length=30)
    overview = forms.CharField(widget=TinyMCE(attrs={'height':500}))  
    description = forms.CharField(widget=TinyMCE(attrs={'height':500}))  
    ACTIVE = 1
    INACTIVE = 0
    STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'), 
    )
    status =forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = ReviewProgram
        fields = ['title', 'overview','description','image','status']

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance:
            self.instance.reviewprogram = instance
            self.initial['title'] = instance.title
            self.initial['overview'] = instance.overview
            self.initial['description'] = instance.description
            self.initial['image'] = instance.image
            self.initial['status'] = instance.status

class ParticipantsAssetMultiField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return '{} {}'.format(obj, obj.email)


class StudentsForm(forms.ModelForm):

    participants = ParticipantsAssetMultiField(label="", required=False,
        queryset=User.objects.filter(is_teacher=False, is_active=True,
        is_superuser=False), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = ReviewProgram
        fields = ['participants']

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if instance:
            self.instance.reviewprogram = instance
            self.initial['participants'] = [participant.user for participant in
                Enrollment.objects.filter(reviewprogram=instance)]