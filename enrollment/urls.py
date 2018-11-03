from django.conf.urls import url,include

from students import views
 
urlpatterns = [
    url(r'^$', views.list_enrollments, name='list_enrollments'),  
    url(r'^(?P<student_user_id>\d+)/reviewprogram/(?P<student_reviewprogram_id>\d+)$', views.list_students_attempts, name='list_students_attempts'), 
    
]