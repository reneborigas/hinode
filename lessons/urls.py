from django.conf.urls import url

from lessons import views

urlpatterns = [ 
url(r'^$', views.list_lessons, name='list_lessons'),
url(r'^create$', views.create_lesson, name='create_lesson'),
url(r'^(?P<lesson_id>\d+)$', views.edit_lesson, name='edit_lesson'),
 ]