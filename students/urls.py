from django.conf.urls import url,include

from students import views as students_views 
urlpatterns = [

    url(r'^$', students_views.list_students, name='list_students'), 
       url(r'^(?P<user_id>\d+)/change$', students_views.edit_student,
        name='edit_student'), 
    url(r'^create$', students_views.create_student, name='create_student'),
     url(r"^(?P<user_id>\d+)/change_password/$", students_views.student_change_password,
        name="student_change_password"),
]