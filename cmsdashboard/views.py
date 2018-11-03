 

from django.shortcuts import redirect, render

from django.contrib.auth.decorators import user_passes_test
from cms.views import instructor_check,student_check
from mocktests.models import Attempt

from django.contrib.auth.models import AbstractUser, UserManager,User
# Create your views here.

@user_passes_test(instructor_check)
def view_dashboard(request): 

    ongoingattempts = Attempt.objects.filter(status=1)
    
    finishedattempts = Attempt.objects.filter(status=2)
    # for finishedattempt in finishedattempts:
    #     finishedattempt.updateresult()

    students = User.objects.filter(is_staff=False, is_superuser=False, is_teacher=False)
    
    successfulresults = Attempt.objects.filter(result=1,status=2)    
    failedresults = Attempt.objects.filter(result=0,status=2)    

    totalattempts= (successfulresults.count() +  ongoingattempts.count() + failedresults.count())
    
    successpercent = ((successfulresults.count() / totalattempts) * 100)
    failedpercent = ((failedresults.count() / totalattempts) * 100)
    ongoingpercent = ((ongoingattempts.count() / totalattempts) * 100)

    return render(request, 'dashboard.html',{'ongoingattempts':ongoingattempts,'successfulresults':successfulresults,'failedresults':failedresults,'students':students,
    'successpercent':successpercent,'failedpercent':failedpercent,'ongoingpercent':ongoingpercent})