from django.conf.urls import url, include

from cms import views


urlpatterns = [
    url(r'^$', views.instructor_reviewprograms, name='instructor_reviewprograms'),
    url(r'^create$', views.create_reviewprogram, name='create_reviewprogram'),
    url(r'^(?P<reviewprogram_id>\d+)$', views.edit_reviewprogram, name='edit_reviewprogram'),
    url(r'^(?P<reviewprogram_id>\d+)/students$', views.edit_students,
        name='edit_students'),
    url(r'^(?P<reviewprogram_id>\d+)/results$', views.view_reviewprogram_results, 
    	name='view_reviewprogram_results'),
    url(r'^s', views.student_reviewprograms, name='student_reviewprograms'),
    url(r'^(?P<reviewprogram_id>\d+)/s$', views.view_reviewprogram, name='view_reviewprogram'),
]