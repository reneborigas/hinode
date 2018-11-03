from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelformset_factory
from django.shortcuts import redirect, render

from programs.models import ReviewProgram 
from mocktests.models import MockTest,MockTestSection,MockTestSubSection 
from cms.views import instructor_check
from questions.forms import QuestionForm, ChoiceForm
from questions.models import Question, Choice,MockTestSentence
 

def update(question_form, question, choice_formset):
    question.question_no = question_form.cleaned_data['question_no']
    
    question.question_text = question_form.cleaned_data['question_text']
    question.audio_file = question_form.cleaned_data['audio_file']
    question.image = question_form.cleaned_data['image'] 
    question.mocktestsentence =question_form.cleaned_data['mocktestsentence']
    question.save()
    
    for choice_form in choice_formset.forms:
        choice = choice_form.save(commit=False)
        choice.question = question 
        choice.save()


@user_passes_test(instructor_check)
def create_question(request, reviewprogram_id,mocktest_id,mocktestsection_id,mocktestsubsection_id):
    ChoiceFormSet = modelformset_factory(Choice, ChoiceForm, extra=4)
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id) 
    mocktestsection  = MockTestSection.objects.get(id=mocktestsection_id) 
    mocktestsubsection  = MockTestSubSection.objects.get(id=mocktestsubsection_id)
    question_form = QuestionForm()
    question_form.fields['mocktestsentence'].queryset = MockTestSentence.objects.filter(mocktestsubsection_id=mocktestsubsection)
    choice_formset = ChoiceFormSet(queryset=Choice.objects.none())
    if request.method == 'POST':
        question_form = QuestionForm(data=request.POST,files=request.FILES)
        choice_formset = ChoiceFormSet(data=request.POST,files=request.FILES)
        if question_form.is_valid() and choice_formset.is_valid():
            question = question_form.save(commit=False)
            question.mocktestsubsection = mocktestsubsection
            question.save()
            for choice_form in choice_formset.forms:
                choice = choice_form.save(commit=False)
                choice.question = question
                choice.save()
            messages.success(request, 'Question created successfully!')
            return redirect('/manage/' + reviewprogram_id  + '/mocktests/'+ mocktest_id + '/sections/'+ mocktestsection_id + '/subsections/' + mocktestsubsection_id +  '/questions/create')
    return render(request, 'create_question.html', {'form': question_form,
        'choice_formset': choice_formset,  'reviewprogram': reviewprogram, 'mocktest': mocktest ,'mocktestsection':mocktestsection,'mocktestsubsection':mocktestsubsection})


@user_passes_test(instructor_check)
def edit_question(request, reviewprogram_id,mocktest_id,mocktestsection_id,mocktestsubsection_id , question_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id) 
    mocktestsection  = MockTestSection.objects.get(id=mocktestsection_id) 
    mocktestsubsection  = MockTestSubSection.objects.get(id=mocktestsubsection_id)
    
    question = Question.objects.get(id=question_id)
    mocktestsentence = MockTestSentence.objects.filter(id=question.mocktestsentence_id)
    
    if request.user == reviewprogram.instructor:
        ChoiceFormSet = modelformset_factory(Choice, ChoiceForm, extra=0)
        choices = Choice.objects.filter(question=question)
        question_form = QuestionForm(instance=question)
        
        question_form.fields['mocktestsentence'].queryset = MockTestSentence.objects.filter(mocktestsubsection_id=mocktestsubsection)
        choice_formset = ChoiceFormSet(queryset=Choice.objects
            .filter(question=question))
        if request.method == 'POST' and 'update' in request.POST:
            question_form = QuestionForm(instance=question, data=request.POST,files=request.FILES)
            choice_formset = ChoiceFormSet(data=request.POST,files=request.FILES)
            if question_form.is_valid() and choice_formset.is_valid():
                Choice.objects.filter(question=question).delete()
                update(question_form, question, choice_formset)
                messages.success(request, 'Question updated successfully!')
                return redirect('/manage/' + reviewprogram_id + '/mocktests/'+ mocktest_id + '/sections/'+ mocktestsection_id + '/subsections/' + mocktestsubsection_id +  '/questions')
        if request.method == 'POST' and 'delete' in request.POST:
            question.delete()
            Choice.objects.filter(question=question).delete()
            messages.success(request, 'Question deleted successfully!')
            return redirect('/manage/' + reviewprogram_id + '/mocktests/'+ mocktest_id + '/sections/'+ mocktestsection_id + '/subsections/' + mocktestsubsection_id +  '/questions')
        return render(request, 'edit_question.html', {'form': question_form,'mocktest_sentences':mocktestsentence,
            'choice_formset': choice_formset, 
            'question': question, 'choices': choices,  'reviewprogram': reviewprogram, 'mocktest': mocktest ,'mocktestsection':mocktestsection,'mocktestsubsection':mocktestsubsection})
    return redirect('/manage/' + reviewprogram_id)


@user_passes_test(instructor_check)
def list_questions(request, reviewprogram_id,mocktest_id,mocktestsection_id,mocktestsubsection_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id) 
    mocktestsection  = MockTestSection.objects.get(id=mocktestsection_id) 
    mocktestsubsection  = MockTestSubSection.objects.get(id=mocktestsubsection_id)

    if request.user == reviewprogram.instructor:
        questions = Question.objects.filter(mocktestsubsection=mocktestsubsection)
        return render(request, 'list_questions.html', {'reviewprogram': reviewprogram,'mocktest':mocktest
            ,'mocktestsection':mocktestsection,'mocktestsubsection':mocktestsubsection,'questions': questions})
    return redirect('/manage/')