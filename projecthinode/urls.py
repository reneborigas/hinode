"""projecthinode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url ,include
from programs import views as program_views
from contact import views as contact_views
from students import views as student_views
from cms import urls as cms_urls
from questions import urls as questions_urls
from mocktests import urls as mocktests_urls
from lessons import urls as lessons_urls
from cmsdashboard import urls as dashboard_urls
from evaluations import urls as evaluations_urls
from students import urls as students_urls
from enrollment import urls as enrollment_urls
from evaluations.views import AttemptListJSON
from lessons import views as lesson_views

urlpatterns = [
     url(r'^admin/', admin.site.urls),
        url(r'^$', program_views.home, name='home'),
        # url(r'^$', include('allauth.urls'),name='home'),
        url(r'^reviewprograms/$', program_views.loadreviewprograms, name='program'),  
        
        url(r'^about/$', program_views.about, name='about'), 
        url(r'^profile/$', program_views.userProfile, name='profile'), 
        url(r'^contact/$', contact_views.contact, name='contact') ,
        url(r'^accounts/', include('allauth.urls')),
        url(r'^reviewprograms/(?P<reviewprogram_id>\d+)$', program_views.items, name='programitems'),    
        url(r'^reviewprograms/(?P<reviewprogram_id>\d+)/lessons/(?P<lesson_id>\d+)/s$', lesson_views.view_lesson, name='view_lesson'),
        url(r'^evaluations/reviewprogram/(?P<reviewprogram_id>\d+)$', student_views.list_students_attempts_front, name='list_students_attempts_front'), 
        url(r'^evaluations/(?P<attempt_id>\d+)$', student_views.view_attempt_front, name='view_attempt_front'), 
        url(r'^manage/', include(cms_urls)),
        url(r'^dashboard/', include(dashboard_urls)),
        url(r'^results/', include(evaluations_urls)),
        url(r'^students/', include(students_urls)),  
        url(r'^enrollments/', include(enrollment_urls)),   
        url(r'^manage/(?P<reviewprogram_id>\d+)/mocktests/(?P<mocktest_id>\d+)/sections/(?P<mocktestsection_id>\d+)/subsections/(?P<mocktestsubsection_id>\d+)/questions/', include(questions_urls)),
        url(r'^manage/(?P<reviewprogram_id>\d+)/mocktests/', include(mocktests_urls)),
        url(r'^reviewprograms/(?P<reviewprogram_id>\d+)/mocktests/', include(mocktests_urls)),  
         url(r'^manage/(?P<reviewprogram_id>\d+)/lessons/', include(lessons_urls)), 
         url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
         url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
         url(r'^my/datatable/data/$',  AttemptListJSON.as_view() , name='order_list_json'),
         url(r'^tinymce/', include('tinymce.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)