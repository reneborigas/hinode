from django.conf.urls import url,include

from evaluations import views
 
urlpatterns = [
    url(r'^$', views.list_attempts, name='list_attempts'), 
      url(r'^(?P<attempt_id>\d+)$', views.view_attempt, name='view_attempt'), 
]