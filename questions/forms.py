from django import forms

from tinymce.widgets import TinyMCE

from questions.models import Question, Choice


class QuestionForm(forms.ModelForm):

    question_no = forms.IntegerField(label="Question No.: ",help_text="")
    question_text = forms.CharField(widget=TinyMCE(attrs={'height':500}),label="Question: ")
    # hint = forms.CharField(widget=TinyMCE(attrs={'height':500}),required=False) 
    class Meta:
        model = Question
        fields = ['question_no', 'question_text', 'image','audio_file','mocktestsentence']

    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        if instance:
            self.instance.question = instance 
            self.initial['question_no'] = instance.question_no
            self.initial['question_text'] = instance.question_text
            self.initial['audio_file'] = instance.audio_file
            self.initial['image'] = instance.image
            self.initial['mocktestsentence'] = instance.mocktestsentence
             

class ChoiceForm(forms.ModelForm):

    choice_text = forms.CharField(widget=TinyMCE(attrs={'height':500}),required=False)
    correct = forms.BooleanField(label='', required=False, widget=forms.RadioSelect(choices=[(True, 'Correct')]))

    class Meta:
        model = Choice
        fields = ['choice_text', 'correct','image']

    def __init__(self, instance=None, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        if instance:
            self.instance.choice = instance
            self.initial['choice_text'] = instance.choice_text
            self.initial['correct'] = instance.correct
            self.initial['image'] = instance.image