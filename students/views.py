from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from cms.views import instructor_check,student_check
from mocktests.models import Attempt,Score,MockTestSection,MockTest
from programs.models import Enrollment,ReviewProgram
from lessons.models import Lesson

from programs.views import get_reviewprograms

from students.forms import UserCreationForm,UserChangeForm,AdminPasswordChangeForm

from django.contrib.auth.models import AbstractUser, UserManager,User

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

from django.conf import settings

# Create your views here.


@user_passes_test(instructor_check) 
def list_students(request):  


    # students = User.objects.filter(is_staff=False, is_superuser=False, is_teacher=False).prefetch_related('enrolled') 
    students = User.objects.filter(is_teacher=False,is_staff=False).order_by('-date_joined')
    
    return render(request, 'list_students.html',{'students':students})


@user_passes_test(instructor_check) 
def list_enrollments(request):  


    # students = User.objects.filter(is_staff=False, is_superuser=False, is_teacher=False).prefetch_related('enrolled') 
    students = Enrollment.objects.all().order_by('-date_created')
    
    return render(request, 'list_enrollments.html',{'students':students})


@user_passes_test(instructor_check) 
def list_students_attempts(request,student_user_id,student_reviewprogram_id):  
    student = Enrollment.objects.get(user=student_user_id,reviewprogram=student_reviewprogram_id)
    
    mocktests = MockTest.objects.filter(reviewprogram=student_reviewprogram_id)
    
    for mocktest in mocktests:
        mocktest.setmocktestsections()
        for mocktestsection in mocktest.mocktestsections:
            mocktestsection.setattempts(user=student_user_id)
           
            for attempt in mocktestsection.attempts:
                 
                attempt.setscores()
              

    attempts = Attempt.objects.filter(user=student_user_id).order_by('-attempt_date','-start_time') 
      
    return render(request, 'list_students_attempts.html',{'attempts':attempts,'student':student, 'mocktests':mocktests})

@user_passes_test(student_check) 
def list_students_attempts_front(request,reviewprogram_id):  
    student = Enrollment.objects.get(user=request.user,reviewprogram=reviewprogram_id)
    reviewprograms = get_reviewprograms(request.user)
    lessons=Lesson.objects.filter(reviewprogram_id=reviewprogram_id)
    reviewprogram = student.reviewprogram
    mocktests = MockTest.objects.filter(reviewprogram=reviewprogram_id)
 
    for mocktest in mocktests:
        mocktest.setmocktestsections()
        for mocktestsection in mocktest.mocktestsections:
            mocktestsection.setattempts(user=request.user)
           
            for attempt in mocktestsection.attempts:
                 
                attempt.setscores()
              

    attempts = Attempt.objects.filter(user=request.user).order_by('-attempt_date','-start_time') 
      
    return render(request, 'list_students_attempts_front.html',{'attempts':attempts,'student':student, 'mocktests':mocktests,'reviewprogram':reviewprogram,'lessons':lessons,'reviewprograms':reviewprograms})


@user_passes_test(instructor_check) 
def view_attempt(request,attempt_id):   

    attempt = Attempt.objects.get(id=attempt_id) 
    scores= Score.objects.filter(attempt_id=attempt_id)
    attemptcount = Attempt.objects.filter(mocktestsection=attempt.mocktestsection,user=attempt.user)
    attempt.mocktestsection.max_no_of_attempts

    return render(request, 'view_attempt.html',{'attempt':attempt,'scores':scores,'attemptcount':attemptcount})

@user_passes_test(student_check) 
def view_attempt_front(request,attempt_id):   


    reviewprograms = get_reviewprograms(request.user)
    
    
    attempt = Attempt.objects.get(id=attempt_id) 
    scores= Score.objects.filter(attempt_id=attempt_id)
    attemptcount = Attempt.objects.filter(mocktestsection=attempt.mocktestsection,user=attempt.user)
    attempt.mocktestsection.max_no_of_attempts


    reviewprogram = attempt.mocktestsection.mocktest.reviewprogram
    lessons=Lesson.objects.filter(reviewprogram_id=attempt.mocktestsection.mocktest.reviewprogram.id)
    mocktests=MockTest.objects.filter(reviewprogram_id=attempt.mocktestsection.mocktest.reviewprogram.id)


    return render(request, 'view_attempt_front.html',{'mocktests':mocktests,'attempt':attempt,'scores':scores,'attemptcount':attemptcount,'reviewprograms':reviewprograms,'reviewprogram':reviewprogram,'lessons':lessons})

class AttemptListJSON(BaseDatatableView):
    # The model we're going to show
    model = Attempt 

    # define the columns that will be returned
    columns = ['end_time']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['end_time',   '']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 500

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'user':
            # escape HTML for security reasons
            return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
        else:
            return super(AttemptListJSON, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(name__istartswith=search)

        # more advanced example using extra parameters
        filter_customer = self.request.GET.get('customer', None)

        # if filter_customer:
        #     customer_parts = filter_customer.split(' ')
        #     qs_params = None
        #     for part in customer_parts:
        #         q = Q(customer_firstname__istartswith=part)|Q(customer_lastname__istartswith=part)
        #         qs_params = qs_params | q if qs_params else q
        #     qs = qs.filter(qs_params)
        return qs

@user_passes_test(instructor_check,settings.LOGIN_REDIRECT_URL)
def create_student(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            # student.instructor = request.user
            student.save()
            messages.success(request, 'Student record created successfully!')
            return redirect('/students/')
    return render(request, 'create_student.html', {'form': form})

def delete_student(user):
    user.delete()

@user_passes_test(instructor_check,settings.LOGIN_REDIRECT_URL)
def edit_student(request, user_id):
    user = User.objects.get(id=user_id) 
    form = UserChangeForm(instance=user)
    if request.method == 'POST' and 'update' in request.POST:
        form = UserChangeForm(instance=user, data=request.POST )
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']   
            user.last_name = form.cleaned_data['last_name']   
            user.email = form.cleaned_data['email']    
            user.save()
            messages.success(request, 'Student record updated successfully!')
            return redirect('/students/')
    if request.method == 'POST' and 'delete' in request.POST:
        delete_student(delete_student)
        messages.success(request, 'Student record deleted successfully!')
        return redirect('/students/')
    return render(request, 'edit_student.html', {'form': form,
        'student': user})
    


@user_passes_test(instructor_check,settings.LOGIN_REDIRECT_URL)
def student_change_password(request, user_id):
    user = User.objects.get(id=user_id) 
     
    form = AdminPasswordChangeForm(user) 
    if request.method == 'POST' :
        print(request.method)

        form = AdminPasswordChangeForm(user, request.POST ) 
        if form.is_valid():
            form.save() 
            messages.success(request, 'Password successfully changed!')
            return redirect('/students/' + user_id +'/change' ) 
    return render(request, 'account/password_change.html', {'form': form,
        'student': user})
    
