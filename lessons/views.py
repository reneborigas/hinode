from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.shortcuts import redirect, render


from programs.models import ReviewProgram, Enrollment
from cms.views import instructor_check, student_check, format_score
from lessons.models import Lesson 
from django.contrib.auth.models import AbstractUser, UserManager,User

from lessons.forms import LessonForm 
from mocktests.models import MockTest
from programs.views import get_reviewprograms

def update(form, lesson):
    lesson.title = form.cleaned_data['title']
    lesson.subtitle = form.cleaned_data['subtitle']
    lesson.overview = form.cleaned_data['overview'] 
    lesson.description = form.cleaned_data['description']  
    lesson.status = form.cleaned_data['status']  
    lesson.save()
def delete(lesson):
    # Score.objects.filter(mocktest=mocktest).delete()
    # mocktest_questions = MockTestQuestion.objects.filter(mocktest=mocktest)
    # for mocktest_question in mocktest_questions:
    #     StudentAnswer.objects.filter(mocktest_question=mocktest_question).delete()
    # mocktest_questions.delete()
    lesson.delete()


@user_passes_test(instructor_check)
def list_lessons(request, reviewprogram_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    if request.user == reviewprogram.instructor:
        lessons = Lesson.objects.filter(reviewprogram=reviewprogram_id)
        return render(request, 'list_lessons.html', {'reviewprogram': reviewprogram,
            'lessons': lessons})
    return redirect('/manage/')


@user_passes_test(instructor_check)
def create_lesson(request, reviewprogram_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    
    # if MockTestSection.objects.filter(reviewprogram=reviewprogram).exists():
    form = LessonForm(reviewprogram=reviewprogram)
    if request.method == 'POST':
            form = LessonForm(reviewprogram=reviewprogram, data=request.POST)
            if form.is_valid():
                lessons = form.save(commit=False)
                lessons.reviewprogram = reviewprogram
                lessons.postedby= request.user
                lessons.save()
                # add_questions(reviewprogram, mocktest)
                messages.success(request, 'Lessons created successfully!')
                return redirect('/manage/' + reviewprogram_id + '/lessons/')
    return render(request, 'create_lesson.html', {'form': form,
            'reviewprogram': reviewprogram })
    # messages.error(request, 'ReviewProgram has no questions!')
    return redirect('/manage/' + reviewprogram_id)




@user_passes_test(instructor_check)
def edit_lesson(request, reviewprogram_id, lesson_id):
    reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
    lesson = Lesson.objects.get(id=lesson_id) 
    if request.user == reviewprogram.instructor:   
        form = LessonForm(instance=lesson)
        if request.method == 'POST' and 'update' in request.POST:
            form = LessonForm(instance=lesson, data=request.POST)
            if form.is_valid():
                update(form, lesson)
                # add_questions(reviewprogram, mocktest)
                messages.success(request, 'Lesson updated successfully!')
                return redirect('/manage/' + reviewprogram_id + '/lessons/')
        if request.method == 'POST' and 'delete' in request.POST:
            delete(lesson)
            messages.success(request, 'Lesson deleted successfully!')
            return redirect('/manage/' + reviewprogram_id + '/lessons/')
        return render(request, 'edit_lesson.html', {'form': form,
            'reviewprogram': reviewprogram, 'lesson': lesson })
    return redirect('/manage/' + reviewprogram_id + '/lessons/')



@user_passes_test(student_check)
def view_lesson(request, reviewprogram_id, lesson_id):
    if (Enrollment.objects.filter(user=request.user, reviewprogram=reviewprogram_id)
        .exists()):
        reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
        reviewprograms = get_reviewprograms(request.user)

        lesson = Lesson.objects.get(id=lesson_id) 
        lessons = Lesson.objects.filter(reviewprogram=reviewprogram_id)
        mocktests=MockTest.objects.filter(reviewprogram_id=reviewprogram_id)

        # mocktest_questions = MockTestQuestion.objects.filter(mocktest=mocktest)
        # try:
        #     score = (Score.objects.get(user=request.user, mocktest=mocktest)
        #         .score)
        #     result = format_score(score, mocktest_questions.count())
        # except ObjectDoesNotExist:
        #     result = "MockTest not yet taken."
        return render(request, 'view_lesson.html', {'mocktests':mocktests,'reviewprogram': reviewprogram,
            'lesson': lesson, 'reviewprograms':reviewprograms,'lessons':lessons})
    return redirect('/reviewprograms/')
