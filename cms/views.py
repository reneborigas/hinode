from itertools import chain

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
 

from cms.forms import ReviewProgramForm, StudentsForm
from programs.models import ReviewProgram, Enrollment
from mocktests.models import MockTest,MockTestSubSection,MockTestSection, Attempt

from questions.models import Question, Choice
 
def instructor_check(user):  
    if user.id == None:
        return False
    return user.is_teacher

def student_check(user):
    if user.id == None:
        return False
    return not user.is_teacher


def delete_reviewprogram(reviewprogram):
    reviewprogram.delete()
    # Enrollment.objects.filter(reviewprogram=reviewprogram).delete()

    # mocktestsubsection = MockTestSection.objects.filter(reviewprogram=reviewprogram)
    # questions = Question.objects.filter(reviewprogram=reviewprogram)
    # mocktests = MockTest.objects.filter(reviewprogram=reviewprogram)


    # for question in questions:
    #     exam_questions = MockTestQuestion.objects.filter(question=question)
    #     for exam_question in exam_questions:
    #         StudentAnswer.objects.filter(exam_question=exam_question).delete()
    #     Choice.objects.filter(question=question).delete()
    #     exam_questions.delete()
    # for exam in mocktests:
    #     Score.objects.filter(exam=exam)
    # questions.delete()
    # mocktests.delete()
   


def format_score(score, count):
    percentage = str(float(score) / float(count) * 100) + '%'
    return str(score) + '/' + str(count) + ' ' + percentage


@user_passes_test(instructor_check,settings.LOGIN_REDIRECT_URL)
def instructor_reviewprograms(request): 
    
    reviewprograms = ReviewProgram.objects.filter(instructor=request.user).order_by('-date_updated')
    mocktest_unflattened = list()
    for reviewprogram in reviewprograms:
        mocktest_unflattened.append(MockTest.objects.filter(reviewprogram=reviewprogram))
    mocktests = list(chain.from_iterable(mocktest_unflattened))
    mocktests.sort(key=lambda x: x.active_to)
    return render(request, 'instructor_reviewprograms.html' ,{'reviewprograms':reviewprograms,'mocktests':mocktests})


@user_passes_test(instructor_check,settings.LOGIN_REDIRECT_URL)
def create_reviewprogram(request):
    form = ReviewProgramForm()
    if request.method == 'POST':
        form = ReviewProgramForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            reviewprogram = form.save(commit=False)
            reviewprogram.instructor = request.user
            reviewprogram.save()
            messages.success(request, 'Review program created successfully!')
            return redirect('/manage/')
    return render(request, 'create_reviewprogram.html', {'form': form})


@user_passes_test(instructor_check,settings.LOGIN_REDIRECT_URL)
def edit_reviewprogram(request, reviewprogram_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    if request.user == reviewprogram.instructor:
        form = ReviewProgramForm(instance=reviewprogram)
        if request.method == 'POST' and 'update' in request.POST:
            form = ReviewProgramForm(instance=reviewprogram, data=request.POST,files=request.FILES)
            if form.is_valid():
                reviewprogram.title = form.cleaned_data['title']
                reviewprogram.overview = form.cleaned_data['overview']
                reviewprogram.description = form.cleaned_data['description']
                reviewprogram.status = form.cleaned_data['status']
                reviewprogram.image = form.cleaned_data['image']
                reviewprogram.save()
                messages.success(request, 'Review Program updated successfully!')
                return redirect('/manage/')
        if request.method == 'POST' and 'delete' in request.POST:
            delete_reviewprogram(reviewprogram)
            messages.success(request, 'Review Program deleted successfully!')
            return redirect('/manage/')
        return render(request, 'edit_reviewprogram.html', {'form': form,
            'reviewprogram': reviewprogram})
    return redirect('/manage/')


@user_passes_test(instructor_check,settings.LOGIN_REDIRECT_URL)
def edit_students(request, reviewprogram_id): 

    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id) 
     
    if request.user == reviewprogram.instructor:
        students = Enrollment.objects.filter(reviewprogram=reviewprogram_id)
        form = StudentsForm(instance=reviewprogram)
        if request.method == 'POST':
            form = StudentsForm(instance=reviewprogram, data=request.POST)
            if form.is_valid():
               
                Enrollment.objects.filter(reviewprogram=reviewprogram).delete()
                for student in form.cleaned_data['participants']:
                    part = Enrollment(user=student, reviewprogram=reviewprogram)
                    part.save()
                messages.success(request, 'Participants updated successfully!')
                return redirect('/manage/' + reviewprogram_id) 
        return render(request, 'edit_students.html', {'form': form,
            'reviewprogram': reviewprogram, 'students': students})
    return redirect('/manage/')


@user_passes_test(instructor_check,settings.LOGIN_REDIRECT_URL)
def view_reviewprogram_results(request, reviewprogram_id):
    reviewprogram = reviewprogram.objects.get(id=reviewprogram_id)
    if request.user == reviewprogram.owner:
        students = Enrollment.objects.filter(reviewprogram=reviewprogram_id)
        exams = Exam.objects.filter(reviewprogram=reviewprogram_id)
        scores = {}
        for student in students:
            scores[student] = {}
            for exam in exams:
                try:
                    count = ExamQuestion.objects.filter(exam=exam).count()
                    score = Attempt.objects.get(user=student.user,
                        exam=exam).score
                    scores[student][exam] = format_score(score, count)
                except ObjectDoesNotExist:
                    scores[student][exam] = "Not taken"
        return render(request, 'view_reviewprogram_results.html', {'reviewprogram': reviewprogram,
            'exams': exams, 'scores': scores})
    return redirect('/reviewprograms/')


@user_passes_test(student_check,settings.LOGIN_REDIRECT_URL)
def student_reviewprograms(request):
    students = Enrollment.objects.filter(user=request.user)
    reviewprograms = list()
    unfinished = list()
    for student in students:
        reviewprograms.append(reviewprogram.objects.filter(id=student.reviewprogram.id))
    reviewprograms = list(chain.from_iterable(reviewprograms))
    reviewprograms.sort(key=lambda x: x.updated, reverse=True)
    for reviewprogram in reviewprograms:
        exams = Exam.objects.filter(reviewprogram=reviewprogram)
        for exam in exams:
            if (exam.active and not Attempt.objects.filter(user=request.user,
                exam=exam).exists() and ExamQuestion.objects.filter(exam=exam)
                .exists()):
                    unfinished.append(exam)
    unfinished.sort(key=lambda x: x.active_to)
    return render(request, 'student_reviewprograms.html', {'reviewprograms': reviewprograms,
        'exams': unfinished})


@user_passes_test(student_check,settings.LOGIN_REDIRECT_URL)
def view_reviewprogram(request, reviewprogram_id):
    if (Enrollment.objects.filter(user=request.user, reviewprogram=reviewprogram_id)
        .exists()):
        reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
        scores = {}
        exams = MockTest.objects.filter(reviewprogram=reviewprogram_id).order_by('active_to')
        students = Enrollment.objects.filter(reviewprogram=reviewprogram_id)
        for exam in exams:
                try:
                    count = MockTestQuestion.objects.filter(exam=exam).count()
                    score = Attempt.objects.get(user=request.user,
                        mocktest=mocktest).score
                    scores[exam] = format_score(score, count)
                except ObjectDoesNotExist:
                    scores[exam] = "Not taken"
        return render(request, 'view_reviewprogram.html', {'reviewprogram': reviewprogram,
            'students': students, 'exams': exams, 'scores': scores})
    return redirect('/reviewprograms/s')