import operator 
from itertools import chain
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.shortcuts import redirect, render

from programs.models import ReviewProgram, Enrollment
from cms.views import instructor_check, student_check, format_score
from programs.views import get_reviewprograms
from mocktests.forms import MockTestForm,SectionForm,SubSectionForm,SentenceForm
from mocktests.models import MockTest,MockTestSection,MockTestSubSection, Attempt,Score
from lessons.models import Lesson
from questions.models import Question, Choice,StudentAnswer,MockTestSentence
from django.contrib.auth.models import AbstractUser, UserManager, User
import datetime

def update(form, mocktest):
    mocktest.title = form.cleaned_data['title']
    mocktest.subtitle = form.cleaned_data['subtitle']
    mocktest.overview = form.cleaned_data['overview']
    mocktest.guidelines = form.cleaned_data['guidelines']
    mocktest.description = form.cleaned_data['description'] 
    mocktest.active_from = form.cleaned_data['active_from']
    mocktest.active_to = form.cleaned_data['active_to'] 
    mocktest.status = form.cleaned_data['status']  
    mocktest.save()
    
def updatesection(form, mocktestsection):

    mocktestsection.title = form.cleaned_data['title']
    mocktestsection.subtitle = form.cleaned_data['subtitle']
    mocktestsection.guidelines = form.cleaned_data['guidelines']
    mocktestsection.description = form.cleaned_data['description']   
    mocktestsection.test_time_minutes = form.cleaned_data['test_time_minutes']  
    mocktestsection.max_no_of_attempts = form.cleaned_data['max_no_of_attempts']  
    mocktestsection.passing_mark = form.cleaned_data['passing_mark']  
    mocktestsection.password = form.cleaned_data['password']  
    mocktestsection.status = form.cleaned_data['status']  
    mocktestsection.save()

def updatesubsection(form, mocktestsubsection):
    mocktestsubsection.title = form.cleaned_data['title']
    mocktestsubsection.subtitle = form.cleaned_data['subtitle']
    mocktestsubsection.guidelines = form.cleaned_data['guidelines']
    mocktestsubsection.description = form.cleaned_data['description']  
    mocktestsubsection.status = form.cleaned_data['status']  
    mocktestsubsection.save() 

def updatesentence(form, mocktestsentence):
    mocktestsentence.sentence_no = form.cleaned_data['sentence_no']
    mocktestsentence.sentence_text = form.cleaned_data['sentence_text'] 
    mocktestsentence.image = form.cleaned_data['image']   
    mocktestsentence.save() 

def delete(mocktest):
    # Score.objects.filter(mocktest=mocktest).delete()
    # mocktest_questions = MockTestQuestion.objects.filter(mocktest=mocktest)
    # for mocktest_question in mocktest_questions:
    #     StudentAnswer.objects.filter(mocktest_question=mocktest_question).delete()
    # mocktest_questions.delete()
    mocktest.delete()


def deletesection(mocktestsection):
    # Score.objects.filter(mocktest=mocktest).delete()
    # mocktest_questions = MockTestQuestion.objects.filter(mocktest=mocktest)
    # for mocktest_question in mocktest_questions:
    #     StudentAnswer.objects.filter(mocktest_question=mocktest_question).delete()
    # mocktest_questions.delete()
    mocktestsection.delete()

def deletesubsection(mocktestsubsection):
    # Score.objects.filter(mocktest=mocktest).delete()
    # mocktest_questions = MockTestQuestion.objects.filter(mocktest=mocktest)
    # for mocktest_question in mocktest_questions:
    #     StudentAnswer.objects.filter(mocktest_question=mocktest_question).delete()
    # mocktest_questions.delete()
    mocktestsubsection.delete()

def deletesentence(mocktestsence):
    # Score.objects.filter(mocktest=mocktest).delete()
    # mocktest_questions = MockTestQuestion.objects.filter(mocktest=mocktest)
    # for mocktest_question in mocktest_questions:
    #     StudentAnswer.objects.filter(mocktest_question=mocktest_question).delete()
    # mocktest_questions.delete()
    mocktestsence.delete()

def add_questions(reviewprogram, mocktest):
    MockTestQuestion.objects.filter(mocktest=mocktest).delete()
    questions = (Question.objects.filter(reviewprogram=reviewprogram, category=mocktest.category)
        .order_by('?')[:mocktest.question_count])
    for question in questions:
        quest = MockTestQuestion(question=question, mocktest=mocktest)
        quest.save()


@user_passes_test(instructor_check)
def create_mocktest(request, reviewprogram_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    
    # if MockTestSection.objects.filter(reviewprogram=reviewprogram).exists():
    form = MockTestForm(reviewprogram=reviewprogram)
    if request.method == 'POST':
            form = MockTestForm(reviewprogram=reviewprogram, data=request.POST)
            if form.is_valid():
                mocktest = form.save(commit=False)
                mocktest.reviewprogram = reviewprogram
                mocktest.postedby= request.user
                mocktest.save()
                # add_questions(reviewprogram, mocktest)
                messages.success(request, 'Mock Test created successfully!')
                return redirect('/manage/' + reviewprogram_id + '/mocktests/')
    return render(request, 'create_mocktest.html', {'form': form,
            'reviewprogram': reviewprogram })
    # messages.error(request, 'ReviewProgram has no questions!')
    return redirect('/manage/' + reviewprogram_id)

@user_passes_test(instructor_check)
def create_section(request,reviewprogram_id ,mocktest_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id)
    # if MockTestSection.objects.filter(reviewprogram=reviewprogram).exists():
    form = SectionForm(mocktest=mocktest)
    if request.method == 'POST':
            form = SectionForm(mocktest=mocktest, data=request.POST)
            if form.is_valid():
                mocktestsection = form.save(commit=False)
                mocktestsection.mocktest = mocktest
                mocktestsection.postedby= request.user
                mocktestsection.save()
                # add_questions(reviewprogram, mocktest)
                messages.success(request, 'Mock Test Section created successfully!')
                return redirect('/manage/' + reviewprogram_id + '/mocktests/' + mocktest_id +'/sections')
    return render(request, 'create_section.html', {'form': form,
            'reviewprogram': reviewprogram,'mocktest':mocktest })
    # messages.error(request, 'ReviewProgram has no questions!')
    return redirect('/manage/' + reviewprogram_id + '/mocktests/' + mocktest_id )
@user_passes_test(instructor_check)
def create_subsection(request,reviewprogram_id ,mocktest_id,mocktestsection_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id)
    mocktestsection = MockTestSection.objects.get(id=mocktestsection_id)
    # if MockTestSection.objects.filter(reviewprogram=reviewprogram).exists():
    form = SubSectionForm(mocktestsection=mocktestsection)
    if request.method == 'POST':
            form = SubSectionForm(mocktestsection=mocktestsection, data=request.POST)
            if form.is_valid():
                mocktestsubsection = form.save(commit=False)
                mocktestsubsection.mocktestsection = mocktestsection
                mocktestsubsection.postedby= request.user
                mocktestsubsection.save()
                # add_questions(reviewprogram, mocktest)
                messages.success(request, 'Mock Test Sub Section created successfully!')
                return redirect('/manage/' + reviewprogram_id + '/mocktests/' + mocktest_id +'/sections/'+ mocktestsection_id +'/subsections')
    return render(request, 'create_subsection.html', {'form': form,
            'reviewprogram': reviewprogram,'mocktest':mocktest ,'mocktestsection':mocktestsection })
    # messages.error(request, 'ReviewProgram has no questions!')
    return redirect('/manage/' + reviewprogram_id + '/mocktests/' + mocktest_id )

@user_passes_test(instructor_check)
def create_mocktest_sentence(request,reviewprogram_id ,mocktest_id,mocktestsection_id,mocktestsubsection_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id)
    mocktestsection = MockTestSection.objects.get(id=mocktestsection_id)
    mocktestsubsection = MockTestSubSection.objects.get(id=mocktestsubsection_id)
     
    # if MockTestSection.objects.filter(reviewprogram=reviewprogram).exists():
    form = SentenceForm()
    if request.method == 'POST':
            form = SentenceForm( data=request.POST,files=request.FILES)
            if form.is_valid():
                mocktestsentence = form.save(commit=False)
                mocktestsentence.mocktestsubsection = mocktestsubsection 
                mocktestsentence.save()
                # add_questions(reviewprogram, mocktest)
                messages.success(request, 'Mock Test Sentence created successfully!')
                return redirect('/manage/' + reviewprogram_id + '/mocktests/' + mocktest_id +'/sections/'+ mocktestsection_id +'/subsections/'+ mocktestsubsection_id +'/sentences')
    return render(request, 'create_sentence.html', {'form': form,
            'reviewprogram': reviewprogram,'mocktest':mocktest ,'mocktestsection':mocktestsection,'mocktestsubsection':mocktestsubsection })
    # messages.error(request, 'ReviewProgram has no questions!')
    return redirect('/manage/' + reviewprogram_id + '/mocktests/' + mocktest_id )

@user_passes_test(instructor_check)
def edit_mocktest_sentence(request, reviewprogram_id, mocktest_id, mocktestsection_id, mocktestsubsection_id,mocktestsentence_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id) 
    mocktestsection  = MockTestSection.objects.get(id=mocktestsection_id) 
    mocktestsubsection  = MockTestSubSection.objects.get(id=mocktestsubsection_id)
    mocktestsentence  = MockTestSentence.objects.get(id=mocktestsentence_id)
    questions = Question.objects.filter(mocktestsentence_id=mocktestsentence)
    if request.user == reviewprogram.instructor:   
        form = SentenceForm(instance=mocktestsentence)
     
        if request.method == 'POST' and 'update' in request.POST:
            form = SentenceForm(instance=mocktestsentence, data=request.POST,files=request.FILES) 
           
            if form.is_valid():
                updatesentence(form, mocktestsentence)
                # add_questions(reviewprogram, mocktest)
                messages.success(request, 'Mock Test Sentence updated successfully!')
                return redirect('/manage/' + reviewprogram_id + '/mocktests/' + mocktest_id + '/sections/'+ mocktestsection_id + '/subsections/'+ mocktestsubsection_id + '/sentences' )
        if request.method == 'POST' and 'delete' in request.POST:
            deletesentence(mocktestsence)
            messages.success(request, 'MockTest Sub Section deleted successfully!')
            return redirect('/manage/' + reviewprogram_id + '/mocktests/'+ mocktest_id + '/sections/'+ mocktestsection_id + '/subsections/'+ mocktestsubsection_id + '/sentences' )
        return render(request, 'edit_sentence.html', {'form': form,'questions':questions,
            'reviewprogram': reviewprogram, 'mocktest': mocktest ,'mocktestsection':mocktestsection,'mocktestsubsection':mocktestsubsection,'mocktestsentence':mocktestsentence})
    return redirect('/manage/' + reviewprogram_id + '/mocktests/' + mocktest_id +'/sections/'+ mocktestsection_id + '/subsections/'+ mocktestsubsection_id + '/sentences' )




@user_passes_test(instructor_check)
def edit_mocktest(request, reviewprogram_id, mocktest_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id) 
    if request.user == reviewprogram.instructor:   
        form = MockTestForm(instance=mocktest)
        if request.method == 'POST' and 'update' in request.POST:
            form = MockTestForm(instance=mocktest, data=request.POST)
            if form.is_valid():
                update(form, mocktest)
                # add_questions(reviewprogram, mocktest)
                messages.success(request, 'Mock Test updated successfully!')
                return redirect('/manage/' + reviewprogram_id + '/mocktests/')
        if request.method == 'POST' and 'delete' in request.POST:
            delete(mocktest)
            messages.success(request, 'Mock Test deleted successfully!')
            return redirect('/manage/' + reviewprogram_id + '/mocktests/')
        return render(request, 'edit_mocktest.html', {'form': form,
            'reviewprogram': reviewprogram, 'mocktest': mocktest })
    return redirect('/manage/' + reviewprogram_id + '/mocktests/')

@user_passes_test(instructor_check)
def edit_section(request, reviewprogram_id, mocktest_id, mocktestsection_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id) 
    mocktestsection  = MockTestSection.objects.get(id=mocktestsection_id) 

    if request.user == reviewprogram.instructor:   
        form = SectionForm(instance=mocktestsection)
        if request.method == 'POST' and 'update' in request.POST:
            form = SectionForm(instance=mocktestsection, data=request.POST)
            if form.is_valid():
                updatesection(form, mocktestsection)
                # add_questions(reviewprogram, mocktest)
                messages.success(request, 'Mock Test Section updated successfully!')
                return redirect('/manage/' + reviewprogram_id + '/mocktests/' + mocktest_id + '/sections' )
        if request.method == 'POST' and 'delete' in request.POST:
            deletesection(mocktestsection)
            messages.success(request, 'MockTest deleted successfully!')
            return redirect('/manage/' + reviewprogram_id + '/mocktests/'+ mocktest_id + '/sections' )
        return render(request, 'edit_section.html', {'form': form,
            'reviewprogram': reviewprogram, 'mocktest': mocktest ,'mocktestsection':mocktestsection})
    return redirect('/manage/' + reviewprogram_id + '/mocktests/' + mocktest_id +'/sections' ) 

@user_passes_test(instructor_check)
def edit_subsection(request, reviewprogram_id, mocktest_id, mocktestsection_id, mocktestsubsection_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id) 
    mocktestsection  = MockTestSection.objects.get(id=mocktestsection_id) 
    mocktestsubsection  = MockTestSubSection.objects.get(id=mocktestsubsection_id)

    if request.user == reviewprogram.instructor:   
        form = SubSectionForm(instance=mocktestsubsection)
        if request.method == 'POST' and 'update' in request.POST:
            form = SubSectionForm(instance=mocktestsubsection, data=request.POST)
            if form.is_valid():
                updatesubsection(form, mocktestsubsection)
                # add_questions(reviewprogram, mocktest)
                messages.success(request, 'Mock Test Sub Section updated successfully!')
                return redirect('/manage/' + reviewprogram_id + '/mocktests/' + mocktest_id + '/sections/'+ mocktestsection_id + '/subsections' )
        if request.method == 'POST' and 'delete' in request.POST:
            deletesubsection(mocktestsubsection)
            messages.success(request, 'MockTest Sub Section deleted successfully!')
            return redirect('/manage/' + reviewprogram_id + '/mocktests/'+ mocktest_id + '/sections/'+ mocktestsection_id + '/subsections' )
        return render(request, 'edit_subsection.html', {'form': form,
            'reviewprogram': reviewprogram, 'mocktest': mocktest ,'mocktestsection':mocktestsection,'mocktestsubsection':mocktestsubsection})
    return redirect('/manage/' + reviewprogram_id + '/mocktests/' + mocktest_id +'/sections/'+ mocktestsection_id + '/subsections' )


@user_passes_test(instructor_check)
def list_mocktests(request, reviewprogram_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    if request.user == reviewprogram.instructor:
        mocktests = MockTest.objects.filter(reviewprogram=reviewprogram_id).order_by('active_to')
        return render(request, 'list_mocktests.html', {'reviewprogram': reviewprogram,
            'mocktests': mocktests})
    return redirect('/manage/')


@user_passes_test(instructor_check)
def view_mocktest_results(request, reviewprogram_id, mocktest_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id)
    if request.user == reviewprogram.owner:
        participants = Participation.objects.filter(reviewprogram=reviewprogram)
        count = MockTestQuestion.objects.filter(mocktest=mocktest).count()
        scores = {}     
        for participant in participants:
            try:            
                score = (Attempt.objects.get(user=participant.user, mocktest=mocktest)
                    .score)
                scores[participant] = format_score(score, count)
            except ObjectDoesNotExist:
                scores[participant] = "Not taken"
        return render(request, 'view_mocktest_results.html', {'reviewprogram': reviewprogram,
            'mocktest': mocktest, 'scores': scores})
    return redirect('/reviewprograms/')


@user_passes_test(instructor_check)
def view_participant_result(request, reviewprogram_id, mocktest_id, student_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id)
    if request.user == reviewprogram.owner:
        student = User.objects.get(id=student_id)
        mocktest = MockTest.objects.get(id=mocktest_id)
        mocktest_questions = MockTestQuestion.objects.filter(mocktest=mocktest)
        score = Attempt.objects.get(user=student, mocktest=mocktest).score
        result = format_score(score, mocktest_questions.count())
        answers = {}
        for mocktest_question in mocktest_questions:
            answers[mocktest_question] = StudentAnswer.objects.get(user=
                student, mocktest_question=mocktest_question).answer
        return render(request, 'view_result.html', {'reviewprogram': reviewprogram,
            'mocktest': mocktest, 'mocktest_questions': mocktest_questions, 'result': result,
            'answers': answers, 'student': student})
    return redirect('/reviewprograms/')


@user_passes_test(instructor_check)
def view_assigned(request, reviewprogram_id, mocktest_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id)
    if request.user == reviewprogram.owner:
        mocktest_questions = MockTestQuestion.objects.filter(mocktest=mocktest)
        return render(request, 'view_questions.html', {'reviewprogram': reviewprogram,
            'mocktest': mocktest, 'mocktest_questions': mocktest_questions})
    return redirect('/reviewprograms/')


@user_passes_test(instructor_check)
def view_sections(request, reviewprogram_id, mocktest_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id)
    if request.user == reviewprogram.instructor:
        mocktest_sections = MockTestSection.objects.filter(mocktest=mocktest)
        return render(request, 'view_sections.html', {'reviewprogram': reviewprogram,
            'mocktest': mocktest, 'mocktest_sections': mocktest_sections})
    return redirect('/manage/')

@user_passes_test(instructor_check)
def view_subsections(request, reviewprogram_id, mocktest_id,mocktestsection_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id)
    mocktestsection = MockTestSection.objects.get(id=mocktestsection_id) 
    if request.user == reviewprogram.instructor:
        mocktest_subsections = MockTestSubSection.objects.filter(mocktestsection=mocktestsection)
        return render(request, 'view_subsections.html', {'reviewprogram': reviewprogram,
            'mocktest': mocktest,'mocktestsection': mocktestsection, 'mocktest_subsections': mocktest_subsections})
    return redirect('/manage/')

@user_passes_test(instructor_check)
def view_mocktest_sentences(request, reviewprogram_id, mocktest_id,mocktestsection_id,mocktestsubsection_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    mocktest = MockTest.objects.get(id=mocktest_id)
    mocktestsection = MockTestSection.objects.get(id=mocktestsection_id) 
    mocktestsubsection = MockTestSubSection.objects.get(id=mocktestsubsection_id) 
    if request.user == reviewprogram.instructor:
        mocktest_sentences = MockTestSentence.objects.filter(mocktestsubsection=mocktestsubsection)
        return render(request, 'view_sentences.html', {'reviewprogram': reviewprogram,
            'mocktest': mocktest,'mocktestsection': mocktestsection, 'mocktestsubsection': mocktestsubsection,'mocktest_sentences':mocktest_sentences})
    return redirect('/manage/')

@user_passes_test(student_check)
def view_mocktest(request, reviewprogram_id, mocktest_id):
    if (Enrollment.objects.filter(user=request.user, reviewprogram=reviewprogram_id)
        .exists()):
        reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
        mocktest = MockTest.objects.get(id=mocktest_id)
        mocktestsections = MockTestSection.objects.filter(mocktest=mocktest_id)
        reviewprograms = get_reviewprograms(request.user)
        mocktests=MockTest.objects.filter(reviewprogram_id=reviewprogram_id)
        lessons=Lesson.objects.filter(reviewprogram_id=reviewprogram_id)
        for mocktestsection in mocktestsections:
             mocktestsection.get_attempts(user=request.user)
             mocktestsection.get_total_no_of_items()
        # mocktest_questions = MockTestQuestion.objects.filter(mocktest=mocktest)
        # try:
        #     score = (Score.objects.get(user=request.user, mocktest=mocktest)
        #         .score)
        #     result = format_score(score, mocktest_questions.count())
        # except ObjectDoesNotExist:
        #     result = "MockTest not yet taken."
        return render(request, 'view_mocktest.html', {'lessons':lessons,'mocktests':mocktests,'reviewprogram': reviewprogram,
            'mocktest': mocktest, 'mocktestsections': mocktestsections, 'reviewprograms':reviewprograms})
    return redirect('/reviewprograms/')


@user_passes_test(student_check,settings.LOGIN_REDIRECT_URL)
def view_mocktestsection(request, reviewprogram_id, mocktest_id, mocktestsection_id):
    mocktestsection = MockTestSection.objects.get(id=mocktestsection_id)
     
    try:      
        referer = request.META['HTTP_REFERER'] 
        if ((reverse('input_password', args=[reviewprogram_id,mocktest_id, mocktestsection_id]) in
            referer) or
            (reverse('view_mocktestsection', args=[reviewprogram_id,mocktest_id, mocktestsection_id]) in
            referer) or
            not mocktestsection.password): 
            
            if (Enrollment.objects.filter(user=request.user, reviewprogram=reviewprogram_id).exists()):
                reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
                mocktest = MockTest.objects.get(id=mocktest_id)
                
                mocktestsection = MockTestSection.objects.get(id=mocktestsection_id) 

                mocktestsection.get_attempts(user=request.user)
                mocktestsection.get_total_no_of_items()

                mocktestsubsections = MockTestSubSection.objects.filter(mocktestsection=mocktestsection_id)
               
                totalitems=0
                for mocktestsubsection in mocktestsubsections:
                    totalitems += mocktestsubsection.question_set.count() 
                     
                if request.method == 'POST':  
                    attempt = Attempt.objects.get(id=request.POST.get('attemptid'))
                    if not attempt: 
                        attempt = Attempt.objects.create(user=request.user,
                                mocktestsection=mocktestsection,totalitems=totalitems,start_time=datetime.datetime.now(),result=2)

                     
                    totalcorrect=0
                    for mocktestsubsection in mocktestsubsections:
                        correct = 0
                        
                        for mocktest_question in mocktestsubsection.question_set.all():
                            
                            try:
                                st_answer = StudentAnswer.objects.create(
                                    user=request.user,question=mocktest_question,
                                    choice_id=request.POST.get(str(mocktest_question.id)),
                                    attempt=attempt)
                                if (st_answer.question.choice_set.get(id=
                                    st_answer.choice_id).correct):
                                    correct += 1

                               
                            except ObjectDoesNotExist:
                                continue;
                                
                        score = Score.objects.create(user=request.user,attempt=attempt,mocktestsubsection=mocktestsubsection, score=correct,totalitems=mocktestsubsection.question_set.count())
                        totalcorrect += correct
                        
                    if totalcorrect < mocktestsection.passing_mark:
                        attempt.result=0
                    else:
                        attempt.result=1 

                    attempt.totalscore =   totalcorrect
                    attempt.end_time = datetime.datetime.now()
                    attempt.status = 2
                    attempt.save()



                    messages.success(request, 'Mock Test finished with ' +
                        str(totalcorrect) + ' correct answers!')
                 
                    return redirect('/reviewprograms/' +  reviewprogram_id + '/mocktests/' +
                        mocktest_id + '/s')
                else:
                    if  mocktestsection.no_of_attempts -1 == mocktestsection.max_no_of_attempts:
                        return redirect('/reviewprograms/' +  reviewprogram_id + '/mocktests/' +
                        mocktest_id + '/s')
                    else:
                        print("Created!")
                        Attempt.objects.filter(result=2,user=request.user).delete()
                        attempt = Attempt.objects.create(user=request.user,
                                mocktestsection=mocktestsection,totalitems=totalitems,start_time=datetime.datetime.now(),result=2)
                    
                return render(request, 'view_mocktestsection.html', {'reviewprogram': reviewprogram,
                    'mocktest': mocktest, 'mocktestsection': mocktestsection,'mocktestsubsections':mocktestsubsections,'attempt':attempt })
               

                # mocktest_questions = MockTestQuestion.objects.filter(mocktest=mocktest)
                # try:
                #     score = (Score.objects.get(user=request.user, mocktest=mocktest)
                #         .score)
                #     result = format_score(score, mocktest_questions.count())
                # except ObjectDoesNotExist:
                #     result = "MockTest not yet taken."
                
            return redirect('/reviewprograms/')
        return redirect('/reviewprograms/'+reviewprogram_id+'/mocktests/'+mocktest_id+'/s' )
    except KeyError as e:  
        return redirect('/reviewprograms/' +  reviewprogram_id + '/mocktests/' +
            mocktest_id + '/s')


@user_passes_test(student_check)
def input_password(request, reviewprogram_id, mocktest_id,mocktestsection_id):
    if (Enrollment.objects.filter(user=request.user, reviewprogram=reviewprogram_id).exists()):
        reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
        mocktest = MockTest.objects.get(id=mocktest_id)
        reviewprograms = get_reviewprograms(request.user)
        lessons= Lesson.objects.filter(reviewprogram=reviewprogram_id)
        mocktests = MockTest.objects.filter(reviewprogram=reviewprogram_id)
        mocktestsection = MockTestSection.objects.get(id=mocktestsection_id)
        mocktestsection.get_attempts(user=request.user)
        mocktestsection.get_total_no_of_items()

        if request.method == 'POST':
            entered = request.POST.get('input')
            if entered == mocktestsection.password:
                return redirect('/reviewprograms/' +  reviewprogram_id + '/mocktests/' +
                        mocktest_id + '/s/'+ mocktestsection_id )
            messages.error(request, 'Invalid Mock Test Password!')           
        return render(request, 'input_password.html', {'reviewprogram': reviewprogram,'reviewprograms':reviewprograms,'lessons':lessons,'mocktests':mocktests,
            'mocktest': mocktest, 'mocktestsection': mocktestsection }) 
    return redirect('/reviewprograms/')
    
    
    # if request.method == 'POST':
    #     entered = request.POST.get('input')
    #     if entered == mocktestsection.password:
    #         return redirect('/manage/' +  reviewprogram_id + '/mocktests/' +
    #                 mocktest_id + '/s/'+ mocktestsection_id )
    # return render(request, 'input_password.html', {'reviewprogram': reviewprogram,
    #     'mocktest': mocktest, 'mocktestsection': mocktestsection })

@user_passes_test(student_check)
def take_mocktest(request, reviewprogram_id, mocktest_id):
    mocktest = MockTest.objects.get(id=mocktest_id)
    try:
        referer = request.META['HTTP_REFERER']
        if ((reverse('input_password', args=[reviewprogram_id, mocktest_id]) in
            referer) or
            (reverse('take_mocktest', args=[reviewprogram_id, mocktest_id]) in
            referer) or
            not mocktest.password):
            if (Participation.objects.filter(user=request.user, reviewprogram=reviewprogram_id)
                .exists()):
                reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
                mocktest_questions = MockTestQuestion.objects.filter(mocktest=mocktest)
                if mocktest.active:
                    if Attempt.objects.filter(user=request.user, mocktest=mocktest).exists():
                        messages.error(request, 'MockTest already taken!')
                        return redirect('/reviewprograms/' +  reviewprogram_id + '/mocktests/' +
                            mocktest_id + '/s')
                    if request.method == 'POST':
                        correct = 0
                        for mocktest_quest in mocktest_questions:
                            try:
                                st_answer = StudentAnswer.objects.create(
                                    user=request.user, mocktest_question=mocktest_quest,
                                    answer=request.POST.get(str(mocktest_quest.question.id)))
                                if (st_answer.mocktest_question.question.choice_set.get(id=
                                    st_answer.answer).correct):
                                    correct += 1
                            except ObjectDoesNotExist:
                                continue;
                        score = Attempt.objects.create(user=request.user,
                            mocktest=mocktest, score=correct)
                        messages.success(request, 'MockTest finished with ' +
                            str(correct) + ' correct answers!')
                        return redirect('/reviewprograms/' +  reviewprogram_id + '/mocktests/' +
                            mocktest_id + '/s')
                    return render(request, 'take_mocktest.html', {'reviewprogram': reviewprogram,
                        'mocktest': mocktest, 'mocktest_questions': mocktest_questions})
                messages.error(request, 'MockTest inactive!')
                return redirect('/reviewprograms/' +  reviewprogram_id + '/mocktests/' + mocktest_id + '/s')
            return redirect('/reviewprograms/s')
        return redirect('/reviewprograms/' +  reviewprogram_id + '/mocktests/' +
            mocktest_id + '/p')
    except KeyError:
        return redirect('/reviewprograms/' +  reviewprogram_id + '/mocktests/' +
            mocktest_id + '/p')


@user_passes_test(student_check)
def view_result(request, reviewprogram_id, mocktest_id):
    if (Participation.objects.filter(user=request.user, reviewprogram=reviewprogram_id)
        .exists() and Attempt.objects.filter(user=request.user, mocktest=mocktest_id)
        .exists()):
        reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
        mocktest = MockTest.objects.get(id=mocktest_id)
        mocktest_questions = MockTestQuestion.objects.filter(mocktest=mocktest)
        score = Score.objects.get(user=request.user, mocktest=mocktest).score
        result = format_score(score, mocktest_questions.count())
        answers = {}
        for mocktest_question in mocktest_questions:
            answers[mocktest_question] = StudentAnswer.objects.get(user=
                request.user, mocktest_question=mocktest_question).answer
        return render(request, 'view_result.html', {'reviewprogram': reviewprogram,
            'mocktest': mocktest, 'mocktest_questions': mocktest_questions, 'result': result,
            'answers': answers})
    return redirect('/reviewprograms/s')