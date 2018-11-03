from django.conf.urls import url,include

from cmsdashboard import views
 
urlpatterns = [
    url(r'^$', views.view_dashboard, name='dashboard'), 
]