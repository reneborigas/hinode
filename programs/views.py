from itertools import chain

from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import ReviewProgram,Enrollment
from mocktests.models import MockTest
from lessons.models import Lesson
# Create your views here. 
def home(request):  
    return redirect('/accounts/login/')
  
def about(request):
    context= {}
    template = 'about.html'  
    return render(request,template,context)

@login_required
def loadreviewprograms(request):
    # populate_db()    
        if request.user.is_teacher:
            return redirect('/manage/') 
        reviewprograms = get_reviewprograms(request.user)
        context= {'reviewprograms': reviewprograms}
        template = 'program.html'  
        return render(request,template,context)

def get_reviewprograms(user):
    enrollments = Enrollment.objects.filter(user=user)
    reviewprograms = list()
    unfinished = list()
    for enrollment in enrollments:
        reviewprograms.append(ReviewProgram.objects.filter(id=enrollment.reviewprogram.id))
    reviewprograms = list(chain.from_iterable(reviewprograms))
    reviewprograms.sort(key=lambda x: x.date_updated, reverse=True)
    return reviewprograms

@login_required
def userProfile(request):   
    user=request.user
    context= {'user':user}
    template = 'profile.html'  
    return render(request,template,context)


 
def items(request,reviewprogram_id):
    if (Enrollment.objects.filter(user=request.user, reviewprogram=reviewprogram_id).exists()):
        reviewprograms = get_reviewprograms(request.user)
        reviewprogram = ReviewProgram.objects.get(id=reviewprogram_id)
        lessons=Lesson.objects.filter(reviewprogram_id=reviewprogram.id)
        mocktests=MockTest.objects.filter(reviewprogram_id=reviewprogram.id)

        context= {'reviewprograms': reviewprograms,'reviewprogram': reviewprogram,'lessons':lessons,'mocktests':mocktests}
        template = 'review_program_item.html'  
        
        return render(request,template,context)
    return redirect('/reviewprograms/')
# def populate_db():
#     if ReviewProgram.object.count() == 0:
#         programs().save()