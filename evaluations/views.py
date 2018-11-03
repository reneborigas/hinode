from django.shortcuts import redirect, render

from django.contrib.auth.decorators import user_passes_test
from cms.views import instructor_check,student_check
from mocktests.models import Attempt,Score

from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

# Create your views here.

@user_passes_test(instructor_check) 
def list_attempts(request):  


    attempts = Attempt.objects.all().order_by('-attempt_date','-start_time') 
      
    return render(request, 'list_attempts.html',{'attempts':attempts})

@user_passes_test(instructor_check) 
def view_attempt(request,attempt_id):   

    attempt = Attempt.objects.get(id=attempt_id) 
    scores= Score.objects.filter(attempt_id=attempt_id)
    attemptcount = Attempt.objects.filter(mocktestsection=attempt.mocktestsection,user=attempt.user)
    attempt.mocktestsection.max_no_of_attempts

    return render(request, 'view_attempt.html',{'attempt':attempt,'scores':scores,'attemptcount':attemptcount})

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